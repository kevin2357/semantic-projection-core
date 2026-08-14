from __future__ import annotations

import json
from importlib import metadata

import pytest

import semantic_projection.runtime_identity as runtime_identity_module
from semantic_projection import ENGINE_VERSION, __version__
from semantic_projection.resources import (
    aggregate_resource_records,
    bundled_contexts,
    load_bundled_context,
    runtime_package_records,
    semantic_resource_manifest,
)
from semantic_projection.runtime_cli import main, runtime_report
from semantic_projection.runtime_identity import projection_runtime_identity, runtime_release_manifest
from semantic_projection.validation import validate_contract
from tests.paths import EXAMPLES_ROOT

EXPECTED_CONTEXTS = {
    "cognitive_architecture.general.v0": "0.2.0",
    "orthodox.general.v1": "1.0.0",
    "orthodox.relationship.general.v1": "1.0.0",
    "orthodox.relationship.professional.v1": "1.0.0",
    "orthodox.synastry.general.v1": "1.0.0",
    "orthodox.synastry.professional.v1": "1.0.0",
    "woofmapped.dog_direct.v1": "1.0.0",
    "woofmapped.doghouse.general.v0": "0.1.0",
    "woofmapped.handler_guidance.v1": "1.0.0",
    "woofmapped.hybrid_horoscope.v1": "1.0.0",
    "woofmapped.synastry.dog_dog.v1": "1.0.0",
    "woofmapped.synastry.dog_dog.v1.asymmetric": "1.0.0",
    "woofmapped.synastry.human_dog.v1": "1.0.0",
}


def test_distribution_engine_and_package_versions_are_aligned():
    assert metadata.version("semantic-projection-core") == ENGINE_VERSION == __version__ == "0.11.0"


def test_all_versioned_contexts_are_packaged_and_match_examples():
    contexts = bundled_contexts()
    assert {item["context_id"]: item["context_version"] for item in contexts} == EXPECTED_CONTEXTS
    for item in contexts:
        packaged = load_bundled_context(item["context_id"], item["context_version"])
        example = json.loads((EXAMPLES_ROOT / "contexts" / item["resource"]).read_text(encoding="utf-8"))
        assert packaged == example


def test_context_resolution_requires_exact_version():
    with pytest.raises(LookupError, match="available versions"):
        load_bundled_context("woofmapped.handler_guidance.v1", "9.9.9")


def test_semantic_resource_manifest_is_stable_and_sensitive_to_changes():
    first = semantic_resource_manifest()
    second = semantic_resource_manifest()
    assert first == second
    assert first["resource_count"] > len(EXPECTED_CONTEXTS)
    records = first["resources"]
    changed = [*records[:-1], {**records[-1], "sha256": "0" * 64}]
    assert aggregate_resource_records(records) != aggregate_resource_records(changed)


def test_runtime_release_manifest_fingerprints_code_profiles_schemas_and_contexts():
    manifest = runtime_release_manifest()
    validate_contract(manifest, "runtime_release_manifest_v1.schema.json")
    assert manifest["manifest_contract"] == "semantic_projection.runtime_release_manifest.v1"
    assert manifest["runtime_package"]["resource_count"] > manifest["semantic_resources"]["resource_count"]
    runtime_paths = {item["path"] for item in manifest["runtime_package"]["resources"]}
    assert {"distribution/METADATA", "distribution/WHEEL", "distribution/entry_points.txt"} <= runtime_paths
    assert all(item["path"].endswith(".json") for item in manifest["schemas"]["resources"])
    assert len(manifest["profiles"]) == 4
    assert len(manifest["contexts"]) == len(EXPECTED_CONTEXTS)
    woof = next(item for item in manifest["profiles"] if item["profile_id"] == "woofmapped_astrology.v0")
    paths = {item["path"] for item in woof["policy_resource_set"]["resources"]}
    assert "profiles/woofmapped_astrology/object_mappings.py" in paths
    assert "profiles/woofmapped_astrology/relationship_mappings.py" in paths
    assert "profiles/woofmapped_astrology/projected_term_registry.json" in paths


