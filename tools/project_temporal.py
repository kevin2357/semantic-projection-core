#!/usr/bin/env python3
"""Project a Foundry temporal source bundle, interactively or entirely by flags."""

from __future__ import annotations

import argparse

from _projection_cli import add_common_profile_arguments, build_registry, prompt, read_json, resolve_context, resolve_profile, run_main, write_json


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bundle", help="Foundry temporal_projection_source_bundle.v1 JSON")
    parser.add_argument("--options", help="Optional TemporalProjectionOptions JSON")
    parser.add_argument("--out", help="Projected temporal graph output")
    parser.add_argument("--request-out", help="Optional normalized temporal request output")
    parser.add_argument("--receipt-out", help="Optional routing receipt output")
    add_common_profile_arguments(parser)
    args = parser.parse_args(argv)

    profile_id, profile_version, target_domain, profile_key = resolve_profile(args)
    bundle_path = prompt("Temporal source bundle JSON", args.bundle)
    out_path = prompt("Output JSON", args.out)
    context = resolve_context(args, target_domain=target_domain, route="temporal")

    from semantic_projection import TemporalProjectionOptions, project_foundry_temporal_bundle

    options = read_json(args.options) if args.options else TemporalProjectionOptions().to_dict()
    result = project_foundry_temporal_bundle(
        read_json(bundle_path), profile_id=profile_id, profile_version=profile_version,
        context=context, options=options, output_mode=args.output_mode,
        registry=build_registry(profile_key == "custom"),
    )
    write_json(out_path, result.artifact)
    write_json(args.request_out, result.request)
    write_json(args.receipt_out, result.receipt)
    print(f"Wrote projected temporal graph: {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(run_main(main))
