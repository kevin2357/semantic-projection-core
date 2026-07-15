from __future__ import annotations

import json
from copy import deepcopy

from semantic_projection import (
    ProjectionContext,
    ProjectionOptions,
    ProjectionProfileRegistry,
    ProjectionRequest,
    project,
    projection_request_id,
)
from semantic_projection.profiles.demo import DemonstrationProjectionProfile
from semantic_projection.profiles.orthodox_astrology import OrthodoxAstrologyProfile


def orthodox_request() -> ProjectionRequest:
    context = ProjectionContext(
        context_id="orthodox.natal.general.v1",
        context_version="1.0.0",
        subject_scope="individual",
        target_domain="orthodox_astrology.v1",
        application_context="natal_interpretation",
    ).to_dict()
    options = ProjectionOptions(unmapped_policy="diagnostic").to_dict()
    source_identity = {
        "source_chart_id": "fixture:orthodox",
        "source_chart_ids": ["fixture:orthodox"],
        "sensor_instance_id": "fixture:orthodox",
    }
    source_graph = {
        "graph_type": "canonical_astrology_graph",
        "graph_version": "1.3.0",
        "objects": [
            {
                "id": "natal:Mars",
                "name": "Mars",
                "object_type": "planet_or_point",
                "operator_hints": [{"operator": "act"}],
                "structural_strength_score": 0.8,
            },
            {
                "id": "natal:Venus",
                "name": "Venus",
                "object_type": "planet_or_point",
                "operator_hints": [{"operator": "value"}],
                "structural_strength_score": 0.9,
            },
            {
                "id": "natal:Unsupported",
                "name": "Unsupported",
                "object_type": "calculated_point",
            },
        ],
        "relationships": [{
            "id": "aspect:Mars:square:Venus",
            "relationship_type": "ASPECT",
            "source_id": "natal:Mars",
            "target_id": "natal:Venus",
            "aspect": "square",
            "orb": 1.0,
            "operator_hints": [{"operator": "stress"}],
            "structural_strength_score": 0.75,
        }],
    }
    return ProjectionRequest(
        request_id=projection_request_id(
            profile_id="orthodox_astrology.v1",
            profile_version="1.0.0",
            source_identity=source_identity,
            context=context,
            options=options,
        ),
        profile_id="orthodox_astrology.v1",
        profile_version="1.0.0",
        source_graph=source_graph,
        structural_evidence={"graph_version": "1.3.0"},
        source_identity=source_identity,
        context=context,
        options=options,
    )


def registry() -> ProjectionProfileRegistry:
    result = ProjectionProfileRegistry()
    result.register(OrthodoxAstrologyProfile())
    return result


def test_venus_and_mars_project_to_orthodox_primitives():
    result = project(orthodox_request(), registry=registry()).to_dict()
    by_canonical = {
        row["attributes"]["canonical_object_name"]: row
        for row in result["objects"]
    }
    assert by_canonical["Venus"]["name"] == "value_attraction_harmony"
    assert {"value", "attract", "bond"} <= set(by_canonical["Venus"]["operators"])
    assert by_canonical["Venus"]["attributes"]["source_names"] == ["Venus"]
    assert by_canonical["Mars"]["name"] == "action_assertion_drive"
    assert result["audit"]["coverage"]["unmapped_source_object_count"] == 0


def test_mars_square_venus_projects_inside_orthodox_ontology():
    result = project(orthodox_request(), registry=registry()).to_dict()
    relationship = result["relationships"][0]
    assert relationship["relationship_type"] == "pressures_and_develops"
    assert {"stress", "activate", "develop"} <= set(relationship["operators"])
    assert {
        "conflict_drive", "growth_edge", "romance_affection", "values_resources"
    } <= set(relationship["theme_tags"])
    assert relationship["attributes"]["source_object_name"] == "Mars"
    assert relationship["attributes"]["target_object_name"] == "Venus"
    assert relationship["attributes"]["projection_relevance_components"] == {
        "context_salience": 1.0,
        "profile_salience": 0.98,
        "structural_strength": 0.75,
    }
    assert relationship["projection_relevance_score"] == 0.735


def test_projection_preserves_canonical_input_and_is_deterministic():
    request = orthodox_request()
    before = json.dumps(request.source_graph, sort_keys=True)
    first = project(request, registry=registry()).to_dict()
    second = project(request, registry=registry()).to_dict()
    assert first == second
    assert json.dumps(request.source_graph, sort_keys=True) == before
    assert all("theme_tags" not in row for row in request.source_graph["relationships"])


def test_demo_merge_uses_source_names_array_without_last_write_loss():
    profile = DemonstrationProjectionProfile()
    value = ProjectionProfileRegistry()
    value.register(profile)
    context = ProjectionContext(
        context_id="demonstration.general.v0",
        context_version="0.1.0",
        subject_scope="system",
        target_domain="demonstration_semantics.v0",
        application_context="merge_test",
    ).to_dict()
    identity = {
        "source_chart_id": "fixture:merge",
        "source_chart_ids": ["fixture:merge"],
        "sensor_instance_id": "fixture:merge",
    }
    options = ProjectionOptions().to_dict()
    request = ProjectionRequest(
        request_id=projection_request_id(
            profile_id=profile.manifest.profile_id,
            profile_version=profile.manifest.profile_version,
            source_identity=identity,
            context=context,
            options=options,
        ),
        profile_id=profile.manifest.profile_id,
        profile_version=profile.manifest.profile_version,
        source_graph={
            "graph_type": "canonical_astrology_graph",
            "graph_version": "1.3.0",
            "objects": [
                {"id": "a", "name": "Input A", "demo_category": "shared"},
                {"id": "b", "name": "Input B", "demo_category": "shared"},
            ],
            "relationships": [],
        },
        structural_evidence={},
        source_identity=identity,
        context=context,
        options=options,
    )
    result = project(request, registry=value).to_dict()
    assert result["objects"][0]["attributes"]["source_names"] == [
        "Input A", "Input B"
    ]
