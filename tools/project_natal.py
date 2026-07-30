#!/usr/bin/env python3
"""Project a canonical natal/static graph, interactively or entirely by flags."""

from __future__ import annotations

import argparse
from copy import deepcopy

from _projection_cli import (
    add_common_profile_arguments, build_registry, extract_evidence, extract_graph,
    extract_identity, prompt, read_json, resolve_context, resolve_profile, run_main, write_json,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", help="Canonical graph or full Foundry/SDK JSON package")
    parser.add_argument("--structural-evidence", help="Optional structural-evidence JSON override")
    parser.add_argument("--source-identity", help="Optional source-identity JSON override")
    parser.add_argument("--options", help="Optional ProjectionOptions JSON")
    parser.add_argument("--out", help="Projected semantic graph output")
    parser.add_argument("--request-out", help="Optional normalized ProjectionRequest output")
    add_common_profile_arguments(parser)
    args = parser.parse_args(argv)

    profile_id, profile_version, target_domain, profile_key = resolve_profile(args)
    source_path = prompt("Canonical graph/package JSON", args.source)
    out_path = prompt("Output JSON", args.out)
    context = resolve_context(args, target_domain=target_domain, route="natal")
    package = read_json(source_path)
    graph = extract_graph(package)
    if str(graph.get("graph_type") or "").lower() == "synastry":
        raise ValueError("This is a synastry graph; use tools/project_synastry.py")

    from semantic_projection import ProjectionOptions, ProjectionRequest, materialize_projected_graph, project, projection_request_id

    options = read_json(args.options) if args.options else ProjectionOptions().to_dict()
    identity = extract_identity(package, graph, args.source_identity)
    request = ProjectionRequest(
        request_id=projection_request_id(profile_id=profile_id, profile_version=profile_version, source_identity=identity, context=context, options=options),
        profile_id=profile_id, profile_version=profile_version, source_graph=graph,
        structural_evidence=extract_evidence(package, args.structural_evidence),
        source_identity=identity, context=deepcopy(context),
        source_registries=deepcopy(package.get("source_registries") or {}), options=options,
    )
    artifact = project(request, registry=build_registry(profile_key == "custom")).to_dict()
    write_json(out_path, materialize_projected_graph(artifact, mode=args.output_mode))
    write_json(args.request_out, request.to_dict())
    print(f"Wrote projected natal/static graph: {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(run_main(main))
