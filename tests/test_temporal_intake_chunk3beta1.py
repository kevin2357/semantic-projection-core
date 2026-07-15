from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path

import pytest

from semantic_projection import (
    ProjectionContext,
    TemporalProjectionNotImplementedError,
    TemporalSourceContractError,
    adapt_foundry_temporal_source_bundle,
    project_temporal,
    validate_foundry_temporal_source_bundle,
)


FIXTURE = Path(__file__).parent / "fixtures" / "foundry_temporal_source_bundle_v1_tiny.json"


def load_bundle() -> dict:
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


def context() -> ProjectionContext:
    return ProjectionContext(
        context_id="cognitive_architecture.general.v0",
        context_version="0.2.0",
        subject_scope="individual",
        target_domain="cognitive_architecture_demo.v0",
        application_context="cognitive_architecture_demo",
    )


def test_valid_foundry_bundle_adapts_without_mutating_input():
    bundle = load_bundle()
    original = deepcopy(bundle)
    request = adapt_foundry_temporal_source_bundle(
        bundle,
        profile_id="cognitive_architecture_demo.v0",
        profile_version="0.2.0",
        context=context(),
    )

    assert bundle == original
    assert request.request_contract == "temporal_projection_request.v1"
    assert request.request_id.startswith("temporal_projection_request:")
    assert request.static_source_graph["graph_version"] == "1.3.0"
    assert request.temporal_source_graph["metadata"]["authoritative_unit"] == "activation_arc"
    assert request.upstream_contracts["bundle_contract_version"] == "1.0.0"
    assert request.extensions["execution_status"] == "validated_intake_only"


def test_temporal_request_id_is_deterministic():
    bundle = load_bundle()
    first = adapt_foundry_temporal_source_bundle(
        bundle,
        profile_id="cognitive_architecture_demo.v0",
        profile_version="0.2.0",
        context=context(),
    )
    second = adapt_foundry_temporal_source_bundle(
        bundle,
        profile_id="cognitive_architecture_demo.v0",
        profile_version="0.2.0",
        context=context(),
    )
    assert first.request_id == second.request_id
    assert first.to_dict() == second.to_dict()


@pytest.mark.parametrize(
    ("path", "value", "message"),
    [
        (("metadata", "contract_version"), "9.0.0", "Unsupported Foundry temporal bundle contract version"),
        (("temporal_source_graph", "metadata", "authoritative_unit"), "daily_snapshot", "authoritative_unit"),
        (("temporal_source_graph", "metadata", "projection_neutral"), False, "projection_neutral"),
    ],
)
def test_unsupported_contract_variants_fail_cleanly(path, value, message):
    bundle = load_bundle()
    cursor = bundle
    for key in path[:-1]:
        cursor = cursor[key]
    cursor[path[-1]] = value
    with pytest.raises(TemporalSourceContractError, match=message):
        validate_foundry_temporal_source_bundle(bundle)


def test_unknown_activator_ref_fails_referential_integrity():
    bundle = load_bundle()
    bundle["temporal_source_graph"]["activations"][0]["activator_ref"] = "canonical:transiting_object:missing"
    with pytest.raises(TemporalSourceContractError, match="unknown activator"):
        validate_foundry_temporal_source_bundle(bundle)


def test_unknown_target_ref_fails_referential_integrity():
    bundle = load_bundle()
    bundle["temporal_source_graph"]["activations"][0]["target_ref"] = "natal:Missing"
    with pytest.raises(TemporalSourceContractError, match="absent from static_source_graph"):
        validate_foundry_temporal_source_bundle(bundle)


def test_observation_count_must_reconcile():
    bundle = load_bundle()
    bundle["temporal_source_graph"]["activations"][0]["observation_count"] += 1
    with pytest.raises(TemporalSourceContractError, match="observation_count"):
        validate_foundry_temporal_source_bundle(bundle)


def test_temporal_execution_remains_disabled_in_c1():
    with pytest.raises(TemporalProjectionNotImplementedError, match="Stage C1"):
        project_temporal()
