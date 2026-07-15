from __future__ import annotations

from copy import deepcopy
from dataclasses import asdict, is_dataclass
from typing import Any, Mapping

from .contracts import (
    ProjectionContext,
    TemporalProjectionOptions,
    TemporalProjectionRequest,
)
from .ids import (
    temporal_projection_request_id, projection_request_id,
    projected_temporal_activator_id,
)
from .validation import (
    ProjectionValidationError,
    validate_contract,
    validate_temporal_projection_request,
)

FOUNDRY_BUNDLE_PACKAGE_TYPE = "temporal_projection_source_bundle"
SUPPORTED_FOUNDRY_BUNDLE_CONTRACT_VERSIONS = frozenset({"1.0.0"})
FOUNDRY_TEMPORAL_GRAPH_PACKAGE_TYPE = "canonical_temporal_activation_graph"
SUPPORTED_FOUNDRY_TEMPORAL_GRAPH_CONTRACT_VERSIONS = frozenset({"1.0.0"})
EXPECTED_AUTHORITATIVE_UNIT = "activation_arc"
EXPECTED_CONSUMER_STATUS = "reserved_for_semantic_projection_core_temporal_support"


class TemporalSourceContractError(ProjectionValidationError):
    """Raised when an upstream temporal handoff violates the supported contract."""


class TemporalProjectionNotImplementedError(NotImplementedError):
    """Raised when execution is requested before Stage C is complete."""


def _plain_mapping(value: Mapping[str, Any] | ProjectionContext | TemporalProjectionOptions) -> dict[str, Any]:
    if hasattr(value, "to_dict"):
        return dict(value.to_dict())  # type: ignore[union-attr]
    if is_dataclass(value):
        return asdict(value)
    return dict(value)


def _require_equal(actual: Any, expected: Any, label: str) -> None:
    if actual != expected:
        raise TemporalSourceContractError(
            f"Unsupported {label}: expected {expected!r}, received {actual!r}."
        )


def _validate_supported_contracts(bundle: Mapping[str, Any]) -> None:
    metadata = bundle.get("metadata") or {}
    _require_equal(
        metadata.get("package_type"),
        FOUNDRY_BUNDLE_PACKAGE_TYPE,
        "temporal bundle package_type",
    )
    bundle_version = metadata.get("contract_version")
    if bundle_version not in SUPPORTED_FOUNDRY_BUNDLE_CONTRACT_VERSIONS:
        raise TemporalSourceContractError(
            "Unsupported Foundry temporal bundle contract version "
            f"{bundle_version!r}; supported versions: "
            f"{sorted(SUPPORTED_FOUNDRY_BUNDLE_CONTRACT_VERSIONS)}."
        )
    _require_equal(metadata.get("projection_neutral"), True, "bundle projection_neutral")
    _require_equal(metadata.get("consumer_status"), EXPECTED_CONSUMER_STATUS, "bundle consumer_status")

    temporal = bundle.get("temporal_source_graph") or {}
    temporal_metadata = temporal.get("metadata") or {}
    _require_equal(
        temporal_metadata.get("package_type"),
        FOUNDRY_TEMPORAL_GRAPH_PACKAGE_TYPE,
        "temporal graph package_type",
    )
    graph_version = temporal_metadata.get("contract_version")
    if graph_version not in SUPPORTED_FOUNDRY_TEMPORAL_GRAPH_CONTRACT_VERSIONS:
        raise TemporalSourceContractError(
            "Unsupported Foundry canonical temporal graph contract version "
            f"{graph_version!r}; supported versions: "
            f"{sorted(SUPPORTED_FOUNDRY_TEMPORAL_GRAPH_CONTRACT_VERSIONS)}."
        )
    _require_equal(temporal_metadata.get("projection_neutral"), True, "temporal graph projection_neutral")
    _require_equal(
        temporal_metadata.get("authoritative_unit"),
        EXPECTED_AUTHORITATIVE_UNIT,
        "temporal graph authoritative_unit",
    )


