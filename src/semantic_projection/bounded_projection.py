from __future__ import annotations

from copy import deepcopy
from typing import Any

from .bounded import validate_foundry_bounded_natal_dataset
from .bounded_contract import (
    build_projected_bounded_contract,
    projected_bounded_correspondence_id,
)
from .contracts import (
    BoundedNatalProjectionRequest,
    ProjectedBoundedSemanticGraph,
    ProjectionContext,
)
from .ids import projected_object_id
from .profiles.woofmapped_bounded_astrology import (
    WoofmappedBoundedAstrologyProfile,
)
from .term_registry import term_ref, validate_projected_term_registry
from .validation import validate_bounded_natal_projection_request

JsonDict = dict[str, Any]
EVIDENCE_REF_FIELDS = (
    "uncertainty_evidence_ref",
    "house_uncertainty_evidence_ref",
    "triplicity_uncertainty_evidence_ref",
)


class BoundedProjectionExecutionError(RuntimeError):
    pass


def _source_ref(row: JsonDict) -> str:
    return f"canonical:object:{row['id']}"


def _evidence_refs(row: JsonDict) -> list[str]:
    return sorted(
        {
            str(row[field])
            for field in EVIDENCE_REF_FIELDS
            if isinstance(row.get(field), str) and row.get(field)
        }
    )


def _epistemic_basis(row: JsonDict, registry: JsonDict) -> JsonDict:
    refs = _evidence_refs(row)
    if not refs:
        raise BoundedProjectionExecutionError(
            f"Bounded source object {row.get('id')!r} has no evidence refs"
        )
    scopes: set[str] = set()
    for ref in refs:
        record = registry[ref]
        classification = record.get("classification")
        if classification != "invariant":
            raise BoundedProjectionExecutionError(
                f"Canonical bounded object {row.get('id')!r} evidence {ref!r} "
                f"is not invariant: {classification!r}"
            )
        scopes.add(str(record.get("proof_scope") or "not_declared_by_source_record"))
    family = row["evidence_metadata"]["evidence_family_group"]
    return {
        "classification": "invariant",
        "evidence_refs": refs,
        "evidence_family_groups": [family],
        "proof_scope": "+".join(sorted(scopes)),
    }


def _registry_subset(objects: list[JsonDict], registry: JsonDict) -> JsonDict:
    errors = validate_projected_term_registry(registry)
    if errors:
        raise BoundedProjectionExecutionError(
            "Invalid bounded projected term registry: " + "; ".join(errors)
        )
    terms = registry["terms"]
    used: set[str] = set()
    for row in objects:
        attributes = row["attributes"]
        for value in (
            row["name"],
            attributes.get("projected_mode"),
            attributes.get("projected_domain"),
        ):
            if isinstance(value, str) and value in terms:
                used.add(value)
        if row["name"] in terms:
            attributes["term_ref"] = term_ref(registry, row["name"])
        if attributes.get("projected_mode") in terms:
            attributes["mode_ref"] = term_ref(
                registry, attributes["projected_mode"]
            )
        if attributes.get("projected_domain") in terms:
            attributes["domain_ref"] = term_ref(
                registry, attributes["projected_domain"]
            )
    return {
        "registry_id": registry["registry_id"],
        "registry_version": registry["registry_version"],
        "target_ontology": registry["target_ontology"],
        "materialization": "used_terms_subset",
        "terms": {key: deepcopy(terms[key]) for key in sorted(used)},
    }


