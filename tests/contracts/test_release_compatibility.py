from __future__ import annotations

from importlib import metadata

from semantic_projection import ENGINE_VERSION, __version__, bundled_contexts, release_compatibility
from semantic_projection.materialization import MATERIALIZATION_MODES
from semantic_projection.profiles import builtin_projection_registry
from semantic_projection.temporal import (
    SUPPORTED_FOUNDRY_BUNDLE_CONTRACT_VERSIONS,
    SUPPORTED_FOUNDRY_TEMPORAL_GRAPH_CONTRACT_VERSIONS,
)
from semantic_projection.validation import SUPPORTED_SOURCE_GRAPH_VERSIONS, SUPPORTED_TEMPORAL_REQUEST_CONTRACTS


def test_release_contract_matches_implemented_versions_and_profiles():
    contract = release_compatibility()
    distribution = contract["distribution"]
    assert distribution == {
        "name": "semantic-projection-core",
        "version": metadata.version("semantic-projection-core"),
        "python_requires": ">=3.10",
        "engine_version": ENGINE_VERSION,
        "engine_contract_version": "1.0.0",
    }
    assert distribution["version"] == __version__

    declared_profiles = {
        (item["profile_id"], item["profile_version"]): item
        for item in contract["profiles"]
    }
    implemented_profiles = {
        (item["profile_id"], item["profile_version"]): item
        for item in builtin_projection_registry().manifests()
    }
    assert declared_profiles.keys() == implemented_profiles.keys()
    for identity, declared in declared_profiles.items():
        assert declared["static_source_graph_types"] == implemented_profiles[identity]["supported_source_graph_types"]


def test_release_contract_matches_implemented_source_and_output_contracts():
    contract = release_compatibility()
    source = contract["source_contracts"]
    assert source["canonical_static_graph_versions"] == sorted(SUPPORTED_SOURCE_GRAPH_VERSIONS)
    assert source["foundry_temporal_bundle"]["contract_version"] in SUPPORTED_FOUNDRY_BUNDLE_CONTRACT_VERSIONS
    assert source["foundry_temporal_graph"]["contract_version"] in SUPPORTED_FOUNDRY_TEMPORAL_GRAPH_CONTRACT_VERSIONS
    assert source["temporal_request"] in SUPPORTED_TEMPORAL_REQUEST_CONTRACTS
    assert contract["output_contracts"]["materialization_modes"] == sorted(MATERIALIZATION_MODES)
    assert contract["output_contracts"]["temporal_foundations"] == {
        "package_type": "projected_temporal_foundations",
        "contract_version": "0.1.0",
    }


def test_release_contract_freezes_four_supported_woofmapped_natal_contexts():
    contract = release_compatibility()
    woof = next(item for item in contract["profiles"] if item["profile_id"] == "woofmapped_astrology.v0")
    declared = {(item["context_id"], item["context_version"]) for item in woof["supported_natal_contexts"]}
    bundled = {(item["context_id"], item["context_version"]) for item in bundled_contexts()}
    assert declared == {
        ("woofmapped.dog_direct.v1", "1.0.0"),
        ("woofmapped.doghouse.general.v0", "0.1.0"),
        ("woofmapped.handler_guidance.v1", "1.0.0"),
        ("woofmapped.hybrid_horoscope.v1", "1.0.0"),
    }
    assert declared <= bundled


def test_release_contract_console_scripts_match_installed_distribution_metadata():
    contract = release_compatibility()
    installed = {
        item.name
        for item in metadata.entry_points().select(group="console_scripts")
        if item.dist and item.dist.metadata["Name"] == "semantic-projection-core"
    }
    assert set(contract["console_scripts"]) == installed
