from __future__ import annotations

import json
from importlib.resources import files
from typing import Any

from jsonschema import Draft202012Validator
from referencing import Registry, Resource

SCHEMA_PACKAGE = "semantic_projection.schemas"
SUPPORTED_SOURCE_GRAPH_VERSIONS = {"1.3.0"}
SUPPORTED_TEMPORAL_REQUEST_CONTRACTS = {"temporal_projection_request.v1"}
SUPPORTED_BOUNDED_NATAL_REQUEST_CONTRACTS = {
    "bounded_natal_projection_request.v1"
}


class ProjectionValidationError(ValueError):
    pass


def load_schema(schema_name: str) -> dict[str, Any]:
    resource = files(SCHEMA_PACKAGE).joinpath(schema_name)
    return json.loads(resource.read_text(encoding="utf-8"))


def validate_contract(value: dict[str, Any], schema_name: str) -> None:
    schema = load_schema(schema_name)
    registry = Registry()
    schema_root = files(SCHEMA_PACKAGE)
    for resource in schema_root.iterdir():
        if resource.name.endswith(".schema.json"):
            content = json.loads(resource.read_text(encoding="utf-8"))
            registry = registry.with_resource(resource.name, Resource.from_contents(content))
    validator = Draft202012Validator(schema, registry=registry)
    errors = sorted(validator.iter_errors(value), key=lambda error: list(error.path))
    if errors:
        first = errors[0]
        path = ".".join(str(part) for part in first.path) or "<root>"
        raise ProjectionValidationError(f"{schema_name} validation failed at {path}: {first.message}")


def validate_projection_request(request: dict[str, Any]) -> None:
    validate_contract(request, "projection_request_v1.schema.json")
    graph = request.get("source_graph") or {}
    temporal_graph_types = {
        "transit_dataset",
        "transit_range_dataset",
        "transit_period_dataset",
    }
    if graph.get("graph_type") == "bounded_canonical_astrology_graph":
        raise ProjectionValidationError(
            "Bounded natal source packages require "
            "bounded_natal_projection_request.v1; they cannot be projected "
            "through the exact static semantic graph route."
        )
    if str(graph.get("graph_type") or "").lower() in temporal_graph_types:
        raise ProjectionValidationError(
            "Temporal source packages require temporal_projection_request.v1; they cannot be projected as a static semantic graph."
        )
    graph_version = graph.get("graph_version")
    if graph_version not in SUPPORTED_SOURCE_GRAPH_VERSIONS:
        raise ProjectionValidationError(
            f"Unsupported canonical source graph version {graph_version!r}; supported versions: {sorted(SUPPORTED_SOURCE_GRAPH_VERSIONS)}"
        )
    context = request.get("context") or {}
    if context.get("target_domain") and request.get("profile_id", "").split(".")[0] == "":
        raise ProjectionValidationError("profile_id must be non-empty")


def validate_bounded_natal_projection_request(request: dict[str, Any]) -> None:
    """Validate a prepared bounded request without executing projection."""

    validate_contract(request, "bounded_natal_projection_request_v1.schema.json")
    contract = request.get("request_contract")
    if contract not in SUPPORTED_BOUNDED_NATAL_REQUEST_CONTRACTS:
        raise ProjectionValidationError(
            f"Unsupported bounded natal request contract {contract!r}; "
            "supported contracts: "
            f"{sorted(SUPPORTED_BOUNDED_NATAL_REQUEST_CONTRACTS)}"
        )


def validate_projected_graph_ids(graph: dict[str, Any]) -> None:
    for field in ("objects", "relationships"):
        ids = [row.get("id") for row in graph.get(field) or []]
        duplicates = sorted({value for value in ids if value is not None and ids.count(value) > 1})
        if duplicates:
            raise ProjectionValidationError(f"Duplicate {field} IDs: {duplicates[:5]}")


def validate_projected_bounded_semantic_graph(graph: dict[str, Any]) -> None:
    """Validate bounded output shape, references, and epistemic closure."""

    validate_contract(graph, "projected_bounded_semantic_graph_v1.schema.json")
    validate_projected_graph_ids(graph)
    object_ids = {row["id"] for row in graph.get("objects") or []}
    correspondence_ids: set[str] = set()
    evidence = (graph.get("source_evidence") or {}).get("records") or {}
    for kind in ("objects", "relationships"):
        for row in graph.get(kind) or []:
            correspondence_id = row["correspondence_id"]
            if correspondence_id in correspondence_ids:
                raise ProjectionValidationError(
                    f"Duplicate bounded correspondence ID {correspondence_id!r}"
                )
            correspondence_ids.add(correspondence_id)
            missing = [
                ref
                for ref in row["epistemic_basis"]["evidence_refs"]
                if ref not in evidence
            ]
            if missing:
                raise ProjectionValidationError(
                    f"Projected bounded {kind[:-1]} {row['id']!r} references "
                    f"missing source evidence: {missing[:5]}"
                )
    for row in graph.get("relationships") or []:
        for endpoint in ("source_id", "target_id"):
            if row[endpoint] not in object_ids:
                raise ProjectionValidationError(
                    f"Projected bounded relationship {row['id']!r} references "
                    f"unknown {endpoint} {row[endpoint]!r}"
                )


