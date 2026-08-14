from __future__ import annotations

from collections.abc import Mapping
from copy import deepcopy
from typing import Any

from .bounded_contract import OUTPUT_CONTRACT
from .ids import stable_hash
from .validation import validate_projected_bounded_semantic_graph

JsonDict = dict[str, Any]
REQUIRED_WOOFMAPPED_BOUNDED_CONTEXT_IDS = frozenset({
    "woofmapped.doghouse.general.v0",
    "woofmapped.handler_guidance.v1",
    "woofmapped.dog_direct.v1",
    "woofmapped.hybrid_horoscope.v1",
})
REQUIRED_WOOFMAPPED_BOUNDED_CONTEXTS = {
    "woofmapped.doghouse.general.v0": "0.1.0",
    "woofmapped.handler_guidance.v1": "1.0.0",
    "woofmapped.dog_direct.v1": "1.0.0",
    "woofmapped.hybrid_horoscope.v1": "1.0.0",
}
CONTEXT_VARIANT_ATTRIBUTE_KEYS = frozenset({
    "audience_framing",
    "context_framing",
    "contextual_relevance",
})


class BoundedContextSetValidationError(ValueError):
    pass


def _context_invariant_attributes(attributes: Mapping[str, Any]) -> JsonDict:
    return {
        key: deepcopy(value)
        for key, value in sorted(attributes.items())
        if key not in CONTEXT_VARIANT_ATTRIBUTE_KEYS
    }


def bounded_epistemic_view(graph: Mapping[str, Any]) -> JsonDict:
    """Return only source-proof material that must be identical across contexts."""

    rows = [*(graph.get("objects") or []), *(graph.get("relationships") or [])]
    return {
        "source_identity": deepcopy(graph["source_identity"]),
        "source_artifact_ref": deepcopy(graph["source_artifact_ref"]),
        "source_capabilities": deepcopy(graph["source_capabilities"]),
        "source_feature_dispositions": deepcopy(
            graph["source_feature_dispositions"]
        ),
        "source_evidence": deepcopy(graph["source_evidence"]),
        "limitations": list(graph.get("limitations") or []),
        "epistemic_identity": deepcopy(
            graph["provenance"]["epistemic_identity"]
        ),
        "rows": {
            row["correspondence_id"]: {
                "source_refs": sorted(
                    row.get("source_refs")
                    or row.get("source_relationship_refs")
                    or []
                ),
                "epistemic_basis": deepcopy(row["epistemic_basis"]),
            }
            for row in sorted(rows, key=lambda value: value["correspondence_id"])
        },
    }


def bounded_structural_correspondence_view(graph: Mapping[str, Any]) -> JsonDict:
    """Normalize context-specific row IDs into cross-context correspondence space."""

    objects = graph.get("objects") or []
    relationships = graph.get("relationships") or []
    correspondence_by_id = {
        row["id"]: row["correspondence_id"] for row in [*objects, *relationships]
    }
    return {
        "target_ontology": graph["target_ontology"],
        "profile": {
            "profile_id": graph["metadata"]["profile_id"],
            "profile_version": graph["metadata"]["profile_version"],
        },
        "objects": {
            row["correspondence_id"]: {
                "object_type": row["object_type"],
                "name": row["name"],
                "operators": sorted(row["operators"]),
                "attributes": _context_invariant_attributes(row["attributes"]),
                "source_refs": sorted(row["source_refs"]),
                "mapping_rule_refs": sorted(row["mapping_rule_refs"]),
            }
            for row in sorted(objects, key=lambda value: value["correspondence_id"])
        },
        "relationships": {
            row["correspondence_id"]: {
                "relationship_type": row["relationship_type"],
                "source_correspondence_id": correspondence_by_id[row["source_id"]],
                "target_correspondence_id": correspondence_by_id[row["target_id"]],
                "operators": sorted(row["operators"]),
                "theme_tags": sorted(row["theme_tags"]),
                "attributes": _context_invariant_attributes(row["attributes"]),
                "source_relationship_refs": sorted(
                    row["source_relationship_refs"]
                ),
                "mapping_rule_refs": sorted(row["mapping_rule_refs"]),
            }
            for row in sorted(
                relationships, key=lambda value: value["correspondence_id"]
            )
        },
        "projected_term_registry": deepcopy(graph["projected_term_registry"]),
    }


