from __future__ import annotations

import json
from copy import deepcopy

import pytest

from semantic_projection import (
    BoundedProjectionExecutionError,
    ProjectionContext,
    adapt_foundry_bounded_natal_dataset,
    project_bounded_natal_objects,
    validate_contract,
)
from semantic_projection.profiles.woofmapped_bounded_astrology import (
    WoofmappedBoundedAstrologyProfile,
)
from semantic_projection.term_registry import validate_projected_term_registry
from tests.paths import FIXTURES_ROOT

FIXTURE = FIXTURES_ROOT / "agf" / "bounded_natal_v1_tiny.json"


def _metadata(*, tier: str, derivation: str, family: str, token: str, owner: str | None = None) -> dict:
    result = {
        "evidence_tier": tier,
        "derivation_type": derivation,
        "derivation_family": family,
        "source_sensor_id": "astrowoof:dog:018f",
        "sensor_instance_id": "astrowoof:dog:018f",
        "source_chart_ids": ["astrowoof:dog:018f"],
        "record_independence_group": f"astrowoof:dog:018f:object-record:{token}",
        "evidence_family_group": f"astrowoof:dog:018f:object-family:{owner or token}",
        "independence_group": f"astrowoof:dog:018f:object-family:{owner or token}",
        "source_chart_family_group": f"chart:018f:object-family:{owner or token}",
    }
    if owner:
        result["root_owner_object_ref"] = owner
        result["owner_object_ref"] = owner
    return result


def _add_object(artifact: dict, row: dict, *, evidence_ref: str) -> None:
    artifact["uncertainty_assessment"]["evidence_registry"][evidence_ref] = {
        "evidence_contract_version": "agf.bounded_uncertainty_evidence.v1.0.0",
        "feature_key": evidence_ref,
        "classification": "invariant",
        "value_kind": "categorical_test_fixture",
        "possibilities": {"possibility_type": "categorical_set", "values": ["stable"], "count": 1},
        "prerequisite_refs": [],
        "range_evidence": None,
        "transition_witnesses": [],
        "counterexamples": [],
        "proof_scope": "complete_normalized_birth_interval",
    }
    row["uncertainty_evidence_ref"] = evidence_ref
    if row.get("house_number") is not None and row.get("object_type") != "bounded_house_cusp":
        house_ref = evidence_ref + ":house"
        artifact["uncertainty_assessment"]["evidence_registry"][house_ref] = {
            **deepcopy(artifact["uncertainty_assessment"]["evidence_registry"][evidence_ref]),
            "feature_key": house_ref,
            "value_kind": "natal_house_number",
        }
        row["house_uncertainty_evidence_ref"] = house_ref
    artifact["canonical_astrology_graph"]["objects"].append(row)


