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
    mapping_execution_id,
    temporal_projection_request_id,
    projection_request_id,
    projected_temporal_graph_id,
    projected_temporal_activator_id,
    projected_temporal_sequence_id,
    projected_temporal_activation_id,
    projected_temporal_state_id,
)
from .validation import (
    ProjectionValidationError,
    validate_contract,
    validate_temporal_projection_request,
    validate_projected_temporal_activation_graph,
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


def _normalized_body(value: Any) -> str:
    return str(value or "").strip().replace("_", " ").lower()


def _activator_selection_status(profile: Any, source: Mapping[str, Any]) -> str:
    """Mirror static source-selection policy for persistent temporal activators."""
    body = _normalized_body(source.get("source_body") or source.get("name"))
    scope_exclusions = {
        _normalized_body(value)
        for value in (getattr(profile, "temporal_activator_scope_exclusions", set()) or set())
    }
    if body in scope_exclusions:
        return "excluded_by_profile_scope"
    policy = getattr(profile, "source_selection_policy", {}) or {}
    if policy.get("node_variant") == "true" and body == "mean node":
        return "excluded_by_source_selection_policy"
    if policy.get("node_variant") == "mean" and body == "true node":
        return "excluded_by_source_selection_policy"
    if policy.get("fortune_variant") == "part_of_fortune" and body == "fortune":
        return "excluded_by_source_selection_policy"
    return "eligible"


def _project_static_target_and_activators(
    request_obj: TemporalProjectionRequest,
) -> tuple[
    dict[str, Any],
    list[dict[str, Any]],
    dict[str, dict[str, Any]],
    dict[str, Any],
]:
    """Reuse the static engine and profile object mappings for Stage C3/C4."""
    from .profiles import builtin_projection_registry
    from .engine import project

    registry = builtin_projection_registry()
    profile = registry.resolve(request_obj.profile_id, request_obj.profile_version)
    static_request = _static_projection_request(request_obj)
    projected_target = project(static_request, registry=registry).to_dict()
    context_id = str(request_obj.context.get("context_id"))

    projected_activators: list[dict[str, Any]] = []
    activator_drafts: dict[str, dict[str, Any]] = {}
    excluded: list[dict[str, str]] = []
    unmapped: list[str] = []
    source_activators = sorted(
        request_obj.temporal_source_graph.get("activators") or [],
        key=lambda row: str(row.get("id") or ""),
    )

    for source in source_activators:
        source_ref = str(source.get("id") or "")
        selection_status = _activator_selection_status(profile, source)
        if selection_status != "eligible":
            excluded.append({"source_activator_ref": source_ref, "reason": selection_status})
            continue

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

        draft = deepcopy(drafts[0])
        operator_ref = str(draft.get("target_key") or draft.get("name") or source_ref)
        projected_id = projected_temporal_activator_id(
            profile_id=request_obj.profile_id,
            source_activator_ref=source_ref,
            projected_operator_ref=operator_ref,
            context_id=context_id,
        )
        activator_drafts[source_ref] = {
            **draft,
            "id": projected_id,
            "source_refs": [source_ref],
        }
        projected_activators.append({
            "id": projected_id,
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
                "temporal_projection_stage": "C4",
                "mapping_reuse": "profile.project_object",
                "source_selection_status": selection_status,
            },
        })

    profile_scope_excluded = [
        row for row in excluded if row.get("reason") == "excluded_by_profile_scope"
    ]
    source_policy_excluded = [
        row for row in excluded if row.get("reason") == "excluded_by_source_selection_policy"
    ]
    coverage = {
        "source_activator_count": len(source_activators),
        "eligible_activator_count": len(source_activators) - len(excluded),
        "mapped_eligible_activator_count": len(projected_activators),
        "mapped_activator_count": len(projected_activators),
        "unmapped_activator_count": len(unmapped),
        "unmapped_activator_refs": unmapped,
        "policy_excluded_activator_count": len(excluded),
        "policy_excluded_activators": excluded,
        "profile_scope_excluded_activator_count": len(profile_scope_excluded),
        "profile_scope_excluded_activators": profile_scope_excluded,
        "source_selection_policy_excluded_activator_count": len(source_policy_excluded),
        "source_selection_policy_excluded_activators": source_policy_excluded,
        "eligible_but_unmapped_activator_count": len(unmapped),
        "eligible_but_unmapped_activator_refs": unmapped,
        "static_source_object_count": len(request_obj.static_source_graph.get("objects") or []),
        "projected_target_object_count": len(projected_target.get("objects") or []),
    }
    return projected_target, projected_activators, activator_drafts, coverage


