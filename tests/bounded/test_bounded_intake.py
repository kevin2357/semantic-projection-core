from __future__ import annotations

import json
from copy import deepcopy

import pytest

from semantic_projection import (
    BoundedNatalSourceContractError,
    ProjectionContext,
    ProjectionValidationError,
    adapt_foundry_bounded_natal_dataset,
    identify_artifact,
    validate_foundry_bounded_natal_dataset,
    validate_projection_request,
)
from tests.paths import FIXTURES_ROOT

FIXTURE = FIXTURES_ROOT / "agf" / "bounded_natal_v1_tiny.json"


def load_artifact() -> dict:
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


def context() -> ProjectionContext:
    return ProjectionContext(
        context_id="woofmapped.doghouse.general.v0",
        context_version="0.1.0",
        subject_scope="dog",
        target_domain="woofmapped_astrology.v0",
        application_context="woofmapped_natal_projection",
        constraints={"house_mapping_policy": "doghouse"},
    )


def adapt(artifact: dict):
    return adapt_foundry_bounded_natal_dataset(
        artifact,
        profile_id="woofmapped_bounded_astrology.v0",
        profile_version="0.1.0",
        context=context(),
    )


def test_valid_artifact_adapts_atomically_without_mutating_source():
    artifact = load_artifact()
    original = deepcopy(artifact)
    request = adapt(artifact)

    assert artifact == original
    assert request.request_contract == "bounded_natal_projection_request.v1"
    assert request.request_id.startswith("bounded_natal_projection_request:")
    assert request.source_artifact == artifact
    assert request.source_artifact is not artifact
    assert request.source_identity["source_chart_id"] == "astrowoof:dog:018f"
    assert len(request.source_identity["source_artifact_sha256"]) == 64
    assert request.extensions["execution_status"] == "validated_intake_only"
    assert identify_artifact(artifact).kind == "foundry_bounded_natal_dataset"
    assert identify_artifact(request.to_dict()).kind == "bounded_natal_projection_request"


def test_request_identity_is_deterministic_and_context_sensitive():
    artifact = load_artifact()
    first = adapt(artifact)
    second = adapt(artifact)
    assert first.to_dict() == second.to_dict()

    handler = context()
    handler.context_id = "woofmapped.handler_guidance.v1"
    handler.context_version = "1.0.0"
    changed = adapt_foundry_bounded_natal_dataset(
        artifact,
        profile_id="woofmapped_bounded_astrology.v0",
        profile_version="0.1.0",
        context=handler,
    )
    assert changed.request_id != first.request_id
    assert changed.source_identity == first.source_identity


@pytest.mark.parametrize(
    ("mutate", "message"),
    [
        (lambda value: value["metadata"].__setitem__("schema_version", "9.0.0"), "validation failed"),
        (lambda value: value["canonical_astrology_graph"].__setitem__("graph_version", "1.6.0"), "validation failed"),
        (lambda value: value["uncertainty_assessment"].__setitem__("evidence_contract_version", "future"), "validation failed"),
        (lambda value: value["metadata"].__setitem__("source_chart_id", "different"), "source_chart_ids"),
        (lambda value: value["canonical_astrology_graph"]["objects"][0].__setitem__("longitude", 1.0), "forbidden precision"),
        (lambda value: value["canonical_astrology_graph"]["relationships"][0].__setitem__("strength", 1.0), "forbidden exact/scored"),
        (lambda value: value["canonical_astrology_graph"]["relationships"][0].__setitem__("target_id", "missing"), "unknown target_id"),
        (lambda value: value["uncertainty_assessment"]["evidence_registry"].pop("uncertainty:bodies:Sun"), "missing evidence"),
        (lambda value: value["canonical_astrology_graph"]["objects"][0]["evidence_metadata"].__setitem__("evidence_family_group", ""), "non-empty string"),
        (lambda value: value["uncertainty_assessment"]["evidence_registry"]["uncertainty:bodies:Sun"].__setitem__("classification", "probably"), "unknown classification"),
        (lambda value: value["capabilities"].__setitem__("supports_exact_longitudes", True), "capabilities disagree"),
    ],
)
def test_invalid_cross_section_variants_fail_deterministically(mutate, message):
    artifact = load_artifact()
    mutate(artifact)
    with pytest.raises(BoundedNatalSourceContractError, match=message):
        validate_foundry_bounded_natal_dataset(artifact)


def test_released_extra_availability_reason_is_preserved_not_reinterpreted():
    artifact = load_artifact()
    evidence = artifact["uncertainty_assessment"]["evidence_registry"]["uncertainty:bodies:Sun"]
    evidence["classification"] = "unavailable"
    evidence["availability"] = "prerequisite_variable_or_unavailable"
    validate_foundry_bounded_natal_dataset(artifact)
    assert adapt(artifact).source_artifact["uncertainty_assessment"]["evidence_registry"]["uncertainty:bodies:Sun"] == evidence


def test_promoted_qualifiers_require_their_distinct_evidence_refs():
    artifact = load_artifact()
    artifact["canonical_astrology_graph"]["objects"][0]["house_number"] = 8
    with pytest.raises(BoundedNatalSourceContractError, match="house_uncertainty_evidence_ref"):
        validate_foundry_bounded_natal_dataset(artifact)

    artifact = load_artifact()
    artifact["canonical_astrology_graph"]["objects"][0]["triplicity_ruler"] = "Sun"
    with pytest.raises(BoundedNatalSourceContractError, match="triplicity_uncertainty_evidence_ref"):
        validate_foundry_bounded_natal_dataset(artifact)


def test_existing_static_route_rejects_bounded_graph_with_route_guidance():
    artifact = load_artifact()
    request = {
        "request_id": "wrong-route",
        "profile_id": "woofmapped_astrology.v0",
        "profile_version": "0.1.0",
        "source_graph": artifact["canonical_astrology_graph"],
        "structural_evidence": artifact["structural_evidence_graph"],
        "source_identity": {
            "source_chart_ids": ["astrowoof:dog:018f"],
            "sensor_instance_id": "astrowoof:dog:018f",
        },
        "context": context().to_dict(),
        "source_registries": {},
        "options": {},
    }
    with pytest.raises(ProjectionValidationError, match="bounded_natal_projection_request"):
        validate_projection_request(request)
