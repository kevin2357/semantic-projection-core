from __future__ import annotations

from collections.abc import Mapping
from copy import deepcopy
from typing import Any

from .contracts import (
    BoundedNatalProjectionRequest,
    ProjectionContext,
    ProjectionOptions,
)
from .ids import stable_hash
from .validation import (
    ProjectionValidationError,
    validate_bounded_natal_projection_request,
    validate_contract,
)

JsonDict = dict[str, Any]

BOUNDED_REQUEST_CONTRACT = "bounded_natal_projection_request.v1"
SUPPORTED_BOUNDED_SOURCE = {
    "package_type": "bounded_natal_dataset",
    "package_schema_version": "1.0.0",
    "graph_type": "bounded_canonical_astrology_graph",
    "graph_version": "1.7.0",
    "canonical_graph_contract": "bounded_canonical_astrology_graph.v1",
    "evidence_contract": "agf.bounded_uncertainty_evidence.v1.0.0",
    "calculation_profile": "agf.bounded_natal.calculation_profile.v1.12.0",
    "interval_proof_profile": "agf.interval_proof.v1.0.0",
}
EPISTEMIC_CLASSIFICATIONS = {
    "invariant",
    "conditional",
    "variable",
    "unavailable",
    "inconclusive",
}
FORBIDDEN_OBJECT_FIELDS = {"longitude", "pretty", "sign_degree"}
FORBIDDEN_RELATIONSHIP_FIELDS = {
    "orb",
    "distance",
    "applying_delta",
    "strength",
    "structural_strength_score",
}
EVIDENCE_REF_FIELDS = {
    "uncertainty_evidence_ref",
    "house_uncertainty_evidence_ref",
    "triplicity_uncertainty_evidence_ref",
}


class BoundedNatalSourceContractError(ValueError):
    """The supplied AGF bounded artifact is unsupported or internally unsafe."""


def _reject(message: str) -> None:
    raise BoundedNatalSourceContractError(message)


def _required_string(value: Mapping[str, Any], key: str, path: str) -> str:
    result = value.get(key)
    if not isinstance(result, str) or not result:
        _reject(f"{path}.{key} must be a non-empty string")
    return result


def _unique_ids(rows: list[JsonDict], kind: str) -> set[str]:
    values = [_required_string(row, "id", f"canonical graph {kind}") for row in rows]
    duplicates = sorted({value for value in values if values.count(value) > 1})
    if duplicates:
        _reject(f"Duplicate bounded canonical {kind} IDs: {duplicates[:5]}")
    return set(values)


def _evidence_refs(row: Mapping[str, Any]) -> list[str]:
    return [
        str(value)
        for key, value in row.items()
        if key in EVIDENCE_REF_FIELDS and isinstance(value, str) and value
    ]


def _validate_evidence_metadata(
    row: Mapping[str, Any],
    *,
    source_chart_ids: list[str],
    label: str,
) -> None:
    metadata = row.get("evidence_metadata")
    if not isinstance(metadata, Mapping):
        _reject(f"{label} is missing evidence_metadata")
    for key in (
        "record_independence_group",
        "evidence_family_group",
        "source_chart_family_group",
    ):
        _required_string(metadata, key, f"{label}.evidence_metadata")
    if metadata.get("source_chart_ids") != source_chart_ids:
        _reject(f"{label}.evidence_metadata.source_chart_ids does not match source identity")


