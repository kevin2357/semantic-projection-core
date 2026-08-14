from __future__ import annotations

from copy import deepcopy

import pytest

from semantic_projection import (
    adapt_foundry_bounded_natal_dataset,
    project_bounded_natal,
)
from semantic_projection.profiles.woofmapped_bounded_astrology import (
    WoofmappedBoundedAstrologyProfile,
)
from tests.bounded.test_bounded_object_projection import (
    _metadata,
    artifact_with_object_families,
    context,
)


def _relationship_metadata(*, token: str, family: str) -> dict:
    return _metadata(
        tier="derived" if "derived" in token or "owner" in token else "core",
        derivation="direct_relation_between_derived_objects" if "derived" in token else "direct",
        family="bounded_relationship",
        token=token,
        owner=family,
    )


def _add_relationship(
    artifact: dict,
    *,
    row_id: str,
    relationship_type: str,
    source_id: str,
    target_id: str,
    evidence_ref: str,
    family: str,
    aspect: str | None = None,
) -> None:
    evidence = {
        "evidence_contract_version": "agf.bounded_uncertainty_evidence.v1.0.0",
        "feature_key": evidence_ref,
        "classification": "invariant",
        "value_kind": "bounded_relationship",
        "possibilities": {
            "possibility_type": "categorical_set",
            "values": [aspect or relationship_type],
            "count": 1,
        },
        "prerequisite_refs": [],
        "range_evidence": None,
        "transition_witnesses": [],
        "counterexamples": [],
        "proof_scope": "complete_normalized_birth_interval",
    }
    artifact["uncertainty_assessment"]["evidence_registry"][evidence_ref] = evidence
    row = {
        "id": row_id,
        "relationship_type": relationship_type,
        "source_id": source_id,
        "target_id": target_id,
        "uncertainty_evidence_ref": evidence_ref,
        "evidence_metadata": _relationship_metadata(token=row_id, family=family),
    }
    if aspect:
        row["aspect"] = aspect
    artifact["canonical_astrology_graph"]["relationships"].append(row)


def artifact_with_relationship_families(*, duplicate_derived_family: bool = False) -> dict:
    artifact = artifact_with_object_families()
    graph = artifact["canonical_astrology_graph"]
    sun = "astrowoof:dog:018f:Sun"
    mars = "astrowoof:dog:018f:Mars"
    asc = "astrowoof:dog:018f:ASC"
    fortune = "astrowoof:dog:018f:Fortune"
    harmonic = "astrowoof:dog:018f:Sun:H3"
    _add_relationship(
        artifact, row_id="rel:owner:sun:h3",
        relationship_type="BOUNDED_HAS_HARMONIC_POINT",
        source_id=sun, target_id=harmonic,
        evidence_ref="uncertainty:rel:owner:sun:h3", family="Sun",
    )
    _add_relationship(
        artifact, row_id="rel:derived:sun:h3:square:1",
        relationship_type="BOUNDED_INVARIANT_DERIVED_ASPECT",
        source_id=sun, target_id=harmonic, aspect="square",
        evidence_ref="uncertainty:rel:derived:sun:h3:square:1",
        family="Sun:derived-square",
    )
    if duplicate_derived_family:
        _add_relationship(
            artifact, row_id="rel:derived:sun:h3:square:2",
            relationship_type="BOUNDED_INVARIANT_DERIVED_ASPECT",
            source_id=sun, target_id=harmonic, aspect="square",
            evidence_ref="uncertainty:rel:derived:sun:h3:square:2",
            family="Sun:derived-square",
        )
    _add_relationship(
        artifact, row_id="rel:declination:sun:mars:parallel",
        relationship_type="BOUNDED_INVARIANT_DECLINATION_PARALLEL",
        source_id=sun, target_id=mars,
        evidence_ref="uncertainty:rel:declination:sun:mars:parallel",
        family="Sun:Mars:parallel",
    )
    _add_relationship(
        artifact, row_id="rel:angle:sun:asc:trine",
        relationship_type="BOUNDED_INVARIANT_ANGLE_ASPECT",
        source_id=sun, target_id=asc, aspect="trine",
        evidence_ref="uncertainty:rel:angle:sun:asc:trine",
        family="Sun:ASC:trine",
    )
    _add_relationship(
        artifact, row_id="rel:calculated:mars:fortune:sextile",
        relationship_type="BOUNDED_INVARIANT_CALCULATED_POINT_ASPECT",
        source_id=mars, target_id=fortune, aspect="sextile",
        evidence_ref="uncertainty:rel:calculated:mars:fortune:sextile",
        family="Mars:Fortune:sextile",
    )
    _add_relationship(
        artifact, row_id="rel:unsupported:sun:mars:nonsense",
        relationship_type="BOUNDED_INVARIANT_ASPECT",
        source_id=sun, target_id=mars, aspect="septnovile",
        evidence_ref="uncertainty:rel:unsupported:sun:mars:nonsense",
        family="Sun:Mars:unsupported",
    )
    graph["relationships"] = sorted(graph["relationships"], key=lambda row: row["id"])
    graph["summary"]["relationship_count"] = len(graph["relationships"])
    return artifact


def request(artifact: dict):
    return adapt_foundry_bounded_natal_dataset(
        artifact,
        profile_id="woofmapped_bounded_astrology.v0",
        profile_version="0.1.0",
        context=context(),
    )


