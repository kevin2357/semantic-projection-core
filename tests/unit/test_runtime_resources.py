from __future__ import annotations

import json
from importlib import metadata

import pytest

from semantic_projection import ENGINE_VERSION, __version__
from semantic_projection.resources import (
    aggregate_resource_records,
    bundled_contexts,
    load_bundled_context,
    semantic_resource_manifest,
)
from semantic_projection.runtime_cli import main, runtime_report
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
    assert metadata.version("semantic-projection-core") == ENGINE_VERSION == __version__ == "0.10.0"


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


def test_runtime_report_discovers_distribution_entry_points():
    report = runtime_report()
    assert report["status"] == "ok"
    assert report["profile_entry_points_discovered"] == 3
    assert {item["name"] for item in report["profile_entry_points"]} == {
        "cognitive_architecture_demo",
        "orthodox_astrology",
        "woofmapped_astrology",
    }
    assert {item["name"] for item in report["console_entry_points"]} >= {
        "semantic-project",
        "semantic-temporal-foundations",
        "semantic-temporal-intake",
        "semantic-temporal-project",
        "semantic-temporal-run",
    }


def test_runtime_cli_rejects_editable_installation(capsys):
    assert main(["--require-installed"]) == 2
    assert "editable installation" in capsys.readouterr().err
