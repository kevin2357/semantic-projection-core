from __future__ import annotations

from collections.abc import Mapping
from dataclasses import asdict, dataclass, field
from typing import Any, TypeVar

JsonDict = dict[str, Any]
T = TypeVar("T", bound="DictContract")


class DictContract:
    """Small dependency-free base for extraction-ready JSON contracts."""

    def to_dict(self) -> JsonDict:
        return asdict(self)

    @classmethod
    def from_dict(cls: type[T], value: Mapping[str, Any]) -> T:  # noqa: PYI019 -- Python 3.10 lacks typing.Self
        return cls(**dict(value))  # type: ignore[arg-type]


@dataclass(slots=True)
class ProjectionProfileManifest(DictContract):
    profile_id: str
    profile_version: str
    engine_contract_version: str
    source_ontology: str
    target_ontology: str
    implementation: JsonDict
    supported_source_graph_types: list[str]
    required_context_fields: list[str] = field(default_factory=list)
    optional_context_fields: list[str] = field(default_factory=list)
    mapping_rule_namespace: str = ""
    output_contract: str = "projected_semantic_graph.v1"
    deterministic: bool = True
    status: str = "experimental"
    extensions: JsonDict = field(default_factory=dict)


@dataclass(slots=True)
class ProjectionContext(DictContract):
    context_id: str
    context_version: str
    subject_scope: str
    target_domain: str
    application_context: str
    relationship_type: str | None = None
    age_band: str | None = None
    audience: str | None = None
    output_intent: str = "structured_semantic_model"
    constraints: JsonDict = field(default_factory=dict)
    parameters: JsonDict = field(default_factory=dict)
    extensions: JsonDict = field(default_factory=dict)




@dataclass(slots=True)
class ProjectionOptions(DictContract):
    """Execution/materialization controls, intentionally separate from context."""

    retain_unmapped_sources: bool = True
    include_audit: bool = True
    include_diagnostics: bool = True
    unmapped_policy: str = "diagnostic"
    compact_audit: bool = False
    extensions: JsonDict = field(default_factory=dict)

@dataclass(slots=True)
class ProjectionRequest(DictContract):
    request_id: str
    profile_id: str
    profile_version: str
    source_graph: JsonDict
    structural_evidence: JsonDict
    source_identity: JsonDict
    context: JsonDict
    source_registries: JsonDict = field(default_factory=dict)
    options: JsonDict = field(
        default_factory=lambda: ProjectionOptions().to_dict()
    )


@dataclass(slots=True)
class BoundedNatalProjectionRequest(DictContract):
    """Atomic request prepared from one validated AGF bounded natal dataset."""

    request_id: str
    request_contract: str
    profile_id: str
    profile_version: str
    source_artifact: JsonDict
    source_identity: JsonDict
    context: JsonDict
    options: JsonDict = field(
        default_factory=lambda: ProjectionOptions().to_dict()
    )
    upstream_contracts: JsonDict = field(default_factory=dict)
    limitations: list[str] = field(default_factory=list)
    extensions: JsonDict = field(default_factory=dict)


@dataclass(slots=True)
class ProjectedObject(DictContract):
    id: str
    object_type: str
    name: str
    target_ontology: str
    operators: list[str]
    source_refs: list[str]
    mapping_rule_refs: list[str]
    context_refs: list[str]
    attributes: JsonDict = field(default_factory=dict)
    structural_strength_score: float | None = None
    projection_relevance_score: float | None = None
    provenance: JsonDict = field(default_factory=dict)


@dataclass(slots=True)
class ProjectedRelationship(DictContract):
    id: str
    relationship_type: str
    source_id: str
    target_id: str
    source_relationship_refs: list[str]
    mapping_rule_refs: list[str]
    context_refs: list[str]
    operators: list[str] = field(default_factory=list)
    theme_tags: list[str] = field(default_factory=list)
    attributes: JsonDict = field(default_factory=dict)
    projection_relevance_score: float | None = None
    provenance: JsonDict = field(default_factory=dict)


@dataclass(slots=True)
class MappingExecution(DictContract):
    execution_id: str
    mapping_rule_id: str
    mapping_rule_version: str
    source_refs: list[str]
    context_refs: list[str]
    result_refs: list[str]
    status: str
    conditions_evaluated: list[JsonDict] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


@dataclass(slots=True)
class ProjectionDiagnostics(DictContract):
    errors: list[JsonDict] = field(default_factory=list)
    warnings: list[JsonDict] = field(default_factory=list)
    infos: list[JsonDict] = field(default_factory=list)
    unmapped_source_refs: list[str] = field(default_factory=list)
    fallbacks: list[JsonDict] = field(default_factory=list)


@dataclass(slots=True)
class ProjectionAudit(DictContract):
    profile_id: str
    profile_version: str
    engine_version: str
    request_hash: str
    source_graph_hash: str
    context_hash: str
    coverage: JsonDict
    mapping_executions: list[JsonDict] = field(default_factory=list)
    unmapped_source_refs: list[str] = field(default_factory=list)
    fallbacks: list[JsonDict] = field(default_factory=list)
    diagnostics_ref: str = "projection_diagnostics"


