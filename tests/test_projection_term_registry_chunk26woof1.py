from __future__ import annotations

from tests.support import project_dataset
from semantic_projection import ProjectionContext


def source_package() -> dict:
    objects = [
        {"id":"natal:Sun","name":"Sun","object_type":"planet_or_point","sign":"Libra","house":8},
        {"id":"natal:True_Node","name":"True Node","object_type":"calculated_point","sign":"Cancer","house":6},
        {"id":"natal:Mean_Node","name":"Mean Node","object_type":"calculated_point","sign":"Cancer","house":6},
        {"id":"natal:Fortune","name":"Fortune","object_type":"lot","sign":"Cancer","house":5},
        {"id":"natal:Part_of_Fortune","name":"Part of Fortune","object_type":"lot","sign":"Cancer","house":5},
    ]
    relationships = [
        {"id":"r:sun:true","relationship_type":"ASPECT","source_id":"natal:Sun","target_id":"natal:True_Node","aspect":"trine"},
        {"id":"r:sun:mean","relationship_type":"ASPECT","source_id":"natal:Sun","target_id":"natal:Mean_Node","aspect":"trine"},
        {"id":"r:true:mean","relationship_type":"ASPECT","source_id":"natal:True_Node","target_id":"natal:Mean_Node","aspect":"conjunction"},
        {"id":"r:sun:fortune","relationship_type":"ASPECT","source_id":"natal:Sun","target_id":"natal:Fortune","aspect":"square"},
        {"id":"r:sun:pof","relationship_type":"ASPECT","source_id":"natal:Sun","target_id":"natal:Part_of_Fortune","aspect":"square"},
    ]
    return {
        "metadata":{"analysis_type":"natal_dataset","source_chart_id":"natal:test","source_chart_ids":["natal:test"],"sensor_instance_id":"natal:test"},
        "canonical_astrology_graph":{"graph_type":"canonical_astrology_graph","graph_version":"1.3.0","objects":objects,"relationships":relationships},
        "structural_evidence_graph":{"graph_version":"1.3.0"},
    }


def cognitive_context() -> ProjectionContext:
    return ProjectionContext(
        context_id="cognitive_architecture.general.v0",
        context_version="0.2.0",
        subject_scope="individual",
        target_domain="cognitive_architecture_demo.v0",
        application_context="cognitive_architecture_demo",
    )


def woof_context(policy: str = "doghouse") -> ProjectionContext:
    return ProjectionContext(
        context_id="woofmapped.doghouse.general.v0",
        context_version="0.1.0",
        subject_scope="dog",
        target_domain="woofmapped_astrology.v0",
        application_context="woofmapped_natal_projection",
        constraints={"house_mapping_policy":policy},
    )


def test_used_projected_term_registry_is_embedded_and_referenced():
    result=project_dataset(
        source_package(),
        profile_id="woofmapped_astrology.v0",
        profile_version="0.1.0",
        context=woof_context(),
    )
    registry=result["projected_term_registry"]
    assert registry["materialization"]=="used_terms_subset"
    assert "pack_role_identity" in registry["terms"]
    assert "social_harmony_maintenance_mode" in registry["terms"]
    assert "doghouse_8_deep_trust_vulnerability" in registry["terms"]
    sun=next(row for row in result["objects"] if row["attributes"].get("canonical_object_name")=="Sun")
    assert sun["attributes"]["term_ref"]
    assert sun["attributes"]["mode_ref"]
    assert sun["attributes"]["domain_ref"]
    assert registry["terms"]["pack_role_identity"]["output_guidance"]["composition_template"]


def test_node_and_fortune_source_selection_removes_alias_duplicates():
    result=project_dataset(
        source_package(),
        profile_id="cognitive_architecture_demo.v0",
        profile_version="0.2.0",
        context=cognitive_context(),
    )
    names=[row["name"] for row in result["objects"]]
    assert names.count("developmental_orientation")==1
    assert names.count("resource_ease_convergence")==1
    source_refs={ref for row in result["objects"] for ref in row["source_refs"]}
    assert "canonical:object:natal:Mean_Node" not in source_refs
    assert "canonical:object:natal:Fortune" not in source_refs
    relation_refs={ref for row in result["relationships"] for ref in row["source_relationship_refs"]}
    assert "canonical:relationship:r:true:mean" not in relation_refs
    scope=result["summary"]["profile_scope_coverage"]
    assert scope["objects"]["excluded_by_source_selection_policy_count"]==2
    assert scope["relationships"]["excluded_by_source_selection_policy_count"]==3
    assert scope["objects"]["declared_scope_coverage"]==1.0
    assert scope["relationships"]["declared_scope_coverage"]==1.0


def test_woofmapped_house_policy_is_explicit_and_validated():
    try:
        project_dataset(
            source_package(),
            profile_id="woofmapped_astrology.v0",
            profile_version="0.1.0",
            context=woof_context("direct_translated"),
        )
    except Exception as exc:
        assert "does not implement house_mapping_policy=direct_translated" in str(exc)
    else:
        raise AssertionError("unsupported house policy should fail")
