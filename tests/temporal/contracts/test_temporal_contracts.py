from __future__ import annotations

import pytest

from semantic_projection import (
    ProjectedTemporalActivation,
    ProjectedTemporalActivator,
    ProjectedTemporalSequenceSummary,
    ProjectedTemporalState,
    ProjectionValidationError,
    load_bundled_context,
    projected_temporal_activation_id,
    projected_temporal_activator_id,
    projected_temporal_contract_skeleton,
    projected_temporal_sequence_id,
    projected_temporal_state_id,
    projection_runtime_identity,
    validate_projected_temporal_activation_graph,
)

RUNTIME_IDENTITY = projection_runtime_identity(
    profile_id="cognitive_architecture_demo.v0",
    profile_version="0.2.0",
    context=load_bundled_context("cognitive_architecture.general.v0", "0.2.0"),
    route="temporal_projection",
    output_contract="projected_temporal_activation_graph.v1",
)


def target_graph() -> dict:
    return {
        "metadata": {
            "package_type": "projected_semantic_graph",
            "projection_id": "projection:static",
            "contract_version": "1.0.0",
        },
        "objects": [
            {
                "id": "projected:cognitive:moon",
                "object_type": "projected_operator",
                "name": "Emotional Regulation",
            }
        ],
        "relationships": [],
    }


def metadata() -> dict:
    return {
        "package_type": "projected_temporal_activation_graph",
        "contract_version": "1.0.0",
        "temporal_projection_id": "temporal_projection:test",
        "static_projection_id": "projection:static",
        "engine_version": "0.6.0",
        "profile_id": "cognitive_architecture_demo.v0",
        "profile_version": "0.2.0",
        "context_id": "cognitive_architecture.general.v0",
        "context_version": "0.2.0",
        "materialization_mode": "full",
        "runtime_identity": RUNTIME_IDENTITY,
    }


def complete_graph() -> dict:
    context_id = "cognitive_architecture.general.v0"
    activator_id = projected_temporal_activator_id(
        profile_id="cognitive_architecture_demo.v0",
        source_activator_ref="canonical:transiting_object:mars",
        projected_operator_ref="term:action_selection",
        context_id=context_id,
    )
    sequence_id = projected_temporal_sequence_id(
        profile_id="cognitive_architecture_demo.v0",
        source_sequence_ref="temporal_sequence:source",
        context_id=context_id,
    )
    activation_id = projected_temporal_activation_id(
        profile_id="cognitive_architecture_demo.v0",
        source_activation_ref="temporal_activation:source",
        projected_activator_ref=activator_id,
        projected_target_ref="projected:cognitive:moon",
        projected_relationship_type="facilitates_and_automates",
        context_id=context_id,
    )
    state_id = projected_temporal_state_id(
        profile_id="cognitive_architecture_demo.v0",
        source_state_ref="temporal_state:source",
        projected_activation_ref=activation_id,
        context_id=context_id,
    )
    activator = ProjectedTemporalActivator(
        id=activator_id,
        source_activator_ref="canonical:transiting_object:mars",
        source_body="Mars",
        projected_operator_ref="term:action_selection",
        operators=["assert", "mobilize"],
        source_refs=["canonical:transiting_object:mars"],
        mapping_rule_refs=["cognitive.object.mars"],
        context_refs=[context_id],
        provenance={"source_contract": "canonical_temporal_activation_graph.v1"},
    ).to_dict()
    state = ProjectedTemporalState(
        id=state_id,
        source_state_ref="temporal_state:source",
        projected_activation_ref=activation_id,
        observed_at="2026-01-01T12:00:00-07:00",
        phase="closest_observed",
        orb=0.9,
        distance=59.1,
        strength_label="very tight",
        activator_state={"retrograde": False, "sign": None},
        projected_state_composition={},
        source_refs=["transit_observation:source"],
        provenance={"preserved_source_fact": True},
    ).to_dict()
    activation = ProjectedTemporalActivation(
        id=activation_id,
        source_activation_ref="temporal_activation:source",
        source_sequence_ref="temporal_sequence:source",
        projected_sequence_id=sequence_id,
        pass_index=1,
        projected_activator_ref=activator_id,
        projected_target_ref="projected:cognitive:moon",
        projected_relationship_type="facilitates_and_automates",
        projected_relationship_term_ref="term:facilitates_and_automates",
        temporal_role="current_activation",
        directionality="activator_to_target",
        temporal_facts={
            "start_at": "2026-01-01T12:00:00-07:00",
            "closest_observed_at": "2026-01-01T12:00:00-07:00",
            "exact_at": None,
            "end_at": "2026-01-01T12:00:00-07:00",
            "exactness": {"status": "closest_observed_only"},
            "motion": {"states": ["direct"]},
            "observation_count": 1,
            "observation_states": [state],
        },
        source_refs=["temporal_activation:source"],
        mapping_rule_refs=["cognitive.aspect.sextile"],
        context_refs=[context_id],
        provenance={"source_contract": "canonical_temporal_activation_graph.v1"},
    ).to_dict()
    sequence = ProjectedTemporalSequenceSummary(
        id=sequence_id,
        source_sequence_ref="temporal_sequence:source",
        activation_refs=[activation_id],
        pass_count=1,
        source_refs=["temporal_sequence:source"],
        provenance={},
    ).to_dict()
    graph = projected_temporal_contract_skeleton(
        metadata=metadata(),
        source_identity={"source_chart_id": "natal:test"},
        target_identity={"chart_id": "natal:test"},
        period={"start_at": "2026-01-01", "end_at": "2026-01-02"},
        projected_target_graph=target_graph(),
        upstream_source_limitations=["No solved exact event is asserted."],
    ).to_dict()
    graph["projected_activators"] = [activator]
    graph["projected_activations"] = [activation]
    graph["projected_sequences"] = [sequence]
    graph["summary"] = {
        "projected_activator_count": 1,
        "projected_activation_count": 1,
        "projected_sequence_count": 1,
        "projected_observation_state_count": 1,
    }
    validate_projected_temporal_activation_graph(graph)
    return graph


