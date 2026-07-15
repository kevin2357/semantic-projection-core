from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .artifact_identity import identify_artifact
from .contracts import TemporalProjectionRequest
from .logging_config import configure_logging, log_event
from .temporal import project_temporal
from .materialization import materialize_projected_temporal_graph


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Project one canonical temporal activation arc into one directional target-domain arc."
    )
    parser.add_argument("--request", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--output-mode", choices=["full", "standard", "summary", "forensic"], default="standard")
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
        full_result = project_temporal(TemporalProjectionRequest.from_dict(payload))
        result = materialize_projected_temporal_graph(full_result, mode=args.output_mode)
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        log_event(
            logger,
            "temporal_projection_completed",
            output=args.out,
            output_mode=args.output_mode,
            projected_activators=len(full_result["projected_activators"]),
            projected_activations=len(full_result["projected_activations"]),
            projected_sequences=len(full_result["projected_sequences"]),
            source_activators=full_result["summary"]["coverage"]["activators"]["source_activator_count"],
            eligible_activators=full_result["summary"]["coverage"]["activators"]["eligible_activator_count"],
            policy_excluded_activators=full_result["summary"]["coverage"]["activators"]["policy_excluded_activator_count"],
            source_activations=full_result["summary"]["coverage"]["activations"]["source_activation_count"],
            eligible_activations=full_result["summary"]["coverage"]["activations"]["eligible_activation_count"],
            target_scope_excluded=full_result["summary"]["coverage"]["activations"]["target_excluded_by_profile_scope_count"],
            target_source_policy_excluded=full_result["summary"]["coverage"]["activations"]["target_excluded_by_source_selection_policy_count"],
            failed_activations=full_result["summary"]["coverage"]["activations"]["failed_activation_count"],
        )
        print(f"Wrote projected temporal activation graph: {args.out}")
        return 0
    except Exception as exc:
        log_event(logger, "temporal_projection_rejected", error=str(exc))
        if args.debug:
            raise
        print(f"ERROR temporal_projection: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
