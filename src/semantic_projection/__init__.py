"""Extraction-ready semantic projection contracts and generic engine."""

from .contracts import (
    MappingExecution,
    ProjectedObject,
    ProjectedRelationship,
    ProjectedSemanticGraph,
    ProjectedTemporalActivator,
    ProjectedTemporalActivation,
    ProjectedTemporalActivationGraph,
    ProjectedTemporalSequenceSummary,
    ProjectedTemporalState,
    ProjectionAudit,
    ProjectionContext,
    ProjectionDiagnostics,
    ProjectionProfileManifest,
    ProjectionOptions,
    ProjectionRequest,
    TemporalProjectionOptions,
    TemporalProjectionRequest,
)
from .engine import ENGINE_VERSION, ProjectionExecutionError, project
from .ids import (
    mapping_execution_id,
    projected_object_id,
    projected_package_id,
    projected_relationship_id,
    projection_request_id,
    temporal_projection_request_id,
    projected_temporal_graph_id,
    projected_temporal_activator_id,
    projected_temporal_sequence_id,
    projected_temporal_activation_id,
    projected_temporal_state_id,
)
from .profile import ProjectionProfile
from .registry import ProjectionProfileRegistry, ProjectionProfileRegistryError
from .rendering import (
    LocalNarrative,
    ProjectedTermResolutionError,
    ProjectedTermResolver,
    RenderedSentence,
    render_local_narrative,
    render_object_sentence,
    render_relationship_sentence,
)
from .validation import (
    ProjectionValidationError,
    validate_contract,
    validate_projection_request,
    validate_temporal_projection_request,
)
from .temporal import (
    TemporalProjectionNotImplementedError,
    TemporalSourceContractError,
    adapt_foundry_temporal_source_bundle,
    project_temporal,
    project_temporal_foundations,
    validate_foundry_temporal_source_bundle,
)

__all__ = [
    "ENGINE_VERSION", "MappingExecution", "ProjectedObject",
    "ProjectedRelationship", "ProjectedSemanticGraph",
    "ProjectedTemporalActivation", "ProjectedTemporalActivationGraph",
    "ProjectedTemporalState", "ProjectionAudit",
    "ProjectionContext", "ProjectionDiagnostics", "ProjectionExecutionError",
    "ProjectionOptions", "ProjectionProfile", "ProjectionProfileManifest", "ProjectionProfileRegistry",
    "ProjectionProfileRegistryError", "ProjectionRequest",
    "ProjectionValidationError", "mapping_execution_id", "project",
    "projected_object_id", "projected_package_id",
    "projected_relationship_id", "projection_request_id", "validate_contract",
    "validate_projection_request", "LocalNarrative",
    "ProjectedTermResolutionError", "ProjectedTermResolver",
    "RenderedSentence", "render_local_narrative",
    "render_object_sentence", "render_relationship_sentence",
]

from .materialization import (
    materialize_projected_temporal_graph,
    temporal_projection_summary_view,
    MATERIALIZATION_MODES,
    external_audit_artifact,
    materialize_projected_graph,
    projection_summary_view,
)


def project_with_builtin_profiles(request):
    """Project a generic request using the bundled reference profiles."""
    from .profiles import builtin_projection_registry
    return project(request, registry=builtin_projection_registry())

__all__.extend([
    "project_with_builtin_profiles",
    "MATERIALIZATION_MODES",
    "external_audit_artifact",
    "materialize_projected_graph",
    "projection_summary_view",
    "materialize_projected_temporal_graph",
    "temporal_projection_summary_view",
])


__all__.extend([
    "TemporalProjectionOptions",
    "TemporalProjectionRequest",
    "TemporalProjectionNotImplementedError",
    "TemporalSourceContractError",
    "adapt_foundry_temporal_source_bundle",
    "project_temporal",
    "temporal_projection_request_id",
    "validate_foundry_temporal_source_bundle",
    "validate_temporal_projection_request",
])


from .logging_config import configure_logging, log_event
from .temporal_contract import projected_temporal_contract_skeleton
from .validation import validate_projected_temporal_activation_graph


__all__.extend([
    "ProjectedTemporalActivator",
    "ProjectedTemporalSequenceSummary",
    "configure_logging",
    "log_event",
    "projected_temporal_contract_skeleton",
    "validate_projected_temporal_activation_graph",
    "projected_temporal_graph_id",
    "projected_temporal_activator_id",
    "projected_temporal_sequence_id",
    "projected_temporal_activation_id",
    "projected_temporal_state_id",
])

from .artifact_identity import ArtifactIdentity, identify_artifact
__all__.extend(["ArtifactIdentity", "identify_artifact", "project_temporal_foundations"])
