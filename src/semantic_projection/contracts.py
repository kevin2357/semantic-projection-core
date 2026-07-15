from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Mapping, TypeVar, Type

JsonDict = dict[str, Any]
T = TypeVar("T", bound="DictContract")


class DictContract:
    """Small dependency-free base for extraction-ready JSON contracts."""

    def to_dict(self) -> JsonDict:
        return asdict(self)

    @classmethod
    def from_dict(cls: Type[T], value: Mapping[str, Any]) -> T:
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

@dataclass
class ProjectedTemporalState:
    state_id: str
    projected_object_id: str
    observed_at: str
    attributes: JsonDict = field(default_factory=dict)
    source_refs: list[str] = field(default_factory=list)

    def to_dict(self) -> JsonDict:
        return asdict(self)


@dataclass
class ProjectedTemporalActivation:
    activation_id: str
    activation_type: str
    activator_id: str
    target_id: str
    relationship_type: str
    start_at: str | None = None
    exact_at: str | None = None
    end_at: str | None = None
    phase: str | None = None
    pass_index: int | None = None
    applying: bool | None = None
    orb: float | None = None
    attributes: JsonDict = field(default_factory=dict)
    source_refs: list[str] = field(default_factory=list)
    mapping_rule_refs: list[str] = field(default_factory=list)
    provenance: JsonDict = field(default_factory=dict)

    def to_dict(self) -> JsonDict:
        return asdict(self)


@dataclass
class ProjectedTemporalActivationGraph:
    metadata: JsonDict
    source_identity: JsonDict
    source_graph_ref: JsonDict
    target_ontology: str
    target_graph_ref: JsonDict
    transient_objects: list[JsonDict]
    temporal_states: list[JsonDict]
    activations: list[JsonDict]
    indexes: JsonDict
    summary: JsonDict
    audit: JsonDict
    diagnostics: JsonDict

    def to_dict(self) -> JsonDict:
        return asdict(self)