def test_temporal_contract_skeleton_is_schema_valid():
    graph = projected_temporal_contract_skeleton(
        metadata=metadata(),
        source_identity={"source_chart_id": "natal:test"},
        target_identity={"chart_id": "natal:test"},
        period={},
        projected_target_graph=target_graph(),
    ).to_dict()
    assert graph["metadata"]["package_type"] == "projected_temporal_activation_graph"
    assert graph["projected_artifact_limitations"]


def test_complete_projected_temporal_contract_validates():
    graph = complete_graph()
    assert graph["projected_activations"][0]["directionality"] == "activator_to_target"
    assert graph["projected_activations"][0]["temporal_facts"]["exactness"]["status"] == "closest_observed_only"


def test_projected_temporal_ids_are_deterministic_and_namespaced():
    first = complete_graph()
    second = complete_graph()
    assert first == second
    assert first["projected_activators"][0]["id"].startswith("projected_temporal_activator:")
    assert first["projected_activations"][0]["id"].startswith("projected_temporal_activation:")


def test_unknown_target_fails_referential_integrity():
    graph = complete_graph()
    graph["projected_activations"][0]["projected_target_ref"] = "projected:missing"
    with pytest.raises(ProjectionValidationError, match="unknown target"):
        validate_projected_temporal_activation_graph(graph)


def test_state_must_reference_owning_activation():
    graph = complete_graph()
    graph["projected_activations"][0]["temporal_facts"]["observation_states"][0]["projected_activation_ref"] = "wrong"
    with pytest.raises(ProjectionValidationError, match="owning activation"):
        validate_projected_temporal_activation_graph(graph)


def test_source_and_projected_limitations_are_distinct():
    graph = complete_graph()
    assert graph["upstream_source_limitations"] == ["No solved exact event is asserted."]
    assert "Stage C2" in graph["projected_artifact_limitations"][0]
