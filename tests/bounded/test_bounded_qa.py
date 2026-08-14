from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timedelta
from time import perf_counter

import pytest

from semantic_projection import (
    BoundedNatalSourceContractError,
    BoundedProjectionExecutionError,
    ProjectionContext,
    adapt_foundry_bounded_natal_dataset,
    project_bounded_natal,
)
from semantic_projection.profiles.woofmapped_bounded_astrology import (
    WoofmappedBoundedAstrologyProfile,
)
from tests.bounded.test_bounded_relationship_projection import (
    _add_relationship,
    artifact_with_relationship_families,
)


def _request(artifact: dict):
    return adapt_foundry_bounded_natal_dataset(
        artifact,
        profile_id="woofmapped_bounded_astrology.v0",
        profile_version="0.1.0",
        context=ProjectionContext(
            context_id="woofmapped.doghouse.general.v0",
            context_version="0.1.0",
            subject_scope="dog",
            target_domain="woofmapped_astrology.v0",
            application_context="woofmapped_natal_projection",
            constraints={"house_mapping_policy": "doghouse"},
        ),
    )


def _project(artifact: dict) -> dict:
    return project_bounded_natal(_request(artifact)).to_dict()


@pytest.mark.parametrize(
    ("hours", "evaluation_count"),
    [(1, 61), (24, 1441), (48, 2881)],
)
def test_supported_interval_widths_project_without_representative_state(
    hours, evaluation_count
):
    artifact = artifact_with_relationship_families()
    start = datetime.fromisoformat(artifact["birth_time_basis"]["earliest_local"])
    artifact["birth_time_basis"]["latest_local"] = (
        start + timedelta(hours=hours)
    ).isoformat()
    artifact["uncertainty_assessment"]["evaluation_count"] = evaluation_count

    result = _project(artifact)

    assert result["objects"]
    assert result["relationships"]
    assert result["limitations"][0] == "bounded_invariant_subgraph_not_exact_chart"
    assert all("longitude" not in row["attributes"] for row in result["objects"])
    assert all("orb" not in row["attributes"] for row in result["relationships"])


def test_complex_prerequisite_evidence_is_preserved_without_becoming_a_claim():
    artifact = artifact_with_relationship_families()
    registry = artifact["uncertainty_assessment"]["evidence_registry"]
    complex_ref = "uncertainty:qa:circular-transition"
    complex_record = {
        "evidence_contract_version": "agf.bounded_uncertainty_evidence.v1.0.0",
        "feature_key": "qa:circular-transition",
        "classification": "variable",
        "value_kind": "longitude_range",
        "possibilities": {
            "possibility_type": "categorical_set",
            "values": ["Pisces", "Aries"],
            "count": 2,
        },
        "prerequisite_refs": [],
        "range_evidence": {
            "range_type": "circular_disjoint",
            "segments": [
                {"minimum": 0.0, "maximum": 1.0},
                {"minimum": 359.0, "maximum": 360.0},
            ],
            "wraps_origin": True,
        },
        "transition_witnesses": [
            {"before": "Pisces", "after": "Aries", "sample_index": 17}
        ],
        "counterexamples": [{"value": "Pisces", "sample_index": 0}],
        "proof_scope": "complete_normalized_birth_interval",
    }
    registry[complex_ref] = complex_record
    registry["uncertainty:bodies:Sun"]["prerequisite_refs"].append(complex_ref)

    result = _project(artifact)

    assert result["source_evidence"]["records"][complex_ref] == complex_record
    assert all(
        complex_ref not in row["epistemic_basis"]["evidence_refs"]
        for row in [*result["objects"], *result["relationships"]]
    )


def test_unavailable_and_inconclusive_features_remain_source_state_not_rows():
    artifact = artifact_with_relationship_families()
    assessment = artifact["uncertainty_assessment"]
    assessment["feature_dispositions"].update(
        {
            "terrestrial_frame": "inconclusive",
            "optional_external_objects": "unavailable",
        }
    )
    for classification in ("unavailable", "inconclusive"):
        ref = f"uncertainty:qa:{classification}"
        assessment["evidence_registry"][ref] = {
            "evidence_contract_version": "agf.bounded_uncertainty_evidence.v1.0.0",
            "feature_key": ref,
            "classification": classification,
            "value_kind": "qa_feature",
            "possibilities": None,
            "prerequisite_refs": [],
            "range_evidence": None,
            "transition_witnesses": [],
            "counterexamples": [],
            "proof_scope": "complete_normalized_birth_interval",
        }

    result = _project(artifact)

    assert result["source_feature_dispositions"]["terrestrial_frame"] == (
        "inconclusive"
    )
    assert result["source_feature_dispositions"]["optional_external_objects"] == (
        "unavailable"
    )
    assert not {
        "uncertainty:qa:unavailable",
        "uncertainty:qa:inconclusive",
    } & result["source_evidence"]["records"].keys()