def project_temporal_foundations(
    request: TemporalProjectionRequest | Mapping[str, Any],
) -> dict[str, Any]:
    """Execute Stage C3-compatible static-target and persistent-activator projection."""
    from .contracts import TemporalProjectionRequest as RequestContract

    request_obj = (
        request if isinstance(request, RequestContract)
        else RequestContract.from_dict(deepcopy(dict(request)))
    )
    validate_temporal_projection_request(request_obj.to_dict())
    projected_target, projected_activators, _, coverage = (
        _project_static_target_and_activators(request_obj)
    )
    context_id = str(request_obj.context.get("context_id"))
    target_index = projected_target.get("indexes", {}).get(
        "projected_objects_by_source_ref", {}
    )
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
        "coverage": coverage,
        "projected_term_registry": deepcopy(
            projected_target.get("projected_term_registry") or {}
        ),
        "limitations": [
            "Stage C3 maps the static target graph and persistent activators only.",
            "Use project_temporal() for the Stage C4 experimental full graph.",
        ],
    }


def _project_state_composition(
    *,
    profile: Any,
    static_request: Any,
    source_activator: Mapping[str, Any],
    activation: Mapping[str, Any],
    state: Mapping[str, Any],
) -> dict[str, Any]:
    activator_state = state.get("activator_state") or {}
    sign = activator_state.get("sign")
    domain_house = activation.get("transit_house_in_target_chart")
    if sign is None and domain_house is None:
        return {
            "mode_ref": None,
            "domain_ref": None,
            "mode_availability": "source_sign_not_supplied",
            "domain_availability": "source_house_not_supplied",
            "availability": "source_position_not_supplied",
            "mapping_reuse": "profile.project_object",
        }

    synthetic = {
        "id": source_activator.get("id"),
        "object_type": "planet_or_point",
        "name": source_activator.get("source_body") or source_activator.get("name"),
        "source_key": source_activator.get("source_body") or source_activator.get("name"),
        "sign": sign,
        "house": domain_house,
    }
    drafts = profile.project_object(deepcopy(synthetic), static_request) or []
    attrs = (drafts[0].get("attributes") or {}) if drafts else {}
    mode = attrs.get("projected_mode")
    domain = attrs.get("projected_domain")
    return {
        "mode_ref": mode,
        "domain_ref": domain,
        "mode_availability": (
            "projected" if mode is not None
            else ("source_sign_not_supplied" if sign is None else "profile_mapping_unavailable")
        ),
        "domain_availability": (
            "projected" if domain is not None
            else ("source_house_not_supplied" if domain_house is None else "profile_mapping_unavailable")
        ),
        "availability": (
            "fully_projected" if mode is not None and domain is not None
            else "partially_projected" if mode is not None or domain is not None
            else "source_position_present_but_profile_mapping_unavailable"
        ),
        "mapping_reuse": "profile.project_object",
    }



