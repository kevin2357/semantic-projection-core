from __future__ import annotations

import hashlib
import json
from typing import Any


def canonical_json(value: Any) -> str:
    """Stable JSON encoding used by all projection identifiers."""
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    )


def stable_hash(value: Any, *, length: int = 24) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()[:length]


def projection_request_id(*, profile_id: str, profile_version: str, source_identity: dict, context: dict, options: dict | None = None) -> str:
    token = stable_hash({
        "profile_id": profile_id,
        "profile_version": profile_version,
        "source_identity": source_identity,
        "context": context,
        "options": options or {},
    })
    return f"projection_request:{token}"


def projected_package_id(request: dict) -> str:
    return f"projection:{stable_hash(request)}"


def projected_object_id(*, profile_id: str, target_key: str, source_refs: list[str], context_id: str) -> str:
    return f"projected:{profile_id}:{stable_hash([target_key, sorted(source_refs), context_id])}"


def projected_relationship_id(*, profile_id: str, relationship_type: str, source_id: str, target_id: str, source_refs: list[str], context_id: str) -> str:
    return f"projected_relation:{profile_id}:{stable_hash([relationship_type, source_id, target_id, sorted(source_refs), context_id])}"


def mapping_execution_id(*, mapping_rule_id: str, source_refs: list[str], context_id: str, result_refs: list[str]) -> str:
    return f"mapping_execution:{stable_hash([mapping_rule_id, sorted(source_refs), context_id, sorted(result_refs)])}"


def temporal_projection_request_id(
    *,
    profile_id: str,
    profile_version: str,
    source_identity: dict,
    target_identity: dict,
    temporal_graph_id: str,
    context: dict,
    options: dict | None = None,
) -> str:
    """Stable identity for a generic temporal projection request."""
    token = stable_hash({
        "profile_id": profile_id,
        "profile_version": profile_version,
        "source_identity": source_identity,
        "target_identity": target_identity,
        "temporal_graph_id": temporal_graph_id,
        "context": context,
        "options": options or {},
    })
    return f"temporal_projection_request:{token}"



def projected_temporal_graph_id(
    *,
    request_id: str,
    static_projection_id: str,
    temporal_graph_id: str,
    profile_id: str,
    profile_version: str,
    context_id: str,
    options: dict | None = None,
) -> str:
    return "temporal_projection:" + stable_hash({
        "request_id": request_id,
        "static_projection_id": static_projection_id,
        "temporal_graph_id": temporal_graph_id,
        "profile_id": profile_id,
        "profile_version": profile_version,
        "context_id": context_id,
        "options": options or {},
    })


def projected_temporal_activator_id(
    *, profile_id: str, source_activator_ref: str, projected_operator_ref: str, context_id: str
) -> str:
    return f"projected_temporal_activator:{profile_id}:" + stable_hash([
        source_activator_ref, projected_operator_ref, context_id
    ])


def projected_temporal_sequence_id(
    *, profile_id: str, source_sequence_ref: str, context_id: str
) -> str:
    return f"projected_temporal_sequence:{profile_id}:" + stable_hash([
        source_sequence_ref, context_id
    ])


def projected_temporal_activation_id(
    *,
    profile_id: str,
    source_activation_ref: str,
    projected_activator_ref: str,
    projected_target_ref: str,
    projected_relationship_type: str,
    context_id: str,
) -> str:
    return f"projected_temporal_activation:{profile_id}:" + stable_hash([
        source_activation_ref,
        projected_activator_ref,
        projected_target_ref,
        projected_relationship_type,
        context_id,
    ])


def projected_temporal_state_id(
    *, profile_id: str, source_state_ref: str, projected_activation_ref: str, context_id: str
) -> str:
    return f"projected_temporal_state:{profile_id}:" + stable_hash([
        source_state_ref, projected_activation_ref, context_id
    ])
