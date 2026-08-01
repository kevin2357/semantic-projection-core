from __future__ import annotations

import json

import pytest

from semantic_projection import (
    ProjectionContext,
    ProjectionExecutionError,
    ProjectionProfileRegistry,
    ProjectionProfileRegistryError,
    ProjectionRequest,
    project,
    projection_request_id,
)
from semantic_projection.profiles.demo import DemonstrationProjectionProfile


def request(*, unmapped_policy: str = "diagnostic") -> ProjectionRequest:
    context = ProjectionContext(
        context_id="demonstration.general.v0",
        context_version="0.1.0",
        subject_scope="system",
        target_domain="demonstration_semantics.v0",
        application_context="engine_test",
    ).to_dict()
    source_identity = {
        "source_chart_id": "fixture:engine",
        "source_chart_ids": ["fixture:engine"],
        "sensor_instance_id": "fixture:engine",
    }
    source_graph = {
        "graph_type": "canonical_astrology_graph",
        "graph_version": "1.3.0",
        "objects": [
            {"id": "source:a", "name": "A", "demo_category": "shared", "operator_hints": ["start"]},
            {"id": "source:b", "name": "B", "demo_category": "shared", "operator_hints": ["continue"]},
            {"id": "source:c", "name": "C", "project_demo": False},
        ],
        "relationships": [
            {
                "id": "relation:a_b",
                "relationship_type": "DEMO",
                "source_id": "source:a",
                "target_id": "source:b",
                "demo_relation": "coordinates_with",
            },
            {
                "id": "relation:b_c",
                "relationship_type": "DEMO",
                "source_id": "source:b",
                "target_id": "source:c",
            },
        ],
    }
    profile_id = "demonstration_projection.v0"
    profile_version = "0.1.0"
    options = {
        "retain_unmapped_sources": True,
        "include_audit": True,
        "include_diagnostics": True,
        "unmapped_policy": unmapped_policy,
    }
    return ProjectionRequest(
        request_id=projection_request_id(
            profile_id=profile_id,
            profile_version=profile_version,
            source_identity=source_identity,
            context=context,
            options=options,
        ),
        profile_id=profile_id,
        profile_version=profile_version,
        source_graph=source_graph,
        structural_evidence={"graph_version": "1.3.0"},
        source_identity=source_identity,
        context=context,
        options=options,
    )


def registry() -> ProjectionProfileRegistry:
    value = ProjectionProfileRegistry()
    value.register(DemonstrationProjectionProfile())
    return value


def test_engine_projects_merges_audits_and_reports_unmapped_sources():
    result = project(request(), registry=registry()).to_dict()
    assert result["target_ontology"] == "demonstration_semantics.v0"
    assert len(result["objects"]) == 1
    assert result["objects"][0]["source_refs"] == [
        "canonical:object:source:a",
        "canonical:object:source:b",
    ]
    assert set(result["objects"][0]["operators"]) == {"continue", "start"}
    assert len(result["relationships"]) == 1
    assert result["relationships"][0]["relationship_type"] == "coordinates_with"
    assert result["audit"]["coverage"] == {
        "source_object_count": 3,
        "mapped_source_object_count": 2,
        "unmapped_source_object_count": 1,
        "source_relationship_count": 2,
        "mapped_source_relationship_count": 1,
        "unmapped_source_relationship_count": 1,
    }
    assert result["diagnostics"]["unmapped_source_refs"] == [
        "canonical:object:source:c",
        "canonical:relationship:relation:b_c",
    ]
    assert len(result["audit"]["mapping_executions"]) == 3
    assert result["summary"]["profile_finalize_called"] is True


def test_engine_is_deterministic_and_does_not_mutate_request():
    value = request()
    before = json.dumps(value.to_dict(), sort_keys=True)
    first = project(value, registry=registry()).to_dict()
    second = project(value, registry=registry()).to_dict()
    assert first == second
    assert json.dumps(value.to_dict(), sort_keys=True) == before


def test_passthrough_policy_retains_unmapped_object_placeholder():
    result = project(request(unmapped_policy="passthrough"), registry=registry()).to_dict()
    placeholders = [row for row in result["objects"] if row["object_type"] == "unmapped_source_placeholder"]
    assert len(placeholders) == 1
    assert result["diagnostics"]["fallbacks"][0]["fallback"] == "passthrough_placeholder"


def test_fail_policy_stops_on_unmapped_source():
    with pytest.raises(ProjectionExecutionError, match="Unmapped object source"):
        project(request(unmapped_policy="fail"), registry=registry())


def test_registry_requires_exact_profile_version():
    value = registry()
    assert value.resolve("demonstration_projection.v0", "0.1.0").manifest.profile_id == "demonstration_projection.v0"
    with pytest.raises(ProjectionProfileRegistryError, match="available versions"):
        value.resolve("demonstration_projection.v0", "9.9.9")
    with pytest.raises(ProjectionProfileRegistryError, match="Unknown projection profile"):
        value.resolve("missing.v0", "0.1.0")


def test_registry_rejects_duplicate_registration():
    value = registry()
    with pytest.raises(ProjectionProfileRegistryError, match="already registered"):
        value.register(DemonstrationProjectionProfile())
