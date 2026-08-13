from __future__ import annotations

import json
from copy import deepcopy

import pytest

from semantic_projection import (
    ProjectionContext,
    ProjectionValidationError,
    adapt_foundry_bounded_natal_dataset,
    bounded_evidence_closure,
    build_projected_bounded_contract,
    identify_artifact,
    projected_bounded_correspondence_id,
    validate_projected_bounded_semantic_graph,
)
from tests.paths import FIXTURES_ROOT

FIXTURE = FIXTURES_ROOT / "agf" / "bounded_natal_v1_tiny.json"


def source_artifact() -> dict:
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


def context(context_id: str = "woofmapped.doghouse.general.v0") -> ProjectionContext:
    versions = {
        "woofmapped.doghouse.general.v0": "0.1.0",
        "woofmapped.handler_guidance.v1": "1.0.0",
    }
    return ProjectionContext(
        context_id=context_id,
        context_version=versions[context_id],
        subject_scope="dog",
        target_domain="woofmapped_astrology.v0",
        application_context="woofmapped_natal_projection",
        constraints={"house_mapping_policy": "doghouse"},
    )


def request(context_id: str = "woofmapped.doghouse.general.v0"):
    return adapt_foundry_bounded_natal_dataset(
        source_artifact(),
        profile_id="woofmapped_bounded_astrology.v0",
        profile_version="0.1.0",
        context=context(context_id),
    )


def projected_rows(context_id: str = "woofmapped.doghouse.general.v0") -> tuple[list[dict], list[dict]]:
    profile_id = "woofmapped_bounded_astrology.v0"
    sun_ref = "canonical:object:astrowoof:dog:018f:Sun"
    mars_ref = "canonical:object:astrowoof:dog:018f:Mars"
    sun_correspondence = projected_bounded_correspondence_id(
        kind="object", profile_id=profile_id, semantic_key="pack_role_identity", source_refs=[sun_ref]
    )
    mars_correspondence = projected_bounded_correspondence_id(
        kind="object", profile_id=profile_id, semantic_key="chase_play_defense_drive", source_refs=[mars_ref]
    )
    objects = [
        {
            "id": f"projected:{context_id}:sun",
            "correspondence_id": sun_correspondence,
            "object_type": "woofmapped_operator",
            "name": "pack_role_identity",
            "target_ontology": "woofmapped_astrology.v0",
            "operators": ["express_pack_role"],
            "attributes": {},
            "source_refs": [sun_ref],
            "mapping_rule_refs": ["woofmapped_bounded_astrology.v0.object.sun"],
            "context_refs": [context_id],
            "epistemic_basis": {
                "classification": "invariant",
                "evidence_refs": ["uncertainty:bodies:Sun"],
                "evidence_family_groups": ["astrowoof:dog:018f:object-family:Sun"],
                "proof_scope": "complete_normalized_birth_interval",
            },
            "provenance": {},
        },
        {
            "id": f"projected:{context_id}:mars",
            "correspondence_id": mars_correspondence,
            "object_type": "woofmapped_operator",
            "name": "chase_play_defense_drive",
            "target_ontology": "woofmapped_astrology.v0",
            "operators": ["execute"],
            "attributes": {},
            "source_refs": [mars_ref],
            "mapping_rule_refs": ["woofmapped_bounded_astrology.v0.object.mars"],
            "context_refs": [context_id],
            "epistemic_basis": {
                "classification": "invariant",
                "evidence_refs": ["uncertainty:bodies:Sun"],
                "evidence_family_groups": ["astrowoof:dog:018f:object-family:Mars"],
                "proof_scope": "complete_normalized_birth_interval",
            },
            "provenance": {},
        },
    ]
    relationship_ref = "canonical:relationship:rel:bounded:trine"
    relationships = [{
        "id": f"projected_relation:{context_id}:trine",
        "correspondence_id": projected_bounded_correspondence_id(
            kind="relationship",
            profile_id=profile_id,
            semantic_key="natural_behavioral_channel",
            source_refs=[relationship_ref],
        ),
        "relationship_type": "natural_behavioral_channel",
        "source_id": objects[0]["id"],
        "target_id": objects[1]["id"],
        "operators": ["flow"],
        "theme_tags": [],
        "attributes": {},
        "source_relationship_refs": [relationship_ref],
        "mapping_rule_refs": ["woofmapped_bounded_astrology.v0.aspect.trine"],
        "context_refs": [context_id],
        "epistemic_basis": {
            "classification": "invariant",
            "evidence_refs": ["uncertainty:aspects:Sun:Mars"],
            "evidence_family_groups": ["astrowoof:dog:018f:relationship-family:Sun:Mars"],
            "proof_scope": "complete_normalized_birth_interval",
        },
        "provenance": {},
    }]
    return objects, relationships