def validate_temporal_projection_request(request: dict[str, Any]) -> None:
    """Validate Core's generic temporal request without executing projection."""
    validate_contract(request, "temporal_projection_request_v1.schema.json")
    if request.get("request_contract") not in SUPPORTED_TEMPORAL_REQUEST_CONTRACTS:
        raise ProjectionValidationError(
            f"Unsupported temporal request contract {request.get('request_contract')!r}; "
            f"supported contracts: {sorted(SUPPORTED_TEMPORAL_REQUEST_CONTRACTS)}"
        )
    graph = request.get("static_source_graph") or {}
    graph_version = graph.get("graph_version")
    if graph_version not in SUPPORTED_SOURCE_GRAPH_VERSIONS:
        raise ProjectionValidationError(
            f"Unsupported static canonical source graph version {graph_version!r}; "
            f"supported versions: {sorted(SUPPORTED_SOURCE_GRAPH_VERSIONS)}"
        )
    context = request.get("context") or {}
    if not context.get("context_id"):
        raise ProjectionValidationError("Temporal projection context_id must be non-empty.")
    if not request.get("profile_id"):
        raise ProjectionValidationError("Temporal projection profile_id must be non-empty.")


def validate_projected_temporal_activation_graph(graph: dict[str, Any]) -> None:
    """Validate the Stage C2 projected temporal output contract and references."""
    validate_contract(graph, "projected_temporal_activation_graph_v1.schema.json")

    activator_ids = [row.get("id") for row in graph.get("projected_activators") or []]
    activation_ids = [row.get("id") for row in graph.get("projected_activations") or []]
    sequence_ids = [row.get("id") for row in graph.get("projected_sequences") or []]
    for label, ids in (
        ("projected activator", activator_ids),
        ("projected activation", activation_ids),
        ("projected sequence", sequence_ids),
    ):
        duplicates = sorted({value for value in ids if value and ids.count(value) > 1})
        if duplicates:
            raise ProjectionValidationError(f"Duplicate {label} IDs: {duplicates[:5]}")

    target_ids = {row.get("id") for row in (graph.get("projected_target_graph") or {}).get("objects") or []}
    activator_id_set = set(activator_ids)
    activation_id_set = set(activation_ids)
    sequence_id_set = set(sequence_ids)
    state_ids: set[str] = set()

    for activation in graph.get("projected_activations") or []:
        if activation.get("projected_activator_ref") not in activator_id_set:
            raise ProjectionValidationError(f"Projected activation {activation.get('id')!r} references an unknown activator.")
        if activation.get("projected_target_ref") not in target_ids:
            raise ProjectionValidationError(f"Projected activation {activation.get('id')!r} references an unknown target.")
        if activation.get("projected_sequence_id") not in sequence_id_set:
            raise ProjectionValidationError(f"Projected activation {activation.get('id')!r} references an unknown sequence.")
        facts = activation.get("temporal_facts") or {}
        states = facts.get("observation_states") or []
        if facts.get("observation_count") != len(states):
            raise ProjectionValidationError(f"Projected activation {activation.get('id')!r} observation_count does not reconcile.")
        for state in states:
            sid = state.get("id")
            if sid in state_ids:
                raise ProjectionValidationError(f"Duplicate projected temporal state ID {sid!r}.")
            state_ids.add(sid)
            if state.get("projected_activation_ref") != activation.get("id"):
                raise ProjectionValidationError(f"Projected state {sid!r} does not reference its owning activation.")

    for sequence in graph.get("projected_sequences") or []:
        missing = [ref for ref in sequence.get("activation_refs") or [] if ref not in activation_id_set]
        if missing:
            raise ProjectionValidationError(f"Projected sequence {sequence.get('id')!r} contains unknown activations: {missing[:5]}")
        if sequence.get("pass_count") != len(sequence.get("activation_refs") or []):
            raise ProjectionValidationError(f"Projected sequence {sequence.get('id')!r} pass_count does not reconcile.")
