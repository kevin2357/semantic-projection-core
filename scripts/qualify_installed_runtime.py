"""Qualify an installed SPC wheel without importing from a source checkout."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
from copy import deepcopy
from hashlib import sha256
from importlib import metadata
from pathlib import Path
from typing import Any

from semantic_projection import (
    ProjectionContext,
    ProjectionOptions,
    ProjectionRequest,
    ProjectionValidationError,
    load_bundled_context,
    project_foundry_temporal_bundle,
    project_with_builtin_profiles,
    projection_request_id,
    runtime_release_manifest,
    validate_contract,
    validate_projected_temporal_activation_graph,
)
from semantic_projection.profiles import builtin_projection_registry

STATIC_CASES = (
    ("orthodox", "orthodox_astrology.v1", "1.0.0", "orthodox.general.v1", "1.0.0"),
    (
        "cognitive",
        "cognitive_architecture_demo.v0",
        "0.2.0",
        "cognitive_architecture.general.v0",
        "0.2.0",
    ),
    ("woof-general", "woofmapped_astrology.v0", "0.1.0", "woofmapped.doghouse.general.v0", "0.1.0"),
    ("woof-handler", "woofmapped_astrology.v0", "0.1.0", "woofmapped.handler_guidance.v1", "1.0.0"),
    ("woof-direct-to-dog", "woofmapped_astrology.v0", "0.1.0", "woofmapped.dog_direct.v1", "1.0.0"),
    ("woof-hybrid", "woofmapped_astrology.v0", "0.1.0", "woofmapped.hybrid_horoscope.v1", "1.0.0"),
)


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def digest(value: Any) -> str:
    return sha256(canonical_bytes(value)).hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def make_request(
    package: dict[str, Any], profile_id: str, profile_version: str, context: dict[str, Any]
) -> ProjectionRequest:
    metadata_value = package.get("metadata") or {}
    source_identity = {
        "source_chart_id": metadata_value.get("source_chart_id"),
        "source_chart_ids": metadata_value.get("source_chart_ids") or [],
        "sensor_instance_id": metadata_value.get("sensor_instance_id"),
    }
    options = ProjectionOptions().to_dict()
    request_id = projection_request_id(
        profile_id=profile_id,
        profile_version=profile_version,
        source_identity=source_identity,
        context=context,
        options=options,
    )
    return ProjectionRequest(
        request_id=request_id,
        profile_id=profile_id,
        profile_version=profile_version,
        source_graph=deepcopy(package["canonical_astrology_graph"]),
        structural_evidence=deepcopy(package.get("structural_evidence_graph") or {}),
        source_identity=source_identity,
        context=deepcopy(context),
        source_registries=deepcopy(package.get("source_registries") or {}),
        options=options,
    )


def assert_registry_closed(artifact: dict[str, Any]) -> dict[str, Any]:
    registry = artifact["projected_term_registry"]
    if registry.get("materialization") != "used_terms_subset":
        raise AssertionError("projected registry is not a used-terms subset")
    terms = registry.get("terms") or {}
    if not terms:
        raise AssertionError("projected registry is empty")
    prefix = f"{registry['registry_id']}:{registry['registry_version']}:"
    refs: set[str] = set()
    for row in artifact.get("objects") or []:
        attrs = row.get("attributes") or {}
        refs.update(value for key, value in attrs.items() if key.endswith("_ref") and isinstance(value, str) and value.startswith(prefix))
    for row in artifact.get("relationships") or []:
        attrs = row.get("attributes") or {}
        refs.update(value for key, value in attrs.items() if key.endswith("_ref") and isinstance(value, str) and value.startswith(prefix))
    missing = sorted(ref for ref in refs if ref[len(prefix):] not in terms)
    if missing:
        raise AssertionError(f"unresolved projected-term references: {missing[:5]}")
    return {
        "registry_id": registry["registry_id"],
        "registry_version": registry["registry_version"],
        "term_count": len(terms),
        "referenced_term_count": len(refs),
        "registry_sha256": digest(registry),
    }


def merge_registries_strict(registries: list[dict[str, Any]]) -> dict[str, Any]:
    """Model the documented downstream merge rule and reject semantic conflicts."""
    merged: dict[str, Any] = {}
    identities: dict[str, tuple[str, str]] = {}
    for registry in registries:
        identity = (registry["registry_id"], registry["registry_version"])
        for key, definition in (registry.get("terms") or {}).items():
            if key in merged and (identities[key] != identity or merged[key] != definition):
                raise ValueError(f"conflicting projected-term definition: {key}")
            merged[key] = deepcopy(definition)
            identities[key] = identity
    return merged


def static_case(
    package: dict[str, Any], profile_id: str, profile_version: str, context_id: str, context_version: str
) -> tuple[dict[str, Any], dict[str, Any]]:
    context = load_bundled_context(context_id, context_version)
    request = make_request(package, profile_id, profile_version, context)
    first = project_with_builtin_profiles(request).to_dict()
    second = project_with_builtin_profiles(request).to_dict()
    if canonical_bytes(first) != canonical_bytes(second):
        raise AssertionError("repeated static projections are not byte-identical after canonical serialization")
    validate_contract(first, "projected_semantic_graph_v1.schema.json")
    if not first.get("objects") or not first.get("relationships"):
        raise AssertionError("representative static projection has no row-bearing graph")
    registry = assert_registry_closed(first)
    return first, {
        "artifact_sha256": digest(first),
        "object_count": len(first["objects"]),
        "relationship_count": len(first["relationships"]),
        "runtime_resource_set_sha256": first["metadata"]["runtime_identity"]["semantic_resources"]["sha256"],
        "registry": registry,
    }


def expect_failure(label: str, function, exception_type: type[BaseException]) -> dict[str, str]:
    try:
        function()
    except exception_type as exc:
        return {"case": label, "status": "rejected", "exception": type(exc).__name__, "message": str(exc)}
    raise AssertionError(f"negative case unexpectedly succeeded: {label}")


def verify_physically_missing_resource(package_file: Path) -> dict[str, str]:
    package_root = package_file.parent
    with tempfile.TemporaryDirectory(prefix="spc-missing-resource-") as temp_name:
        shadow_root = Path(temp_name)
        shadow_package = shadow_root / "semantic_projection"
        shutil.copytree(package_root, shadow_package)
        missing = shadow_package / "contexts" / "woofmapped_handler_guidance_context.json"
        missing.unlink()
        environment = dict(os.environ)
        environment["PYTHONPATH"] = str(shadow_root)
        command = [
            sys.executable,
            "-c",
            (
                "from semantic_projection import load_bundled_context; "
                "load_bundled_context('woofmapped.handler_guidance.v1', '1.0.0')"
            ),
        ]
        completed = subprocess.run(command, capture_output=True, text=True, env=environment, check=False)
        if completed.returncode == 0 or "LookupError" not in completed.stderr:
            raise AssertionError("runtime did not reject a physically missing bundled context")
        return {
            "case": "physically-missing-packaged-context",
            "status": "rejected",
            "exception": "LookupError",
            "message": "an isolated copy of the installed package rejected an exact context after its JSON resource was removed",
        }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fixture-dir", type=Path, required=True)
    parser.add_argument("--result-out", type=Path, required=True)
    args = parser.parse_args()

    package_file = Path(sys.modules["semantic_projection"].__file__).resolve()
    script_file = Path(__file__).resolve()
    if "site-packages" not in {part.lower() for part in package_file.parts}:
        raise RuntimeError(f"semantic_projection did not resolve from site-packages: {package_file}")
    if package_file.is_relative_to(script_file.parent):
        raise RuntimeError(f"semantic_projection resolved beneath harness directory: {package_file}")
    distribution_version = metadata.version("semantic-projection-core")
    natal = load_json(args.fixture_dir / "natal_full_tiny.json")
    temporal_bundle = load_json(args.fixture_dir / "foundry_temporal_source_bundle_v1_tiny.json")

    artifacts: dict[str, dict[str, Any]] = {}
    static_results: dict[str, Any] = {}
    for label, profile_id, profile_version, context_id, context_version in STATIC_CASES:
        artifact, summary = static_case(natal, profile_id, profile_version, context_id, context_version)
        artifacts[label] = artifact
        static_results[label] = summary

    woof_labels = ("woof-general", "woof-handler", "woof-direct-to-dog", "woof-hybrid")
    topology = {
        label: {
            "objects": sorted(tuple(row["source_refs"]) for row in artifacts[label]["objects"]),
            "relationships": sorted(
                tuple(row["source_relationship_refs"]) for row in artifacts[label]["relationships"]
            ),
        }
        for label in woof_labels
    }
    if len({canonical_bytes(value) for value in topology.values()}) != 1:
        raise AssertionError("Woofmapping contexts do not preserve identical source topology")
    merged_terms = merge_registries_strict([artifacts[label]["projected_term_registry"] for label in woof_labels])

    temporal_context = ProjectionContext.from_dict(
        load_bundled_context("woofmapped.handler_guidance.v1", "1.0.0")
    )
    temporal_first = project_foundry_temporal_bundle(
        temporal_bundle,
        profile_id="woofmapped_astrology.v0",
        profile_version="0.1.0",
        context=temporal_context,
        output_mode="full",
        registry=builtin_projection_registry(),
    )
    temporal_second = project_foundry_temporal_bundle(
        temporal_bundle,
        profile_id="woofmapped_astrology.v0",
        profile_version="0.1.0",
        context=temporal_context,
        output_mode="full",
        registry=builtin_projection_registry(),
    )
    if canonical_bytes(temporal_first.artifact) != canonical_bytes(temporal_second.artifact):
        raise AssertionError("repeated temporal projections differ")
    if canonical_bytes(temporal_first.receipt) != canonical_bytes(temporal_second.receipt):
        raise AssertionError("repeated temporal route receipts differ")
    validate_projected_temporal_activation_graph(temporal_first.artifact)
    validate_contract(temporal_first.receipt, "temporal_projection_route_receipt_v1.schema.json")
    temporal_registry = assert_registry_closed(temporal_first.artifact["projected_target_graph"])

    invalid_version = deepcopy(natal)
    invalid_version["canonical_astrology_graph"]["graph_version"] = "9.9.9"
    negative_results = [
        expect_failure(
            "unsupported-source-version",
            lambda: project_with_builtin_profiles(
                make_request(
                    invalid_version,
                    "orthodox_astrology.v1",
                    "1.0.0",
                    load_bundled_context("orthodox.general.v1", "1.0.0"),
                )
            ),
            ProjectionValidationError,
        ),
        expect_failure(
            "unsupported-profile-version",
            lambda: project_with_builtin_profiles(
                make_request(
                    natal,
                    "woofmapped_astrology.v0",
                    "9.9.9",
                    load_bundled_context("woofmapped.doghouse.general.v0", "0.1.0"),
                )
            ),
            Exception,
        ),
        expect_failure(
            "missing-context-resource",
            lambda: load_bundled_context("woofmapped.handler_guidance.v1", "9.9.9"),
            LookupError,
        ),
    ]
    conflicting = deepcopy(artifacts["woof-handler"]["projected_term_registry"])
    conflict_key = next(iter(conflicting["terms"]))
    conflicting["terms"][conflict_key]["canonical_label"] += " CONFLICT"
    negative_results.append(
        expect_failure(
            "conflicting-registry-entry",
            lambda: merge_registries_strict([artifacts["woof-handler"]["projected_term_registry"], conflicting]),
            ValueError,
        )
    )
    negative_results.append(verify_physically_missing_resource(package_file))
    malformed = deepcopy(artifacts["orthodox"])
    malformed.pop("metadata")
    negative_results.append(
        expect_failure(
            "invalid-output-contract",
            lambda: validate_contract(malformed, "projected_semantic_graph_v1.schema.json"),
            ProjectionValidationError,
        )
    )

    release_manifest = runtime_release_manifest()
    result = {
        "evidence_contract": "semantic_projection.installed_qa.v1",
        "status": "pass",
        "execution": {
            "python": sys.version.split()[0],
            "executable": str(Path(sys.executable).resolve()),
            "semantic_projection_module": str(package_file),
            "harness": str(script_file),
            "distribution_version": distribution_version,
            "source_checkout_imported": False,
        },
        "release_identity": {
            "package_version": release_manifest["distribution"]["package_version"],
            "runtime_package_set_sha256": release_manifest["runtime_package"]["sha256"],
            "semantic_resource_set_sha256": release_manifest["semantic_resources"]["sha256"],
            "profile_ids": [item["profile_id"] for item in release_manifest["profiles"]],
        },
        "static": static_results,
        "woof_context_equivalence": {
            "contexts": list(woof_labels),
            "source_topology_sha256": digest(next(iter(topology.values()))),
            "merged_projected_term_count": len(merged_terms),
        },
        "temporal": {
            "artifact_sha256": digest(temporal_first.artifact),
            "receipt_sha256": digest(temporal_first.receipt),
            "activator_count": len(temporal_first.artifact["projected_activators"]),
            "activation_count": len(temporal_first.artifact["projected_activations"]),
            "registry": temporal_registry,
        },
        "negative_cases": negative_results,
        "fixture_hashes": {
            path.name: sha256(path.read_bytes()).hexdigest()
            for path in sorted(args.fixture_dir.iterdir())
            if path.is_file()
        },
    }
    args.result_out.parent.mkdir(parents=True, exist_ok=True)
    args.result_out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": "pass", "result": str(args.result_out), "static_cases": len(static_results)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
