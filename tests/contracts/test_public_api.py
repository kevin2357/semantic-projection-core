from __future__ import annotations

import semantic_projection


def test_public_api_exports_current_supported_routes():
    expected = {
        "ProjectionRequest",
        "TemporalProjectionRequest",
        "project",
        "project_with_builtin_profiles",
        "project_foundry_temporal_bundle",
        "project_synastry",
        "materialize_projected_graph",
        "materialize_projected_temporal_graph",
        "identify_artifact",
        "BoundedNatalProjectionRequest",
        "ProjectedBoundedSemanticGraph",
        "adapt_foundry_bounded_natal_dataset",
        "bounded_evidence_closure",
        "build_projected_bounded_contract",
        "project_bounded_natal",
        "validate_projected_bounded_semantic_graph",
    }
    assert expected <= set(semantic_projection.__all__)
    assert all(hasattr(semantic_projection, name) for name in expected)


def test_builtin_convenience_api_projects_a_valid_request():
    request = semantic_projection.ProjectionRequest(
        request_id="request:public-api",
        profile_id="orthodox_astrology.v1",
        profile_version="1.0.0",
        source_graph={
            "graph_type": "natal",
            "graph_version": "1.3.0",
            "objects": [{"id": "natal:Sun", "name": "Sun", "object_type": "planet"}],
            "relationships": [],
        },
        structural_evidence={},
        source_identity={
            "source_chart_id": "natal:test",
            "source_chart_ids": ["natal:test"],
            "sensor_instance_id": "natal:test",
        },
        context={
            "context_id": "orthodox.general.v1",
            "context_version": "1.0.0",
            "subject_scope": "individual",
            "target_domain": "orthodox_astrology.v1",
            "application_context": "test",
        },
    )
    result = semantic_projection.project_with_builtin_profiles(request)
    assert result.metadata["profile_id"] == "orthodox_astrology.v1"
    assert result.objects
