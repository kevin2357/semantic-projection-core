from __future__ import annotations

import json
from pathlib import Path

from semantic_projection import (
    ProjectionContext,
    adapt_foundry_temporal_source_bundle,
    materialize_projected_temporal_graph,
    project_temporal,
)
from semantic_projection.ids import stable_hash

FIXTURE = Path(__file__).parent / "fixtures" / "foundry_temporal_source_bundle_v1_tiny.json"


def _full():
    bundle = json.loads(FIXTURE.read_text(encoding="utf-8"))
    request = adapt_foundry_temporal_source_bundle(
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
    return project_temporal(request)


def test_c5_materializations_preserve_semantic_payload():
    full = _full()
    standard = materialize_projected_temporal_graph(full, mode="standard")
    summary = materialize_projected_temporal_graph(full, mode="summary")
    forensic = materialize_projected_temporal_graph(full, mode="forensic")
    assert standard["metadata"]["materialization_mode"] == "standard"
    assert summary["metadata"]["materialization_mode"] == "summary"
    assert forensic["metadata"]["materialization_mode"] == "forensic"
    assert stable_hash(full["projected_activations"]) == stable_hash(standard["projected_activations"])
    assert stable_hash(full["projected_activations"]) == stable_hash(forensic["projected_activations"])
    assert "projected_activations" not in summary
    assert forensic["forensic_integrity"]["projected_activation_count"] == 1


def test_c5_state_availability_and_audit_reconciliation():
    full = _full()
    state = full["projected_activations"][0]["temporal_facts"]["observation_states"][0]
    composition = state["projected_state_composition"]
    assert "mode_availability" in composition
    assert "domain_availability" in composition
    assert full["audit"]["reconciliation"]["projected_activation_count"] == 1
    assert full["diagnostics"]["summary"]["error_count"] == 0


def test_c5_target_resolution_categories_present():
    full = _full()
    coverage = full["summary"]["coverage"]["activations"]
    assert "target_excluded_by_profile_scope_count" in coverage
    assert "target_excluded_by_source_selection_policy_count" in coverage
    assert "target_eligible_but_unmapped_count" in coverage
    assert "target_missing_from_static_source_graph_count" in coverage
