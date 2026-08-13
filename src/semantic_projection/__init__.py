"""Extraction-ready semantic projection contracts and generic engine."""

from ._version import __version__

from .contracts import (
    BoundedNatalProjectionRequest,
    MappingExecution,
    ProjectedBoundedSemanticGraph,
    ProjectedObject,
    ProjectedRelationship,
    ProjectedSemanticGraph,
    ProjectedTemporalActivation,
    ProjectedTemporalActivationGraph,
    ProjectedTemporalActivator,
    ProjectedTemporalSequenceSummary,
    ProjectedTemporalState,
    ProjectionAudit,
    ProjectionContext,
    ProjectionDiagnostics,
    ProjectionOptions,
    ProjectionProfileManifest,
    ProjectionRequest,
    TemporalProjectionOptions,
    TemporalProjectionRequest,
)
from .engine import ENGINE_VERSION, ProjectionExecutionError, project
from .ids import (
    bounded_correspondence_id,
    mapping_execution_id,
    projected_object_id,
    projected_package_id,
    projected_relationship_id,
    projected_temporal_activation_id,
    projected_temporal_activator_id,
    projected_temporal_graph_id,
    projected_temporal_sequence_id,
    projected_temporal_state_id,
    projection_request_id,
    temporal_projection_request_id,
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
from .temporal import (
    TemporalProjectionNotImplementedError,
    TemporalSourceContractError,
    adapt_foundry_temporal_source_bundle,
    canonical_temporal_fact_view,
    project_temporal,
    project_temporal_foundations,
    validate_foundry_temporal_source_bundle,
)
from .validation import (
    ProjectionValidationError,
    validate_bounded_natal_projection_request,
    validate_contract,
    validate_projected_bounded_semantic_graph,
    validate_projection_request,
    validate_temporal_projection_request,
)

__all__ = [
    "__version__", "ENGINE_VERSION", "MappingExecution", "ProjectedObject",
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

from .bounded_contract import (
    OUTPUT_CONTRACT as BOUNDED_OUTPUT_CONTRACT,
    bounded_evidence_closure,
    build_projected_bounded_contract,
    projected_bounded_correspondence_id,
)

__all__.extend([
    "BOUNDED_OUTPUT_CONTRACT",
    "ProjectedBoundedSemanticGraph",
    "bounded_correspondence_id",
    "bounded_evidence_closure",
    "build_projected_bounded_contract",
    "projected_bounded_correspondence_id",
    "validate_projected_bounded_semantic_graph",
])

from .bounded_projection import (
    BoundedProjectionExecutionError,
    project_bounded_natal_objects,
)

__all__.extend([
    "BoundedProjectionExecutionError",
    "project_bounded_natal_objects",
])


__all__.extend([
    "TemporalProjectionOptions",
    "TemporalProjectionRequest",
    "TemporalProjectionNotImplementedError",
    "TemporalSourceContractError",
    "adapt_foundry_temporal_source_bundle",
    "canonical_temporal_fact_view",
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

from .temporal_pipeline import (
    TemporalPipelineResult,
    classify_temporal_target,
    project_foundry_temporal_bundle,
)
__all__.extend([
    "TemporalPipelineResult",
    "classify_temporal_target",
    "project_foundry_temporal_bundle",
])

from .synastry import SynastryProjectionResult, prepare_synastry_source_graph, project_synastry
__all__.extend(["SynastryProjectionResult", "prepare_synastry_source_graph", "project_synastry"])

from .resources import bundled_contexts, load_bundled_context, release_compatibility, semantic_resource_manifest
__all__.extend(["bundled_contexts", "load_bundled_context", "release_compatibility", "semantic_resource_manifest"])

from .runtime_identity import projection_runtime_identity, runtime_release_manifest
__all__.extend(["projection_runtime_identity", "runtime_release_manifest"])

from .bounded import (
    BOUNDED_REQUEST_CONTRACT,
    SUPPORTED_BOUNDED_SOURCE,
    BoundedNatalSourceContractError,
    adapt_foundry_bounded_natal_dataset,
    validate_foundry_bounded_natal_dataset,
)

__all__.extend([
    "BOUNDED_REQUEST_CONTRACT",
    "SUPPORTED_BOUNDED_SOURCE",
    "BoundedNatalProjectionRequest",
    "BoundedNatalSourceContractError",
    "adapt_foundry_bounded_natal_dataset",
    "validate_bounded_natal_projection_request",
    "validate_foundry_bounded_natal_dataset",
])