def artifact_with_object_families() -> dict:
    artifact = json.loads(FIXTURE.read_text(encoding="utf-8"))
    root = "astrowoof:dog:018f:Sun"
    additions = [
        ({
            "id": "astrowoof:dog:018f:ASC", "object_type": "bounded_angle",
            "name": "ASC", "sign_index": 6, "house_number": 1,
            "evidence_metadata": _metadata(tier="angle", derivation="derived", family="angle", token="ASC"),
        }, "uncertainty:angle:ASC"),
        ({
            "id": "astrowoof:dog:018f:house:1", "object_type": "bounded_house_cusp",
            "name": "House 1 cusp", "house_number": 1, "sign_index": 6,
            "traditional_ruler": "Venus", "modern_ruler": "Venus",
            "evidence_metadata": _metadata(tier="angle", derivation="derived", family="house_cusp", token="house:1"),
        }, "uncertainty:cusp:1"),
        ({
            "id": "astrowoof:dog:018f:Fortune", "object_type": "bounded_calculated_point",
            "name": "Fortune", "sign_index": 2, "house_number": 4,
            "possible_formula_ids": ["day_formula", "night_formula"],
            "evidence_metadata": _metadata(tier="calculated_point", derivation="derived", family="calculated_point", token="Fortune"),
        }, "uncertainty:calculated:Fortune"),
        ({
            "id": "astrowoof:dog:018f:Sun:H3", "object_type": "bounded_harmonic_point",
            "name": "Sun harmonic 3", "sign_index": 1, "owner_object_ref": root,
            "transform_kind": "harmonic", "harmonic_number": 3,
            "evidence_metadata": _metadata(tier="harmonic", derivation="derived", family="harmonic", token="Sun:H3", owner=root),
        }, "uncertainty:transform:Sun:H3"),
        ({
            "id": "astrowoof:dog:018f:sect", "object_type": "bounded_sect_state",
            "name": "Day sect", "sect": "day",
            "evidence_metadata": _metadata(tier="derived", derivation="derived", family="sect", token="sect"),
        }, "uncertainty:sect"),
        ({
            "id": "astrowoof:dog:018f:Eros", "object_type": "bounded_calculated_point",
            "name": "Eros", "sign_index": 5,
            "evidence_metadata": _metadata(tier="calculated_point", derivation="derived", family="calculated_point", token="Eros"),
        }, "uncertainty:calculated:Eros"),
    ]
    for row, evidence_ref in additions:
        _add_object(artifact, row, evidence_ref=evidence_ref)
    graph = artifact["canonical_astrology_graph"]
    graph["objects"] = sorted(graph["objects"], key=lambda row: row["id"])
    graph["summary"]["object_count"] = len(graph["objects"])
    return artifact


def context(context_id: str = "woofmapped.doghouse.general.v0") -> ProjectionContext:
    versions = {
        "woofmapped.doghouse.general.v0": "0.1.0",
        "woofmapped.handler_guidance.v1": "1.0.0",
    }
    return ProjectionContext(
        context_id=context_id,
        context_version=versions.get(context_id, "1.0.0"),
        subject_scope="dog",
        target_domain="woofmapped_astrology.v0",
        application_context="woofmapped_natal_projection",
        constraints={"house_mapping_policy": "doghouse"},
    )


def request(artifact: dict | None = None, context_id: str = "woofmapped.doghouse.general.v0"):
    return adapt_foundry_bounded_natal_dataset(
        artifact or artifact_with_object_families(),
        profile_id="woofmapped_bounded_astrology.v0",
        profile_version="0.1.0",
        context=context(context_id),
    )


def test_profile_manifest_owns_separate_bounded_policy_identity():
    profile = WoofmappedBoundedAstrologyProfile()
    assert profile.manifest.profile_id == "woofmapped_bounded_astrology.v0"
    assert profile.manifest.profile_version == "0.1.0"
    assert profile.manifest.output_contract == "projected_bounded_semantic_graph.v1"
    assert profile.manifest.target_ontology == "woofmapped_astrology.v0"
    assert profile.source_selection_policy["structural_strength"] == "unavailable_no_default"
    assert profile.projected_term_registry()["registry_id"] == "woofmapped_bounded_astrology.projected_terms"
    validate_contract(profile.manifest.to_dict(), "projection_profile_manifest_v1.schema.json")
    assert validate_projected_term_registry(profile.projected_term_registry()) == []