def _validate_cross_field_integrity(bundle: Mapping[str, Any]) -> None:
    target_identity = bundle.get("target_identity") or {}
    temporal = bundle.get("temporal_source_graph") or {}
    temporal_target = temporal.get("target_identity") or {}
    static_graph = bundle.get("static_source_graph") or {}

    bundle_chart_id = target_identity.get("chart_id")
    temporal_chart_id = temporal_target.get("chart_id")
    static_chart_id = static_graph.get("source_chart_id")
    if not bundle_chart_id:
        raise TemporalSourceContractError("target_identity.chart_id must be non-empty.")
    if temporal_chart_id != bundle_chart_id:
        raise TemporalSourceContractError(
            "Temporal target identity mismatch: "
            f"bundle chart_id={bundle_chart_id!r}, temporal graph chart_id={temporal_chart_id!r}."
        )
    if static_chart_id and static_chart_id != bundle_chart_id:
        raise TemporalSourceContractError(
            "Static target graph identity mismatch: "
            f"bundle chart_id={bundle_chart_id!r}, static graph source_chart_id={static_chart_id!r}."
        )

    activators = temporal.get("activators") or []
    activator_ids = {row.get("id") for row in activators}
    static_object_ids = {row.get("id") for row in static_graph.get("objects") or []}
    activation_ids: set[str] = set()
    state_ids: set[str] = set()
    sequence_ids: set[str] = set()
    state_count = 0

    for activation in temporal.get("activations") or []:
        activation_id = activation.get("id")
        if activation_id in activation_ids:
            raise TemporalSourceContractError(f"Duplicate temporal activation id {activation_id!r}.")
        activation_ids.add(activation_id)
        sequence_ids.add(activation.get("sequence_id"))

        activator_ref = activation.get("activator_ref")
        if activator_ref not in activator_ids:
            raise TemporalSourceContractError(
                f"Activation {activation_id!r} references unknown activator {activator_ref!r}."
            )
        target_ref = activation.get("target_ref")
        if target_ref not in static_object_ids:
            raise TemporalSourceContractError(
                f"Activation {activation_id!r} references target {target_ref!r} "
                "that is absent from static_source_graph.objects."
            )
        if activation.get("target_chart_ref") not in (None, bundle_chart_id):
            raise TemporalSourceContractError(
                f"Activation {activation_id!r} target_chart_ref does not match bundle target."
            )

        states = activation.get("observation_states") or []
        if activation.get("observation_count") != len(states):
            raise TemporalSourceContractError(
                f"Activation {activation_id!r} observation_count does not match observation_states."
            )
        state_count += len(states)
        for state in states:
            state_id = state.get("state_id")
            if state_id in state_ids:
                raise TemporalSourceContractError(f"Duplicate temporal state id {state_id!r}.")
            state_ids.add(state_id)

    summary = temporal.get("summary") or {}
    expected_counts = {
        "activator_count": len(activator_ids),
        "activation_count": len(activation_ids),
        "observation_state_count": state_count,
        "sequence_count": len(sequence_ids),
    }
    for field, actual in expected_counts.items():
        reported = summary.get(field)
        if reported is not None and reported != actual:
            raise TemporalSourceContractError(
                f"Temporal summary {field}={reported!r} does not reconcile with rows ({actual})."
            )

    index_groups = temporal.get("indexes") or {}
    for index_name, index in index_groups.items():
        if not isinstance(index, Mapping):
            raise TemporalSourceContractError(f"Temporal index {index_name!r} must be an object.")
        for key, refs in index.items():
            if not isinstance(refs, list):
                raise TemporalSourceContractError(
                    f"Temporal index {index_name!r}[{key!r}] must contain a list of activation IDs."
                )
            missing = [ref for ref in refs if ref not in activation_ids]
            if missing:
                raise TemporalSourceContractError(
                    f"Temporal index {index_name!r}[{key!r}] contains unknown activation IDs: "
                    f"{missing[:5]}."
                )


