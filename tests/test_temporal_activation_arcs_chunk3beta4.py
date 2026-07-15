from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

from semantic_projection import (
    ProjectionContext,
    adapt_foundry_temporal_source_bundle,
    project_temporal,
    validate_projected_temporal_activation_graph,
)

FIXTURE = Path(__file__).parent / "fixtures" / "foundry_temporal_source_bundle_v1_tiny.json"


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


def test_c4_projects_one_source_arc_once_and_preserves_temporal_facts():
    result = project_temporal(request())
    assert result["metadata"]["package_type"] == "projected_temporal_activation_graph"
    assert len(result["projected_activators"]) == 1
    assert len(result["projected_activations"]) == 1
    arc = result["projected_activations"][0]
    assert arc["directionality"] == "activator_to_target"
    assert arc["temporal_role"] == "current_activation"
    assert arc["projected_relationship_type"] == "enables_optional_coordination"
    assert arc["temporal_facts"]["exact_at"] is None
    assert arc["temporal_facts"]["exactness"]["status"] == "closest_observed_only"
    assert arc["temporal_facts"]["observation_count"] == 1
    assert len(arc["temporal_facts"]["observation_states"]) == 1
    validate_projected_temporal_activation_graph(result)


def test_c4_is_deterministic_and_input_immutable():
    req = request()
    before = deepcopy(req.to_dict())
    assert project_temporal(req) == project_temporal(req)
    assert req.to_dict() == before


def test_c4_classifies_mean_node_as_policy_excluded():
    req = request()
    req.temporal_source_graph["activators"].append({
        "id": "canonical:transiting_object:mean_node",
        "object_type": "transiting_object",
        "name": "Mean Node",
        "source_body": "Mean Node",
    })
    result = project_temporal(req)
    coverage = result["summary"]["coverage"]["activators"]
    assert coverage["policy_excluded_activator_count"] == 1
    assert coverage["eligible_but_unmapped_activator_count"] == 0