def test_empty_contract_is_valid_and_preserves_source_epistemic_state():
    graph = build_projected_bounded_contract(
        request(), target_ontology="woofmapped_astrology.v0"
    ).to_dict()
    assert graph["metadata"]["output_contract"] == "projected_bounded_semantic_graph.v1"
    assert graph["objects"] == []
    assert graph["source_capabilities"]["supports_exact_longitudes"] is False
    assert graph["source_feature_dispositions"]["representative_longitudes"] == "prohibited_precision_laundering"
    assert graph["provenance"]["context_epistemic_policy"] == "certainty_invariant_across_contexts"
    assert identify_artifact(graph).kind == "projected_bounded_graph"


def test_evidence_closure_includes_resolvable_prerequisites_and_preserves_opaque_refs():
    artifact = source_artifact()
    closure = bounded_evidence_closure(
        artifact, ["uncertainty:aspects:Sun:Mars"]
    )
    assert list(closure["records"]) == [
        "uncertainty:aspects:Sun:Mars",
        "uncertainty:bodies:Sun",
    ]
    assert closure["resolved_prerequisite_refs"] == ["uncertainty:bodies:Sun"]
    assert closure["unresolved_prerequisite_refs"] == ["provider:ephemeris"]
    assert closure["source_registry_record_count"] == 2
    assert closure["materialized_record_count"] == 2


def test_direct_missing_evidence_is_fatal():
    with pytest.raises(ValueError, match="Missing direct bounded evidence"):
        bounded_evidence_closure(source_artifact(), ["uncertainty:missing"])


def test_nonempty_contract_validates_evidence_endpoints_and_correspondence_indexes():
    objects, relationships = projected_rows()
    graph = build_projected_bounded_contract(
        request(),
        target_ontology="woofmapped_astrology.v0",
        objects=objects,
        relationships=relationships,
    ).to_dict()
    assert graph["summary"]["source_evidence_record_count"] == 2
    assert len(graph["indexes"]["entity_by_correspondence_id"]) == 3
    assert graph["summary"]["raw_counts_are_weights"] is False


def test_correspondence_is_context_independent_but_projection_identity_is_not():
    general_objects, general_relationships = projected_rows()
    handler_objects, handler_relationships = projected_rows(
        "woofmapped.handler_guidance.v1"
    )
    general = build_projected_bounded_contract(
        request(), target_ontology="woofmapped_astrology.v0",
        objects=general_objects, relationships=general_relationships,
    ).to_dict()
    handler = build_projected_bounded_contract(
        request("woofmapped.handler_guidance.v1"),
        target_ontology="woofmapped_astrology.v0",
        objects=handler_objects, relationships=handler_relationships,
    ).to_dict()
    assert general["metadata"]["projection_id"] != handler["metadata"]["projection_id"]
    assert [row["correspondence_id"] for row in general["objects"]] == [
        row["correspondence_id"] for row in handler["objects"]
    ]
    assert general["provenance"]["epistemic_identity"] == handler["provenance"]["epistemic_identity"]
    assert general["source_evidence"] == handler["source_evidence"]


@pytest.mark.parametrize(
    ("mutate", "message"),
    [
        (lambda graph: graph["objects"][0].__setitem__("structural_strength_score", 1.0), "False schema"),
        (lambda graph: graph["objects"][0]["epistemic_basis"].__setitem__("classification", "variable"), "'invariant' was expected"),
        (lambda graph: graph["relationships"][0].__setitem__("target_id", "missing"), "unknown target_id"),
        (lambda graph: graph["objects"][0]["epistemic_basis"].__setitem__("evidence_refs", ["missing"]), "missing source evidence"),
        (lambda graph: graph["objects"][1].__setitem__("correspondence_id", graph["objects"][0]["correspondence_id"]), "Duplicate bounded correspondence"),
    ],
)
def test_invalid_projected_contract_variants_fail(mutate, message):
    objects, relationships = projected_rows()
    graph = build_projected_bounded_contract(
        request(), target_ontology="woofmapped_astrology.v0",
        objects=objects, relationships=relationships,
    ).to_dict()
    mutate(graph)
    with pytest.raises(ProjectionValidationError, match=message):
        validate_projected_bounded_semantic_graph(graph)


def test_contract_builder_is_deterministic_and_does_not_mutate_rows():
    objects, relationships = projected_rows()
    before_objects, before_relationships = deepcopy(objects), deepcopy(relationships)
    first = build_projected_bounded_contract(
        request(), target_ontology="woofmapped_astrology.v0",
        objects=objects, relationships=relationships,
    ).to_dict()
    second = build_projected_bounded_contract(
        request(), target_ontology="woofmapped_astrology.v0",
        objects=objects, relationships=relationships,
    ).to_dict()
    assert first == second
    assert objects == before_objects
    assert relationships == before_relationships