def validate_foundry_temporal_source_bundle(bundle: Mapping[str, Any]) -> None:
    """Validate the frozen Foundry 0.4.2 temporal handoff and Core invariants."""
    plain = deepcopy(dict(bundle))
    _validate_supported_contracts(plain)
    try:
        validate_contract(plain, "temporal_projection_source_bundle_v1.schema.json")
    except ProjectionValidationError as exc:
        raise TemporalSourceContractError(str(exc)) from exc
    _validate_cross_field_integrity(plain)


def adapt_foundry_temporal_source_bundle(
    bundle: Mapping[str, Any],
    *,
    profile_id: str,
    profile_version: str,
    context: Mapping[str, Any] | ProjectionContext,
    options: Mapping[str, Any] | TemporalProjectionOptions | None = None,
) -> TemporalProjectionRequest:
    """Convert a Foundry bundle into Core's generic temporal request.

    This is a Stage C1/C2 intake operation only. It validates and preserves the
    handoff without executing projected temporal semantics.
    """
    plain_bundle = deepcopy(dict(bundle))
    validate_foundry_temporal_source_bundle(plain_bundle)

    context_dict = _plain_mapping(context)
    options_dict = _plain_mapping(options or TemporalProjectionOptions())
    temporal = plain_bundle["temporal_source_graph"]
    request_id = temporal_projection_request_id(
        profile_id=profile_id,
        profile_version=profile_version,
        source_identity=plain_bundle["source_identity"],
        target_identity=plain_bundle["target_identity"],
        temporal_graph_id=temporal["metadata"]["graph_id"],
        context=context_dict,
        options=options_dict,
    )
    request = TemporalProjectionRequest(
        request_id=request_id,
        request_contract="temporal_projection_request.v1",
        profile_id=profile_id,
        profile_version=profile_version,
        source_identity=deepcopy(plain_bundle["source_identity"]),
        target_identity=deepcopy(plain_bundle["target_identity"]),
        static_source_graph=deepcopy(plain_bundle["static_source_graph"]),
        structural_evidence=deepcopy(plain_bundle["structural_evidence"]),
        temporal_source_graph=deepcopy(temporal),
        source_registries=deepcopy(plain_bundle["source_registries"]),
        context=context_dict,
        options=options_dict,
        upstream_contracts={
            "bundle_package_type": plain_bundle["metadata"]["package_type"],
            "bundle_contract_version": plain_bundle["metadata"]["contract_version"],
            "bundle_id": plain_bundle["metadata"]["bundle_id"],
            "temporal_graph_package_type": temporal["metadata"]["package_type"],
            "temporal_graph_contract_version": temporal["metadata"]["contract_version"],
            "temporal_graph_id": temporal["metadata"]["graph_id"],
        },
        limitations=list(plain_bundle.get("limitations") or []),
        extensions={
            "adapter": "foundry_temporal_source_bundle.v1",
            "execution_status": "validated_intake_only",
        },
    )
    validate_temporal_projection_request(request.to_dict())
    return request


def _static_projection_request(request: TemporalProjectionRequest):
    from .contracts import ProjectionRequest, ProjectionOptions
    return ProjectionRequest(
        request_id=projection_request_id(
            profile_id=request.profile_id,
            profile_version=request.profile_version,
            source_identity=request.source_identity,
            context=request.context,
            options=ProjectionOptions().to_dict(),
        ),
        profile_id=request.profile_id,
        profile_version=request.profile_version,
        source_graph=deepcopy(request.static_source_graph),
        structural_evidence=deepcopy(request.structural_evidence),
        source_identity=deepcopy(request.source_identity),
        context=deepcopy(request.context),
        source_registries=deepcopy(request.source_registries),
        options=ProjectionOptions().to_dict(),
    )


