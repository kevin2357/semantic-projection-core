from __future__ import annotations

from semantic_projection.materialization import (
    external_audit_artifact,
    materialize_projected_graph,
)
from tests.support import enforce_unmapped_threshold


def fixture() -> dict:
    return {
        "metadata": {"projection_id": "p1", "profile_id": "demo", "materialization_mode": "full"},
        "source_identity": {"source_chart_id": "x"},
        "source_graph_ref": {"source_graph_hash": "h"},
        "target_ontology": "demo",
        "objects": [{"id": "o1"}],
        "relationships": [{"id": "r1"}],
        "indexes": {},
        "summary": {
            "profile_scope_coverage": {
                "objects": {"eligible_count": 2, "eligible_but_unmapped_count": 0, "declared_scope_coverage": 1.0},
                "relationships": {"eligible_count": 1, "eligible_but_unmapped_count": 0, "declared_scope_coverage": 1.0},
            }
        },
        "audit": {
            "coverage": {"source_object_count": 10, "unmapped_source_object_count": 8, "source_relationship_count": 10, "unmapped_source_relationship_count": 9},
            "mapping_executions": [{"execution_id": "e1"}],
            "unmapped_source_refs": ["x"],
            "fallbacks": [],
        },
        "diagnostics": {"errors": [], "warnings": [], "infos": [{}], "unmapped_source_refs": ["x"], "fallbacks": []},
        "projected_term_registry": {"registry_id": "terms", "registry_version": "1", "target_ontology": "demo", "terms": {"a": {}}},
    }


def test_materializations_are_bounded_and_deterministic():
    full = fixture()
    standard = materialize_projected_graph(full, mode="standard")
    summary = materialize_projected_graph(full, mode="summary")
    forensic_a = materialize_projected_graph(full, mode="forensic")
    forensic_b = materialize_projected_graph(full, mode="forensic")
    assert standard["objects"] == [{"id": "o1"}]
    assert "mapping_executions" not in standard["audit"]
    assert "objects" not in summary
    assert forensic_a["forensic_integrity"] == forensic_b["forensic_integrity"]


def test_external_audit_is_separable():
    audit = external_audit_artifact(fixture())
    assert audit["metadata"]["package_type"] == "projection_forensic_audit"
    assert audit["audit"]["mapping_executions"]
    assert audit["metadata"]["artifact_hash"]


def test_threshold_defaults_to_eligible_scope():
    enforce_unmapped_threshold(fixture(), 0.0, scope="eligible")
    try:
        enforce_unmapped_threshold(fixture(), 0.5, scope="canonical")
    except ValueError as exc:
        assert "canonical" in str(exc)
    else:
        raise AssertionError("canonical threshold should fail")
