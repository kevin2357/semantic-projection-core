from __future__ import annotations

from copy import deepcopy
from typing import Any

from .ids import stable_hash

JsonDict = dict[str, Any]

MATERIALIZATION_MODES = {"full", "standard", "summary", "forensic"}


def _diagnostics_summary(diagnostics: JsonDict, audit: JsonDict) -> JsonDict:
    return {
        "error_count": len(diagnostics.get("errors") or []),
        "warning_count": len(diagnostics.get("warnings") or []),
        "info_count": len(diagnostics.get("infos") or []),
        "unmapped_source_count": len(
            diagnostics.get("unmapped_source_refs")
            or audit.get("unmapped_source_refs")
            or []
        ),
        "fallback_count": len(diagnostics.get("fallbacks") or audit.get("fallbacks") or []),
    }


def _compact_audit(audit: JsonDict) -> JsonDict:
    return {
        key: deepcopy(audit.get(key))
        for key in (
            "profile_id",
            "profile_version",
            "engine_version",
            "request_hash",
            "source_graph_hash",
            "context_hash",
            "coverage",
            "diagnostics_ref",
        )
        if key in audit
    } | {
        "mapping_execution_count": len(audit.get("mapping_executions") or []),
        "unmapped_source_count": len(audit.get("unmapped_source_refs") or []),
        "fallback_count": len(audit.get("fallbacks") or []),
    }


def projection_summary_view(projected: JsonDict) -> JsonDict:
    """Small portable projection summary with truthful profile-scope coverage."""
    audit = projected.get("audit") or {}
    diagnostics = projected.get("diagnostics") or {}
    return {
        "metadata": deepcopy(projected.get("metadata") or {}),
        "source_identity": deepcopy(projected.get("source_identity") or {}),
        "source_graph_ref": deepcopy(projected.get("source_graph_ref") or {}),
        "target_ontology": projected.get("target_ontology"),
        "summary": deepcopy(projected.get("summary") or {}),
        "coverage": deepcopy(audit.get("coverage") or {}),
        "profile_scope_coverage": deepcopy(
            (projected.get("summary") or {}).get("profile_scope_coverage") or {}
        ),
        "diagnostics_summary": _diagnostics_summary(diagnostics, audit),
        "projected_term_registry_ref": {
            key: value
            for key, value in (projected.get("projected_term_registry") or {}).items()
            if key in {"registry_id", "registry_version", "target_ontology", "materialization"}
        },
    }


def materialize_projected_graph(
    projected: JsonDict,
    *,
    mode: str = "standard",
) -> JsonDict:
    """Create a deterministic consumer materialization from one full graph.

    full
        Existing complete graph, full audit, and full diagnostics.
    standard
        Graph and used-term registry with compact audit/diagnostics summaries.
    summary
        No graph rows; compact coverage and diagnostics only.
    forensic
        Complete graph plus explicit integrity hashes and size-oriented counts.
    """
    if mode not in MATERIALIZATION_MODES:
        raise ValueError(f"Unknown projection materialization mode: {mode}")
    if mode == "summary":
        result = projection_summary_view(projected)
        result.setdefault("metadata", {})["materialization_mode"] = "summary"
        return result

    result = deepcopy(projected)
    result.setdefault("metadata", {})["materialization_mode"] = mode
    if mode == "standard":
        audit = result.get("audit") or {}
        diagnostics = result.get("diagnostics") or {}
        result["audit"] = _compact_audit(audit)
        result["diagnostics"] = {
            "summary": _diagnostics_summary(diagnostics, audit),
            "errors": deepcopy(diagnostics.get("errors") or []),
            "warnings": deepcopy(diagnostics.get("warnings") or []),
        }
        return result

    if mode == "forensic":
        registry = result.get("projected_term_registry") or {}
        result["forensic_integrity"] = {
            "projected_object_hash": stable_hash(result.get("objects") or []),
            "projected_relationship_hash": stable_hash(result.get("relationships") or []),
            "audit_hash": stable_hash(result.get("audit") or {}),
            "diagnostics_hash": stable_hash(result.get("diagnostics") or {}),
            "projected_term_registry_hash": stable_hash(registry),
            "mapping_execution_count": len((result.get("audit") or {}).get("mapping_executions") or []),
            "registry_term_count": len(registry.get("terms") or {}),
        }
    return result


def external_audit_artifact(projected: JsonDict) -> JsonDict:
    """Materialize the full audit/diagnostics as a separable deterministic artifact."""
    metadata = projected.get("metadata") or {}
    artifact = {
        "metadata": {
            "package_type": "projection_forensic_audit",
            "projection_id": metadata.get("projection_id"),
            "profile_id": metadata.get("profile_id"),
            "profile_version": metadata.get("profile_version"),
            "context_id": metadata.get("context_id"),
            "engine_version": metadata.get("engine_version"),
        },
        "source_identity": deepcopy(projected.get("source_identity") or {}),
        "source_graph_ref": deepcopy(projected.get("source_graph_ref") or {}),
        "audit": deepcopy(projected.get("audit") or {}),
        "diagnostics": deepcopy(projected.get("diagnostics") or {}),
    }
    artifact["metadata"]["artifact_hash"] = stable_hash(artifact)
    return artifact
