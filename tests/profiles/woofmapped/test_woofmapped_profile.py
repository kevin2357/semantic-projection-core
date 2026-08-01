from __future__ import annotations

import json

from semantic_projection import ProjectionContext
from semantic_projection.profiles import builtin_projection_registry
from semantic_projection.profiles.woofmapped_astrology import (
    WoofmappedAstrologyProfile,
)
from tests.factories import project_dataset


def package_fixture() -> dict:
    objects = [
        {
            "id": "natal:Mars",
            "name": "Mars",
            "object_type": "planet_or_point",
            "sign": "Leo",
            "house": 6,
            "structural_strength_score": 0.8,
        },
        {
            "id": "natal:Venus",
            "name": "Venus",
            "object_type": "planet_or_point",
            "sign": "Scorpio",
            "house": 8,
            "structural_strength_score": 0.9,
        },
        {
            "id": "natal:Mercury",
            "name": "Mercury",
            "object_type": "planet_or_point",
            "sign": "Gemini",
            "house": 3,
            "structural_strength_score": 0.86,
        },
        {
            "id": "natal:ASC",
            "name": "ASC",
            "object_type": "angle",
            "sign": "Aquarius",
            "house": 1,
            "structural_strength_score": 0.95,
        },
        {
            "id": "house:8",
            "name": "House 8",
            "object_type": "house_cusp",
            "facts": {"house": 8},
            "structural_strength_score": 0.7,
        },
    ]
    aspect_names = [
        "conjunction",
        "semisextile",
        "sextile",
        "square",
        "trine",
        "quincunx",
        "opposition",
    ]
    relationships = []
    for index, aspect in enumerate(aspect_names):
        relationships.append(
            {
                "id": f"aspect:{aspect}:{index}",
                "relationship_type": "ASPECT",
                "source_id": "natal:Mars",
                "target_id": "natal:Venus",
                "aspect": aspect,
                "structural_strength_score": 0.75,
            }
        )
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
            "objects": objects,
            "relationships": relationships,
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
    )


def woof_context() -> ProjectionContext:
    return ProjectionContext(
        context_id="woofmapped.doghouse.general.v0",
        context_version="0.1.0",
        subject_scope="dog",
        target_domain="woofmapped_astrology.v0",
        application_context="woofmapped_natal_projection",
        audience="handler_general",
        constraints={"house_mapping_policy": "doghouse"},
    )


def by_canonical(result: dict) -> dict[str, dict]:
    return {
        row["attributes"]["canonical_object_name"]: row
        for row in result["objects"]
        if row.get("attributes", {}).get("canonical_object_name")
    }


def test_builtin_registry_contains_woofmapped_profile():
    profile = builtin_projection_registry().resolve("woofmapped_astrology.v0", "0.1.0")
    assert isinstance(profile, WoofmappedAstrologyProfile)


def test_expanded_cognitive_maps_sign_house_angle_and_all_sdk_aspects():
    result = project_dataset(
        package_fixture(),
        profile_id="cognitive_architecture_demo.v0",
        profile_version="0.2.0",
        context=cognitive_context(),
    )
    objects = by_canonical(result)
    mars = objects["Mars"]
    assert mars["name"] == "action_selection"
    assert mars["attributes"]["projected_mode"] == "expressive_self_amplification_mode"
    assert mars["attributes"]["projected_domain"] == "maintenance_routine_error_correction"
    assert objects["ASC"]["name"] == "active_interface"
    assert any(row["object_type"] == "cognitive_domain_primitive" for row in result["objects"])
    assert {row["attributes"]["canonical_aspect"] for row in result["relationships"]} == {
        "conjunction",
        "semisextile",
        "sextile",
        "square",
        "trine",
        "quincunx",
        "opposition",
    }


