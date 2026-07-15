from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from .contracts import ProjectedTemporalActivationGraph
from .validation import validate_projected_temporal_activation_graph


def projected_temporal_contract_skeleton(
    *,
    metadata: Mapping[str, Any],
    source_identity: Mapping[str, Any],
    target_identity: Mapping[str, Any],
    period: Mapping[str, Any],
    projected_target_graph: Mapping[str, Any],
    upstream_source_limitations: list[str] | None = None,
) -> ProjectedTemporalActivationGraph:
    """Build a schema-valid empty Stage C2 contract skeleton.

    This is contract scaffolding only; it does not execute temporal mappings.
    """
    graph = ProjectedTemporalActivationGraph(
        metadata=deepcopy(dict(metadata)),
        source_identity=deepcopy(dict(source_identity)),
        target_identity=deepcopy(dict(target_identity)),
        period=deepcopy(dict(period)),
        projected_target_graph=deepcopy(dict(projected_target_graph)),
        projected_activators=[],
        projected_activations=[],
        projected_sequences=[],
        indexes={},
        summary={
            "projected_activator_count": 0,
            "projected_activation_count": 0,
            "projected_sequence_count": 0,
            "projected_observation_state_count": 0,
        },
        projected_term_registry={},
        audit={},
        diagnostics={"errors": [], "warnings": [], "infos": []},
        provenance={},
        upstream_source_limitations=list(upstream_source_limitations or []),
        projected_artifact_limitations=[
            "Stage C2 defines and validates the projected temporal contract but does not execute mappings."
        ],
    )
    validate_projected_temporal_activation_graph(graph.to_dict())
    return graph