def _classify_temporal_target_resolution(
    *,
    source_target_ref: str,
    static_source_ids: set[str],
    target_resolution: Mapping[str, Any],
    profile: Any,
    static_source_by_id: Mapping[str, Mapping[str, Any]],
) -> str:
    if source_target_ref not in static_source_ids:
        return "target_missing_from_static_source_graph"
    if target_resolution.get(source_target_ref):
        return "mapped"
    source = static_source_by_id.get(source_target_ref) or {}
    name = _normalized_body(source.get("name") or source.get("source_key"))
    policy = getattr(profile, "source_selection_policy", {}) or {}
    if policy.get("node_variant") == "true" and name == "mean node":
        return "target_excluded_by_source_selection_policy"
    if policy.get("node_variant") == "mean" and name == "true node":
        return "target_excluded_by_source_selection_policy"
    if policy.get("fortune_variant") == "part_of_fortune" and name == "fortune":
        return "target_excluded_by_source_selection_policy"
    explicit_scope_exclusions = {
        _normalized_body(value)
        for value in (getattr(profile, "temporal_target_scope_exclusions", set()) or set())
    }
    if name in explicit_scope_exclusions:
        return "target_excluded_by_profile_scope"
    object_type = str(source.get("object_type") or "")
    if any(token in source_target_ref for token in ("harmonic:", "antiscia_point:", "contra_antiscia_point:")):
        return "target_excluded_by_profile_scope"
    if object_type and object_type not in {"planet_or_point", "angle", "lot"}:
        return "target_excluded_by_profile_scope"
    return "target_eligible_but_unmapped"


def _temporal_diagnostic_summary(diagnostics: Mapping[str, Any]) -> dict[str, Any]:
    counts: dict[str, int] = {}
    for level in ("errors", "warnings", "infos"):
        for row in diagnostics.get(level) or []:
            code = str(row.get("code") or "unknown")
            counts[code] = counts.get(code, 0) + 1
    return {
        "error_count": len(diagnostics.get("errors") or []),
        "warning_count": len(diagnostics.get("warnings") or []),
        "info_count": len(diagnostics.get("infos") or []),
        "counts_by_code": dict(sorted(counts.items())),
    }


def canonical_temporal_fact_view(temporal_facts: Mapping[str, Any]) -> dict[str, Any]:
    """Return the profile-independent Foundry fact layer from one projected envelope."""
    facts = deepcopy(dict(temporal_facts))
    states = []
    for state in facts.get("observation_states") or []:
        states.append({
            "source_state_ref": state.get("source_state_ref"),
            "observed_at": state.get("observed_at"),
            "phase": state.get("phase"),
            "orb": state.get("orb"),
            "distance": state.get("distance"),
            "strength_label": state.get("strength_label"),
            "activator_state": deepcopy(state.get("activator_state") or {}),
        })
    facts["observation_states"] = states
    return facts


def _annotate_upstream_limitations(limitations: list[str]) -> list[dict[str, Any]]:
    """Preserve upstream text while marking statements superseded by this artifact."""
    rows: list[dict[str, Any]] = []
    for text in limitations:
        normalized = str(text)
        superseded = "does not yet execute this bundle" in normalized.lower()
        row: dict[str, Any] = {
            "text": normalized,
            "source": "temporal_projection_source_bundle.v1",
            "status": "superseded_for_this_artifact" if superseded else "active_source_limitation",
        }
        if superseded:
            row["superseded_by"] = "projected_temporal_activation_graph.v1"
        rows.append(row)
    return rows


