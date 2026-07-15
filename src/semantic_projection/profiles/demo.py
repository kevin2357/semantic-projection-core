from __future__ import annotations

from typing import Any

from ..contracts import ProjectionContext, ProjectionProfileManifest, ProjectionRequest, ProjectedSemanticGraph


class DemonstrationProjectionProfile:
    """Small domain-neutral profile used to prove the generic engine."""

    manifest = ProjectionProfileManifest(
        profile_id="demonstration_projection.v0",
        profile_version="0.1.0",
        engine_contract_version="1.0.0",
        source_ontology="canonical_astrology_graph.v1",
        target_ontology="demonstration_semantics.v0",
        implementation={
            "type": "python",
            "entrypoint": (
                "semantic_projection.profiles.demo:"
                "DemonstrationProjectionProfile"
            ),
        },
        supported_source_graph_types=["demonstration"],
        optional_context_fields=["parameters"],
        mapping_rule_namespace="demonstration_projection.v0",
        status="reference_test_profile",
    )

    def validate_context(self, context: ProjectionContext) -> list[dict[str, Any]]:
        return []

    def project_object(
        self,
        source_object: dict[str, Any],
        request: ProjectionRequest,
    ) -> list[dict[str, Any]]:
        if source_object.get("project_demo") is False:
            return []
        category = str(source_object.get("demo_category") or "generic_primitive")
        return [{
            "target_key": category,
            "merge_key": category,
            "object_type": "demonstration_primitive",
            "name": category,
            "operators": list(source_object.get("operator_hints") or []),
            "attributes": {"source_names": [source_object.get("name")]},
            "structural_strength_score": source_object.get("structural_strength_score"),
            "projection_relevance_score": 1.0,
            "mapping_rule_id": f"demonstration_projection.v0.object.{category}",
        }]

    def project_relationship(
        self,
        source_relationship: dict[str, Any],
        projected_object_index: dict[str, list[dict[str, Any]]],
        request: ProjectionRequest,
    ) -> list[dict[str, Any]]:
        source_id = source_relationship.get("source_id")
        target_id = source_relationship.get("target_id")
        if not projected_object_index.get(str(source_id)) or not projected_object_index.get(str(target_id)):
            return []
        relation = str(source_relationship.get("demo_relation") or "interacts_with")
        return [{
            "relationship_type": relation,
            "source_source_id": str(source_id),
            "target_source_id": str(target_id),
            "operators": [relation],
            "theme_tags": [],
            "attributes": {"source_relationship_type": source_relationship.get("relationship_type")},
            "projection_relevance_score": 1.0,
            "mapping_rule_id": f"demonstration_projection.v0.relationship.{relation}",
        }]

    def finalize(
        self,
        graph: ProjectedSemanticGraph,
        request: ProjectionRequest,
    ) -> None:
        graph.summary["profile_finalize_called"] = True
