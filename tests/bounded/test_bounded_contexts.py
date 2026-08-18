from __future__ import annotations

from copy import deepcopy

import pytest

from semantic_projection import (
    REQUIRED_WOOFMAPPED_BOUNDED_CONTEXT_IDS,
    BoundedContextSetValidationError,
    ProjectionContext,
    adapt_foundry_bounded_natal_dataset,
    load_bundled_context,
    project_bounded_natal,
    validate_parallel_bounded_contexts,
)
from tests.bounded.test_bounded_relationship_projection import (
    artifact_with_relationship_families,
)
from tests.bounded.test_bounded_source_selection import (
    MEAN_HARMONIC,
    MEAN_NODE,
    TRUE_HARMONIC,
    TRUE_NODE,
    _node_artifact,
)

CONTEXT_VERSIONS = {
    "woofmapped.doghouse.general.v0": "0.1.0",
    "woofmapped.handler_guidance.v1": "1.0.0",
    "woofmapped.dog_direct.v1": "1.0.0",
    "woofmapped.hybrid_horoscope.v1": "1.0.0",
}


def _four_context_artifacts() -> list[dict]:
    source = artifact_with_relationship_families(duplicate_derived_family=True)
    results = []
    for context_id in sorted(REQUIRED_WOOFMAPPED_BOUNDED_CONTEXT_IDS):
        context = ProjectionContext.from_dict(
            load_bundled_context(context_id, CONTEXT_VERSIONS[context_id])
        )
        request = adapt_foundry_bounded_natal_dataset(
            source,
            profile_id="woofmapped_bounded_astrology.v0",
            profile_version="0.1.0",
            context=context,
        )
        results.append(project_bounded_natal(request).to_dict())
    return results


def test_all_four_contexts_are_structurally_parallel_and_epistemically_invariant():
    artifacts = _four_context_artifacts()
    report = validate_parallel_bounded_contexts(artifacts)

    assert report["status"] == "passed"
    assert report["contexts"] == sorted(REQUIRED_WOOFMAPPED_BOUNDED_CONTEXT_IDS)
    assert report["canonical_context_priority"] is None
    assert report["context_priority_policy"] == (
        "no_projection_context_has_epistemic_priority"
    )
    assert len(report["epistemic_sha256"]) == 64
    assert len(report["structural_semantic_sha256"]) == 64
    assert len(set(report["projection_ids"].values())) == 4
    assert report["object_correspondence_count"] == len(artifacts[0]["objects"])
    assert report["relationship_correspondence_count"] == len(
        artifacts[0]["relationships"]
    )


def test_correspondence_sets_match_while_materialized_ids_remain_context_specific():
    artifacts = _four_context_artifacts()
    object_correspondence = [
        {row["correspondence_id"] for row in artifact["objects"]}
        for artifact in artifacts
    ]
    relationship_correspondence = [
        {row["correspondence_id"] for row in artifact["relationships"]}
        for artifact in artifacts
    ]
    object_ids = [{row["id"] for row in artifact["objects"]} for artifact in artifacts]

    assert all(value == object_correspondence[0] for value in object_correspondence)
    assert all(
        value == relationship_correspondence[0]
        for value in relationship_correspondence
    )
    assert len({frozenset(value) for value in object_ids}) == 4


def test_explicit_context_framing_and_relevance_may_vary():
    artifacts = _four_context_artifacts()
    artifacts[1]["objects"][0]["projection_relevance_score"] = 0.123
    artifacts[2]["objects"][0]["attributes"]["context_framing"] = "handler-owned"

    assert validate_parallel_bounded_contexts(artifacts)["status"] == "passed"


