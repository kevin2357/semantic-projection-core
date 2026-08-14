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
from .ids import projected_object_id, projected_relationship_id
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


def _equal_micro_allocation(
    total: float, member_count: int, member_index: int
) -> float:
    """Allocate a six-decimal total without cumulative rounding inflation."""

    if member_count < 1 or not 0 <= member_index < member_count:
        raise BoundedProjectionExecutionError(
            "Cannot allocate relevance for an unindexed family member"
        )
    total_units = round(float(total) * 1_000_000)
    quotient, remainder = divmod(total_units, member_count)
    member_units = quotient + (1 if member_index < remainder else 0)
    return member_units / 1_000_000


def _source_ref(row: JsonDict, *, kind: str) -> str:
    return f"canonical:{kind}:{row['id']}"


def _evidence_refs(row: JsonDict) -> list[str]:
    return sorted(
        {
            str(row[field])
            for field in EVIDENCE_REF_FIELDS
            if isinstance(row.get(field), str) and row.get(field)
        }
    )


def _epistemic_basis(row: JsonDict, registry: JsonDict, *, kind: str) -> JsonDict:
    refs = _evidence_refs(row)
    if not refs:
        raise BoundedProjectionExecutionError(
            f"Bounded source {kind} {row.get('id')!r} has no evidence refs"
        )
    scopes: set[str] = set()
    for ref in refs:
        record = registry[ref]
        classification = record.get("classification")
        if classification != "invariant":
            raise BoundedProjectionExecutionError(
                f"Canonical bounded {kind} {row.get('id')!r} evidence {ref!r} "
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


def _registry_subset(
    objects: list[JsonDict], relationships: list[JsonDict], registry: JsonDict
) -> JsonDict:
    errors = validate_projected_term_registry(registry)
    if errors:
        raise BoundedProjectionExecutionError(
            "Invalid bounded projected term registry: " + "; ".join(errors)
        )
    terms = registry["terms"]
    used: set[str] = set()
    for row in objects:
        attributes = row["attributes"]
        required = {
            "term_ref": row["name"],
            "mode_ref": attributes.get("projected_mode"),
            "domain_ref": attributes.get("projected_domain"),
        }
        for ref_field, value in required.items():
            if value is None and ref_field != "term_ref":
                continue
            if not isinstance(value, str) or value not in terms:
                raise BoundedProjectionExecutionError(
                    f"Bounded object {row['id']!r} requires missing projected "
                    f"term {value!r} for {ref_field}"
                )
            used.add(value)
            attributes[ref_field] = term_ref(registry, value)
    for row in relationships:
        attributes = row["attributes"]
        required = {
            "relation_ref": row["relationship_type"],
            "interaction_mode_ref": attributes.get("interaction_mode"),
        }
        for ref_field, value in required.items():
            if value is None and ref_field != "relation_ref":
                continue
            if not isinstance(value, str) or value not in terms:
                raise BoundedProjectionExecutionError(
                    f"Bounded relationship {row['id']!r} requires missing "
                    f"projected term {value!r} for {ref_field}"
                )
            used.add(value)
            attributes[ref_field] = term_ref(registry, value)
    return {
        "registry_id": registry["registry_id"],
        "registry_version": registry["registry_version"],
        "target_ontology": registry["target_ontology"],
        "materialization": "used_terms_subset",
        "terms": {key: deepcopy(terms[key]) for key in sorted(used)},
    }


def _project_bounded_natal(
    request: BoundedNatalProjectionRequest | JsonDict,
    *,
    profile: WoofmappedBoundedAstrologyProfile | None = None,
    include_relationships: bool,
) -> ProjectedBoundedSemanticGraph:
    """Execute the bounded profile with an optional object-only compatibility path."""

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
    object_status = {
        row["id"]: selected_profile.classify_source_object(row, source_index)
        for row in source_objects
    }
    projected: list[JsonDict] = []
    mapped_source_ids: list[str] = []
    outside_scope_ids: list[str] = []
    for source_object in source_objects:
        status = object_status[source_object["id"]]
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
        source_ref = _source_ref(source_object, kind="object")
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
            "epistemic_basis": _epistemic_basis(
                source_object, registry, kind="object"
            ),
            "projection_relevance_score": None,
            "provenance": deepcopy(draft.get("provenance") or {}),
        })
        mapped_source_ids.append(source_object["id"])

    projected.sort(key=lambda row: row["id"])
    projected_by_source_id = {
        row["source_refs"][0].split("canonical:object:", 1)[1]: row
        for row in projected
    }
    source_relationships = sorted(graph["relationships"], key=lambda row: row["id"])
    relationship_status = {
        row["id"]: selected_profile.classify_source_relationship(row, object_status)
        for row in source_relationships
    }
    relationship_drafts: list[tuple[JsonDict, JsonDict]] = []
    outside_relationship_ids: list[str] = []
    if include_relationships:
        for source_relationship in source_relationships:
            if relationship_status[source_relationship["id"]] != "eligible":
                outside_relationship_ids.append(source_relationship["id"])
                continue
            draft = selected_profile.project_relationship(deepcopy(source_relationship))
            if draft is None:
                raise BoundedProjectionExecutionError(
                    f"Eligible bounded relationship {source_relationship['id']!r} produced no mapping"
                )
            relationship_drafts.append((source_relationship, draft))
    else:
        outside_relationship_ids = [row["id"] for row in source_relationships]

    scored_family_members: dict[str, list[str]] = {}
    for source_relationship, draft in relationship_drafts:
        if draft.get("base_relevance") is None:
            continue
        family = source_relationship["evidence_metadata"]["evidence_family_group"]
        scored_family_members.setdefault(family, []).append(
            source_relationship["id"]
        )
    for members in scored_family_members.values():
        members.sort()
    scored_family_positions = {
        family: {member_id: index for index, member_id in enumerate(members)}
        for family, members in scored_family_members.items()
    }

    projected_relationships: list[JsonDict] = []
    mapped_relationship_ids: list[str] = []
    for source_relationship, draft in relationship_drafts:
        source_id = str(source_relationship["source_id"])
        target_id = str(source_relationship["target_id"])
        source_projected = projected_by_source_id.get(source_id)
        target_projected = projected_by_source_id.get(target_id)
        if source_projected is None or target_projected is None:
            raise BoundedProjectionExecutionError(
                f"Eligible bounded relationship {source_relationship['id']!r} has no projected endpoints"
            )
        source_ref = _source_ref(source_relationship, kind="relationship")
        family = source_relationship["evidence_metadata"]["evidence_family_group"]
        base_relevance = draft.get("base_relevance")
        family_members = scored_family_members.get(family, [])
        family_member_count = len(family_members)
        family_member_index = scored_family_positions.get(family, {}).get(
            source_relationship["id"], -1
        )
        relevance = (
            None
            if base_relevance is None
            else _equal_micro_allocation(
                float(base_relevance), family_member_count, family_member_index
            )
        )
        semantic_key = str(draft["semantic_key"])
        relationship_type = str(draft["relationship_type"])
        projected_relationships.append({
            "id": projected_relationship_id(
                profile_id=manifest.profile_id,
                relationship_type=relationship_type,
                source_id=source_projected["id"],
                target_id=target_projected["id"],
                source_refs=[source_ref],
                context_id=context.context_id,
            ),
            "correspondence_id": projected_bounded_correspondence_id(
                kind="relationship",
                profile_id=manifest.profile_id,
                semantic_key=semantic_key,
                source_refs=[source_ref],
            ),
            "relationship_type": relationship_type,
            "source_id": source_projected["id"],
            "target_id": target_projected["id"],
            "operators": sorted(set(draft.get("operators") or [])),
            "theme_tags": [str(draft["interaction_mode"])],
            "attributes": {
                "source_relationship_type": source_relationship["relationship_type"],
                "source_aspect": source_relationship.get("aspect"),
                "interaction_mode": draft["interaction_mode"],
                "topology_only": bool(draft["topology_only"]),
                "source_evidence_family_group": family,
                "relevance_accounting": {
                    "policy": "evidence_family_equal_allocation",
                    "base_profile_relevance": base_relevance,
                    "scored_family_member_count": family_member_count,
                    "member_allocation": (
                        None
                        if base_relevance is None
                        else _equal_micro_allocation(
                            1.0, family_member_count, family_member_index
                        )
                    ),
                    "raw_record_count_is_weight": False,
                },
            },
            "source_relationship_refs": [source_ref],
            "mapping_rule_refs": [draft["mapping_rule_id"]],
            "context_refs": [context.context_id],
            "epistemic_basis": _epistemic_basis(
                source_relationship, registry, kind="relationship"
            ),
            "projection_relevance_score": relevance,
            "provenance": deepcopy(draft.get("provenance") or {}),
        })
        mapped_relationship_ids.append(source_relationship["id"])
    projected_relationships.sort(key=lambda row: row["id"])
    term_registry = _registry_subset(
        projected, projected_relationships, selected_profile.projected_term_registry()
    )
    eligible_object_families = {
        source_index[row_id]["evidence_metadata"]["evidence_family_group"]
        for row_id, status in object_status.items() if status == "eligible"
    }
    mapped_object_families = {
        source_index[row_id]["evidence_metadata"]["evidence_family_group"]
        for row_id in mapped_source_ids
    }
    relationship_index = {row["id"]: row for row in source_relationships}
    eligible_relationship_families = {
        relationship_index[row_id]["evidence_metadata"]["evidence_family_group"]
        for row_id, status in relationship_status.items() if status == "eligible"
    }
    mapped_relationship_families = {
        relationship_index[row_id]["evidence_metadata"]["evidence_family_group"]
        for row_id in mapped_relationship_ids
    }
    audit = {
        "profile_id": manifest.profile_id,
        "profile_version": manifest.profile_version,
        "object_mapping_status": "complete_for_declared_slice_4_scope",
        "relationship_mapping_status": (
            "complete_for_declared_slice_5_scope"
            if include_relationships else "deferred_to_slice_5"
        ),
        "coverage": {
            "source_object_count": len(source_objects),
            "mapped_source_object_count": len(mapped_source_ids),
            "outside_declared_scope_count": len(outside_scope_ids),
            "mapped_source_object_ids": sorted(mapped_source_ids),
            "outside_declared_scope_ids": sorted(outside_scope_ids),
            "source_relationship_count": len(source_relationships),
            "mapped_source_relationship_count": len(mapped_relationship_ids),
            "outside_declared_scope_relationship_count": len(outside_relationship_ids),
            "mapped_source_relationship_ids": sorted(mapped_relationship_ids),
            "outside_declared_scope_relationship_ids": sorted(outside_relationship_ids),
            "family_coverage": {
                "eligible_object_family_count": len(eligible_object_families),
                "mapped_object_family_count": len(mapped_object_families),
                "eligible_relationship_family_count": len(eligible_relationship_families),
                "mapped_relationship_family_count": len(mapped_relationship_families),
                "raw_record_counts_are_weights": False,
                "relationship_relevance_aggregation_unit": "evidence_family_group",
            },
        },
        "source_selection_policy": deepcopy(
            selected_profile.source_selection_policy
        ),
    }
    diagnostics = {
        "errors": [],
        "warnings": [],
        "infos": ([
            {
                "code": "bounded.relationship_mapping.deferred",
                "message": "Relationship projection is intentionally deferred to Slice 5.",
            }
        ] if not include_relationships else []),
    }
    return build_projected_bounded_contract(
        request_value,
        target_ontology=manifest.target_ontology,
        objects=projected,
        relationships=projected_relationships,
        projected_term_registry=term_registry,
        audit=audit,
        diagnostics=diagnostics,
    )


def project_bounded_natal_objects(
    request: BoundedNatalProjectionRequest | JsonDict,
    *,
    profile: WoofmappedBoundedAstrologyProfile | None = None,
) -> ProjectedBoundedSemanticGraph:
    """Project bounded objects only for the explicit Slice 4 compatibility path."""

    return _project_bounded_natal(
        request, profile=profile, include_relationships=False
    )


def project_bounded_natal(
    request: BoundedNatalProjectionRequest | JsonDict,
    *,
    profile: WoofmappedBoundedAstrologyProfile | None = None,
) -> ProjectedBoundedSemanticGraph:
    """Project supported bounded objects and relationships."""

    return _project_bounded_natal(
        request, profile=profile, include_relationships=True
    )