def test_object_projection_covers_deliberate_supported_families_and_reports_unsupported():
    result = project_bounded_natal_objects(request()).to_dict()
    by_source = {
        row["source_refs"][0].split("canonical:object:", 1)[1]: row
        for row in result["objects"]
    }
    assert len(result["objects"]) == 6
    assert by_source["astrowoof:dog:018f:Sun"]["name"] == "pack_role_identity"
    assert by_source["astrowoof:dog:018f:Sun"]["attributes"]["projected_mode"] == "immediate_chase_mode"
    assert by_source["astrowoof:dog:018f:ASC"]["name"] == "behavioral_doorway"
    assert by_source["astrowoof:dog:018f:house:1"]["name"] == "doghouse_1_body_temperament_presence"
    assert by_source["astrowoof:dog:018f:Fortune"]["name"] == "easy_good_thing_channel"
    harmonic = by_source["astrowoof:dog:018f:Sun:H3"]
    assert harmonic["name"] == "pack_role_identity"
    assert harmonic["attributes"]["coordinate_transform"] == "harmonic:3"
    assert harmonic["attributes"]["source_owner_object_ref"] == "astrowoof:dog:018f:Sun"
    assert "reexpress_through_coordinate_transform" in harmonic["operators"]
    outside = result["audit"]["coverage"]["outside_declared_scope_ids"]
    assert outside == ["astrowoof:dog:018f:Eros", "astrowoof:dog:018f:sect"]
    assert result["relationships"] == []
    assert result["audit"]["relationship_mapping_status"] == "deferred_to_slice_5"
    runtime_profile = result["metadata"]["runtime_identity"]["profile"]
    assert runtime_profile["policy_resource_set"]["bundled"] is True
    assert len(runtime_profile["policy_resource_set"]["sha256"]) == 64


def test_projection_preserves_evidence_and_never_creates_strength_or_exact_values():
    result = project_bounded_natal_objects(request()).to_dict()
    for row in result["objects"]:
        assert "structural_strength_score" not in row
        assert row["projection_relevance_score"] is None
        assert row["epistemic_basis"]["classification"] == "invariant"
        assert row["epistemic_basis"]["evidence_family_groups"]
        assert all(ref in result["source_evidence"]["records"] for ref in row["epistemic_basis"]["evidence_refs"])
        assert not ({"longitude", "sign_degree", "pretty"} & row["attributes"].keys())


def test_registry_is_bounded_profile_owned_used_subset_with_resolvable_refs():
    result = project_bounded_natal_objects(request()).to_dict()
    registry = result["projected_term_registry"]
    assert registry["registry_id"] == "woofmapped_bounded_astrology.projected_terms"
    assert registry["materialization"] == "used_terms_subset"
    assert len(registry["terms"]) < 56
    for row in result["objects"]:
        attributes = row["attributes"]
        assert attributes["term_ref"].startswith(f"{registry['registry_id']}:{registry['registry_version']}:")
        if attributes.get("projected_mode"):
            assert attributes["mode_ref"]
        if attributes.get("projected_domain"):
            assert attributes["domain_ref"]


def test_projection_is_deterministic_and_does_not_mutate_request():
    prepared = request()
    before = deepcopy(prepared.to_dict())
    first = project_bounded_natal_objects(prepared).to_dict()
    second = project_bounded_natal_objects(prepared).to_dict()
    assert first == second
    assert prepared.to_dict() == before


def test_context_validation_rejects_unknown_context_and_wrong_house_policy():
    artifact = artifact_with_object_families()
    unknown = adapt_foundry_bounded_natal_dataset(
        artifact,
        profile_id="woofmapped_bounded_astrology.v0",
        profile_version="0.1.0",
        context=context("woofmapped.unknown.v1"),
    )
    with pytest.raises(ValueError, match="does not support context"):
        project_bounded_natal_objects(unknown)
    wrong = context()
    wrong.constraints["house_mapping_policy"] = "kennel"
    invalid_policy = adapt_foundry_bounded_natal_dataset(
        artifact,
        profile_id="woofmapped_bounded_astrology.v0",
        profile_version="0.1.0",
        context=wrong,
    )
    with pytest.raises(ValueError, match="house_mapping_policy=doghouse"):
        project_bounded_natal_objects(invalid_policy)


def test_canonical_row_with_noninvariant_direct_evidence_is_rejected():
    artifact = artifact_with_object_families()
    artifact["uncertainty_assessment"]["evidence_registry"]["uncertainty:bodies:Sun"]["classification"] = "variable"
    with pytest.raises(BoundedProjectionExecutionError, match="is not invariant"):
        project_bounded_natal_objects(request(artifact))
