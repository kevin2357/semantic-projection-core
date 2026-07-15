from __future__ import annotations

from copy import deepcopy
from dataclasses import replace
import json
from typing import Any

from .contracts import (
    MappingExecution,
    ProjectedObject,
    ProjectedRelationship,
    ProjectedSemanticGraph,
    ProjectionAudit,
    ProjectionContext,
    ProjectionDiagnostics,
    ProjectionRequest,
)
from .diagnostics import diagnostic
from .ids import (
    mapping_execution_id,
    projected_object_id,
    projected_package_id,
    projected_relationship_id,
    stable_hash,
)
from .profile import ProjectionProfile
from .term_registry import attach_registry_refs_and_subset
from .registry import ProjectionProfileRegistry
from .validation import (
    ProjectionValidationError,
    validate_contract,
    validate_projected_graph_ids,
    validate_projection_request,
)

JsonDict = dict[str, Any]
ENGINE_VERSION = "0.7.0"


class ProjectionExecutionError(RuntimeError):
    pass


def _unique(values: list[str]) -> list[str]:
    return sorted({str(value) for value in values if value is not None})


def _source_ref(row: JsonDict, *, kind: str) -> str:
    identifier = row.get("id") or row.get("relationship_id") or row.get("source_key")
    if identifier is None:
        identifier = stable_hash(row)
    return f"canonical:{kind}:{identifier}"


def _context(request: ProjectionRequest) -> ProjectionContext:
    return ProjectionContext.from_dict(request.context)


def _request_copy(request: ProjectionRequest) -> ProjectionRequest:
    return ProjectionRequest.from_dict(deepcopy(request.to_dict()))


def _projected_object_from_draft(
    *,
    profile: ProjectionProfile,
    request: ProjectionRequest,
    source_ref: str,
    draft: JsonDict,
) -> ProjectedObject:
    context_id = str(request.context.get("context_id"))
    target_key = str(draft.get("target_key") or draft.get("name") or source_ref)
    rule_id = str(draft["mapping_rule_id"])
    source_refs = _unique([source_ref, *(draft.get("source_refs") or [])])
    merge_key = draft.get("merge_key")
    identity_source_refs = [] if merge_key is not None else source_refs
    return ProjectedObject(
        id=projected_object_id(
            profile_id=profile.manifest.profile_id,
            target_key=str(merge_key or target_key),
            source_refs=identity_source_refs,
            context_id=context_id,
        ),
        object_type=str(draft.get("object_type") or "projected_semantic_primitive"),
        name=str(draft.get("name") or target_key),
        target_ontology=profile.manifest.target_ontology,
        operators=_unique(list(draft.get("operators") or [])),
        source_refs=source_refs,
        mapping_rule_refs=_unique([rule_id, *(draft.get("mapping_rule_refs") or [])]),
        context_refs=_unique([context_id, *(draft.get("context_refs") or [])]),
        attributes=deepcopy(draft.get("attributes") or {}),
        structural_strength_score=draft.get("structural_strength_score"),
        projection_relevance_score=draft.get("projection_relevance_score"),
        provenance=deepcopy(draft.get("provenance") or {}),
    )




def _merge_attributes(existing: JsonDict, incoming: JsonDict) -> JsonDict:
    """Merge profile attributes without silently losing list-valued provenance.

    Profiles should use plural arrays such as ``source_names`` for naturally
    multi-source values. Equal scalars remain scalars; conflicting scalars keep
    the first value and are exposed under ``merged_attribute_values``.
    """
    result = deepcopy(existing)
    conflicts: dict[str, list[Any]] = deepcopy(
        result.get("merged_attribute_values") or {}
    )
    for key, value in incoming.items():
        if key == "merged_attribute_values":
            continue
        if key not in result:
            result[key] = deepcopy(value)
            continue
        current = result[key]
        if current == value:
            continue
        if isinstance(current, list) and isinstance(value, list):
            result[key] = sorted(
                {json.dumps(item, sort_keys=True, default=str): item
                 for item in [*current, *value]}.values(),
                key=lambda item: json.dumps(item, sort_keys=True, default=str),
            )
        elif isinstance(current, dict) and isinstance(value, dict):
            result[key] = _merge_attributes(current, value)
        else:
            values = [current, value, *(conflicts.get(key) or [])]
            deduped = []
            for item in values:
                if item not in deduped:
                    deduped.append(item)
            conflicts[key] = deduped
    if conflicts:
        result["merged_attribute_values"] = conflicts
    return result

