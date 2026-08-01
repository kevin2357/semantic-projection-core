from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).parents[1]
TOOLS = ROOT / "tools"


def _load(name: str):
    if str(TOOLS) not in sys.path:
        sys.path.insert(0, str(TOOLS))
    spec = importlib.util.spec_from_file_location(name, TOOLS / f"{name}.py")
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _value_after(argv: list[str], option: str) -> str:
    return argv[argv.index(option) + 1]


def test_natal_tool_fixes_profile_and_defaults_doghouse_context():
    module = _load("woofmap_natal")
    argv = module.projection_argv(["--source", "natal.json", "--out", "projected.json"])
    assert argv[-2:] == ["--profile", "woofmapped"]
    assert _value_after(argv, "--context").endswith("woofmapped_doghouse_general_context.json")


def test_natal_tool_allows_explicit_context_override():
    module = _load("woofmap_natal")
    argv = module.projection_argv(["--context", "custom.json"])
    assert argv.count("--context") == 2
    assert argv[-4:-2] == ["--context", "custom.json"]


def test_transit_tool_selects_each_supported_audience_context():
    module = _load("woofmap_transit")
    expected = {
        "handler": "woofmapped_handler_guidance_context.json",
        "dog": "woofmapped_dog_direct_context.json",
        "hybrid": "woofmapped_hybrid_horoscope_context.json",
    }
    for audience, filename in expected.items():
        argv = module.projection_argv(["--audience", audience, "--bundle", "transit.json"])
        assert argv[-2:] == ["--profile", "woofmapped"]
        assert _value_after(argv, "--context").endswith(filename)
        assert "--audience" not in argv


def test_synastry_tool_supplies_role_and_species_defaults():
    module = _load("woofmap_synastry")
    human, dog = module.participant_defaults("human-dog")
    assert human == {"role": "handler", "species": "human"}
    assert dog == {"role": "dog", "species": "canine"}

    dog_a, dog_b = module.participant_defaults("dog-dog")
    assert dog_a == dog_b == {"role": "dog", "species": "canine"}


def test_convenience_tools_have_helpful_cli_help():
    for name in ("woofmap_natal", "woofmap_transit", "woofmap_synastry"):
        text = (TOOLS / f"{name}.py").read_text(encoding="utf-8")
        assert "Woofmap" in text
        assert "__main__" in text