@pytest.mark.parametrize(
    "mutation",
    [
        lambda value: value["source_capabilities"].update({"probe": True}),
        lambda value: value["limitations"].append("context-specific certainty"),
        lambda value: value["objects"][0]["epistemic_basis"].update(
            {"evidence_family_groups": ["invented:family"]}
        ),
    ],
)
def test_contexts_cannot_change_epistemic_material(mutation):
    artifacts = _four_context_artifacts()
    mutation(artifacts[1])

    with pytest.raises(
        BoundedContextSetValidationError, match="Epistemic material differs"
    ):
        validate_parallel_bounded_contexts(artifacts)


@pytest.mark.parametrize(
    "mutation",
    [
        lambda value: value["objects"][0].update({"name": "decorative rewrite"}),
        lambda value: value["objects"][0]["operators"].append("invented_operator"),
        lambda value: value["objects"][0]["mapping_rule_refs"].append(
            "invented_mapping"
        ),
        lambda value: value["projected_term_registry"]["terms"].update(
            {"invented_term": {"definition": "context-only ontology drift"}}
        ),
    ],
)
def test_contexts_cannot_change_structural_semantics(mutation):
    artifacts = _four_context_artifacts()
    mutation(artifacts[1])

    with pytest.raises(
        BoundedContextSetValidationError,
        match="Structural semantic correspondence differs",
    ):
        validate_parallel_bounded_contexts(artifacts)


def test_context_set_must_be_exact_and_have_unique_context_ids():
    artifacts = _four_context_artifacts()
    with pytest.raises(BoundedContextSetValidationError, match="Expected 4"):
        validate_parallel_bounded_contexts(artifacts[:-1])

    duplicate = deepcopy(artifacts)
    duplicate[1]["metadata"]["context_id"] = duplicate[0]["metadata"]["context_id"]
    with pytest.raises(BoundedContextSetValidationError, match="Duplicate"):
        validate_parallel_bounded_contexts(duplicate)

    wrong_version = deepcopy(artifacts)
    wrong_version[0]["metadata"]["context_version"] = "9.9.9"
    with pytest.raises(BoundedContextSetValidationError, match="requires version"):
        validate_parallel_bounded_contexts(wrong_version)


def test_context_validation_report_is_order_independent():
    artifacts = _four_context_artifacts()
    assert validate_parallel_bounded_contexts(artifacts) == (
        validate_parallel_bounded_contexts(list(reversed(artifacts)))
    )


def test_source_selection_is_identical_and_deterministic_across_all_four_contexts():
    source = _node_artifact()
    artifacts: list[dict] = []
    for context_id in sorted(REQUIRED_WOOFMAPPED_BOUNDED_CONTEXT_IDS):
        context = ProjectionContext.from_dict(
            load_bundled_context(context_id, CONTEXT_VERSIONS[context_id])
        )
        request = adapt_foundry_bounded_natal_dataset(
            source,
            profile_id="woofmapped_bounded_astrology.v0",
            profile_version="0.1.0",
            context=context,
        )
        first = project_bounded_natal(request).to_dict()
        second = project_bounded_natal(request).to_dict()
        assert first == second
        artifacts.append(first)

    expected_objects = [MEAN_NODE, MEAN_HARMONIC]
    expected_relationships = [
        "rel:mean-node:owner:h3",
        "rel:mean-node:sun:trine",
    ]
    for artifact in artifacts:
        coverage = artifact["audit"]["coverage"]
        assert coverage["excluded_by_source_selection_policy_ids"] == expected_objects
        assert (
            coverage["excluded_by_source_selection_policy_relationship_ids"]
            == expected_relationships
        )
        source_refs = {
            ref
            for row in artifact["objects"]
            for ref in row["source_refs"]
        }
        assert f"canonical:object:{TRUE_NODE}" in source_refs
        assert f"canonical:object:{TRUE_HARMONIC}" in source_refs
        assert f"canonical:object:{MEAN_NODE}" not in source_refs
        assert f"canonical:object:{MEAN_HARMONIC}" not in source_refs

    report = validate_parallel_bounded_contexts(artifacts)
    assert report["status"] == "passed"
    assert report["canonical_context_priority"] is None
