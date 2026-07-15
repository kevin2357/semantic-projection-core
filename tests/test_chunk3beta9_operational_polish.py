from __future__ import annotations

import json
from pathlib import Path

from semantic_projection import ProjectionContext, project_foundry_temporal_bundle

ROOT = Path(__file__).resolve().parents[1]
BUNDLE = ROOT / "outputs" / "fixture_test_files" / "kevin_2026-01_temporal_projection_source.json"


def _load(name: str):
    return json.loads((ROOT / "examples" / "contexts" / name).read_text(encoding="utf-8"))


def test_c9_woofmapped_contexts_have_distinct_audience_contracts():
    handler = ProjectionContext.from_dict(_load("woofmapped_handler_guidance_context.json"))
    dog = ProjectionContext.from_dict(_load("woofmapped_dog_direct_context.json"))
    assert handler.context_id == "woofmapped.handler_guidance.v1"
    assert dog.context_id == "woofmapped.dog_direct.v1"
    assert handler.parameters["audience_contract"]["primary"] == "handler"
    assert dog.parameters["audience_contract"]["address_mode"] == "direct_second_person"
    assert handler.extensions["primitive_mapping_policy"] == dog.extensions["primitive_mapping_policy"]


def test_c9_production_metadata_uses_durable_capability_language():
    bundle = json.loads(BUNDLE.read_text(encoding="utf-8"))
    context = ProjectionContext.from_dict(_load("woofmapped_handler_guidance_context.json"))
    result = project_foundry_temporal_bundle(bundle, profile_id="woofmapped_astrology.v0", profile_version="0.1.0", context=context, output_mode="full")
    metadata = result.artifact["metadata"]
    assert metadata["capability_status"] == "production_ready"
    assert metadata["contract_generation"] == "projected_temporal_activation_graph.v1"
    assert "stage" not in metadata
    assert result.artifact["audit"]["audit_generation"] == "temporal_projection_audit.v1"


def test_c9_woofmapped_context_modes_reuse_same_declared_primitive_scope():
    bundle = json.loads(BUNDLE.read_text(encoding="utf-8"))
    artifacts = []
    for name in ("woofmapped_handler_guidance_context.json", "woofmapped_dog_direct_context.json"):
        result = project_foundry_temporal_bundle(bundle, profile_id="woofmapped_astrology.v0", profile_version="0.1.0", context=ProjectionContext.from_dict(_load(name)), output_mode="standard")
        artifacts.append(result.artifact)
    assert [len(a["projected_activators"]) for a in artifacts] == [11, 11]
    assert [len(a["projected_activations"]) for a in artifacts] == [54, 54]
    assert artifacts[0]["metadata"]["context_id"] != artifacts[1]["metadata"]["context_id"]