def project_temporal(
    request: TemporalProjectionRequest | Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Execute Stage C4 directional activation-arc projection.

    One canonical activation arc produces at most one projected temporal arc.
    Foundry timing facts are preserved without interpretive reinterpretation.
    Stage C6 proves profile/context variation while preserving canonical temporal facts.
    """
    from .contracts import TemporalProjectionRequest as RequestContract
    from .profiles import builtin_projection_registry
    from .engine import ENGINE_VERSION

    if request is None:
        raise TemporalProjectionNotImplementedError(
            "Stage C3 did not implement complete temporal projection. "
            "Stage C4 now requires a temporal_projection_request.v1 argument."
        )

    request_obj = (
        request if isinstance(request, RequestContract)
        else RequestContract.from_dict(deepcopy(dict(request)))
    )
    validate_temporal_projection_request(request_obj.to_dict())

    registry = builtin_projection_registry()
    profile = registry.resolve(request_obj.profile_id, request_obj.profile_version)
    static_request = _static_projection_request(request_obj)
    (
        projected_target,
        projected_activators,
        activator_drafts,
        activator_coverage,
    ) = _project_static_target_and_activators(request_obj)

    context_id = str(request_obj.context.get("context_id"))
    context_version = str(request_obj.context.get("context_version"))
    target_by_id = {
        str(row.get("id")): row for row in projected_target.get("objects") or []
    }
    target_resolution = projected_target.get("indexes", {}).get(
        "projected_objects_by_source_ref", {}
    )
    static_source_by_id = {
        str(row.get("id")): row for row in request_obj.static_source_graph.get("objects") or []
    }
    static_source_ids = set(static_source_by_id)
    source_activators = {
        str(row.get("id")): row
        for row in request_obj.temporal_source_graph.get("activators") or []
    }
    activator_by_source = {
        str(row.get("source_activator_ref")): row for row in projected_activators
    }

    projected_activations: list[dict[str, Any]] = []
    mapping_executions: list[dict[str, Any]] = []
    diagnostics: dict[str, list[dict[str, Any]]] = {
        "errors": [],
        "warnings": [],
        "infos": [],
    }
    arc_status_counts = {
        "source_activation_count": 0,
        "eligible_activation_count": 0,
        "projected_activation_count": 0,
        "activator_policy_excluded_count": 0,
        "activator_profile_scope_excluded_count": 0,
        "activator_source_selection_policy_excluded_count": 0,
        "missing_projected_activator_count": 0,
        "target_policy_excluded_or_unmapped_count": 0,
        "target_excluded_by_profile_scope_count": 0,
        "target_excluded_by_source_selection_policy_count": 0,
        "target_eligible_but_unmapped_count": 0,
        "target_missing_from_static_source_graph_count": 0,
        "unsupported_relationship_count": 0,
        "failed_activation_count": 0,
    }
    sequence_members: dict[str, list[dict[str, Any]]] = {}

    source_activations = sorted(
        request_obj.temporal_source_graph.get("activations") or [],
        key=lambda row: str(row.get("id") or ""),
    )
    arc_status_counts["source_activation_count"] = len(source_activations)

    for source_activation in source_activations:
        source_activation_ref = str(source_activation.get("id") or "")
        source_activator_ref = str(source_activation.get("activator_ref") or "")
        source_target_ref = str(source_activation.get("target_ref") or "")
        source_sequence_ref = str(source_activation.get("sequence_id") or "")
        source_activator = source_activators.get(source_activator_ref) or {}

        activator_status = _activator_selection_status(profile, source_activator)
        if activator_status != "eligible":
            arc_status_counts["activator_policy_excluded_count"] += 1
            if activator_status == "excluded_by_profile_scope":
                arc_status_counts["activator_profile_scope_excluded_count"] += 1
            else:
                arc_status_counts["activator_source_selection_policy_excluded_count"] += 1
            diagnostics["infos"].append({
                "code": f"temporal.activation.activator_{activator_status}",
                "source_activation_ref": source_activation_ref,
                "source_activator_ref": source_activator_ref,
                "resolution_status": activator_status,
            })
            continue

        projected_activator = activator_by_source.get(source_activator_ref)
        activator_draft = activator_drafts.get(source_activator_ref)
        if projected_activator is None or activator_draft is None:
            arc_status_counts["missing_projected_activator_count"] += 1
            diagnostics["warnings"].append({
                "code": "temporal.activation.activator_unmapped",
                "source_activation_ref": source_activation_ref,
                "source_activator_ref": source_activator_ref,
            })
            continue

        target_refs = list(target_resolution.get(source_target_ref) or [])
        if not target_refs:
            resolution_status = _classify_temporal_target_resolution(
                source_target_ref=source_target_ref,
                static_source_ids=static_source_ids,
                target_resolution=target_resolution,
                profile=profile,
                static_source_by_id=static_source_by_id,
            )
            arc_status_counts["target_policy_excluded_or_unmapped_count"] += 1
            arc_status_counts[f"{resolution_status}_count"] += 1
            diagnostics["infos"].append({
                "code": f"temporal.activation.{resolution_status}",
                "source_activation_ref": source_activation_ref,
                "source_target_ref": source_target_ref,
                "resolution_status": resolution_status,
            })
            continue
        projected_target_ref = str(target_refs[0])
        projected_target_object = target_by_id.get(projected_target_ref)
        if projected_target_object is None:
            arc_status_counts["failed_activation_count"] += 1
            diagnostics["errors"].append({
                "code": "temporal.activation.target_index_inconsistent",
                "source_activation_ref": source_activation_ref,
                "projected_target_ref": projected_target_ref,
            })
            continue

        arc_status_counts["eligible_activation_count"] += 1
        aspect = source_activation.get("aspect")
        closest_orb = (source_activation.get("exactness") or {}).get("closest_orb")
        synthetic_relationship = {
            "id": source_activation_ref,
            "relationship_type": "ASPECT",
            "source_id": source_activator_ref,
            "target_id": source_target_ref,
            "aspect": aspect,
            "orb": closest_orb,
            "source_refs": list(source_activation.get("source_refs") or []),
        }
        object_index = {
            source_activator_ref: [activator_draft],
            source_target_ref: [projected_target_object],
        }
        drafts = profile.project_relationship(
            deepcopy(synthetic_relationship),
            deepcopy(object_index),
            static_request,
        ) or []
        if not drafts:
            arc_status_counts["unsupported_relationship_count"] += 1
            diagnostics["warnings"].append({
                "code": "temporal.activation.relationship_unmapped",
                "source_activation_ref": source_activation_ref,
                "aspect": aspect,
            })
            continue

        draft = drafts[0]
        relationship_type = str(draft.get("relationship_type") or "")
        projected_sequence = projected_temporal_sequence_id(
            profile_id=request_obj.profile_id,
            source_sequence_ref=source_sequence_ref,
            context_id=context_id,
        )
        projected_activation_id_value = projected_temporal_activation_id(
            profile_id=request_obj.profile_id,
            source_activation_ref=source_activation_ref,
            projected_activator_ref=str(projected_activator["id"]),
            projected_target_ref=projected_target_ref,
            projected_relationship_type=relationship_type,
            context_id=context_id,
        )

        states: list[dict[str, Any]] = []
        if request_obj.options.get("include_observation_states", True):
            for source_state in source_activation.get("observation_states") or []:
                source_state_ref = str(source_state.get("state_id") or "")
                composition = (
                    _project_state_composition(
                        profile=profile,
                        static_request=static_request,
                        source_activator=source_activator,
                        activation=source_activation,
                        state=source_state,
                    )
                    if request_obj.options.get("include_projected_state_composition", True)
                    else {
                        "mode_ref": None,
                        "domain_ref": None,
                        "mode_availability": "disabled_by_temporal_projection_options",
                        "domain_availability": "disabled_by_temporal_projection_options",
                        "availability": "disabled_by_temporal_projection_options",
                    }
                )
                states.append({
                    "id": projected_temporal_state_id(
                        profile_id=request_obj.profile_id,
                        source_state_ref=source_state_ref,
                        projected_activation_ref=projected_activation_id_value,
                        context_id=context_id,
                    ),
                    "source_state_ref": source_state_ref,
                    "projected_activation_ref": projected_activation_id_value,
                    "observed_at": source_state.get("observed_at"),
                    "phase": source_state.get("phase"),
                    "orb": source_state.get("orb"),
                    "distance": source_state.get("distance"),
                    "strength_label": source_state.get("strength_label"),
                    "activator_state": deepcopy(source_state.get("activator_state") or {}),
                    "projected_state_composition": composition,
                    "source_refs": [source_state_ref],
                    "provenance": {
                        "temporal_projection_stage": "C4",
                        "source_fact_preservation": True,
                    },
                })

        temporal_facts = {
            "start_at": source_activation.get("start_at"),
            "closest_observed_at": source_activation.get("closest_observed_at"),
            "exact_at": source_activation.get("exact_at"),
            "end_at": source_activation.get("end_at"),
            "exactness": deepcopy(source_activation.get("exactness") or {}),
            "motion": deepcopy(source_activation.get("motion") or {}),
            "observation_count": len(states),
            "observation_states": states,
            "source_observation_count": source_activation.get("observation_count"),
            "target_house": source_activation.get("target_house"),
            "target_type": source_activation.get("target_type"),
            "transit_house_in_target_chart": source_activation.get(
                "transit_house_in_target_chart"
            ),
        }
        mapping_rule_id = str(draft.get("mapping_rule_id") or "")
        activation_row = {
            "id": projected_activation_id_value,
            "source_activation_ref": source_activation_ref,
            "source_sequence_ref": source_sequence_ref,
            "projected_sequence_id": projected_sequence,
            "pass_index": int(source_activation.get("pass_index") or 1),
            "projected_activator_ref": str(projected_activator["id"]),
            "projected_target_ref": projected_target_ref,
            "projected_relationship_type": relationship_type,
            "projected_relationship_term_ref": relationship_type,
            "temporal_role": "current_activation",
            "directionality": "activator_to_target",
            "projected_activation_domain_ref": (
                states[0]["projected_state_composition"].get("domain_ref")
                if states else None
            ),
            "projected_activator_mode_refs": sorted({
                state["projected_state_composition"].get("mode_ref")
                for state in states
                if state["projected_state_composition"].get("mode_ref")
            }),
            "temporal_facts": temporal_facts,
            "source_refs": sorted(set([
                source_activation_ref,
                *list(source_activation.get("source_refs") or []),
            ])),
            "mapping_rule_refs": [mapping_rule_id],
            "context_refs": [context_id],
            "provenance": {
                **deepcopy(source_activation.get("provenance") or {}),
                **deepcopy(draft.get("provenance") or {}),
                "temporal_projection_stage": "C4",
                "mapping_reuse": "profile.project_relationship",
                "source_timing_facts_preserved": True,
                "source_aspect": aspect,
            },
        }
        projected_activations.append(activation_row)
        arc_status_counts["projected_activation_count"] += 1
        sequence_members.setdefault(source_sequence_ref, []).append(activation_row)

        result_refs = [projected_activation_id_value]
        mapping_executions.append({
            "execution_id": mapping_execution_id(
                mapping_rule_id=mapping_rule_id,
                source_refs=[source_activation_ref],
                context_id=context_id,
                result_refs=result_refs,
            ),
            "mapping_rule_id": mapping_rule_id,
            "mapping_rule_version": str(draft.get("mapping_rule_version") or ""),
            "source_refs": [source_activation_ref],
            "context_refs": [context_id],
            "result_refs": result_refs,
            "status": "applied",
            "conditions_evaluated": deepcopy(
                draft.get("conditions_evaluated") or []
            ),
            "warnings": [],
        })

    projected_activations.sort(key=lambda row: row["id"])
    projected_sequences: list[dict[str, Any]] = []
    for source_sequence_ref, rows in sorted(sequence_members.items()):
        rows = sorted(rows, key=lambda row: (row["pass_index"], row["id"]))
        projected_sequences.append({
            "id": projected_temporal_sequence_id(
                profile_id=request_obj.profile_id,
                source_sequence_ref=source_sequence_ref,
                context_id=context_id,
            ),
            "source_sequence_ref": source_sequence_ref,
            "activation_refs": [row["id"] for row in rows],
            "pass_count": len(rows),
            "source_refs": [source_sequence_ref],
            "provenance": {
                "temporal_projection_stage": "C4",
                "source_pass_indexes": [row["pass_index"] for row in rows],
                "interpretive_phase_labels_added": False,
            },
        })

    static_projection_id = str(
        projected_target.get("metadata", {}).get("projection_id") or
        projected_target.get("metadata", {}).get("package_id") or
        projected_target.get("metadata", {}).get("request_id") or
        static_request.request_id
    )
    temporal_source_graph_id = str(
        request_obj.temporal_source_graph.get("metadata", {}).get("graph_id") or ""
    )
    temporal_projection_id_value = projected_temporal_graph_id(
        request_id=request_obj.request_id,
        static_projection_id=static_projection_id,
        temporal_graph_id=temporal_source_graph_id,
        profile_id=request_obj.profile_id,
        profile_version=request_obj.profile_version,
        context_id=context_id,
        options=request_obj.options,
    )

    by_activator: dict[str, list[str]] = {}
    by_target: dict[str, list[str]] = {}
    by_sequence: dict[str, list[str]] = {}
    by_aspect: dict[str, list[str]] = {}
    for row in projected_activations:
        by_activator.setdefault(row["projected_activator_ref"], []).append(row["id"])
        by_target.setdefault(row["projected_target_ref"], []).append(row["id"])
        by_sequence.setdefault(row["projected_sequence_id"], []).append(row["id"])
        aspect = str(row["provenance"].get("source_aspect") or "")
        by_aspect.setdefault(aspect, []).append(row["id"])

    observation_count = sum(
        row["temporal_facts"]["observation_count"] for row in projected_activations
    )
    source_observation_count = sum(
        int(row.get("observation_count") or 0) for row in source_activations
    )
    source_sequence_count = len({
        str(row.get("sequence_id") or "") for row in source_activations
    })
    state_availability = {
        "mode_projected_count": 0,
        "mode_source_not_supplied_count": 0,
        "mode_mapping_unavailable_count": 0,
        "domain_projected_count": 0,
        "domain_source_not_supplied_count": 0,
        "domain_mapping_unavailable_count": 0,
    }
    for activation in projected_activations:
        for state in (activation.get("temporal_facts") or {}).get("observation_states") or []:
            comp = state.get("projected_state_composition") or {}
            mode_status = comp.get("mode_availability")
            domain_status = comp.get("domain_availability")
            if mode_status == "projected":
                state_availability["mode_projected_count"] += 1
            elif mode_status in {"source_sign_not_supplied", "source_position_not_supplied"}:
                state_availability["mode_source_not_supplied_count"] += 1
            else:
                state_availability["mode_mapping_unavailable_count"] += 1
            if domain_status == "projected":
                state_availability["domain_projected_count"] += 1
            elif domain_status in {"source_house_not_supplied", "source_position_not_supplied"}:
                state_availability["domain_source_not_supplied_count"] += 1
            else:
                state_availability["domain_mapping_unavailable_count"] += 1

    reconciliation = {
        "source_activation_count": len(source_activations),
        "projected_activation_count": len(projected_activations),
        "source_sequence_count": source_sequence_count,
        "projected_sequence_count": len(projected_sequences),
        "source_observation_state_count": source_observation_count,
        "projected_observation_state_count": observation_count,
        "projected_state_count_matches_projected_arcs": observation_count == sum(
            len((row.get("temporal_facts") or {}).get("observation_states") or [])
            for row in projected_activations
        ),
        "source_pass_identity_preserved": all(
            row.get("source_sequence_ref") and int(row.get("pass_index") or 0) >= 1
            for row in projected_activations
        ),
    }
    diagnostic_summary = _temporal_diagnostic_summary(diagnostics)
    graph = {
        "metadata": {
            "package_type": "projected_temporal_activation_graph",
            "contract_version": "1.0.0",
            "temporal_projection_id": temporal_projection_id_value,
            "static_projection_id": static_projection_id,
            "engine_version": ENGINE_VERSION,
            "profile_id": request_obj.profile_id,
            "profile_version": request_obj.profile_version,
            "context_id": context_id,
            "context_version": context_version,
            "materialization_mode": "full",
            "stage": "C6",
            "execution_status": "cross_profile_temporal_projection_ready",
        },
        "source_identity": deepcopy(request_obj.source_identity),
        "target_identity": deepcopy(request_obj.target_identity),
        "period": deepcopy(request_obj.temporal_source_graph.get("period") or {}),
        "projected_target_graph": projected_target,
        "projected_activators": projected_activators,
        "projected_activations": projected_activations,
        "projected_sequences": projected_sequences,
        "indexes": {
            "projected_activations_by_activator": {
                key: sorted(value) for key, value in sorted(by_activator.items())
            },
            "projected_activations_by_target": {
                key: sorted(value) for key, value in sorted(by_target.items())
            },
            "projected_activations_by_sequence": {
                key: sorted(value) for key, value in sorted(by_sequence.items())
            },
            "projected_activations_by_aspect": {
                key: sorted(value) for key, value in sorted(by_aspect.items())
            },
        },
        "summary": {
            "projected_activator_count": len(projected_activators),
            "projected_activation_count": len(projected_activations),
            "projected_sequence_count": len(projected_sequences),
            "projected_observation_state_count": observation_count,
            "coverage": {
                "activators": activator_coverage,
                "activations": arc_status_counts,
                "state_composition": state_availability,
            },
            "reconciliation": reconciliation,
        },
        "projected_term_registry": deepcopy(
            projected_target.get("projected_term_registry") or {}
        ),
        "audit": {
            "stage": "C6",
            "request_id": request_obj.request_id,
            "mapping_execution_count": len(mapping_executions),
            "mapping_executions": mapping_executions,
            "coverage": {
                "activators": activator_coverage,
                "activations": arc_status_counts,
                "state_composition": state_availability,
            },
            "reconciliation": reconciliation,
            "summary": {
                "mapping_execution_count": len(mapping_executions),
                "applied_mapping_count": sum(1 for row in mapping_executions if row.get("status") == "applied"),
                "coverage": {
                    "eligible_activators": activator_coverage.get("eligible_activator_count"),
                    "mapped_eligible_activators": activator_coverage.get("mapped_eligible_activator_count"),
                    "eligible_activations": arc_status_counts.get("eligible_activation_count"),
                    "projected_activations": arc_status_counts.get("projected_activation_count"),
                },
                "reconciliation": reconciliation,
            },
        },
        "diagnostics": {
            **diagnostics,
            "summary": diagnostic_summary,
        },
        "provenance": {
            "temporal_projection_request_id": request_obj.request_id,
            "source_bundle_id": request_obj.upstream_contracts.get("bundle_id"),
            "canonical_temporal_graph_id": temporal_source_graph_id,
            "static_projection_id": static_projection_id,
            "source_timing_owner": "Astrology Graph Foundry",
            "projected_semantics_owner": "Semantic Projection Core",
            "arc_mapping_reuse": "profile.project_relationship",
            "object_mapping_reuse": "profile.project_object",
        },
        "upstream_source_limitations": _annotate_upstream_limitations(list(request_obj.limitations)),
        "projected_artifact_limitations": [
            "Stage C6 proves cross-profile and context behavior; downstream interpretation remains out of scope.",
            "No consumer-facing transit interpretation, claim synthesis, or narrative rendering is included.",
        ],
    }
    validate_projected_temporal_activation_graph(graph)
    return graph
