"""Extraction-ready semantic projection contracts and generic engine."""

from .contracts import (
    MappingExecution,
    ProjectedObject,
    ProjectedRelationship,
    ProjectedSemanticGraph,
    ProjectedTemporalActivation,
    ProjectedTemporalActivationGraph,
    ProjectedTemporalState,
    ProjectionAudit,
    ProjectionContext,
    ProjectionDiagnostics,
    ProjectionProfileManifest,
    ProjectionOptions,
    ProjectionRequest,
)
from .engine import ENGINE_VERSION, ProjectionExecutionError, project
from .ids import (
    mapping_execution_id,
    projected_object_id,
    projected_package_id,
    projected_relationship_id,
    projection_request_id,
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
from .validation import ProjectionValidationError, validate_contract, validate_projection_request

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
    MATERIALIZATION_MODES,
    external_audit_artifact,
    materialize_projected_graph,
    projection_summary_view,
)


def project_with_builtin_profiles(request):
    """Project a generic request using the bundled reference profiles."""
    from .profiles import builtin_projection_registry
    return project(request, registry=builtin_projection_registry())

__all__.extend(["project_with_builtin_profiles"])
