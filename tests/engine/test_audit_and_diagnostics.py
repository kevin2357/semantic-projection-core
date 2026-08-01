from __future__ import annotations

from semantic_projection.audit import create_empty_audit, empty_coverage
from semantic_projection.diagnostics import diagnostic, empty_diagnostics
from semantic_projection.ids import stable_hash
from semantic_projection.rendering.templates import OBJECT_TEMPLATE_IDS, RELATION_TEMPLATE_IDS


def test_empty_audit_counts_source_rows_and_hashes_inputs():
    request = {
        "source_graph": {
            "objects": [{"id": "a"}, {"id": "b"}],
            "relationships": [{"id": "r"}],
        },
        "context": {"context_id": "test"},
    }
    coverage = empty_coverage(request["source_graph"])
    assert coverage == {
        "source_object_count": 2,
        "mapped_source_object_count": 0,
        "unmapped_source_object_count": 2,
        "source_relationship_count": 1,
        "mapped_source_relationship_count": 0,
        "unmapped_source_relationship_count": 1,
    }
    audit = create_empty_audit(
        profile_id="test.v1",
        profile_version="1.0.0",
        engine_version="1.0.0",
        request=request,
    )
    assert audit.request_hash == stable_hash(request)
    assert audit.source_graph_hash == stable_hash(request["source_graph"])
    assert audit.context_hash == stable_hash(request["context"])
    assert audit.coverage == coverage


def test_diagnostic_helpers_omit_empty_optional_fields():
    assert diagnostic("mapped", "Mapped successfully") == {
        "code": "mapped",
        "message": "Mapped successfully",
    }
    assert diagnostic("invalid", "Invalid row", path="objects.0", details={"reason": "missing ID"}) == {
        "code": "invalid",
        "message": "Invalid row",
        "path": "objects.0",
        "details": {"reason": "missing ID"},
    }
    assert empty_diagnostics().to_dict() == {
        "errors": [],
        "warnings": [],
        "infos": [],
        "unmapped_source_refs": [],
        "fallbacks": [],
    }


def test_renderer_template_catalog_matches_supported_outputs():
    assert set(OBJECT_TEMPLATE_IDS) == {
        "object.natural.subject_mode_domain.v1",
        "object.natural.domain_emphasis.v1",
        "object.technical.explicit_composition.v1",
    }
    assert set(RELATION_TEMPLATE_IDS) == {
        "relationship.natural.active.v1",
        "relationship.technical.explicit.v1",
    }
