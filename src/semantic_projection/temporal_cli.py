from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
import traceback

from .contracts import ProjectionContext, TemporalProjectionOptions
from .temporal import TemporalSourceContractError, adapt_foundry_temporal_source_bundle


def main() -> None:
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
    args = parser.parse_args()

    try:
        bundle = json.loads(Path(args.bundle).read_text(encoding="utf-8"))
        context_payload = json.loads(Path(args.projection_context).read_text(encoding="utf-8"))
        context = ProjectionContext.from_dict(context_payload)
        options = TemporalProjectionOptions(
            include_observation_states=not args.omit_observation_states
        )
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
    except TemporalSourceContractError as exc:
        print(f"ERROR temporal_source_contract: {exc}", file=sys.stderr)
        if args.debug:
            traceback.print_exc()
        raise SystemExit(2) from exc


if __name__ == "__main__":
    main()
