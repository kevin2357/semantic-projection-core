"""Shared support for the human-friendly projection entry points."""

from __future__ import annotations

import json
import sys
from copy import deepcopy
from pathlib import Path
from typing import Any, Callable, Iterable

REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = REPO_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

JsonDict = dict[str, Any]

BUILTIN_PROFILES = {
    "orthodox": ("orthodox_astrology.v1", "1.0.0", "orthodox_astrology.v1"),
    "cognitive": ("cognitive_architecture_demo.v0", "0.2.0", "cognitive_architecture_demo.v0"),
    "woofmapped": ("woofmapped_astrology.v0", "0.1.0", "woofmapped_astrology.v0"),
}
PROFILE_ALIASES = {
    "1": "orthodox", "orthodox": "orthodox",
    "2": "cognitive", "cognitive": "cognitive",
    "3": "woofmapped", "woof": "woofmapped", "woofmapping": "woofmapped", "woofmapped": "woofmapped",
    "4": "custom", "custom": "custom",
}


def read_json(path: str | Path) -> JsonDict:
    value = json.loads(Path(path).expanduser().read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"Expected a JSON object in {path}")
    return value


def write_json(path: str | Path | None, value: JsonDict) -> None:
    if not path:
        return
    target = Path(path).expanduser()
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def prompt(label: str, value: Any = None, *, default: str | None = None) -> str:
    if value is not None and str(value).strip():
        return str(value)
    suffix = f" [{default}]" if default is not None else ""
    answer = input(f"{label}{suffix}: ").strip()
    if answer:
        return answer
    if default is not None:
        return default
    raise ValueError(f"{label} is required")


def choose(label: str, choices: Iterable[tuple[str, str]], value: str | None = None) -> str:
    rows = list(choices)
    keys = {key for key, _ in rows}
    if value is not None:
        if value not in keys:
            raise ValueError(f"Invalid {label.lower()} {value!r}; choose from {sorted(keys)}")
        return value
    print(label + ":")
    for index, (key, description) in enumerate(rows, 1):
        print(f"  {index}. {description} ({key})")
    answer = input("Selection: ").strip()
    if answer.isdigit() and 1 <= int(answer) <= len(rows):
        return rows[int(answer) - 1][0]
    if answer in keys:
        return answer
    raise ValueError(f"Invalid selection {answer!r}")


def resolve_profile(args: Any) -> tuple[str, str, str | None, str]:
    raw = args.profile
    if raw is None:
        print("Projection profile:")
        print("  1. Orthodox Astrology")
        print("  2. Cognitive Architecture")
        print("  3. Woofmapped Astrology")
        print("  4. Installed third-party profile")
        raw = input("Selection: ").strip().lower()
    key = PROFILE_ALIASES.get(str(raw).strip().lower())
    if key is None:
        raise ValueError("Profile must be orthodox, cognitive, woofmapped, or custom")
    if key == "custom":
        profile_id = prompt("Profile ID", args.profile_id)
        version = prompt("Profile version", args.profile_version)
        return profile_id, version, None, key
    profile_id, version, target_domain = BUILTIN_PROFILES[key]
    if args.profile_id and args.profile_id != profile_id:
        raise ValueError(f"--profile-id conflicts with the {key} built-in profile")
    if args.profile_version and args.profile_version != version:
        raise ValueError(f"--profile-version conflicts with the {key} built-in profile")
    return profile_id, version, target_domain, key


def build_registry(custom: bool = False):
    from semantic_projection.profiles import builtin_projection_registry

    registry = builtin_projection_registry()
    if custom:
        registry.discover_entry_points(replace=True)
    return registry


def context_candidates(target_domain: str, route: str) -> list[Path]:
    candidates = []
    for path in sorted((REPO_ROOT / "examples" / "contexts").glob("*.json")):
        context = read_json(path)
        if context.get("target_domain") != target_domain:
            continue
        scope = str(context.get("subject_scope") or "").lower()
        context_id = str(context.get("context_id") or "").lower()
        is_synastry = "synastry" in scope or "synastry" in context_id
        if route == "synastry" and not is_synastry:
            continue
        if route != "synastry" and is_synastry:
            continue
        candidates.append(path)
    return candidates


def resolve_context(args: Any, *, target_domain: str | None, route: str) -> JsonDict:
    if args.context:
        return read_json(args.context)
    if target_domain is None:
        return read_json(prompt("Projection context JSON file"))
    candidates = context_candidates(target_domain, route)
    if not candidates:
        raise ValueError(f"No bundled {route} contexts match target domain {target_domain!r}")
    print("Bundled contexts:")
    for index, path in enumerate(candidates, 1):
        context = read_json(path)
        print(f"  {index}. {context.get('context_id')} ({path.name})")
    answer = input("Selection: ").strip()
    if not answer.isdigit() or not 1 <= int(answer) <= len(candidates):
        raise ValueError(f"Invalid context selection {answer!r}")
    return read_json(candidates[int(answer) - 1])


def extract_graph(package: JsonDict) -> JsonDict:
    graph = package.get("canonical_astrology_graph") or package.get("canonical_source_graph") or package.get("source_graph")
    if graph is None and "objects" in package and "relationships" in package:
        graph = package
    if not isinstance(graph, dict) or "objects" not in graph or "relationships" not in graph:
        raise ValueError("Input must be a complete canonical graph or a package containing canonical_astrology_graph")
    return deepcopy(graph)


def extract_evidence(package: JsonDict, override: str | None) -> JsonDict:
    if override:
        return read_json(override)
    return deepcopy(package.get("structural_evidence_graph") or package.get("structural_evidence") or {})


def extract_identity(package: JsonDict, graph: JsonDict, override: str | None) -> JsonDict:
    if override:
        return read_json(override)
    if isinstance(package.get("source_identity"), dict):
        return deepcopy(package["source_identity"])
    metadata = package.get("metadata") or {}
    graph_metadata = graph.get("metadata") or {}
    chart_id = metadata.get("source_chart_id") or graph.get("source_chart_id") or graph_metadata.get("source_chart_id")
    chart_ids = list(metadata.get("source_chart_ids") or graph.get("source_chart_ids") or graph_metadata.get("source_chart_ids") or [])
    if chart_id and chart_id not in chart_ids:
        chart_ids.insert(0, chart_id)
    return {
        "source_chart_id": chart_id,
        "source_chart_ids": chart_ids,
        "sensor_instance_id": metadata.get("sensor_instance_id") or graph.get("sensor_instance_id") or graph_metadata.get("sensor_instance_id"),
    }


def add_common_profile_arguments(parser: Any) -> None:
    parser.add_argument("--profile", choices=("orthodox", "cognitive", "woofmapped", "custom"))
    parser.add_argument("--profile-id", help="Required with --profile custom")
    parser.add_argument("--profile-version", help="Required with --profile custom")
    parser.add_argument("--context", help="Projection context JSON; omitted values use a filtered bundled-context menu")
    parser.add_argument("--output-mode", choices=("full", "standard", "summary", "forensic"), default="standard")


def run_main(callback: Callable[[], int]) -> int:
    try:
        return callback()
    except (EOFError, KeyboardInterrupt):
        print("\nCancelled.", file=sys.stderr)
        return 130
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
