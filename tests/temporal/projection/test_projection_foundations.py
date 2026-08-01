from __future__ import annotations

import json

from semantic_projection import (
    ProjectionContext,
    adapt_foundry_temporal_source_bundle,
    identify_artifact,
    project_temporal_foundations,
    validate_contract,
)
from tests.paths import FIXTURES_ROOT

FIXTURE = FIXTURES_ROOT / "foundry_temporal_source_bundle_v1_tiny.json"


def request():
    bundle = json.loads(FIXTURE.read_text(encoding="utf-8"))
    return adapt_foundry_temporal_source_bundle(
        bundle,
        profile_id="cognitive_architecture_demo.v0",
        profile_version="0.2.0",
        context=ProjectionContext(
            context_id="cognitive_architecture.general.v0",
            context_version="0.2.0",
            subject_scope="individual",
            target_domain="cognitive_architecture_demo.v0",
            application_context="cognitive_architecture_demo",
        ),
    )


def test_artifact_identity_distinguishes_bundle_and_request():
    bundle = json.loads(FIXTURE.read_text(encoding="utf-8"))
    assert identify_artifact(bundle).kind == "foundry_temporal_projection_source_bundle"
    assert identify_artifact(request().to_dict()).kind == "temporal_projection_request"


def test_foundations_reuse_static_projection_and_object_mapping():
    result = project_temporal_foundations(request())
    assert result["metadata"]["package_type"] == "projected_temporal_foundations"
    assert result["projected_target_graph"]["metadata"]["package_type"] == "projected_semantic_graph"
    assert result["coverage"]["mapped_activator_count"] >= 1
    first = result["projected_activators"][0]
    assert first["mapping_rule_refs"]
    assert first["provenance"]["mapping_reuse"] == "profile.project_object"
    validate_contract(result, "projected_temporal_foundations_v1.schema.json")


def test_foundations_are_deterministic():
    assert project_temporal_foundations(request()) == project_temporal_foundations(request())
