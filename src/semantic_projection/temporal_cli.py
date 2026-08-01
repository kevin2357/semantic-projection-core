from __future__ import annotations

import argparse
import json
import logging
import sys
from pathlib import Path

from .contracts import ProjectionContext, TemporalProjectionOptions
from .logging_config import configure_logging, log_event
from .temporal import adapt_foundry_temporal_source_bundle


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Validate a Foundry temporal_projection_source_bundle.v1 and "
            "adapt it into a generic Core TemporalProjectionRequest. "
            "This command does not execute temporal projection."
        )
    )
    parser.add_argument("--bundle", required=True, help="Foundry temporal source bundle JSON")
    parser.add_argument("--projection-profile", required=True, help="Projection profile ID")
    parser.add_argument("--projection-profile-version", required=True, help="Projection profile version")
    parser.add_argument("--projection-context", required=True, help="ProjectionContext JSON")
    parser.add_argument("--out", required=True, help="Output TemporalProjectionRequest JSON")
    parser.add_argument("--omit-observation-states", action="store_true")
    parser.add_argument("--debug", action="store_true", help="Show traceback for expected validation errors")
    parser.add_argument("--log-file", default="semantic_projection.log", help="UTF-8 Core operational log")
    args = parser.parse_args(argv)
    logger = configure_logging(
        log_path=args.log_file,
        level=logging.DEBUG if args.debug else logging.INFO,
    )
    log_event(
        logger,
        "temporal_intake_start",
        bundle=args.bundle,
        profile_id=args.projection_profile,
        profile_version=args.projection_profile_version,
        context=args.projection_context,
        output=args.out,
    )

    try:
        bundle = json.loads(Path(args.bundle).read_text(encoding="utf-8"))
        context_payload = json.loads(Path(args.projection_context).read_text(encoding="utf-8"))
        context = ProjectionContext.from_dict(context_payload)
        options = TemporalProjectionOptions(include_observation_states=not args.omit_observation_states)
        request = adapt_foundry_temporal_source_bundle(
            bundle,
            profile_id=args.projection_profile,
            profile_version=args.projection_profile_version,
            context=context,
            options=options,
        )
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(
            json.dumps(request.to_dict(), indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        print(f"Wrote validated temporal request: {out}")
        log_event(
            logger,
            "temporal_intake_complete",
            request_id=request.request_id,
            output=str(out),
            activator_count=len(request.temporal_source_graph.get("activators") or []),
            activation_count=len(request.temporal_source_graph.get("activations") or []),
        )
        return 0
    except Exception as exc:
        logger.warning(
            "temporal_intake_rejected reason=%r bundle=%r profile_id=%r",
            str(exc),
            args.bundle,
            args.projection_profile,
        )
        print(f"ERROR temporal_source_contract: {exc}", file=sys.stderr)
        if args.debug:
            raise
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
