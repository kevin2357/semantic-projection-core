from __future__ import annotations

from copy import deepcopy

import pytest

from semantic_projection import ProjectionContext, project_foundry_temporal_bundle, project_synastry
from semantic_projection.io import read_json
from semantic_projection.profiles import builtin_projection_registry
from tests.factories import project_dataset
from tests.paths import EXAMPLES_ROOT, FIXTURES_ROOT


def context(name: str) -> dict:
    return read_json(EXAMPLES_ROOT / "contexts" / name)


@pytest.mark.integration
@pytest.mark.parametrize(
    ("profile_id", "profile_version", "context_name"),
    [
        ("orthodox_astrology.v1", "1.0.0", "orthodox_general_context.json"),
        ("cognitive_architecture_demo.v0", "0.2.0", "cognitive_architecture_general_context.json"),
        ("woofmapped_astrology.v0", "0.1.0", "woofmapped_doghouse_general_context.json"),
    ],
)
def test_realistic_natal_fixture_projects_across_bundled_profiles(profile_id, profile_version, context_name):
    package = read_json(FIXTURES_ROOT / "agf" / "natal_full_tiny.json")
    artifact = project_dataset(
        package,
        profile_id=profile_id,
        profile_version=profile_version,
        context=context(context_name),
    )
    assert artifact["objects"]
    assert artifact["relationships"]
    assert artifact["source_identity"]["source_chart_id"] == "natal:fixture"
    assert artifact["projected_term_registry"]["terms"]
    source_counts = artifact["audit"]["coverage"]
    assert source_counts["source_object_count"] == 8
    assert source_counts["source_relationship_count"] == 7


@pytest.mark.integration
@pytest.mark.parametrize("graph_type", ["composite", "davison", "solar_return", "lunar_return"])
def test_orthodox_profile_accepts_declared_chart_like_source_families(graph_type):
    package = read_json(FIXTURES_ROOT / "agf" / "natal_full_tiny.json")
    package = deepcopy(package)
    package["canonical_astrology_graph"]["graph_type"] = graph_type
    artifact = project_dataset(
        package,
        profile_id="orthodox_astrology.v1",
        profile_version="1.0.0",
        context=context("orthodox_general_context.json"),
    )
    assert artifact["objects"]
    assert artifact["relationships"]
    assert artifact["metadata"]["profile_id"] == "orthodox_astrology.v1"


@pytest.mark.integration
def test_realistic_synastry_fixture_preserves_registries_and_directional_ownership():
    package = read_json(FIXTURES_ROOT / "agf" / "synastry_full_tiny.json")
    result = project_synastry(
        source_graph=package["canonical_astrology_graph"],
        structural_evidence=package["structural_evidence_graph"],
        source_identity=package["metadata"],
        source_registries=package["source_registries"],
        participants=[
            {"participant_id": "human", "role": "handler", "species": "human"},
            {"participant_id": "dog", "role": "dog", "species": "canine"},
        ],
        relationship_kind="human_dog",
        profile_id="woofmapped_astrology.v0",
        profile_version="0.1.0",
        context=context("woofmapped_human_dog_synastry_context.json"),
        registry=builtin_projection_registry(),
    )
    assert result.request.source_registries == package["source_registries"]
    assert {row["attributes"]["source_owner"] for row in result.artifact["relationships"]} == {"human", "dog"}
    assert all(row["attributes"]["inter_participant"] for row in result.artifact["relationships"])


@pytest.mark.integration
@pytest.mark.parametrize("target_type", ["natal", "composite", "davison"])
def test_temporal_pipeline_preserves_supported_target_family_identity(target_type):
    bundle = read_json(FIXTURES_ROOT / "foundry_temporal_source_bundle_v1_tiny.json")
    bundle = deepcopy(bundle)
    bundle["target_identity"]["chart_type"] = target_type
    result = project_foundry_temporal_bundle(
        bundle,
        profile_id="orthodox_astrology.v1",
        profile_version="1.0.0",
        context=ProjectionContext.from_dict(context("orthodox_general_context.json")),
        output_mode="summary",
    )
    assert result.receipt["metadata"]["target_family"] == target_type
    assert result.artifact["target_identity"]["chart_type"] == target_type