def test_woofmapped_operator_mode_doghouse_and_angle_projection():
    result = project_dataset(
        package_fixture(),
        profile_id="woofmapped_astrology.v0",
        profile_version="0.1.0",
        context=woof_context(),
    )
    objects = by_canonical(result)
    assert objects["Mars"]["name"] == "chase_play_defense_drive"
    assert objects["Mars"]["attributes"]["projected_mode"] == "attention_seeking_display_mode"
    assert objects["Mars"]["attributes"]["projected_domain"] == "doghouse_6_training_routine_care"
    assert objects["Venus"]["attributes"]["projected_domain"] == "doghouse_8_deep_trust_vulnerability"
    assert objects["Mercury"]["attributes"]["projected_mode"] == "information_sniffing_mode"
    assert objects["ASC"]["name"] == "behavioral_doorway"
    doghouse = next(row for row in result["objects"] if row["object_type"] == "woofmapped_doghouse_domain")
    assert doghouse["attributes"]["doghouse_number"] == 8
    assert doghouse["attributes"]["house_mapping_policy"] == "doghouse"


def test_woofmapped_all_sdk_aspects_and_projection_first_reasoning():
    result = project_dataset(
        package_fixture(),
        profile_id="woofmapped_astrology.v0",
        profile_version="0.1.0",
        context=woof_context(),
    )
    aspect_types = {row["attributes"]["canonical_aspect"]: row["relationship_type"] for row in result["relationships"]}
    assert aspect_types["square"] == "drive_conflict_requires_outlet"
    assert aspect_types["quincunx"] == "awkward_system_recalibration"
    assert aspect_types["semisextile"] == "subtle_adjacent_nudge"
    square = next(row for row in result["relationships"] if row["attributes"]["canonical_aspect"] == "square")
    assert square["attributes"]["projection_first_reasoning"] == {
        "source_mapping": "chase_play_defense_drive",
        "source_mode": "attention_seeking_display_mode",
        "relationship_mapping": "drive_conflict_requires_outlet",
        "target_mapping": "bonding_preference",
        "target_mode": "obsessive_investigation_mode",
    }


def test_three_profiles_share_source_but_not_target_ontology_or_vocabulary():
    package = package_fixture()
    before = json.dumps(package, sort_keys=True)
    orthodox = project_dataset(package)
    cognitive = project_dataset(
        package,
        profile_id="cognitive_architecture_demo.v0",
        profile_version="0.2.0",
        context=cognitive_context(),
    )
    woof = project_dataset(
        package,
        profile_id="woofmapped_astrology.v0",
        profile_version="0.1.0",
        context=woof_context(),
    )
    assert orthodox["source_graph_ref"] == cognitive["source_graph_ref"] == woof["source_graph_ref"]
    assert orthodox["source_identity"] == cognitive["source_identity"] == woof["source_identity"]
    assert {
        orthodox["target_ontology"],
        cognitive["target_ontology"],
        woof["target_ontology"],
    } == {
        "orthodox_astrology.v1",
        "cognitive_architecture_demo.v0",
        "woofmapped_astrology.v0",
    }
    cognitive_text = json.dumps(cognitive)
    woof_text = json.dumps(woof)
    assert "romance_affection" not in cognitive_text
    assert "doghouse_8_deep_trust_vulnerability" not in cognitive_text
    assert "frictional_coordination" not in woof_text
    assert "behavioral_friction" in woof_text
    assert json.dumps(package, sort_keys=True) == before


def test_woofmapped_guardrails_and_determinism():
    kwargs = {
        "profile_id": "woofmapped_astrology.v0",
        "profile_version": "0.1.0",
        "context": woof_context(),
    }
    first = project_dataset(package_fixture(), **kwargs)
    second = project_dataset(package_fixture(), **kwargs)
    assert first == second
    assert first["summary"]["playful_experimental_projection"] is True
    assert first["summary"]["veterinary_advice"] is False
    assert first["summary"]["behavioral_diagnosis_permitted"] is False
    assert first["summary"]["house_mapping_policy"] == "doghouse"