def _merge_object(existing: ProjectedObject, incoming: ProjectedObject) -> ProjectedObject:
    existing.source_refs = _unique(existing.source_refs + incoming.source_refs)
    existing.mapping_rule_refs = _unique(existing.mapping_rule_refs + incoming.mapping_rule_refs)
    existing.context_refs = _unique(existing.context_refs + incoming.context_refs)
    existing.operators = _unique(existing.operators + incoming.operators)
    existing.attributes = _merge_attributes(existing.attributes, incoming.attributes)
    existing.provenance = {**existing.provenance, **incoming.provenance}
    scores = [
        score for score in (
            existing.structural_strength_score,
            incoming.structural_strength_score,
        ) if score is not None
    ]
    if scores:
        existing.structural_strength_score = max(scores)
    relevance = [
        score for score in (
            existing.projection_relevance_score,
            incoming.projection_relevance_score,
        ) if score is not None
    ]
    if relevance:
        existing.projection_relevance_score = max(relevance)
    return existing


def _resolve_projected_endpoint(
    value: Any,
    projected_object_index: dict[str, list[JsonDict]],
) -> str | None:
    if value is None:
        return None
    value = str(value)
    candidates = projected_object_index.get(value) or []
    if not candidates:
        return None
    return str(candidates[0]["id"])


def _projected_relationship_from_draft(
    *,
    profile: ProjectionProfile,
    request: ProjectionRequest,
    source_ref: str,
    draft: JsonDict,
    projected_object_index: dict[str, list[JsonDict]],
) -> ProjectedRelationship:
    context_id = str(request.context.get("context_id"))
    source_id = draft.get("source_id") or _resolve_projected_endpoint(
        draft.get("source_source_id"), projected_object_index
    )
    target_id = draft.get("target_id") or _resolve_projected_endpoint(
        draft.get("target_source_id"), projected_object_index
    )
    if source_id is None or target_id is None:
        raise ProjectionExecutionError(
            "Projected relationship draft could not resolve source and target endpoints"
        )
    relationship_type = str(draft.get("relationship_type") or "projected_relation")
    source_refs = _unique([source_ref, *(draft.get("source_relationship_refs") or [])])
    rule_id = str(draft["mapping_rule_id"])
    return ProjectedRelationship(
        id=projected_relationship_id(
            profile_id=profile.manifest.profile_id,
            relationship_type=relationship_type,
            source_id=str(source_id),
            target_id=str(target_id),
            source_refs=source_refs,
            context_id=context_id,
        ),
        relationship_type=relationship_type,
        source_id=str(source_id),
        target_id=str(target_id),
        source_relationship_refs=source_refs,
        mapping_rule_refs=_unique([rule_id, *(draft.get("mapping_rule_refs") or [])]),
        context_refs=_unique([context_id, *(draft.get("context_refs") or [])]),
        operators=_unique(list(draft.get("operators") or [])),
        theme_tags=_unique(list(draft.get("theme_tags") or [])),
        attributes=deepcopy(draft.get("attributes") or {}),
        projection_relevance_score=draft.get("projection_relevance_score"),
        provenance=deepcopy(draft.get("provenance") or {}),
    )


def _mapping_execution(
    *,
    request: ProjectionRequest,
    source_ref: str,
    draft: JsonDict,
    result_refs: list[str],
) -> MappingExecution:
    rule_id = str(draft["mapping_rule_id"])
    context_id = str(request.context.get("context_id"))
    return MappingExecution(
        execution_id=mapping_execution_id(
            mapping_rule_id=rule_id,
            source_refs=[source_ref],
            context_id=context_id,
            result_refs=result_refs,
        ),
        mapping_rule_id=rule_id,
        mapping_rule_version=str(draft.get("mapping_rule_version") or "1.0.0"),
        source_refs=[source_ref],
        context_refs=[context_id],
        result_refs=result_refs,
        status=str(draft.get("status") or "applied"),
        conditions_evaluated=deepcopy(draft.get("conditions_evaluated") or []),
        warnings=list(draft.get("warnings") or []),
    )