def test_non_invariant_promoted_row_is_rejected_at_execution():
    artifact = artifact_with_relationship_families()
    registry = artifact["uncertainty_assessment"]["evidence_registry"]
    registry["uncertainty:bodies:Sun"]["classification"] = "variable"

    with pytest.raises(BoundedProjectionExecutionError, match="is not invariant"):
        _project(artifact)


@pytest.mark.parametrize("kind", ["object", "relationship"])
def test_duplicate_source_ids_are_rejected(kind):
    artifact = artifact_with_relationship_families()
    rows = artifact["canonical_astrology_graph"][f"{kind}s"]
    rows.append(deepcopy(rows[0]))
    artifact["canonical_astrology_graph"]["summary"][f"{kind}_count"] += 1

    with pytest.raises(BoundedNatalSourceContractError, match="Duplicate"):
        _request(artifact)


def test_wrong_profile_and_context_fail_closed():
    artifact = artifact_with_relationship_families()
    wrong_profile = _request(artifact).to_dict()
    wrong_profile["profile_version"] = "9.9.9"
    with pytest.raises(
        BoundedProjectionExecutionError, match="manifest does not match request"
    ):
        project_bounded_natal(wrong_profile)

    wrong_context = _request(artifact).to_dict()
    wrong_context["context"]["context_id"] = "woofmapped.unknown.v1"
    with pytest.raises(ValueError, match="does not support context"):
        project_bounded_natal(wrong_context)


def test_missing_projected_term_resource_fails_instead_of_emitting_bare_label():
    profile = WoofmappedBoundedAstrologyProfile()
    registry = profile.projected_term_registry()
    del registry["terms"]["pack_role_identity"]
    profile.projected_term_registry = lambda: registry  # type: ignore[method-assign]

    with pytest.raises(
        BoundedProjectionExecutionError, match="requires missing projected term"
    ):
        project_bounded_natal(
            _request(artifact_with_relationship_families()), profile=profile
        )


def test_large_derived_family_is_linear_deterministic_and_noninflating():
    artifact = artifact_with_relationship_families()
    sibling_count = 300
    for index in range(1, sibling_count):
        _add_relationship(
            artifact,
            row_id=f"rel:derived:sun:h3:square:qa:{index:03d}",
            relationship_type="BOUNDED_INVARIANT_DERIVED_ASPECT",
            source_id="astrowoof:dog:018f:Sun",
            target_id="astrowoof:dog:018f:Sun:H3",
            aspect="square",
            evidence_ref=f"uncertainty:rel:derived:sun:h3:square:qa:{index:03d}",
            family="Sun:derived-square",
        )
    graph = artifact["canonical_astrology_graph"]
    graph["relationships"] = sorted(graph["relationships"], key=lambda row: row["id"])
    graph["summary"]["relationship_count"] = len(graph["relationships"])

    started = perf_counter()
    first = _project(artifact)
    elapsed_seconds = perf_counter() - started
    second = _project(artifact)
    family = "astrowoof:dog:018f:object-family:Sun:derived-square"
    rows = [
        row
        for row in first["relationships"]
        if row["attributes"]["source_evidence_family_group"] == family
    ]

    assert first == second
    assert len(rows) == sibling_count
    assert round(sum(row["projection_relevance_score"] for row in rows), 6) == 0.98
    assert round(
        sum(
            row["attributes"]["relevance_accounting"]["member_allocation"]
            for row in rows
        ),
        6,
    ) == 1.0
    assert elapsed_seconds < 10.0


def test_semantic_output_is_stable_under_source_row_reordering():
    source = artifact_with_relationship_families(duplicate_derived_family=True)
    reordered = deepcopy(source)
    reordered["canonical_astrology_graph"]["objects"].reverse()
    reordered["canonical_astrology_graph"]["relationships"].reverse()
    reordered["uncertainty_assessment"]["evidence_registry"] = dict(
        reversed(
            list(
                reordered["uncertainty_assessment"]["evidence_registry"].items()
            )
        )
    )

    first = _project(source)
    second = _project(reordered)

    for key in ("objects", "relationships", "projected_term_registry", "audit"):
        assert first[key] == second[key]