def validate_foundry_bounded_natal_dataset(
    source_artifact: Mapping[str, Any],
) -> None:
    """Validate SPC's exact supported consumer boundary for AGF 0.8 bounded natal.

    AGF owns the complete native package schema. This validator enforces the
    released identities and the cross-section invariants SPC relies upon.
    """

    if not isinstance(source_artifact, Mapping):
        _reject("Bounded natal source artifact must be a JSON object")
    artifact = dict(source_artifact)
    try:
        validate_contract(artifact, "bounded_natal_source_v1.schema.json")
    except ProjectionValidationError as exc:
        _reject(str(exc))

    metadata = artifact["metadata"]
    graph = artifact["canonical_astrology_graph"]
    assessment = artifact["uncertainty_assessment"]
    provenance = metadata["calculation_provenance"]
    structural = artifact["structural_evidence_graph"]
    boundary = artifact["semantic_boundary"]

    expected = SUPPORTED_BOUNDED_SOURCE
    observed = {
        "package_type": metadata.get("analysis_type"),
        "package_schema_version": metadata.get("schema_version"),
        "graph_type": graph.get("graph_type"),
        "graph_version": graph.get("graph_version"),
        "canonical_graph_contract": metadata.get("canonical_graph_contract"),
        "evidence_contract": assessment.get("evidence_contract_version"),
        "calculation_profile": provenance.get("calculation_profile_version"),
        "interval_proof_profile": (assessment.get("proof_profile") or {}).get("version"),
    }
    mismatches = [
        f"{key}={observed[key]!r} (requires {value!r})"
        for key, value in expected.items()
        if observed.get(key) != value
    ]
    if mismatches:
        _reject("Unsupported bounded natal source contract: " + "; ".join(mismatches))

    source_chart_id = _required_string(metadata, "source_chart_id", "metadata")
    source_chart_ids = metadata.get("source_chart_ids")
    if source_chart_ids != [source_chart_id]:
        _reject("Bounded natal metadata.source_chart_ids must contain exactly source_chart_id")
    for path, value in (
        ("canonical_astrology_graph.source_chart_id", graph.get("source_chart_id")),
        ("canonical_astrology_graph.source_chart_ids", graph.get("source_chart_ids")),
        ("structural_evidence_graph.source_chart_id", structural.get("source_chart_id")),
        ("structural_evidence_graph.source_chart_ids", structural.get("source_chart_ids")),
    ):
        expected_value: Any = source_chart_ids if path.endswith("source_chart_ids") else source_chart_id
        if value != expected_value:
            _reject(f"{path} does not match metadata source identity")
    if boundary.get("bounded_birth_time") is not True:
        _reject("semantic_boundary.bounded_birth_time must be true")
    if boundary.get("canonical_graph_contract") != expected["canonical_graph_contract"]:
        _reject("semantic_boundary canonical graph contract does not match metadata")

    if graph.get("projection_status") != "pre_projection":
        _reject("Bounded canonical graph projection_status must be pre_projection")
    capabilities = artifact["capabilities"]
    graph_capabilities = graph.get("capabilities") or {}
    capability_mismatches = sorted(
        key
        for key, value in capabilities.items()
        if graph_capabilities.get(key) != value
    )
    if capability_mismatches:
        _reject(
            "Package capabilities disagree with canonical graph capabilities: "
            f"{capability_mismatches}"
        )
    for key in (
        "supports_exact_longitudes",
        "supports_structural_strength_scores",
        "supports_canonical_claims",
        "supports_semantic_graph_activation",
    ):
        if graph_capabilities.get(key) is not False:
            _reject(f"Bounded source capability {key} must be false")

    summary = graph.get("summary") or {}
    if summary.get("basis") != "bounded_invariant_subgraph":
        _reject("Bounded canonical graph summary basis must be bounded_invariant_subgraph")
    if summary.get("raw_counts_are_independence_weights") is not False:
        _reject("Bounded canonical raw counts must not be independence weights")
    if structural.get("basis") != "bounded_invariant_subgraph":
        _reject("Structural evidence basis must be bounded_invariant_subgraph")

    objects = list(graph.get("objects") or [])
    relationships = list(graph.get("relationships") or [])
    object_ids = _unique_ids(objects, "object")
    _unique_ids(relationships, "relationship")
    registry = assessment.get("evidence_registry") or {}
    if not isinstance(registry, Mapping):
        _reject("uncertainty_assessment.evidence_registry must be an object")

    for row in objects:
        row_id = str(row["id"])
        forbidden = sorted(FORBIDDEN_OBJECT_FIELDS & row.keys())
        if forbidden:
            _reject(f"Bounded object {row_id!r} contains forbidden precision fields: {forbidden}")
        if "structural_strength_score" in row:
            _reject(f"Bounded object {row_id!r} contains forbidden structural strength")
        _validate_evidence_metadata(
            row,
            source_chart_ids=source_chart_ids,
            label=f"bounded object {row_id!r}",
        )
        owner = row.get("owner_object_ref")
        if owner is not None and owner not in object_ids:
            _reject(f"Bounded object {row_id!r} references unknown owner {owner!r}")
        for ref in _evidence_refs(row):
            if ref not in registry:
                _reject(f"Bounded object {row_id!r} references missing evidence {ref!r}")

    for row in relationships:
        row_id = str(row["id"])
        forbidden = sorted(FORBIDDEN_RELATIONSHIP_FIELDS & row.keys())
        if forbidden:
            _reject(f"Bounded relationship {row_id!r} contains forbidden exact/scored fields: {forbidden}")
        for endpoint in ("source_id", "target_id"):
            if row.get(endpoint) not in object_ids:
                _reject(f"Bounded relationship {row_id!r} has unknown {endpoint} {row.get(endpoint)!r}")
        _validate_evidence_metadata(
            row,
            source_chart_ids=source_chart_ids,
            label=f"bounded relationship {row_id!r}",
        )
        for ref in _evidence_refs(row):
            if ref not in registry:
                _reject(f"Bounded relationship {row_id!r} references missing evidence {ref!r}")

    for key, record in registry.items():
        if not isinstance(record, Mapping):
            _reject(f"Evidence registry entry {key!r} must be an object")
        classification = record.get("classification")
        if classification is not None and classification not in EPISTEMIC_CLASSIFICATIONS:
            _reject(f"Evidence registry entry {key!r} has unknown classification {classification!r}")

    if summary.get("object_count") != len(objects):
        _reject("Bounded canonical graph object_count does not reconcile")
    if summary.get("relationship_count") != len(relationships):
        _reject("Bounded canonical graph relationship_count does not reconcile")