def _handle_unmapped(
    *,
    kind: str,
    source_ref: str,
    source_row: JsonDict,
    request: ProjectionRequest,
    diagnostics: ProjectionDiagnostics,
    projected_objects: dict[str, ProjectedObject],
    source_index: dict[str, list[JsonDict]],
    profile: ProjectionProfile,
) -> None:
    policy = str(request.options.get("unmapped_policy") or "diagnostic")
    diagnostics.unmapped_source_refs.append(source_ref)
    if policy == "fail":
        raise ProjectionExecutionError(f"Unmapped {kind} source {source_ref}")
    if policy == "ignore":
        return
    if policy == "passthrough" and kind == "object":
        source_id = str(source_row.get("id") or source_ref)
        draft = {
            "target_key": f"unmapped:{source_id}",
            "object_type": "unmapped_source_placeholder",
            "name": str(source_row.get("name") or source_id),
            "operators": [],
            "attributes": {"unmapped": True},
            "mapping_rule_id": f"{profile.manifest.profile_id}.fallback.passthrough",
            "warnings": ["Source object retained as unmapped placeholder"],
        }
        projected = _projected_object_from_draft(
            profile=profile,
            request=request,
            source_ref=source_ref,
            draft=draft,
        )
        projected_objects[projected.id] = projected
        source_index.setdefault(source_id, []).append(projected.to_dict())
        diagnostics.fallbacks.append({
            "source_ref": source_ref,
            "fallback": "passthrough_placeholder",
            "result_ref": projected.id,
        })
    diagnostics.infos.append(diagnostic(
        "projection.source_unmapped",
        f"No mapping applied to {kind} source",
        details={"source_ref": source_ref, "policy": policy},
    ))



def _profile_classification(
    profile: ProjectionProfile,
    source_objects: list[JsonDict],
    source_relationships: list[JsonDict],
    mapped_object_refs: set[str],
    mapped_relationship_refs: set[str],
) -> JsonDict:
    classify_object = getattr(profile, "classify_source_object", None)
    classify_relationship = getattr(profile, "classify_source_relationship", None)

    object_status: dict[str, str] = {}
    for row in source_objects:
        source_ref = _source_ref(row, kind="object")
        status = (
            str(classify_object(row))
            if callable(classify_object)
            else ("eligible" if source_ref in mapped_object_refs else "outside_declared_scope")
        )
        object_status[str(row.get("id"))] = status

    relationship_status: dict[str, str] = {}
    for row in source_relationships:
        source_ref = _source_ref(row, kind="relationship")
        status = (
            str(classify_relationship(row, object_status))
            if callable(classify_relationship)
            else ("eligible" if source_ref in mapped_relationship_refs else "outside_declared_scope")
        )
        relationship_status[str(row.get("id"))] = status

    def counts(values: dict[str, str], mapped_refs: set[str], kind: str) -> JsonDict:
        eligible_ids = {key for key, status in values.items() if status == "eligible"}
        mapped_ids = {
            ref.split(f"canonical:{kind}:", 1)[1]
            for ref in mapped_refs
            if ref.startswith(f"canonical:{kind}:")
        }
        eligible_mapped = eligible_ids & mapped_ids
        eligible_unmapped = eligible_ids - mapped_ids
        return {
            "eligible_count": len(eligible_ids),
            "mapped_eligible_count": len(eligible_mapped),
            "eligible_but_unmapped_count": len(eligible_unmapped),
            "outside_declared_scope_count": sum(
                1 for status in values.values() if status == "outside_declared_scope"
            ),
            "excluded_by_source_selection_policy_count": sum(
                1 for status in values.values()
                if status == "excluded_by_source_selection_policy"
            ),
            "declared_scope_coverage": (
                round(len(eligible_mapped) / len(eligible_ids), 6)
                if eligible_ids else 1.0
            ),
            "eligible_but_unmapped_ids": sorted(eligible_unmapped),
        }

    return {
        "classification_contract": "projection_scope_classification.v1",
        "objects": counts(object_status, mapped_object_refs, "object"),
        "relationships": counts(
            relationship_status, mapped_relationship_refs, "relationship"
        ),
        "source_selection_policy": deepcopy(
            getattr(profile, "source_selection_policy", {})
        ),
    }


