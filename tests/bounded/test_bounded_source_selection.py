from __future__ import annotations

from copy import deepcopy

from semantic_projection import (
    adapt_foundry_bounded_natal_dataset,
    project_bounded_natal,
)
from semantic_projection.profiles.woofmapped_bounded_astrology import (
    WoofmappedBoundedAstrologyProfile,
)
from tests.bounded.test_bounded_object_projection import (
    _add_object,
    _metadata,
    artifact_with_object_families,
    context,
)
from tests.bounded.test_bounded_relationship_projection import _add_relationship


TRUE_NODE = "astrowoof:dog:018f:True_Node"
MEAN_NODE = "astrowoof:dog:018f:Mean_Node"
TRUE_HARMONIC = f"{TRUE_NODE}:H3"
MEAN_HARMONIC = f"{MEAN_NODE}:H3"


def _node_artifact(*, include_true: bool = True) -> dict:
    artifact = artifact_with_object_families()
    additions: list[tuple[dict, str]] = []
    if include_true:
        additions.extend(
            [
                (
                    {
                        "id": TRUE_NODE,
                        "object_type": "bounded_natal_body",
                        "name": "True Node",
                        "sign_index": 4,
                        "evidence_metadata": _metadata(
                            tier="core",
                            derivation="direct",
                            family="natal_body",
                            token="True_Node",
                        ),
                    },
                    "uncertainty:body:True_Node",
                ),
                (
                    {
                        "id": TRUE_HARMONIC,
                        "object_type": "bounded_harmonic_point",
                        "name": "True Node harmonic 3",
                        "sign_index": 0,
                        "owner_object_ref": TRUE_NODE,
                        "transform_kind": "harmonic",
                        "harmonic_number": 3,
                        "evidence_metadata": _metadata(
                            tier="harmonic",
                            derivation="derived",
                            family="harmonic",
                            token="True_Node:H3",
                            owner=TRUE_NODE,
                        ),
                    },
                    "uncertainty:transform:True_Node:H3",
                ),
            ]
        )
    additions.extend(
        [
            (
                {
                    "id": MEAN_NODE,
                    "object_type": "bounded_natal_body",
                    "name": "Mean_Node",
                    "sign_index": 4,
                    "evidence_metadata": _metadata(
                        tier="core",
                        derivation="direct",
                        family="natal_body",
                        token="Mean_Node",
                    ),
                },
                "uncertainty:body:Mean_Node",
            ),
            (
                {
                    "id": MEAN_HARMONIC,
                    "object_type": "bounded_harmonic_point",
                    "name": "Mean Node harmonic 3",
                    "sign_index": 0,
                    "owner_object_ref": MEAN_NODE,
                    "transform_kind": "harmonic",
                    "harmonic_number": 3,
                    "evidence_metadata": _metadata(
                        tier="harmonic",
                        derivation="derived",
                        family="harmonic",
                        token="Mean_Node:H3",
                        owner=MEAN_NODE,
                    ),
                },
                "uncertainty:transform:Mean_Node:H3",
            ),
        ]
    )
    for row, evidence_ref in additions:
        _add_object(artifact, row, evidence_ref=evidence_ref)

    sun = "astrowoof:dog:018f:Sun"
    _add_relationship(
        artifact,
        row_id="rel:true-node:sun:trine",
        relationship_type="BOUNDED_INVARIANT_ASPECT",
        source_id=TRUE_NODE if include_true else sun,
        target_id=sun,
        aspect="trine",
        evidence_ref="uncertainty:rel:true-node:sun:trine",
        family="True_Node:Sun:trine",
    )
    _add_relationship(
        artifact,
        row_id="rel:mean-node:sun:trine",
        relationship_type="BOUNDED_INVARIANT_ASPECT",
        source_id=MEAN_NODE,
        target_id=sun,
        aspect="trine",
        evidence_ref="uncertainty:rel:mean-node:sun:trine",
        family="Mean_Node:Sun:trine",
    )
    _add_relationship(
        artifact,
        row_id="rel:mean-node:owner:h3",
        relationship_type="BOUNDED_HAS_HARMONIC_POINT",
        source_id=MEAN_NODE,
        target_id=MEAN_HARMONIC,
        evidence_ref="uncertainty:rel:mean-node:owner:h3",
        family="Mean_Node",
    )
    graph = artifact["canonical_astrology_graph"]
    graph["objects"] = sorted(graph["objects"], key=lambda row: row["id"])
    graph["relationships"] = sorted(graph["relationships"], key=lambda row: row["id"])
    graph["summary"]["object_count"] = len(graph["objects"])
    graph["summary"]["relationship_count"] = len(graph["relationships"])
    return artifact


