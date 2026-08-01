from __future__ import annotations

import json

from semantic_projection import (
    ProjectionContext,
    adapt_foundry_temporal_source_bundle,
    canonical_temporal_fact_view,
    materialize_projected_temporal_graph,
    project_temporal,
)
from semantic_projection.ids import stable_hash
from tests.paths import FIXTURES_ROOT

FIXTURE = FIXTURES_ROOT / "foundry_temporal_source_bundle_v1_tiny.json"


PROFILES = {
    "orthodox": (
        "orthodox_astrology.v1",
        "1.0.0",
        ProjectionContext(
            context_id="orthodox.general.v1",
            context_version="1.0.0",
            subject_scope="individual",
            target_domain="orthodox_astrology.v1",
            application_context="general_interpretation",
        ),
    ),
    "cognitive": (
        "cognitive_architecture_demo.v0",
        "0.2.0",
        ProjectionContext(
            context_id="cognitive_architecture.general.v0",
            context_version="0.2.0",
            subject_scope="individual",
            target_domain="cognitive_architecture_demo.v0",
            application_context="cognitive_architecture_demo",
        ),
    ),
    "woofmapped": (
        "woofmapped_astrology.v0",
        "0.1.0",
        ProjectionContext(
            context_id="woofmapped.doghouse.general.v0",
            context_version="0.1.0",
            subject_scope="dog",
            target_domain="woofmapped_astrology.v0",
            application_context="woofmapped_natal_projection",
            constraints={"house_mapping_policy": "doghouse"},
        ),
    ),
}


def _project(name: str):
    bundle = json.loads(FIXTURE.read_text(encoding="utf-8"))
    profile_id, version, context = PROFILES[name]
    request = adapt_foundry_temporal_source_bundle(
        bundle,
        profile_id=profile_id,
        profile_version=version,
        context=context,
    )
    return project_temporal(request)


def test_same_temporal_facts_produce_distinct_profile_semantics():
    results = {name: _project(name) for name in PROFILES}
    facts = {
        name: stable_hash(canonical_temporal_fact_view(result["projected_activations"][0]["temporal_facts"]))
        for name, result in results.items()
    }
    assert len(set(facts.values())) == 1
    relationships = {result["projected_activations"][0]["projected_relationship_type"] for result in results.values()}
    activator_terms = {result["projected_activators"][0]["projected_operator_ref"] for result in results.values()}
    assert len(relationships) == 3
    assert len(activator_terms) == 3


def test_cross_profile_summary_retains_semantic_hashes():
    full = _project("cognitive")
    summary = materialize_projected_temporal_graph(full, mode="summary")
    assert "projected_activations" not in summary
    assert summary["semantic_hashes"]["projected_activations"] == stable_hash(full["projected_activations"])
    assert summary["semantic_hashes"]["projected_states"]


def test_upstream_limitations_are_annotated_not_mutated():
    full = _project("cognitive")
    rows = full["upstream_source_limitations"]
    assert rows
    assert all({"text", "source", "status"} <= set(row) for row in rows)
    superseded = [row for row in rows if row["status"] == "superseded_for_this_artifact"]
    assert superseded
    assert superseded[0]["superseded_by"] == "projected_temporal_activation_graph.v1"
