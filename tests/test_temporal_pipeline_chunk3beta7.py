from __future__ import annotations

import json
from pathlib import Path

from semantic_projection import (
    ProjectionContext,
    adapt_foundry_temporal_source_bundle,
    materialize_projected_temporal_graph,
    project_foundry_temporal_bundle,
    project_temporal,
)
from semantic_projection.temporal_pipeline import classify_temporal_target

ROOT = Path(__file__).resolve().parents[1]


def fixture_bundle():
    return json.loads((ROOT / "tests" / "fixtures" / "foundry_temporal_source_bundle_v1_tiny.json").read_text())


def context():
    return ProjectionContext.from_dict(json.loads((ROOT / "examples" / "contexts" / "cognitive_architecture_general_context.json").read_text()))


def test_end_to_end_route_matches_explicit_two_step_pipeline():
    bundle = fixture_bundle()
    routed = project_foundry_temporal_bundle(
        bundle,
        profile_id="cognitive_architecture_demo.v0",
        profile_version="0.2.0",
        context=context(),
        output_mode="standard",
    )
    request = adapt_foundry_temporal_source_bundle(
        bundle,
        profile_id="cognitive_architecture_demo.v0",
        profile_version="0.2.0",
        context=context(),
    )
    explicit = materialize_projected_temporal_graph(project_temporal(request), mode="standard")
    assert routed.artifact == explicit
    assert routed.request == request.to_dict()


def test_route_receipt_is_deterministic_and_traceable():
    kwargs = dict(
        bundle=fixture_bundle(),
        profile_id="cognitive_architecture_demo.v0",
        profile_version="0.2.0",
        context=context(),
        output_mode="summary",
    )
    first = project_foundry_temporal_bundle(**kwargs)
    second = project_foundry_temporal_bundle(**kwargs)
    assert first.receipt == second.receipt
    metadata = first.receipt["metadata"]
    assert metadata["package_type"] == "temporal_projection_route_receipt"
    assert metadata["request_id"] == first.request["request_id"]
    assert metadata["profile_id"] == "cognitive_architecture_demo.v0"
    assert len(metadata["route_hash"]) == 24


def test_target_family_classifier_supports_natal_composite_and_davison():
    assert classify_temporal_target({"target_identity": {"chart_type": "natal"}}) == "natal"
    assert classify_temporal_target({"target_identity": {"chart_type": "midpoint_composite"}}) == "composite"
    assert classify_temporal_target({"target_identity": {"chart_id": "davison:abc"}}) == "davison"