def test_projection_runtime_identity_is_route_specific_and_content_addressed():
    context = load_bundled_context("woofmapped.doghouse.general.v0", "0.1.0")
    static = projection_runtime_identity(
        profile_id="woofmapped_astrology.v0",
        profile_version="0.1.0",
        context=context,
        route="static_projection",
        output_contract="projected_semantic_graph.v1",
    )
    temporal = projection_runtime_identity(
        profile_id="woofmapped_astrology.v0",
        profile_version="0.1.0",
        context=context,
        route="temporal_projection",
        output_contract="projected_temporal_activation_graph.v1",
    )
    assert static["identity_contract"] == "semantic_projection.runtime_identity.v1"
    assert static["runtime_package"]["sha256"] == temporal["runtime_package"]["sha256"]
    assert static["profile"]["policy_resource_set"]["sha256"] == temporal["profile"]["policy_resource_set"]["sha256"]
    assert static["context"]["bundled"] is True
    assert len(static["context"]["content_sha256"]) == 64
    assert static["route"] != temporal["route"]


def test_changed_executable_mapping_changes_runtime_and_profile_fingerprints(monkeypatch):
    baseline = runtime_release_manifest()
    records = runtime_package_records()
    target = "profiles/woofmapped_astrology/object_mappings.py"
    changed = [
        {**record, "sha256": "f" * 64} if record["path"] == target else record
        for record in records
    ]
    monkeypatch.setattr(runtime_identity_module, "runtime_package_records", lambda: changed)
    modified = runtime_identity_module.runtime_release_manifest()
    assert modified["runtime_package"]["sha256"] != baseline["runtime_package"]["sha256"]
    baseline_woof = next(item for item in baseline["profiles"] if item["profile_id"] == "woofmapped_astrology.v0")
    modified_woof = next(item for item in modified["profiles"] if item["profile_id"] == "woofmapped_astrology.v0")
    assert modified_woof["policy_resource_set"]["sha256"] != baseline_woof["policy_resource_set"]["sha256"]


def test_modified_context_cannot_claim_bundled_resource_identity():
    context = load_bundled_context("woofmapped.doghouse.general.v0", "0.1.0")
    context["parameters"] = {"consumer_override": True}
    identity = projection_runtime_identity(
        profile_id="woofmapped_astrology.v0",
        profile_version="0.1.0",
        context=context,
        route="static_projection",
        output_contract="projected_semantic_graph.v1",
    )
    assert identity["context"]["bundled"] is False
    assert identity["context"]["resource_path"] is None
    assert identity["context"]["resource_sha256"] is None


def test_runtime_report_discovers_distribution_entry_points():
    report = runtime_report()
    assert report["status"] == "ok"
    assert report["release_compatibility"] == {
        "contract_id": "semantic_projection.release_compatibility.v1",
        "distribution_version": "0.11.0",
    }
    assert report["runtime_release_manifest"]["manifest_contract"] == (
        "semantic_projection.runtime_release_manifest.v1"
    )
    assert report["profile_entry_points_discovered"] == 4
    assert {item["name"] for item in report["profile_entry_points"]} == {
        "cognitive_architecture_demo",
        "orthodox_astrology",
        "woofmapped_astrology",
        "woofmapped_bounded_astrology",
    }
    assert {item["name"] for item in report["console_entry_points"]} >= {
        "semantic-project",
        "semantic-bounded-project",
        "semantic-temporal-foundations",
        "semantic-temporal-intake",
        "semantic-temporal-project",
        "semantic-temporal-run",
    }


def test_runtime_cli_rejects_editable_installation(capsys):
    assert main(["--require-installed"]) == 2
    assert "editable installation" in capsys.readouterr().err


def test_runtime_cli_writes_full_release_manifest(tmp_path):
    output = tmp_path / "release-manifest.json"
    assert main(["--release-manifest-out", str(output)]) == 0
    manifest = json.loads(output.read_text(encoding="utf-8"))
    assert manifest["manifest_contract"] == "semantic_projection.runtime_release_manifest.v1"
    validate_contract(manifest, "runtime_release_manifest_v1.schema.json")
