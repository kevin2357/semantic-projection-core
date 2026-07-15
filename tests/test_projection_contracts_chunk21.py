from __future__ import annotations

import ast
import copy
import json
from pathlib import Path

import pytest

from semantic_projection import (
    ProjectedSemanticGraph,
    ProjectionContext,
    ProjectionProfileManifest,
    ProjectionRequest,
    ProjectionValidationError,
    projected_object_id,
    projection_request_id,
    validate_contract,
    validate_projection_request,
)
from semantic_projection.ids import canonical_json, stable_hash

FIXTURES = Path(__file__).parent / "fixtures" / "projection"


def load(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def test_contract_round_trip_to_plain_dict():
    context = ProjectionContext(
        context_id="orthodox.general.v1",
        context_version="1.0.0",
        subject_scope="individual",
        target_domain="orthodox_astrology",
        application_context="general_interpretation",
    )
    rebuilt = ProjectionContext.from_dict(context.to_dict())
    assert rebuilt.to_dict() == context.to_dict()

    manifest = ProjectionProfileManifest(
        profile_id="orthodox_astrology.v1",
        profile_version="1.0.0",
        engine_contract_version="1.0.0",
        source_ontology="canonical_astrology_graph.v1",
        target_ontology="orthodox_astrology.v1",
        implementation={"type": "python", "entrypoint": "example:Profile"},
        supported_source_graph_types=["natal"],
        mapping_rule_namespace="orthodox_astrology.v1",
    )
    validate_contract(manifest.to_dict(), "projection_profile_manifest_v1.schema.json")


def test_projection_request_fixture_validates():
    request = load("empty_projection_request.json")
    validate_projection_request(request)
    rebuilt = ProjectionRequest.from_dict(request)
    assert rebuilt.to_dict() == request


def test_projected_graph_fixture_validates():
    graph = load("empty_projected_semantic_graph.json")
    validate_contract(graph, "projected_semantic_graph_v1.schema.json")
    assert ProjectedSemanticGraph.from_dict(graph).to_dict() == graph


def test_ids_are_deterministic_and_key_order_independent():
    context_a = {"context_id": "x", "parameters": {"b": 2, "a": 1}}
    context_b = {"parameters": {"a": 1, "b": 2}, "context_id": "x"}
    identity = {"source_chart_ids": ["natal:test"], "sensor_instance_id": "natal:test"}
    first = projection_request_id(
        profile_id="orthodox_astrology.v1",
        profile_version="1.0.0",
        source_identity=identity,
        context=context_a,
    )
    second = projection_request_id(
        profile_id="orthodox_astrology.v1",
        profile_version="1.0.0",
        source_identity=identity,
        context=context_b,
    )
    assert first == second
    assert canonical_json(context_a) == canonical_json(context_b)
    assert stable_hash(context_a) == stable_hash(context_b)
    assert projected_object_id(
        profile_id="orthodox_astrology.v1",
        target_key="value",
        source_refs=["b", "a"],
        context_id="x",
    ) == projected_object_id(
        profile_id="orthodox_astrology.v1",
        target_key="value",
        source_refs=["a", "b"],
        context_id="x",
    )


def test_invalid_request_and_unsupported_graph_version_fail_clearly():
    request = load("empty_projection_request.json")
    missing = copy.deepcopy(request)
    missing.pop("profile_id")
    with pytest.raises(ProjectionValidationError, match="profile_id|Missing required"):
        validate_projection_request(missing)

    unsupported = copy.deepcopy(request)
    unsupported["source_graph"]["graph_version"] = "99.0.0"
    with pytest.raises(ProjectionValidationError, match="Unsupported canonical source graph version"):
        validate_projection_request(unsupported)


def test_projection_core_has_no_pipeline_ephemeris_or_swisseph_imports():
    package_root = Path(__file__).parents[1] / "src" / "semantic_projection"
    forbidden = (
        "astro_analysis_sdk.pipelines",
        "astro_analysis_sdk.ephemeris",
        "swisseph",
        "pyswisseph",
    )
    violations = []
    for path in package_root.rglob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            names = []
            if isinstance(node, ast.Import):
                names = [alias.name for alias in node.names]
            elif isinstance(node, ast.ImportFrom):
                names = [node.module or ""]
            for name in names:
                if any(name == prefix or name.startswith(prefix + ".") for prefix in forbidden):
                    violations.append(f"{path.name}: {name}")
    assert violations == []