def _request(artifact: dict):
    return adapt_foundry_bounded_natal_dataset(
        artifact,
        profile_id="woofmapped_bounded_astrology.v0",
        profile_version="0.1.0",
        context=context(),
    )


def _source_object_ids(result: dict) -> set[str]:
    return {
        ref.split("canonical:object:", 1)[1]
        for row in result["objects"]
        for ref in row["source_refs"]
        if "canonical:object:" in ref
    }


def _source_relationship_ids(result: dict) -> set[str]:
    return {
        ref.split("canonical:relationship:", 1)[1]
        for row in result["relationships"]
        for ref in row["source_relationship_refs"]
    }


def test_profile_classification_excludes_mean_node_family_but_preserves_true_and_fortune():
    artifact = _node_artifact()
    objects = artifact["canonical_astrology_graph"]["objects"]
    index = {row["id"]: row for row in objects}
    profile = WoofmappedBoundedAstrologyProfile()

    assert profile.classify_source_object(index[TRUE_NODE], index) == "eligible"
    assert profile.classify_source_object(index[MEAN_NODE], index) == "excluded_by_source_selection_policy"
    assert profile.classify_source_object(index[TRUE_HARMONIC], index) == "eligible"
    assert profile.classify_source_object(index[MEAN_HARMONIC], index) == "excluded_by_source_selection_policy"
    assert profile.classify_source_object(index["astrowoof:dog:018f:Fortune"], index) == "eligible"


def test_bounded_projection_closes_mean_node_objects_and_relationships_with_explicit_audit():
    result = project_bounded_natal(_request(_node_artifact())).to_dict()
    source_objects = _source_object_ids(result)
    source_relationships = _source_relationship_ids(result)

    assert TRUE_NODE in source_objects
    assert TRUE_HARMONIC in source_objects
    assert "astrowoof:dog:018f:Fortune" in source_objects
    assert MEAN_NODE not in source_objects
    assert MEAN_HARMONIC not in source_objects
    assert "rel:true-node:sun:trine" in source_relationships
    assert "rel:mean-node:sun:trine" not in source_relationships
    assert "rel:mean-node:owner:h3" not in source_relationships

    coverage = result["audit"]["coverage"]
    assert coverage["excluded_by_source_selection_policy_ids"] == [MEAN_NODE, MEAN_HARMONIC]
    assert coverage["excluded_by_source_selection_policy_count"] == 2
    assert coverage["excluded_by_source_selection_policy_relationship_ids"] == [
        "rel:mean-node:owner:h3",
        "rel:mean-node:sun:trine",
    ]
    assert coverage["excluded_by_source_selection_policy_relationship_count"] == 2
    assert MEAN_NODE not in coverage["outside_declared_scope_ids"]
    assert "rel:mean-node:sun:trine" not in coverage[
        "outside_declared_scope_relationship_ids"
    ]
    exclusion_info = next(
        row
        for row in result["diagnostics"]["infos"]
        if row["code"] == "bounded.source_selection.exclusions"
    )
    assert exclusion_info["details"]["object_ids"] == [MEAN_NODE, MEAN_HARMONIC]


def test_mean_node_is_not_promoted_when_true_node_is_absent_and_registry_does_not_expand():
    with_mean = project_bounded_natal(_request(_node_artifact(include_true=False))).to_dict()
    without_mean_artifact = _node_artifact(include_true=False)
    graph = without_mean_artifact["canonical_astrology_graph"]
    graph["objects"] = [row for row in graph["objects"] if row["id"] not in {MEAN_NODE, MEAN_HARMONIC}]
    graph["relationships"] = [
        row
        for row in graph["relationships"]
        if MEAN_NODE not in {row["source_id"], row["target_id"]}
    ]
    graph["summary"]["object_count"] = len(graph["objects"])
    graph["summary"]["relationship_count"] = len(graph["relationships"])
    without_mean = project_bounded_natal(_request(deepcopy(without_mean_artifact))).to_dict()

    assert MEAN_NODE not in _source_object_ids(with_mean)
    assert MEAN_HARMONIC not in _source_object_ids(with_mean)
    assert with_mean["projected_term_registry"] == without_mean["projected_term_registry"]