@dataclass(slots=True)
class ProjectedSemanticGraph(DictContract):
    metadata: JsonDict
    source_identity: JsonDict
    source_graph_ref: JsonDict
    target_ontology: str
    objects: list[JsonDict]
    relationships: list[JsonDict]
    indexes: JsonDict
    summary: JsonDict
    audit: JsonDict
    diagnostics: JsonDict
    projected_term_registry: JsonDict = field(default_factory=dict)


@dataclass(slots=True)
class ProjectedBoundedSemanticGraph(DictContract):
    """Separate output contract for bounded invariant projection."""

    metadata: JsonDict
    source_identity: JsonDict
    source_artifact_ref: JsonDict
    target_ontology: str
    source_capabilities: JsonDict
    source_feature_dispositions: JsonDict
    source_evidence: JsonDict
    objects: list[JsonDict]
    relationships: list[JsonDict]
    indexes: JsonDict
    summary: JsonDict
    projected_term_registry: JsonDict
    audit: JsonDict
    diagnostics: JsonDict
    provenance: JsonDict
    limitations: list[str] = field(default_factory=list)

@dataclass(slots=True)
class TemporalProjectionOptions(DictContract):
    """Execution controls for the future temporal projection pipeline.

    Stage C1 validates and transports these options but does not execute
    temporal projection.
    """

    include_observation_states: bool = True
    include_projected_state_composition: bool = True
    retain_unmapped_sources: bool = True
    include_audit: bool = True
    include_diagnostics: bool = True
    unmapped_policy: str = "diagnostic"
    extensions: JsonDict = field(default_factory=dict)


@dataclass(slots=True)
class TemporalProjectionRequest(DictContract):
    """Generic Core request adapted from an upstream temporal source bundle."""

    request_id: str
    request_contract: str
    profile_id: str
    profile_version: str
    source_identity: JsonDict
    target_identity: JsonDict
    static_source_graph: JsonDict
    structural_evidence: JsonDict
    temporal_source_graph: JsonDict
    source_registries: JsonDict
    context: JsonDict
    options: JsonDict
    upstream_contracts: JsonDict
    limitations: list[str] = field(default_factory=list)
    extensions: JsonDict = field(default_factory=dict)


@dataclass(slots=True)
class ProjectedTemporalActivator(DictContract):
    id: str
    source_activator_ref: str
    source_body: str | None
    projected_operator_ref: str
    projected_object_type: str = "temporal_activator"
    operators: list[str] = field(default_factory=list)
    source_refs: list[str] = field(default_factory=list)
    mapping_rule_refs: list[str] = field(default_factory=list)
    context_refs: list[str] = field(default_factory=list)
    attributes: JsonDict = field(default_factory=dict)
    provenance: JsonDict = field(default_factory=dict)


@dataclass(slots=True)
class ProjectedTemporalState(DictContract):
    id: str
    source_state_ref: str
    projected_activation_ref: str
    observed_at: str
    phase: str
    orb: float | None
    distance: float | None
    strength_label: str | None
    activator_state: JsonDict
    projected_state_composition: JsonDict = field(default_factory=dict)
    source_refs: list[str] = field(default_factory=list)
    provenance: JsonDict = field(default_factory=dict)


@dataclass(slots=True)
class ProjectedTemporalActivation(DictContract):
    id: str
    source_activation_ref: str
    source_sequence_ref: str
    projected_sequence_id: str
    pass_index: int
    projected_activator_ref: str
    projected_target_ref: str
    projected_relationship_type: str
    temporal_role: str
    directionality: str
    temporal_facts: JsonDict
    projected_relationship_term_ref: str | None = None
    projected_activation_domain_ref: str | None = None
    projected_activator_mode_refs: list[str] = field(default_factory=list)
    source_refs: list[str] = field(default_factory=list)
    mapping_rule_refs: list[str] = field(default_factory=list)
    context_refs: list[str] = field(default_factory=list)
    provenance: JsonDict = field(default_factory=dict)


@dataclass(slots=True)
class ProjectedTemporalSequenceSummary(DictContract):
    id: str
    source_sequence_ref: str
    activation_refs: list[str]
    pass_count: int
    source_refs: list[str] = field(default_factory=list)
    provenance: JsonDict = field(default_factory=dict)


@dataclass(slots=True)
class ProjectedTemporalActivationGraph(DictContract):
    metadata: JsonDict
    source_identity: JsonDict
    target_identity: JsonDict
    period: JsonDict
    projected_target_graph: JsonDict
    projected_activators: list[JsonDict]
    projected_activations: list[JsonDict]
    projected_sequences: list[JsonDict]
    indexes: JsonDict
    summary: JsonDict
    projected_term_registry: JsonDict
    audit: JsonDict
    diagnostics: JsonDict
    provenance: JsonDict
    upstream_source_limitations: list[str] = field(default_factory=list)
    projected_artifact_limitations: list[str] = field(default_factory=list)
