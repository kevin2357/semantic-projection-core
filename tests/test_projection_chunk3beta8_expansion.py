from __future__ import annotations

import json
from pathlib import Path

from semantic_projection import ProjectionContext, project_foundry_temporal_bundle

ROOT = Path(__file__).resolve().parents[1]
BUNDLE = ROOT / "outputs" / "fixture_test_files" / "kevin_2026-01_temporal_projection_source.json"


def _bundle():
    return json.loads(BUNDLE.read_text(encoding="utf-8"))


def _context(name: str):
    return ProjectionContext.from_dict(
        json.loads((ROOT / "examples" / "contexts" / name).read_text(encoding="utf-8"))
    )


def test_c8_orthodox_expands_canonical_and_temporal_coverage():
    result = project_foundry_temporal_bundle(
        _bundle(),
        profile_id="orthodox_astrology.v1",
        profile_version="1.0.0",
        context=_context("orthodox_general_context.json"),
        output_mode="standard",
    )
    artifact = result.artifact
    coverage = artifact["audit"]["coverage"]
    assert len(artifact["projected_target_graph"]["objects"]) == 188
    assert len(artifact["projected_activators"]) == 12
    assert len(artifact["projected_activations"]) == 88
    assert coverage["activators"]["eligible_but_unmapped_activator_count"] == 0
    assert coverage["activations"]["target_eligible_but_unmapped_count"] == 0
    assert coverage["activations"]["failed_activation_count"] == 0


def test_c8_woofmapped_temporal_route_remains_complete_for_declared_scope():
    result = project_foundry_temporal_bundle(
        _bundle(),
        profile_id="woofmapped_astrology.v0",
        profile_version="0.1.0",
        context=_context("woofmapped_doghouse_general_context.json"),
        output_mode="standard",
    )
    artifact = result.artifact
    coverage = artifact["audit"]["coverage"]
    assert len(artifact["projected_activators"]) == 11
    assert len(artifact["projected_activations"]) == 54
    assert coverage["activators"]["eligible_but_unmapped_activator_count"] == 0
    assert coverage["activations"]["target_eligible_but_unmapped_count"] == 0
    assert coverage["activations"]["failed_activation_count"] == 0
