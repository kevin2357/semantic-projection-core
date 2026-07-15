from __future__ import annotations

from typing import Any

from .contracts import ProjectionAudit
from .ids import stable_hash


def empty_coverage(source_graph: dict[str, Any]) -> dict[str, int]:
    return {
        "source_object_count": len(source_graph.get("objects") or []),
        "mapped_source_object_count": 0,
        "unmapped_source_object_count": len(source_graph.get("objects") or []),
        "source_relationship_count": len(source_graph.get("relationships") or []),
        "mapped_source_relationship_count": 0,
        "unmapped_source_relationship_count": len(source_graph.get("relationships") or []),
    }


def create_empty_audit(*, profile_id: str, profile_version: str, engine_version: str, request: dict[str, Any]) -> ProjectionAudit:
    source_graph = request.get("source_graph") or {}
    context = request.get("context") or {}
    return ProjectionAudit(
        profile_id=profile_id,
        profile_version=profile_version,
        engine_version=engine_version,
        request_hash=stable_hash(request),
        source_graph_hash=stable_hash(source_graph),
        context_hash=stable_hash(context),
        coverage=empty_coverage(source_graph),
    )
