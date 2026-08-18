from __future__ import annotations

import json

from semantic_projection import (
    ProjectionContext,
    ProjectionRequest,
    adapt_foundry_temporal_source_bundle,
    project_foundry_temporal_bundle,
    project_temporal_foundations,
    project_with_builtin_profiles,
)
from semantic_projection.materialization import external_audit_artifact, materialize_projected_graph
from tests.paths import EXAMPLES_ROOT, FIXTURES_ROOT


def _assert_runtime_identity(identity: dict, *, route: str, output_contract: str) -> None:
    assert identity["identity_contract"] == "semantic_projection.runtime_identity.v1"
    assert identity["distribution"]["version"] == "0.11.1"
    assert identity["runtime_package"]["resource_count"] > 0
    assert len(identity["runtime_package"]["sha256"]) == 64
    assert len(identity["semantic_resources"]["sha256"]) == 64
    assert len(identity["profile"]["policy_resource_set"]["sha256"]) == 64
    assert identity["context"]["bundled"] is True
    assert identity["route"] == route
    assert identity["output_contract"] == output_contract


def test_static_materializations_and_external_audit_preserve_runtime_identity():
    payload = json.loads((FIXTURES_ROOT / "projection" / "empty_projection_request.json").read_text(encoding="utf-8"))
    payload["context"]["target_domain"] = "orthodox_astrology.v1"
    projected = project_with_builtin_profiles(ProjectionRequest.from_dict(payload)).to_dict()
    identity = projected["metadata"]["runtime_identity"]
    _assert_runtime_identity(identity, route="static_projection", output_contract="projected_semantic_graph.v1")
    for mode in ("full", "standard", "summary", "forensic"):
        assert materialize_projected_graph(projected, mode=mode)["metadata"]["runtime_identity"] == identity
    assert external_audit_artifact(projected)["metadata"]["runtime_identity"] == identity


def test_temporal_foundations_projection_and_receipt_preserve_runtime_identity():
    bundle = json.loads((FIXTURES_ROOT / "foundry_temporal_source_bundle_v1_tiny.json").read_text(encoding="utf-8"))
    context = ProjectionContext.from_dict(
        json.loads((EXAMPLES_ROOT / "contexts" / "cognitive_architecture_general_context.json").read_text(encoding="utf-8"))
    )
    request = adapt_foundry_temporal_source_bundle(
        bundle,
        profile_id="cognitive_architecture_demo.v0",
        profile_version="0.2.0",
        context=context,
    )
    foundations = project_temporal_foundations(request)
    _assert_runtime_identity(
        foundations["metadata"]["runtime_identity"],
        route="temporal_foundations",
        output_contract="projected_temporal_foundations.v0.1",
    )
    result = project_foundry_temporal_bundle(
        bundle,
        profile_id="cognitive_architecture_demo.v0",
        profile_version="0.2.0",
        context=context,
        output_mode="standard",
    )
    identity = result.artifact["metadata"]["runtime_identity"]
    _assert_runtime_identity(
        identity,
        route="temporal_projection",
        output_contract="projected_temporal_activation_graph.v1",
    )
    assert result.artifact["provenance"]["runtime_identity"] == identity
    assert result.receipt["metadata"]["runtime_identity"] == identity
