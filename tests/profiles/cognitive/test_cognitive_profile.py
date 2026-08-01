from __future__ import annotations

import json

from semantic_projection import ProjectionContext
from semantic_projection.profiles import builtin_projection_registry
from semantic_projection.profiles.cognitive_architecture_demo import (
    CognitiveArchitectureDemoProfile,
)
from tests.factories import project_dataset


def package_fixture() -> dict:
    return {
        "metadata": {
            "analysis_type": "natal_dataset",
            "source_chart_id": "natal:fixture",
            "source_chart_ids": ["natal:fixture"],
            "sensor_instance_id": "natal:fixture",
        },
        "canonical_astrology_graph": {
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
                    "id": "natal:Sun",
                    "name": "Sun",
                    "object_type": "planet_or_point",
                    "structural_strength_score": 0.95,
                },
                {
                    "id": "natal:Unsupported",
                    "name": "Unsupported",
                    "object_type": "harmonic_point",
                },
            ],
            "relationships": [
                {
                    "id": "aspect:Mars:square:Venus",
                    "relationship_type": "ASPECT",
                    "source_id": "natal:Mars",
                    "target_id": "natal:Venus",
                    "aspect": "square",
                    "operator_hints": [{"operator": "stress"}],
                    "structural_strength_score": 0.75,
                },
                {
                    "id": "aspect:Sun:trine:Mars",
                    "relationship_type": "ASPECT",
                    "source_id": "natal:Sun",
                    "target_id": "natal:Mars",
                    "aspect": "trine",
                    "structural_strength_score": 0.7,
                },
            ],
        },
        "structural_evidence_graph": {"graph_version": "1.3.0"},
    }


def cognitive_context() -> ProjectionContext:
    return ProjectionContext(
        context_id="cognitive_architecture.general.v0",
        context_version="0.2.0",
        subject_scope="individual",
        target_domain="cognitive_architecture_demo.v0",
        application_context="cognitive_architecture_demo",
        constraints={
            "experimental": True,
            "clinical_use": False,
            "diagnostic_use": False,
        },
    )


def test_builtin_registry_contains_cognitive_demo_profile():
    profile = builtin_projection_registry().resolve(
        "cognitive_architecture_demo.v0",
        "0.2.0",
    )
    assert isinstance(profile, CognitiveArchitectureDemoProfile)


def test_core_objects_project_to_cognitive_primitives():
    result = project_dataset(
        package_fixture(),
        profile_id="cognitive_architecture_demo.v0",
        profile_version="0.2.0",
        context=cognitive_context(),
    )
    by_source = {row["attributes"]["canonical_object_name"]: row for row in result["objects"]}
    assert by_source["Mars"]["name"] == "action_selection"
    assert by_source["Venus"]["name"] == "valuation_preference"
    assert by_source["Sun"]["name"] == "identity_organization"
    assert all(row["object_type"] == "cognitive_process_primitive" for row in result["objects"])
    assert result["audit"]["coverage"]["unmapped_source_object_count"] == 1


def test_mars_square_venus_reasons_between_projected_primitives():
    result = project_dataset(
        package_fixture(),
        profile_id="cognitive_architecture_demo.v0",
        profile_version="0.2.0",
        context=cognitive_context(),
    )
    row = next(relationship for relationship in result["relationships"] if relationship["attributes"]["canonical_aspect"] == "square")
    assert row["relationship_type"] == "interferes_and_forces_adaptation"
    assert row["attributes"]["source_process"] == "action_selection"
    assert row["attributes"]["target_process"] == "valuation_preference"
    assert row["attributes"]["interaction_mode"] == "frictional_coordination"
    assert row["attributes"]["projection_first_reasoning"] == {
        "source_mapping": "action_selection",
        "relationship_mapping": "interferes_and_forces_adaptation",
        "target_mapping": "valuation_preference",
    }


def test_cognitive_output_does_not_leak_orthodox_romance_vocabulary():
    result = project_dataset(
        package_fixture(),
        profile_id="cognitive_architecture_demo.v0",
        profile_version="0.2.0",
        context=cognitive_context(),
    )
    serialized = json.dumps(result)
    for forbidden in (
        "romance_affection",
        "values_resources",
        "partnership_mirroring",
        "orthodox_astrology_primitive",
    ):
        assert forbidden not in serialized


def test_same_source_projects_differently_across_profiles():
    package = package_fixture()
    before = json.dumps(package, sort_keys=True)
    orthodox = project_dataset(package)
    cognitive = project_dataset(
        package,
        profile_id="cognitive_architecture_demo.v0",
        profile_version="0.2.0",
        context=cognitive_context(),
    )
    assert orthodox["source_graph_ref"] == cognitive["source_graph_ref"]
    assert orthodox["source_identity"] == cognitive["source_identity"]
    assert orthodox["target_ontology"] == "orthodox_astrology.v1"
    assert cognitive["target_ontology"] == "cognitive_architecture_demo.v0"
    assert {row["name"] for row in orthodox["objects"]} != {row["name"] for row in cognitive["objects"]}
    assert json.dumps(package, sort_keys=True) == before


def test_cognitive_projection_is_deterministic_and_guardrailed():
    kwargs = {
        "profile_id": "cognitive_architecture_demo.v0",
        "profile_version": "0.2.0",
        "context": cognitive_context(),
    }
    first = project_dataset(package_fixture(), **kwargs)
    second = project_dataset(package_fixture(), **kwargs)
    assert first == second
    assert first["summary"]["experimental_demo"] is True
    assert first["summary"]["validated_psychological_model"] is False
    assert first["summary"]["diagnostic_use_permitted"] is False
    assert all("not_diagnostic" in row["attributes"]["demo_guardrails"] for row in first["objects"])
