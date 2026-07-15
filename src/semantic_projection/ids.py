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