def project_temporal_foundations(
    request: TemporalProjectionRequest | Mapping[str, Any],
) -> dict[str, Any]:
    """Execute Stage C3 static-target and persistent-activator projection.

    Activation arcs are deliberately not mapped here. The result is an
    inspectable foundation artifact used to prove reuse of the static profile
    and projected-term vocabulary.
    """
    from .profiles import builtin_projection_registry
    from .engine import project
    from .contracts import TemporalProjectionRequest as RequestContract

    request_obj = (
        request if isinstance(request, RequestContract)
        else RequestContract.from_dict(deepcopy(dict(request)))
    )
    validate_temporal_projection_request(request_obj.to_dict())
    registry = builtin_projection_registry()
    profile = registry.resolve(request_obj.profile_id, request_obj.profile_version)
    static_request = _static_projection_request(request_obj)
    projected_target = project(static_request, registry=registry).to_dict()

    context_id = str(request_obj.context.get("context_id"))
    projected_activators: list[dict[str, Any]] = []
    unmapped: list[str] = []
    source_activators = sorted(
        request_obj.temporal_source_graph.get("activators") or [],
        key=lambda row: str(row.get("id") or ""),
    )
    for source in source_activators:
        source_ref = str(source.get("id") or "")
        synthetic = {
            "id": source_ref,
            "object_type": "planet_or_point",
            "name": source.get("source_body") or source.get("name"),
            "source_key": source.get("source_body") or source.get("name"),
        }
        drafts = profile.project_object(deepcopy(synthetic), static_request) or []
        if not drafts:
            unmapped.append(source_ref)
            continue
        draft = drafts[0]
        operator_ref = str(draft.get("target_key") or draft.get("name") or source_ref)
        projected_activators.append({
            "id": projected_temporal_activator_id(
                profile_id=request_obj.profile_id,
                source_activator_ref=source_ref,
                projected_operator_ref=operator_ref,
                context_id=context_id,
            ),
            "source_activator_ref": source_ref,
            "source_body": source.get("source_body") or source.get("name"),
            "projected_operator_ref": operator_ref,
            "projected_object_type": "temporal_activator",
            "operators": sorted(set(draft.get("operators") or [])),
            "source_refs": [source_ref],
            "mapping_rule_refs": [str(draft.get("mapping_rule_id"))],
            "context_refs": [context_id],
            "attributes": deepcopy(draft.get("attributes") or {}),
            "provenance": {
                **deepcopy(draft.get("provenance") or {}),
                "temporal_projection_stage": "C3",
                "mapping_reuse": "profile.project_object",
            },
        })

    target_index = projected_target.get("indexes", {}).get("projected_objects_by_source_ref", {})
    return {
        "metadata": {
            "package_type": "projected_temporal_foundations",
            "contract_version": "0.1.0",
            "stage": "C3",
            "request_id": request_obj.request_id,
            "profile_id": request_obj.profile_id,
            "profile_version": request_obj.profile_version,
            "context_id": context_id,
            "execution_status": "static_target_and_activators_only",
        },
        "source_identity": deepcopy(request_obj.source_identity),
        "target_identity": deepcopy(request_obj.target_identity),
        "projected_target_graph": projected_target,
        "projected_activators": projected_activators,
        "target_resolution_index": deepcopy(target_index),
        "coverage": {
            "source_activator_count": len(source_activators),
            "mapped_activator_count": len(projected_activators),
            "unmapped_activator_count": len(unmapped),
            "unmapped_activator_refs": unmapped,
            "static_source_object_count": len(request_obj.static_source_graph.get("objects") or []),
            "projected_target_object_count": len(projected_target.get("objects") or []),
        },
        "projected_term_registry": deepcopy(projected_target.get("projected_term_registry") or {}),
        "limitations": [
            "Stage C3 maps the static target graph and persistent activators only.",
            "Projected activation arcs and observation-state compositions begin in Stage C4.",
        ],
    }


def project_temporal(*args: Any, **kwargs: Any) -> None:
    """Reserved complete temporal execution entry point."""
    raise TemporalProjectionNotImplementedError(
        "Complete temporal projection is not implemented in Stage C3. "
        "Use project_temporal_foundations() to inspect static-target and "
        "persistent-activator mapping reuse. Activation arcs begin in Stage C4."
    )
