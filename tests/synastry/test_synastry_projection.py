from __future__ import annotations

import json

from semantic_projection import prepare_synastry_source_graph, project_synastry
from semantic_projection.profiles import builtin_projection_registry
from tests.paths import EXAMPLES_ROOT


def _source_graph():
    return {
        "metadata": {"graph_type": "synastry"},
        "objects": [
            {"id": "human:saturn", "name": "Saturn", "object_type": "planet", "subject_owner": "human", "sign": "Libra", "house": 6},
            {"id": "dog:mars", "name": "Mars", "object_type": "planet", "subject_owner": "dog", "sign": "Aries", "house": 1},
            {"id": "dog:moon", "name": "Moon", "object_type": "luminary", "subject_owner": "dog", "sign": "Cancer", "house": 4},
        ],
        "relationships": [
            {"id": "syn:1", "source_id": "human:saturn", "target_id": "dog:mars", "aspect": "square", "orb": 1.2},
            {"id": "syn:2", "source_id": "dog:moon", "target_id": "human:saturn", "aspect": "trine", "orb": 2.0},
        ],
    }


def _context(name):
    return json.loads((EXAMPLES_ROOT / "contexts" / name).read_text(encoding="utf-8"))


def test_woofmapped_human_dog_synastry_preserves_roles():
    result = project_synastry(
        source_graph=_source_graph(),
        structural_evidence={},
        source_identity={"source_chart_ids": ["human", "dog"]},
        participants=[
            {"participant_id": "human", "role": "handler", "species": "human"},
            {"participant_id": "dog", "role": "dog", "species": "canine"},
        ],
        relationship_kind="human_dog",
        profile_id="woofmapped_astrology.v0",
        profile_version="0.1.0",
        context=_context("woofmapped_human_dog_synastry_context.json"),
        registry=builtin_projection_registry(),
    )
    graph = result.artifact
    assert graph["summary"]["synastry_mode"] is True
    assert graph["summary"]["synastry"]["participant_count"] == 2
    assert len(graph["relationships"]) == 2
    attrs = graph["relationships"][0]["attributes"]
    assert attrs["inter_participant"] is True
    assert {attrs["source_participant_role"], attrs["target_participant_role"]} == {"handler", "dog"}


def test_synastry_projection_preserves_supplied_source_registries():
    result = project_synastry(
        source_graph=_source_graph(),
        structural_evidence={},
        source_identity={"source_chart_ids": ["human", "dog"]},
        participants=[
            {"participant_id": "human", "role": "handler", "species": "human"},
            {"participant_id": "dog", "role": "dog", "species": "canine"},
        ],
        relationship_kind="human_dog",
        profile_id="woofmapped_astrology.v0",
        profile_version="0.1.0",
        context=_context("woofmapped_human_dog_synastry_context.json"),
        registry=builtin_projection_registry(),
        source_registries={"theme_registry": {"example": ["trust"]}},
    )
    assert result.request.source_registries == {"theme_registry": {"example": ["trust"]}}


def test_orthodox_synastry_is_identity_projection_with_ownership():
    result = project_synastry(
        source_graph=_source_graph(),
        structural_evidence={},
        source_identity={"source_chart_ids": ["human", "dog"]},
        participants=[
            {"participant_id": "human", "role": "person_a"},
            {"participant_id": "dog", "role": "person_b"},
        ],
        relationship_kind="synastry",
        profile_id="orthodox_astrology.v1",
        profile_version="1.0.0",
        context=_context("orthodox_synastry_general_context.json"),
        registry=builtin_projection_registry(),
    )
    assert len(result.artifact["objects"]) == 3
    assert len(result.artifact["relationships"]) == 2
    assert all((obj["attributes"] or {}).get("subject_owner") for obj in result.artifact["objects"])
    assert result.artifact["summary"]["synastry_mode"] is True


def test_woofmapped_dog_dog_context_is_symmetric_and_hybrid_context_exists():
    dogdog = _context("woofmapped_dog_dog_synastry_context.json")
    hybrid = _context("woofmapped_hybrid_horoscope_context.json")
    assert dogdog["constraints"]["asymmetric_roles"] is False
    assert hybrid["parameters"]["required_sections"] == ["dog_internal_experience", "observable_behavior", "suggested_activities"]
    assert hybrid["parameters"]["forecast_policy"] == "woofmapped.forecast.blended.v0"


def test_synastry_preparation_retains_discovered_and_unresolved_ownership():
    graph = _source_graph()
    graph["objects"].append({"id": "visitor:jupiter", "name": "Jupiter", "object_type": "planet", "subject_owner": "visitor"})
    graph["objects"].append({"id": "unowned:pluto", "name": "Pluto", "object_type": "planet"})
    prepared, index = prepare_synastry_source_graph(
        graph,
        participants=[
            {"participant_id": "human", "role": "handler"},
            {"participant_id": "dog", "role": "dog"},
        ],
        relationship_kind="human_dog",
    )
    participants = {row["participant_id"]: row for row in index["participants"]}
    assert participants["visitor"]["role"] == "unspecified"
    unowned = next(row for row in prepared["objects"] if row["id"] == "unowned:pluto")
    assert "subject_owner" not in unowned
