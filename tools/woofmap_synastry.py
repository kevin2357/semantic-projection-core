#!/usr/bin/env python3
"""Woofmap human-dog or dog-dog Synastry with role-aware participant defaults."""

from __future__ import annotations

import argparse
from copy import deepcopy

from _projection_cli import (
    REPO_ROOT,
    build_registry,
    extract_evidence,
    extract_graph,
    extract_identity,
    prompt,
    read_json,
    run_main,
    write_json,
)

CONTEXT_FILES = {
    "human-dog": "woofmapped_human_dog_synastry_context.json",
    "dog-dog": "woofmapped_dog_dog_synastry_context.json",
}


def participant_defaults(kind: str) -> tuple[dict, dict]:
    if kind == "human-dog":
        return (
            {"role": "handler", "species": "human"},
            {"role": "dog", "species": "canine"},
        )
    return (
        {"role": "dog", "species": "canine"},
        {"role": "dog", "species": "canine"},
    )


def _participant(args: argparse.Namespace, side: str, defaults: dict) -> dict:
    participant_id = prompt(f"Participant {side.upper()} ID", getattr(args, f"participant_{side}_id"))
    row = {
        "participant_id": participant_id,
        "role": getattr(args, f"participant_{side}_role") or defaults["role"],
        "species": getattr(args, f"participant_{side}_species") or defaults["species"],
    }
    label = getattr(args, f"participant_{side}_label")
    if label:
        row["label"] = label
    return row


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", help="Canonical Synastry graph or full Foundry package")
    parser.add_argument("--kind", choices=tuple(CONTEXT_FILES), default="human-dog")
    for side in ("a", "b"):
        parser.add_argument(f"--participant-{side}-id")
        parser.add_argument(f"--participant-{side}-label")
        parser.add_argument(f"--participant-{side}-role")
        parser.add_argument(f"--participant-{side}-species")
    parser.add_argument("--context", help="Optional Woofmapped Synastry context override")
    parser.add_argument("--structural-evidence", help="Optional structural-evidence JSON override")
    parser.add_argument("--source-identity", help="Optional source-identity JSON override")
    parser.add_argument("--options", help="Optional ProjectionOptions JSON")
    parser.add_argument("--output-mode", choices=("full", "standard", "summary", "forensic"), default="standard")
    parser.add_argument("--out", help="Projected Woofmapped Synastry output")
    parser.add_argument("--request-out", help="Optional normalized ProjectionRequest output")
    args = parser.parse_args(argv)

    source_path = prompt("Canonical Synastry graph/package JSON", args.source)
    out_path = prompt("Output JSON", args.out)
    package = read_json(source_path)
    graph = extract_graph(package)
    defaults_a, defaults_b = participant_defaults(args.kind)
    participants = [
        _participant(args, "a", defaults_a),
        _participant(args, "b", defaults_b),
    ]
    context_path = args.context or str(REPO_ROOT / "examples" / "contexts" / CONTEXT_FILES[args.kind])
    context = read_json(context_path)

    from semantic_projection import ProjectionOptions, materialize_projected_graph, project_synastry

    options = read_json(args.options) if args.options else ProjectionOptions().to_dict()
    source_registries = deepcopy(package.get("source_registries") or {})
    for name in ("theme_registry", "operator_registry", "object_registries", "natal_context_registries"):
        if name in package and name not in source_registries:
            source_registries[name] = deepcopy(package[name])
    result = project_synastry(
        source_graph=graph,
        structural_evidence=extract_evidence(package, args.structural_evidence),
        source_identity=extract_identity(package, graph, args.source_identity),
        participants=participants,
        relationship_kind=args.kind.replace("-", "_"),
        profile_id="woofmapped_astrology.v0",
        profile_version="0.1.0",
        context=context,
        registry=build_registry(),
        options=options,
        source_registries=source_registries,
    )
    write_json(out_path, materialize_projected_graph(result.artifact, mode=args.output_mode))
    write_json(args.request_out, result.request.to_dict())
    print(f"Wrote projected Woofmapped Synastry graph: {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(run_main(main))