def test_supported_relationship_families_project_with_distinct_semantics():
    result = project_bounded_natal(request(artifact_with_relationship_families())).to_dict()
    by_source = {
        row["source_relationship_refs"][0].split("canonical:relationship:", 1)[1]: row
        for row in result["relationships"]
    }
    assert len(result["relationships"]) == 6
    assert by_source["rel:bounded:trine"]["relationship_type"] == "natural_behavioral_channel"
    assert by_source["rel:owner:sun:h3"]["relationship_type"] == "coordinate_transform_of"
    assert by_source["rel:owner:sun:h3"]["attributes"]["topology_only"] is True
    assert by_source["rel:owner:sun:h3"]["projection_relevance_score"] is None
    assert by_source["rel:declination:sun:mars:parallel"]["relationship_type"] == "subsystems_track_together"
    assert by_source["rel:declination:sun:mars:parallel"]["attributes"]["source_aspect"] is None
    assert by_source["rel:angle:sun:asc:trine"]["relationship_type"] == "natural_behavioral_channel"
    assert by_source["rel:calculated:mars:fortune:sextile"]["relationship_type"] == "trainable_usable_channel"
    assert result["audit"]["coverage"]["outside_declared_scope_relationship_ids"] == [
        "rel:unsupported:sun:mars:nonsense"
    ]


@pytest.mark.parametrize(
    "source_type",
    [
        "BOUNDED_HAS_ANTISCIA_POINT",
        "BOUNDED_HAS_CONTRA_ANTISCIA_POINT",
        "BOUNDED_HAS_HARMONIC_POINT",
    ],
)
def test_all_transform_ownership_types_share_unscored_lineage_semantics(source_type):
    draft = WoofmappedBoundedAstrologyProfile().project_relationship(
        {"relationship_type": source_type}
    )
    assert draft["relationship_type"] == "coordinate_transform_of"
    assert draft["topology_only"] is True
    assert draft["base_relevance"] is None


@pytest.mark.parametrize(
    ("source_type", "target_type"),
    [
        ("BOUNDED_INVARIANT_DECLINATION_PARALLEL", "subsystems_track_together"),
        ("BOUNDED_INVARIANT_DECLINATION_CONTRAPARALLEL", "subsystems_counterbalance"),
    ],
)
def test_declination_relationships_remain_distinct_from_longitude_aspects(source_type, target_type):
    draft = WoofmappedBoundedAstrologyProfile().project_relationship(
        {"relationship_type": source_type}
    )
    assert draft["relationship_type"] == target_type
    assert "declination" in draft["provenance"]["operator_preservation_policy"]


def test_relationships_preserve_evidence_family_and_never_emit_exact_geometry_or_strength():
    result = project_bounded_natal(request(artifact_with_relationship_families())).to_dict()
    for row in result["relationships"]:
        assert row["epistemic_basis"]["classification"] == "invariant"
        assert row["epistemic_basis"]["evidence_family_groups"] == [
            row["attributes"]["source_evidence_family_group"]
        ]
        assert "structural_strength_score" not in row
        assert not ({"orb", "distance", "applying_delta", "strength"} & row["attributes"].keys())
        for ref in row["epistemic_basis"]["evidence_refs"]:
            assert ref in result["source_evidence"]["records"]


def test_duplicate_siblings_divide_family_relevance_instead_of_inflating_total():
    single = project_bounded_natal(
        request(artifact_with_relationship_families())
    ).to_dict()
    duplicated = project_bounded_natal(
        request(artifact_with_relationship_families(duplicate_derived_family=True))
    ).to_dict()
    family = "astrowoof:dog:018f:object-family:Sun:derived-square"

    def rows_for(value: dict) -> list[dict]:
        return [
            row for row in value["relationships"]
            if row["attributes"]["source_evidence_family_group"] == family
        ]

    single_rows = rows_for(single)
    duplicate_rows = rows_for(duplicated)
    assert len(single_rows) == 1
    assert len(duplicate_rows) == 2
    assert single_rows[0]["projection_relevance_score"] == 0.98
    assert {row["projection_relevance_score"] for row in duplicate_rows} == {0.49}
    assert sum(row["projection_relevance_score"] for row in duplicate_rows) == 0.98
    assert all(
        row["attributes"]["relevance_accounting"]["scored_family_member_count"] == 2
        for row in duplicate_rows
    )


def test_family_coverage_is_separate_from_raw_record_coverage():
    result = project_bounded_natal(
        request(artifact_with_relationship_families(duplicate_derived_family=True))
    ).to_dict()
    coverage = result["audit"]["coverage"]
    families = coverage["family_coverage"]
    assert coverage["mapped_source_relationship_count"] > families["mapped_relationship_family_count"]
    assert families["raw_record_counts_are_weights"] is False
    assert families["relationship_relevance_aggregation_unit"] == "evidence_family_group"


def test_relationship_terms_are_embedded_and_fully_qualified():
    result = project_bounded_natal(request(artifact_with_relationship_families())).to_dict()
    registry = result["projected_term_registry"]
    assert "coordinate_transform_of" in registry["terms"]
    assert "subsystems_track_together" in registry["terms"]
    for row in result["relationships"]:
        attributes = row["attributes"]
        assert attributes["relation_ref"].startswith(registry["registry_id"])
        assert attributes["interaction_mode_ref"].startswith(registry["registry_id"])


def test_full_relationship_projection_is_deterministic_and_input_immutable():
    prepared = request(artifact_with_relationship_families())
    before = deepcopy(prepared.to_dict())
    assert project_bounded_natal(prepared).to_dict() == project_bounded_natal(prepared).to_dict()
    assert prepared.to_dict() == before