def validate_parallel_bounded_contexts(
    artifacts: list[Mapping[str, Any]],
    *,
    required_context_ids: frozenset[str] = REQUIRED_WOOFMAPPED_BOUNDED_CONTEXT_IDS,
    required_context_versions: Mapping[str, str] = (
        REQUIRED_WOOFMAPPED_BOUNDED_CONTEXTS
    ),
) -> JsonDict:
    """Validate one structurally parallel, certainty-invariant context set."""

    if len(artifacts) != len(required_context_ids):
        raise BoundedContextSetValidationError(
            f"Expected {len(required_context_ids)} bounded context artifacts; "
            f"received {len(artifacts)}"
        )
    values = [deepcopy(dict(value)) for value in artifacts]
    for value in values:
        validate_projected_bounded_semantic_graph(value)
        if value["metadata"]["output_contract"] != OUTPUT_CONTRACT:
            raise BoundedContextSetValidationError(
                "Context set contains a non-bounded output contract"
            )
        if value["provenance"].get("context_epistemic_policy") != (
            "certainty_invariant_across_contexts"
        ):
            raise BoundedContextSetValidationError(
                "Context artifact does not declare certainty-invariant policy"
            )

    by_context: dict[str, JsonDict] = {}
    for value in values:
        context_id = str(value["metadata"]["context_id"])
        if context_id in by_context:
            raise BoundedContextSetValidationError(
                f"Duplicate bounded context artifact {context_id!r}"
            )
        by_context[context_id] = value
    observed = frozenset(by_context)
    if observed != required_context_ids:
        raise BoundedContextSetValidationError(
            "Bounded context identifiers do not match required set: "
            f"missing={sorted(required_context_ids - observed)}, "
            f"unexpected={sorted(observed - required_context_ids)}"
        )
    for context_id, value in by_context.items():
        expected_version = required_context_versions.get(context_id)
        observed_version = value["metadata"]["context_version"]
        if expected_version is None or observed_version != expected_version:
            raise BoundedContextSetValidationError(
                f"Bounded context {context_id!r} requires version "
                f"{expected_version!r}; received {observed_version!r}"
            )

    ordered_contexts = sorted(by_context)
    baseline_id = ordered_contexts[0]
    baseline = by_context[baseline_id]
    baseline_epistemic = bounded_epistemic_view(baseline)
    baseline_structural = bounded_structural_correspondence_view(baseline)
    baseline_profile = (
        baseline["metadata"]["profile_id"],
        baseline["metadata"]["profile_version"],
    )
    projection_ids: set[str] = set()
    for context_id in ordered_contexts:
        value = by_context[context_id]
        profile = (
            value["metadata"]["profile_id"],
            value["metadata"]["profile_version"],
        )
        if profile != baseline_profile:
            raise BoundedContextSetValidationError(
                f"Profile identity differs in context {context_id!r}"
            )
        if bounded_epistemic_view(value) != baseline_epistemic:
            raise BoundedContextSetValidationError(
                f"Epistemic material differs in context {context_id!r}"
            )
        if bounded_structural_correspondence_view(value) != baseline_structural:
            raise BoundedContextSetValidationError(
                f"Structural semantic correspondence differs in context {context_id!r}"
            )
        projection_id = value["metadata"]["projection_id"]
        if projection_id in projection_ids:
            raise BoundedContextSetValidationError(
                f"Projection identity is not context-specific for {context_id!r}"
            )
        projection_ids.add(projection_id)

    epistemic_sha256 = stable_hash(baseline_epistemic, length=64)
    structural_sha256 = stable_hash(baseline_structural, length=64)
    return {
        "validation_contract": "bounded_parallel_context_validation.v1",
        "status": "passed",
        "profile_id": baseline_profile[0],
        "profile_version": baseline_profile[1],
        "source_artifact_sha256": baseline["source_identity"][
            "source_artifact_sha256"
        ],
        "contexts": ordered_contexts,
        "context_versions": {
            context_id: by_context[context_id]["metadata"]["context_version"]
            for context_id in ordered_contexts
        },
        "canonical_context_priority": None,
        "context_priority_policy": "no_projection_context_has_epistemic_priority",
        "object_correspondence_count": len(baseline_structural["objects"]),
        "relationship_correspondence_count": len(
            baseline_structural["relationships"]
        ),
        "epistemic_sha256": epistemic_sha256,
        "structural_semantic_sha256": structural_sha256,
        "allowed_context_variants": {
            "row_projection_relevance_score": True,
            "attribute_keys": sorted(CONTEXT_VARIANT_ATTRIBUTE_KEYS),
            "epistemic_material": False,
            "semantic_primitive_or_mapping": False,
            "projected_term_definition": False,
        },
        "projection_ids": {
            context_id: by_context[context_id]["metadata"]["projection_id"]
            for context_id in ordered_contexts
        },
    }
