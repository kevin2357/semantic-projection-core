from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from typing import Any, Mapping

from .contracts import ProjectionContext, TemporalProjectionOptions
from .ids import stable_hash
from .materialization import materialize_projected_temporal_graph, temporal_projection_summary_view
from .temporal import adapt_foundry_temporal_source_bundle, project_temporal
from .validation import validate_contract


@dataclass(frozen=True, slots=True)
class TemporalPipelineResult:
    """End-to-end Stage C production result.

    The request remains available for audit/debug use, while ``artifact`` is the
    selected consumer materialization and ``receipt`` is a compact routing record.
    """

    request: dict[str, Any]
    artifact: dict[str, Any]
    receipt: dict[str, Any]


def classify_temporal_target(bundle: Mapping[str, Any]) -> str:
    """Return a stable target-family label without imposing domain semantics."""
    target = bundle.get("target_identity") or {}
    candidates = (
        target.get("chart_type"),
        target.get("target_type"),
        target.get("relationship_chart_type"),
        target.get("package_type"),
    )
    for value in candidates:
        if value:
            normalized = str(value).strip().lower().replace(" ", "_")
            if "davison" in normalized:
                return "davison"
            if "composite" in normalized:
                return "composite"
            if "natal" in normalized:
                return "natal"
            return normalized
    chart_id = str(target.get("chart_id") or "").lower()
    if "davison" in chart_id:
        return "davison"
    if "composite" in chart_id:
        return "composite"
    return "natal_or_unspecified"


def project_foundry_temporal_bundle(
    bundle: Mapping[str, Any],
    *,
    profile_id: str,
    profile_version: str,
    context: Mapping[str, Any] | ProjectionContext,
    options: Mapping[str, Any] | TemporalProjectionOptions | None = None,
    output_mode: str = "standard",
    registry: Any | None = None,
) -> TemporalPipelineResult:
    """Validate, adapt, project, materialize, and issue a deterministic receipt.

    This is the supported production routing boundary for Stage C7.  It is
    deliberately a composition of the already-tested intake and projection
    contracts rather than a second execution implementation.
    """
    request = adapt_foundry_temporal_source_bundle(
        bundle,
        profile_id=profile_id,
        profile_version=profile_version,
        context=context,
        options=options,
    )
    full = project_temporal(request, registry=registry)
    artifact = materialize_projected_temporal_graph(full, mode=output_mode)
    summary = temporal_projection_summary_view(full)
    receipt_payload = {
        "package_type": "temporal_projection_route_receipt",
        "contract_version": "1.0.0",
        "source_bundle_id": ((bundle.get("metadata") or {}).get("bundle_id")),
        "source_temporal_graph_id": (((bundle.get("temporal_source_graph") or {}).get("metadata") or {}).get("graph_id")),
        "request_id": request.request_id,
        "projected_graph_id": (full.get("metadata") or {}).get("temporal_projection_id"),
        "profile_id": profile_id,
        "profile_version": profile_version,
        "context_id": (request.context or {}).get("context_id"),
        "context_version": (request.context or {}).get("context_version"),
        "target_family": classify_temporal_target(bundle),
        "output_mode": output_mode,
        "summary_semantic_hashes": deepcopy(summary.get("semantic_hashes") or {}),
        "coverage": deepcopy((summary.get("summary") or {}).get("coverage") or summary.get("coverage") or {}),
    }
    receipt_payload["route_hash"] = stable_hash(receipt_payload, length=24)
    receipt = {"metadata": receipt_payload}
    validate_contract(receipt, "temporal_projection_route_receipt_v1.schema.json")
    return TemporalPipelineResult(
        request=request.to_dict(),
        artifact=artifact,
        receipt=receipt,
    )
