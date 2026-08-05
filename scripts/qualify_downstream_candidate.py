"""Exercise an installed AGF -> SPC -> SBE natal compatibility candidate."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from copy import deepcopy
from hashlib import sha256
from importlib import metadata
from pathlib import Path
from typing import Any

from semantic_projection import (
    ProjectionOptions,
    ProjectionRequest,
    load_bundled_context,
    project_with_builtin_profiles,
    projection_request_id,
    validate_contract,
)

CONTEXTS = {
    "general": ("woofmapped.doghouse.general.v0", "0.1.0", "general"),
    "direct_to_dog": ("woofmapped.dog_direct.v1", "1.0.0", "d2d"),
    "handler": ("woofmapped.handler_guidance.v1", "1.0.0", "handler"),
    "hybrid": ("woofmapped.hybrid_horoscope.v1", "1.0.0", "hybrid"),
}


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def digest_value(value: Any) -> str:
    return sha256(canonical_bytes(value)).hexdigest()


def digest_file(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def make_request(package: dict[str, Any], context: dict[str, Any]) -> ProjectionRequest:
    source_metadata = package.get("metadata") or {}
    identity = {
        "source_chart_id": source_metadata.get("source_chart_id"),
        "source_chart_ids": source_metadata.get("source_chart_ids") or [],
        "sensor_instance_id": source_metadata.get("sensor_instance_id"),
    }
    options = ProjectionOptions().to_dict()
    return ProjectionRequest(
        request_id=projection_request_id(
            profile_id="woofmapped_astrology.v0",
            profile_version="0.1.0",
            source_identity=identity,
            context=context,
            options=options,
        ),
        profile_id="woofmapped_astrology.v0",
        profile_version="0.1.0",
        source_graph=deepcopy(package["canonical_astrology_graph"]),
        structural_evidence=deepcopy(package.get("structural_evidence_graph") or {}),
        source_identity=identity,
        context=deepcopy(context),
        source_registries=deepcopy(package.get("source_registries") or {}),
        options=options,
    )


def source_topology(artifact: dict[str, Any]) -> dict[str, Any]:
    return {
        "objects": sorted(tuple(row.get("source_refs") or []) for row in artifact.get("objects") or []),
        "relationships": sorted(
            tuple(row.get("source_relationship_refs") or []) for row in artifact.get("relationships") or []
        ),
    }


def registry_refs(artifact: dict[str, Any]) -> set[str]:
    refs: set[str] = set()
    for group in (artifact.get("objects") or [], artifact.get("relationships") or []):
        for row in group:
            for key, value in (row.get("attributes") or {}).items():
                if key.endswith("_ref") and isinstance(value, str):
                    refs.add(value)
    return refs


def qualify(args: argparse.Namespace) -> dict[str, Any]:
    package_module = Path(sys.modules["semantic_projection"].__file__).resolve()
    if "site-packages" not in {part.lower() for part in package_module.parts}:
        raise RuntimeError(f"SPC did not resolve from site-packages: {package_module}")

    package = json.loads(args.agf_natal.read_text(encoding="utf-8"))
    graph = package.get("canonical_astrology_graph") or {}
    source_metadata = package.get("metadata") or {}
    if (
        graph.get("graph_version") != "1.3.0"
        or graph.get("graph_type") != "canonical_astrology_graph"
        or source_metadata.get("analysis_type") != "natal_dataset"
    ):
        raise ValueError("AGF candidate did not produce the supported natal graph 1.3.0 boundary")

    args.input_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(args.params, args.input_dir / "params.json")
    artifacts: dict[str, dict[str, Any]] = {}
    context_evidence: dict[str, Any] = {}
    filenames = {
        name: f"natal.{args.subject}.woof.{suffix}.json"
        for name, (_context_id, _context_version, suffix) in CONTEXTS.items()
    }
    for name, (context_id, context_version, _suffix) in CONTEXTS.items():
        context = load_bundled_context(context_id, context_version)
        request = make_request(package, context)
        first = project_with_builtin_profiles(request).to_dict()
        second = project_with_builtin_profiles(request).to_dict()
        if canonical_bytes(first) != canonical_bytes(second):
            raise AssertionError(f"{name} projection is not deterministic")
        validate_contract(first, "projected_semantic_graph_v1.schema.json")
        terms = (first.get("projected_term_registry") or {}).get("terms") or {}
        prefix = (
            f"{first['projected_term_registry']['registry_id']}:"
            f"{first['projected_term_registry']['registry_version']}:"
        )
        unresolved = sorted(ref for ref in registry_refs(first) if not ref.startswith(prefix) or ref[len(prefix):] not in terms)
        if unresolved:
            raise AssertionError(f"{name} has unresolved projected-term refs: {unresolved[:5]}")
        artifact_path = args.input_dir / filenames[name]
        write_json(artifact_path, first)
        artifacts[name] = first
        context_evidence[name] = {
            "context_id": context_id,
            "context_version": context_version,
            "artifact": filenames[name],
            "artifact_sha256": digest_file(artifact_path),
            "objects": len(first.get("objects") or []),
            "relationships": len(first.get("relationships") or []),
            "projected_terms": len(terms),
            "runtime_identity": first["metadata"]["runtime_identity"],
        }

    topologies = {name: digest_value(source_topology(value)) for name, value in artifacts.items()}
    if len(set(topologies.values())) != 1:
        raise AssertionError(f"context source topologies differ: {topologies}")
    source_identities = {digest_value(value.get("source_identity")) for value in artifacts.values()}
    graph_refs = {digest_value(value.get("source_graph_ref")) for value in artifacts.values()}
    if len(source_identities) != 1 or len(graph_refs) != 1:
        raise AssertionError("parallel projections do not share source identity and graph reference")

    manifest = {
        "schema_version": "astrowoof.projected_natal_input.v0.1",
        "subjects": [
            {
                "subject_id": args.subject,
                "contexts": {
                    "general": filenames["general"],
                    "direct_to_dog": filenames["direct_to_dog"],
                    "handler": filenames["handler"],
                    "hybrid": filenames["hybrid"],
                },
                "params": "params.json",
            }
        ],
    }
    write_json(args.input_dir / "astrowoof-input-manifest.json", manifest)

    command = [
        str(args.sbe_command),
        "--input-package",
        str(args.input_dir),
        "--subject",
        args.subject,
        "--output-dir",
        str(args.sbe_output),
        "--bundle-dir",
        str(args.sbe_bundle),
        "--handoff-profile",
        "compact",
        "--fail-fast",
    ]
    completed = subprocess.run(command, capture_output=True, text=True, check=False)
    if completed.returncode != 0:
        raise RuntimeError(f"SBE rejected the candidate: {completed.stderr or completed.stdout}")
    run_manifest_path = args.sbe_output / "run-manifest.json"
    packet_path = args.sbe_output / args.subject / f"{args.subject}.selected-authoring-packet.json"
    if not run_manifest_path.is_file() or not packet_path.is_file():
        raise FileNotFoundError("SBE did not produce its run manifest and selected authoring packet")
    run_manifest = json.loads(run_manifest_path.read_text(encoding="utf-8"))
    packet = json.loads(packet_path.read_text(encoding="utf-8"))
    subject_result = next(
        (item for item in run_manifest.get("subjects") or [] if item.get("subject") == args.subject),
        {},
    )
    registry = packet.get("projected_term_registry") or {}
    if not (registry.get("terms") or {}):
        raise AssertionError("SBE output dropped the projected-term registry")

    return {
        "evidence_contract": "semantic_projection.downstream_candidate_qa.v1",
        "status": "pass",
        "installed_runtime": {
            "python": sys.version.split()[0],
            "agf_distribution_version": metadata.version("astrology-graph-foundry"),
            "spc_distribution_version": metadata.version("semantic-projection-core"),
            "spc_module_from_site_packages": True,
            "sbe_distribution_version": metadata.version("astrowoof-natal-authoring"),
        },
        "agf": {
            "artifact": args.agf_natal.name,
            "artifact_sha256": digest_file(args.agf_natal),
            "graph_type": graph["graph_type"],
            "graph_version": graph["graph_version"],
            "source_chart_id": (package.get("metadata") or {}).get("source_chart_id"),
            "objects": len(graph.get("objects") or []),
            "relationships": len(graph.get("relationships") or []),
        },
        "contexts": context_evidence,
        "parallel_identity": {
            "source_topology_sha256": next(iter(topologies.values())),
            "source_identity_sha256": next(iter(source_identities)),
            "source_graph_ref_sha256": next(iter(graph_refs)),
        },
        "sbe": {
            "exit_code": completed.returncode,
            "run_manifest_sha256": digest_file(run_manifest_path),
            "selected_authoring_packet_sha256": digest_file(packet_path),
            "selected_authoring_packet_bytes": packet_path.stat().st_size,
            "selected_claim_count": len(packet.get("cards") or []),
            "projected_term_count": len(registry.get("terms") or {}),
            "run_status": run_manifest.get("status"),
            "subject_status": subject_result.get("status"),
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--agf-natal", type=Path, required=True)
    parser.add_argument("--params", type=Path, required=True)
    parser.add_argument("--subject", required=True)
    parser.add_argument("--input-dir", type=Path, required=True)
    parser.add_argument("--sbe-command", type=Path, required=True)
    parser.add_argument("--sbe-output", type=Path, required=True)
    parser.add_argument("--sbe-bundle", type=Path, required=True)
    parser.add_argument("--result-out", type=Path, required=True)
    args = parser.parse_args()
    result = qualify(args)
    write_json(args.result_out, result)
    print(json.dumps({"status": "pass", "result": str(args.result_out)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
