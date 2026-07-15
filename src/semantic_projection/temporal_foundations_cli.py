from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .artifact_identity import identify_artifact
from .contracts import TemporalProjectionRequest
from .logging_config import configure_logging, log_event
from .temporal import project_temporal_foundations


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build Stage C3 temporal projection foundations.")
    parser.add_argument("--request", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--log-file")
    parser.add_argument("--debug", action="store_true")
    args = parser.parse_args(argv)
    logger = configure_logging(log_path=args.log_file)
    try:
        payload = json.loads(Path(args.request).read_text(encoding="utf-8"))
        identity = identify_artifact(payload)
        if identity.kind != "temporal_projection_request":
            raise ValueError(
                "Expected temporal_projection_request.v1; "
                f"received {identity.kind} ({identity.package_type!r})."
            )
        result = project_temporal_foundations(TemporalProjectionRequest.from_dict(payload))
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(
            json.dumps(result, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        log_event(
            logger,
            "temporal_foundations_completed",
            output=args.out,
            projected_activators=len(result["projected_activators"]),
        )
        print(f"Wrote temporal foundations: {args.out}")
        return 0
    except Exception as exc:
        log_event(logger, "temporal_foundations_rejected", error=str(exc))
        if args.debug:
            raise
        print(f"ERROR temporal_foundations: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