def project_bounded_natal_objects(
    request: BoundedNatalProjectionRequest | JsonDict,
    *,
    profile: WoofmappedBoundedAstrologyProfile | None = None,
) -> ProjectedBoundedSemanticGraph:
    """Project bounded objects only; relationships remain a later slice."""

    request_value = (
        request.to_dict()
        if isinstance(request, BoundedNatalProjectionRequest)
        else deepcopy(request)
    )
    validate_bounded_natal_projection_request(request_value)
    artifact = request_value["source_artifact"]
    validate_foundry_bounded_natal_dataset(artifact)
    selected_profile = profile or WoofmappedBoundedAstrologyProfile()
    manifest = selected_profile.manifest
    if (request_value["profile_id"], request_value["profile_version"]) != (
        manifest.profile_id,
        manifest.profile_version,
    ):
        raise BoundedProjectionExecutionError(
            "Resolved bounded profile manifest does not match request"
        )
    context = ProjectionContext.from_dict(request_value["context"])
    selected_profile.validate_context(context)
    if context.target_domain != manifest.target_ontology:
        raise BoundedProjectionExecutionError(
            "Bounded context target_domain does not match profile target ontology"
        )

    graph = artifact["canonical_astrology_graph"]
    registry = artifact["uncertainty_assessment"]["evidence_registry"]
    source_objects = sorted(graph["objects"], key=lambda row: row["id"])
    source_index = {row["id"]: row for row in source_objects}
    projected: list[JsonDict] = []
    mapped_source_ids: list[str] = []
    outside_scope_ids: list[str] = []
    for source_object in source_objects:
        status = selected_profile.classify_source_object(source_object, source_index)
        if status != "eligible":
            outside_scope_ids.append(source_object["id"])
            continue
        draft = selected_profile.project_object(
            deepcopy(source_object),
            source_object_index=deepcopy(source_index),
            context=deepcopy(request_value["context"]),
        )
        if draft is None:
            raise BoundedProjectionExecutionError(
                f"Eligible bounded object {source_object['id']!r} produced no mapping"
            )
        source_ref = _source_ref(source_object)
        semantic_key = str(draft["semantic_key"])
        projected.append({
            "id": projected_object_id(
                profile_id=manifest.profile_id,
                target_key=semantic_key,
                source_refs=[source_ref],
                context_id=context.context_id,
            ),
            "correspondence_id": projected_bounded_correspondence_id(
                kind="object",
                profile_id=manifest.profile_id,
                semantic_key=semantic_key,
                source_refs=[source_ref],
            ),
            "object_type": draft["object_type"],
            "name": draft["name"],
            "target_ontology": manifest.target_ontology,
            "operators": sorted(set(draft.get("operators") or [])),
            "attributes": deepcopy(draft.get("attributes") or {}),
            "source_refs": [source_ref],
            "mapping_rule_refs": [draft["mapping_rule_id"]],
            "context_refs": [context.context_id],
            "epistemic_basis": _epistemic_basis(source_object, registry),
            "projection_relevance_score": None,
            "provenance": deepcopy(draft.get("provenance") or {}),
        })
        mapped_source_ids.append(source_object["id"])

    projected.sort(key=lambda row: row["id"])
    term_registry = _registry_subset(
        projected, selected_profile.projected_term_registry()
    )
    audit = {
        "profile_id": manifest.profile_id,
        "profile_version": manifest.profile_version,
        "object_mapping_status": "complete_for_declared_slice_4_scope",
        "relationship_mapping_status": "deferred_to_slice_5",
        "coverage": {
            "source_object_count": len(source_objects),
            "mapped_source_object_count": len(mapped_source_ids),
            "outside_declared_scope_count": len(outside_scope_ids),
            "mapped_source_object_ids": sorted(mapped_source_ids),
            "outside_declared_scope_ids": sorted(outside_scope_ids),
        },
        "source_selection_policy": deepcopy(
            selected_profile.source_selection_policy
        ),
    }
    diagnostics = {
        "errors": [],
        "warnings": [],
        "infos": [
            {
                "code": "bounded.relationship_mapping.deferred",
                "message": "Relationship projection is intentionally deferred to Slice 5.",
            }
        ],
    }
    return build_projected_bounded_contract(
        request_value,
        target_ontology=manifest.target_ontology,
        objects=projected,
        relationships=[],
        projected_term_registry=term_registry,
        audit=audit,
        diagnostics=diagnostics,
    )
