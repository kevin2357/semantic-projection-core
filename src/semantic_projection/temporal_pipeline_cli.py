from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .artifact_identity import identify_artifact
from .contracts import ProjectionContext, TemporalProjectionOptions
from .logging_config import configure_logging, log_event
from .temporal_pipeline import project_foundry_temporal_bundle


def _write(path: str | None, value: dict) -> None:
    if not path:
        return
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run the complete Foundry temporal bundle -> projected temporal artifact route.")
    parser.add_argument("--bundle", required=True)
    parser.add_argument("--projection-profile", required=True)
    parser.add_argument("--projection-profile-version", required=True)
    parser.add_argument("--projection-context", required=True)
    parser.add_argument("--output-mode", choices=["full", "standard", "summary", "forensic"], default="standard")
    parser.add_argument("--out", required=True, help="Projected temporal artifact")
    parser.add_argument("--request-out", help="Optional normalized temporal request")
    parser.add_argument("--receipt-out", help="Optional deterministic routing receipt")
    parser.add_argument("--omit-observation-states", action="store_true")
    parser.add_argument("--log-file")
    parser.add_argument("--debug", action="store_true")
    args = parser.parse_args(argv)
    logger = configure_logging(log_path=args.log_file)
    try:
        bundle = json.loads(Path(args.bundle).read_text(encoding="utf-8"))
        identity = identify_artifact(bundle)
        if identity.kind != "foundry_temporal_projection_source_bundle":
            raise ValueError(f"Expected temporal_projection_source_bundle.v1; received {identity.kind} ({identity.package_type!r}).")
        context = ProjectionContext.from_dict(json.loads(Path(args.projection_context).read_text(encoding="utf-8")))
        result = project_foundry_temporal_bundle(
            bundle,
            profile_id=args.projection_profile,
            profile_version=args.projection_profile_version,
            context=context,
            options=TemporalProjectionOptions(include_observation_states=not args.omit_observation_states),
            output_mode=args.output_mode,
        )
        _write(args.out, result.artifact)
        _write(args.request_out, result.request)
        _write(args.receipt_out, result.receipt)
        metadata = result.receipt["metadata"]
        log_event(
            logger,
            "temporal_pipeline_completed",
            source_bundle_id=metadata.get("source_bundle_id"),
            request_id=metadata.get("request_id"),
            projected_graph_id=metadata.get("projected_graph_id"),
            profile_id=metadata.get("profile_id"),
            context_id=metadata.get("context_id"),
            target_family=metadata.get("target_family"),
            output_mode=metadata.get("output_mode"),
            route_hash=metadata.get("route_hash"),
            source_activators=((metadata.get("coverage") or {}).get("activators") or {}).get("source_activator_count"),
            eligible_activators=((metadata.get("coverage") or {}).get("activators") or {}).get("eligible_activator_count"),
            projected_activators=((metadata.get("coverage") or {}).get("activators") or {}).get("mapped_eligible_activator_count"),
            profile_scope_excluded_activators=((metadata.get("coverage") or {}).get("activators") or {}).get(
                "profile_scope_excluded_activator_count"
            ),
            policy_excluded_activators=((metadata.get("coverage") or {}).get("activators") or {}).get("policy_excluded_activator_count"),
            eligible_but_unmapped_activators=((metadata.get("coverage") or {}).get("activators") or {}).get(
                "eligible_but_unmapped_activator_count"
            ),
            source_activations=((metadata.get("coverage") or {}).get("activations") or {}).get("source_activation_count"),
            eligible_activations=((metadata.get("coverage") or {}).get("activations") or {}).get("eligible_activation_count"),
            projected_activations=((metadata.get("coverage") or {}).get("activations") or {}).get("projected_activation_count"),
            target_scope_excluded=((metadata.get("coverage") or {}).get("activations") or {}).get("target_excluded_by_profile_scope_count"),
            target_source_policy_excluded=((metadata.get("coverage") or {}).get("activations") or {}).get(
                "target_excluded_by_source_selection_policy_count"
            ),
            target_eligible_but_unmapped=((metadata.get("coverage") or {}).get("activations") or {}).get(
                "target_eligible_but_unmapped_count"
            ),
            failed_activations=((metadata.get("coverage") or {}).get("activations") or {}).get("failed_activation_count"),
            output=args.out,
        )
        print(f"Wrote projected temporal artifact: {args.out}")
        if args.receipt_out:
            print(f"Wrote temporal routing receipt: {args.receipt_out}")
        return 0
    except Exception as exc:
        log_event(logger, "temporal_pipeline_rejected", error=str(exc))
        if args.debug:
            raise
        print(f"ERROR temporal_pipeline: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
