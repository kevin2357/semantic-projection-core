#!/usr/bin/env python3
"""Project a canonical synastry graph, interactively or entirely by flags."""

from __future__ import annotations

import argparse

from _projection_cli import (
    add_common_profile_arguments, build_registry, extract_evidence, extract_graph,
    extract_identity, prompt, read_json, resolve_context, resolve_profile, run_main, write_json,
)


def interactive_participants() -> list[dict]:
    count = int(prompt("Participant count", default="2"))
    if count < 2:
        raise ValueError("Synastry requires at least two participants")
    rows = []
    for index in range(1, count + 1):
        print(f"Participant {index}:")
        participant_id = prompt("  ID")
        role = prompt("  Role", default="unspecified")
        species = input("  Species (optional): ").strip()
        label = input("  Label (optional): ").strip()
        row = {"participant_id": participant_id, "role": role}
        if species:
            row["species"] = species
        if label:
            row["label"] = label
        rows.append(row)
    return rows


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", help="Canonical synastry graph or full Foundry/SDK JSON package")
    parser.add_argument("--participants", help="JSON object containing a participants array")
    parser.add_argument("--relationship-kind", help="For example synastry, human_dog, or dog_dog")
    parser.add_argument("--structural-evidence", help="Optional structural-evidence JSON override")
    parser.add_argument("--source-identity", help="Optional source-identity JSON override")
    parser.add_argument("--options", help="Optional ProjectionOptions JSON")
    parser.add_argument("--out", help="Projected synastry graph output")
    parser.add_argument("--request-out", help="Optional normalized ProjectionRequest output")
    add_common_profile_arguments(parser)
    args = parser.parse_args(argv)

    profile_id, profile_version, target_domain, profile_key = resolve_profile(args)
    source_path = prompt("Canonical synastry graph/package JSON", args.source)
    out_path = prompt("Output JSON", args.out)
    relationship_kind = prompt("Relationship kind", args.relationship_kind, default="synastry")
    context = resolve_context(args, target_domain=target_domain, route="synastry")
    package = read_json(source_path)
    graph = extract_graph(package)
    if args.participants:
        participants = read_json(args.participants).get("participants")
    else:
        participants = interactive_participants()
    if not isinstance(participants, list) or len(participants) < 2:
        raise ValueError("Participants JSON must provide a 'participants' array with at least two records")

    from semantic_projection import ProjectionOptions, materialize_projected_graph, project_synastry

    options = read_json(args.options) if args.options else ProjectionOptions().to_dict()
    result = project_synastry(
        source_graph=graph, structural_evidence=extract_evidence(package, args.structural_evidence),
        source_identity=extract_identity(package, graph, args.source_identity), participants=participants,
        relationship_kind=relationship_kind, profile_id=profile_id, profile_version=profile_version,
        context=context, registry=build_registry(profile_key == "custom"), options=options,
    )
    write_json(out_path, materialize_projected_graph(result.artifact, mode=args.output_mode))
    write_json(args.request_out, result.request.to_dict())
    print(f"Wrote projected synastry graph: {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(run_main(main))
