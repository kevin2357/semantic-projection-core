from __future__ import annotations

from copy import deepcopy

import pytest

from semantic_projection import (
    ProjectionValidationError,
    validate_contract,
    validate_projected_temporal_activation_graph,
    validate_projection_request,
    validate_temporal_projection_request,
)
from semantic_projection.io import read_json
from tests.paths import FIXTURES_ROOT


def static_request() -> dict:
    return read_json(FIXTURES_ROOT / "projection" / "empty_projection_request.json")


@pytest.mark.parametrize(
    ("mutation", "message"),
    [
        (lambda value: value.pop("context"), "context|Missing required"),
        (lambda value: value["source_graph"].pop("objects"), "objects|Missing required"),
        (lambda value: value["source_graph"].update(graph_type="transit_dataset"), "Temporal source packages"),
    ],
)
def test_static_request_validation_error_matrix(mutation, message):
    value = deepcopy(static_request())
    mutation(value)
    with pytest.raises(ProjectionValidationError, match=message):
        validate_projection_request(value)


def test_unknown_schema_and_non_object_contract_fail_clearly():
    with pytest.raises(FileNotFoundError):
        validate_contract({}, "missing.schema.json")
    with pytest.raises(ProjectionValidationError, match="type 'object'"):
        validate_contract([], "projection_context_v1.schema.json")  # type: ignore[arg-type]


def test_temporal_request_and_projected_graph_require_referential_integrity():
    bad_request = {
        "request_id": "temporal_projection_request:test",
        "request_contract": "temporal_projection_request.v1",
    }
    with pytest.raises(ProjectionValidationError):
        validate_temporal_projection_request(bad_request)

    bad_graph = {
        "metadata": {"package_type": "projected_temporal_activation_graph", "contract_version": "1.0.0"},
        "projected_target_graph": {"objects": []},
        "projected_activators": [],
        "projected_activations": [{"id": "activation:bad", "activator_id": "missing", "target_id": "missing"}],
        "projected_sequences": [],
    }
    with pytest.raises(ProjectionValidationError):
        validate_projected_temporal_activation_graph(bad_graph)
