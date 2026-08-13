from __future__ import annotations

from collections.abc import Iterable, Mapping
from copy import deepcopy
from typing import Any

from .bounded import validate_foundry_bounded_natal_dataset
from .contracts import (
    BoundedNatalProjectionRequest,
    ProjectedBoundedSemanticGraph,
)
from .ids import bounded_correspondence_id, stable_hash
from .runtime_identity import projection_runtime_identity
from .validation import (
    validate_bounded_natal_projection_request,
    validate_projected_bounded_semantic_graph,
)

JsonDict = dict[str, Any]
OUTPUT_CONTRACT = "projected_bounded_semantic_graph.v1"


def _sorted_unique(values: Iterable[str]) -> list[str]:
    return sorted({str(value) for value in values if value})


def bounded_evidence_closure(
    source_artifact: Mapping[str, Any],
    direct_refs: Iterable[str],
) -> JsonDict:
    """Materialize direct evidence plus exactly resolvable prerequisite closure."""

    validate_foundry_bounded_natal_dataset(source_artifact)
    registry = source_artifact["uncertainty_assessment"]["evidence_registry"]
    direct = _sorted_unique(direct_refs)
    missing_direct = [ref for ref in direct if ref not in registry]
    if missing_direct:
        raise ValueError(f"Missing direct bounded evidence references: {missing_direct[:5]}")

    selected: set[str] = set()
    resolved_prerequisites: set[str] = set()
    unresolved_prerequisites: set[str] = set()
    pending = list(reversed(direct))
    while pending:
        ref = pending.pop()
        if ref in selected:
            continue
        selected.add(ref)
        record = registry[ref]
        for prerequisite in _sorted_unique(record.get("prerequisite_refs") or []):
            if prerequisite in registry:
                resolved_prerequisites.add(prerequisite)
                if prerequisite not in selected:
                    pending.append(prerequisite)
            else:
                unresolved_prerequisites.add(prerequisite)

    records = {key: deepcopy(registry[key]) for key in sorted(selected)}
    semantic_sha256 = stable_hash(records, length=64)
    return {
        "evidence_contract": source_artifact["uncertainty_assessment"][
            "evidence_contract_version"
        ],
        "materialization": "direct_refs_plus_resolvable_prerequisites",
        "records": records,
        "direct_refs": direct,
        "resolved_prerequisite_refs": sorted(resolved_prerequisites),
        "unresolved_prerequisite_refs": sorted(unresolved_prerequisites),
        "source_registry_record_count": len(registry),
        "materialized_record_count": len(records),
        "semantic_sha256": semantic_sha256,
    }


def projected_bounded_correspondence_id(
    *,
    kind: str,
    profile_id: str,
    semantic_key: str,
    source_refs: Iterable[str],
) -> str:
    return bounded_correspondence_id(
        kind=kind,
        profile_id=profile_id,
        semantic_key=semantic_key,
        source_refs=_sorted_unique(source_refs),
    )


def build_projected_bounded_contract(
    request: BoundedNatalProjectionRequest | Mapping[str, Any],
    *,
    target_ontology: str,
    objects: list[JsonDict] | None = None,
    relationships: list[JsonDict] | None = None,
    projected_term_registry: JsonDict | None = None,
    audit: JsonDict | None = None,
    diagnostics: JsonDict | None = None,
) -> ProjectedBoundedSemanticGraph:
    """Build and validate one bounded output without performing mappings."""

    request_value = (
        request.to_dict()
        if isinstance(request, BoundedNatalProjectionRequest)
        else deepcopy(dict(request))
    )
    validate_bounded_natal_projection_request(request_value)
    source_artifact = request_value["source_artifact"]
    validate_foundry_bounded_natal_dataset(source_artifact)
    projected_objects = sorted(deepcopy(objects or []), key=lambda row: row["id"])
    projected_relationships = sorted(
        deepcopy(relationships or []), key=lambda row: row["id"]
    )
    direct_evidence_refs = _sorted_unique(
        ref
        for row in [*projected_objects, *projected_relationships]
        for ref in (row.get("epistemic_basis") or {}).get("evidence_refs") or []
    )
    evidence = bounded_evidence_closure(source_artifact, direct_evidence_refs)
    context = request_value["context"]
    runtime_identity = projection_runtime_identity(
        profile_id=request_value["profile_id"],
        profile_version=request_value["profile_version"],
        context=context,
        route="bounded_natal_projection",
        output_contract=OUTPUT_CONTRACT,
    )
    source_graph = source_artifact["canonical_astrology_graph"]
    source_assessment = source_artifact["uncertainty_assessment"]
    source_artifact_sha256 = request_value["source_identity"][
        "source_artifact_sha256"
    ]
    epistemic_identity = {
        "source_artifact_sha256": source_artifact_sha256,
        "evidence_semantic_sha256": evidence["semantic_sha256"],
        "source_capabilities_sha256": stable_hash(
            source_artifact["capabilities"], length=64
        ),
        "source_feature_dispositions_sha256": stable_hash(
            source_assessment["feature_dispositions"], length=64
        ),
    }
    graph = ProjectedBoundedSemanticGraph(
        metadata={
            "package_type": "projected_bounded_semantic_graph",
            "contract_version": "1.0.0",
            "output_contract": OUTPUT_CONTRACT,
            "projection_id": "bounded_projection:" + stable_hash(request_value),
            "engine_version": runtime_identity["distribution"]["package_version"],
            "profile_id": request_value["profile_id"],
            "profile_version": request_value["profile_version"],
            "context_id": context["context_id"],
            "context_version": context["context_version"],
            "runtime_identity": runtime_identity,
        },
        source_identity=deepcopy(request_value["source_identity"]),
        source_artifact_ref={
            "package_type": source_artifact["metadata"]["analysis_type"],
            "package_schema_version": source_artifact["metadata"]["schema_version"],
            "graph_type": source_graph["graph_type"],
            "graph_version": source_graph["graph_version"],
            "source_artifact_sha256": source_artifact_sha256,
        },
        target_ontology=target_ontology,
        source_capabilities=deepcopy(source_artifact["capabilities"]),
        source_feature_dispositions=deepcopy(
            source_assessment["feature_dispositions"]
        ),
        source_evidence=evidence,
        objects=projected_objects,
        relationships=projected_relationships,
        indexes={
            "object_by_id": {
                row["id"]: index for index, row in enumerate(projected_objects)
            },
            "relationship_by_id": {
                row["id"]: index
                for index, row in enumerate(projected_relationships)
            },
            "entity_by_correspondence_id": {
                row["correspondence_id"]: row["id"]
                for row in [*projected_objects, *projected_relationships]
            },
        },
        summary={
            "object_count": len(projected_objects),
            "relationship_count": len(projected_relationships),
            "source_evidence_record_count": evidence["materialized_record_count"],
            "source_graph_basis": "bounded_invariant_subgraph",
            "raw_counts_are_weights": False,
            "epistemic_classification": "invariant",
        },
        projected_term_registry=deepcopy(projected_term_registry or {}),
        audit=deepcopy(audit or {}),
        diagnostics=deepcopy(
            diagnostics or {"errors": [], "warnings": [], "infos": []}
        ),
        provenance={
            "upstream_contracts": deepcopy(request_value["upstream_contracts"]),
            "runtime_identity": runtime_identity,
            "epistemic_identity": epistemic_identity,
            "context_epistemic_policy": "certainty_invariant_across_contexts",
            "evidence_materialization_policy": evidence["materialization"],
        },
        limitations=list(request_value.get("limitations") or []),
    )
    validate_projected_bounded_semantic_graph(graph.to_dict())
    return graph