def project(
    request: ProjectionRequest | JsonDict,
    *,
    registry: ProjectionProfileRegistry,
) -> ProjectedSemanticGraph:
    """Execute one deterministic projection request."""
    request_obj = (
        request if isinstance(request, ProjectionRequest)
        else ProjectionRequest.from_dict(deepcopy(request))
    )
    request_obj = _request_copy(request_obj)
    validate_projection_request(request_obj.to_dict())
    profile = registry.resolve(request_obj.profile_id, request_obj.profile_version)

    if profile.manifest.profile_id != request_obj.profile_id or profile.manifest.profile_version != request_obj.profile_version:
        raise ProjectionExecutionError("Resolved profile manifest does not match request")
    if request_obj.context.get("target_domain") != profile.manifest.target_ontology:
        raise ProjectionExecutionError(
            "Projection context target_domain does not match profile target_ontology"
        )

    context = _context(request_obj)
    diagnostics = ProjectionDiagnostics()
    diagnostics.warnings.extend(profile.validate_context(context))

    source_graph = request_obj.source_graph
    source_objects = sorted(source_graph.get("objects") or [], key=lambda row: str(row.get("id") or row.get("source_key") or ""))
    source_relationships = sorted(source_graph.get("relationships") or [], key=lambda row: str(row.get("id") or row.get("relationship_id") or ""))

    projected_objects: dict[str, ProjectedObject] = {}
    source_object_index: dict[str, list[JsonDict]] = {}
    executions: list[MappingExecution] = []
    mapped_object_refs: set[str] = set()
    mapped_relationship_refs: set[str] = set()

    for source_object in source_objects:
        source_ref = _source_ref(source_object, kind="object")
        drafts = profile.project_object(deepcopy(source_object), request_obj) or []
        if not drafts:
            _handle_unmapped(
                kind="object", source_ref=source_ref, source_row=source_object,
                request=request_obj, diagnostics=diagnostics,
                projected_objects=projected_objects,
                source_index=source_object_index, profile=profile,
            )
            continue
        mapped_object_refs.add(source_ref)
        source_id = str(source_object.get("id") or source_object.get("source_key") or source_ref)
        for draft in drafts:
            if not draft.get("mapping_rule_id"):
                raise ProjectionExecutionError("Object draft is missing mapping_rule_id")
            projected = _projected_object_from_draft(
                profile=profile, request=request_obj, source_ref=source_ref, draft=draft
            )
            if projected.id in projected_objects:
                projected = _merge_object(projected_objects[projected.id], projected)
            projected_objects[projected.id] = projected
            source_object_index.setdefault(source_id, []).append(projected.to_dict())
            executions.append(_mapping_execution(
                request=request_obj, source_ref=source_ref,
                draft=draft, result_refs=[projected.id],
            ))

    projected_relationships: dict[str, ProjectedRelationship] = {}
    for source_relationship in source_relationships:
        source_ref = _source_ref(source_relationship, kind="relationship")
        drafts = profile.project_relationship(
            deepcopy(source_relationship), deepcopy(source_object_index), request_obj
        ) or []
        if not drafts:
            _handle_unmapped(
                kind="relationship", source_ref=source_ref,
                source_row=source_relationship, request=request_obj,
                diagnostics=diagnostics, projected_objects=projected_objects,
                source_index=source_object_index, profile=profile,
            )
            continue
        mapped_relationship_refs.add(source_ref)
        for draft in drafts:
            if not draft.get("mapping_rule_id"):
                raise ProjectionExecutionError("Relationship draft is missing mapping_rule_id")
            projected = _projected_relationship_from_draft(
                profile=profile, request=request_obj, source_ref=source_ref,
                draft=draft, projected_object_index=source_object_index,
            )
            projected_relationships[projected.id] = projected
            executions.append(_mapping_execution(
                request=request_obj, source_ref=source_ref,
                draft=draft, result_refs=[projected.id],
            ))

    objects = [value.to_dict() for _, value in sorted(projected_objects.items())]
    relationships = [value.to_dict() for _, value in sorted(projected_relationships.items())]
    diagnostics.unmapped_source_refs = sorted(set(diagnostics.unmapped_source_refs))
    diagnostics.infos = sorted(diagnostics.infos, key=lambda row: (row.get("code", ""), str(row.get("details", {}))))

    request_dict = request_obj.to_dict()
    profile_scope = _profile_classification(
        profile,
        source_objects,
        source_relationships,
        mapped_object_refs,
        mapped_relationship_refs,
    )
    audit = ProjectionAudit(
        profile_id=profile.manifest.profile_id,
        profile_version=profile.manifest.profile_version,
        engine_version=ENGINE_VERSION,
        request_hash=stable_hash(request_dict),
        source_graph_hash=stable_hash(source_graph),
        context_hash=stable_hash(request_obj.context),
        coverage={
            "source_object_count": len(source_objects),
            "mapped_source_object_count": len(mapped_object_refs),
            "unmapped_source_object_count": len(source_objects) - len(mapped_object_refs),
            "source_relationship_count": len(source_relationships),
            "mapped_source_relationship_count": len(mapped_relationship_refs),
            "unmapped_source_relationship_count": len(source_relationships) - len(mapped_relationship_refs),
        },
        mapping_executions=[value.to_dict() for value in sorted(executions, key=lambda row: row.execution_id)],
        unmapped_source_refs=diagnostics.unmapped_source_refs,
        fallbacks=deepcopy(diagnostics.fallbacks),
    )

    graph = ProjectedSemanticGraph(
        metadata={
            "package_type": "projected_semantic_graph",
            "projection_id": projected_package_id(request_dict),
            "engine_version": ENGINE_VERSION,
            "profile_id": profile.manifest.profile_id,
            "profile_version": profile.manifest.profile_version,
            "context_id": context.context_id,
            "context_version": context.context_version,
        },
        source_identity=deepcopy(request_obj.source_identity),
        source_graph_ref={
            "graph_type": source_graph.get("graph_type"),
            "graph_version": source_graph.get("graph_version"),
            "source_graph_hash": audit.source_graph_hash,
        },
        target_ontology=profile.manifest.target_ontology,
        projected_term_registry={},
        objects=objects,
        relationships=relationships,
        indexes={
            "object_by_id": {row["id"]: index for index, row in enumerate(objects)},
            "relationship_by_id": {row["id"]: index for index, row in enumerate(relationships)},
            "projected_objects_by_source_ref": {
                source_id: sorted({row["id"] for row in rows})
                for source_id, rows in sorted(source_object_index.items())
            },
            "projected_relationships_by_source_ref": {
                source_ref: sorted({
                    row["id"]
                    for row in relationships
                    if source_ref in (row.get("source_relationship_refs") or [])
                })
                for source_ref in sorted({
                    ref
                    for row in relationships
                    for ref in (row.get("source_relationship_refs") or [])
                })
            },
        },
        summary={
            "object_count": len(objects),
            "relationship_count": len(relationships),
            "mapped_source_object_count": len(mapped_object_refs),
            "mapped_source_relationship_count": len(mapped_relationship_refs),
            "unmapped_source_count": len(diagnostics.unmapped_source_refs),
            "profile_scope_coverage": deepcopy(profile_scope),
        },
        audit=(
            audit.to_dict()
            if request_obj.options.get("include_audit", True)
            else replace(audit, mapping_executions=[]).to_dict()
        ),
        diagnostics=(
            diagnostics.to_dict()
            if request_obj.options.get("include_diagnostics", True)
            else ProjectionDiagnostics().to_dict()
        ),
    )

    profile.finalize(graph, request_obj)
    registry_provider = getattr(profile, "projected_term_registry", None)
    if callable(registry_provider):
        graph.projected_term_registry = attach_registry_refs_and_subset(
            graph, registry_provider()
        )
        graph.metadata["projected_term_registry_id"] = (
            graph.projected_term_registry.get("registry_id")
        )
        graph.metadata["projected_term_registry_version"] = (
            graph.projected_term_registry.get("registry_version")
        )
    graph.objects = sorted(graph.objects, key=lambda row: row["id"])
    graph.relationships = sorted(graph.relationships, key=lambda row: row["id"])
    graph.indexes["object_by_id"] = {row["id"]: index for index, row in enumerate(graph.objects)}
    graph.indexes["relationship_by_id"] = {row["id"]: index for index, row in enumerate(graph.relationships)}

    graph_dict = graph.to_dict()
    validate_projected_graph_ids(graph_dict)
    validate_contract(graph_dict, "projected_semantic_graph_v1.schema.json")
    return graph