def adapt_foundry_bounded_natal_dataset(
    source_artifact: Mapping[str, Any],
    *,
    profile_id: str,
    profile_version: str,
    context: ProjectionContext | Mapping[str, Any],
    options: ProjectionOptions | Mapping[str, Any] | None = None,
) -> BoundedNatalProjectionRequest:
    """Validate one AGF artifact and prepare an immutable bounded request."""

    artifact = deepcopy(dict(source_artifact))
    validate_foundry_bounded_natal_dataset(artifact)
    context_dict = (
        context.to_dict()
        if isinstance(context, ProjectionContext)
        else deepcopy(dict(context))
    )
    options_dict = (
        ProjectionOptions().to_dict()
        if options is None
        else options.to_dict()
        if isinstance(options, ProjectionOptions)
        else deepcopy(dict(options))
    )
    metadata = artifact["metadata"]
    graph = artifact["canonical_astrology_graph"]
    structural = artifact["structural_evidence_graph"]
    source_artifact_hash = stable_hash(artifact, length=64)
    source_identity = {
        "source_chart_id": metadata["source_chart_id"],
        "source_chart_ids": list(metadata["source_chart_ids"]),
        "sensor_instance_id": structural["sensor_instance_id"],
        "source_artifact_sha256": source_artifact_hash,
    }
    token = stable_hash(
        {
            "request_contract": BOUNDED_REQUEST_CONTRACT,
            "profile_id": profile_id,
            "profile_version": profile_version,
            "source_identity": source_identity,
            "context": context_dict,
            "options": options_dict,
        }
    )
    request = BoundedNatalProjectionRequest(
        request_id=f"bounded_natal_projection_request:{token}",
        request_contract=BOUNDED_REQUEST_CONTRACT,
        profile_id=profile_id,
        profile_version=profile_version,
        source_artifact=artifact,
        source_identity=source_identity,
        context=context_dict,
        options=options_dict,
        upstream_contracts={
            "package_type": metadata["analysis_type"],
            "package_schema_version": metadata["schema_version"],
            "canonical_graph_contract": metadata["canonical_graph_contract"],
            "canonical_graph_version": graph["graph_version"],
            "evidence_contract": artifact["uncertainty_assessment"]["evidence_contract_version"],
            "calculation_profile": metadata["calculation_provenance"]["calculation_profile_version"],
            "interval_proof_profile": artifact["uncertainty_assessment"]["proof_profile"]["version"],
        },
        limitations=[
            "bounded_invariant_subgraph_not_exact_chart",
            "no_representative_or_midpoint_positions",
            "no_exact_longitudes_or_orbs",
            "no_structural_strength_or_canonical_claims",
            "no_temporal_activation",
        ],
        extensions={"execution_status": "validated_intake_only"},
    )
    validate_bounded_natal_projection_request(request.to_dict())
    return request
