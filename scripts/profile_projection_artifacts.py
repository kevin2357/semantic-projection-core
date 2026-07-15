from __future__ import annotations

import argparse
import json
import time
from pathlib import Path
from typing import Any

from semantic_projection.artifact_identity import identify_artifact
from semantic_projection.ids import stable_hash


def _json_size(value: Any) -> int:
    return len(json.dumps(value, ensure_ascii=False, separators=(",", ":")).encode("utf-8"))


def profile(path: Path) -> dict[str, Any]:
    started = time.perf_counter()
    payload = json.loads(path.read_text(encoding="utf-8"))
    read_seconds = time.perf_counter() - started
    identity = identify_artifact(payload)
    row = {
        "path": str(path),
        "bytes": path.stat().st_size,
        "compact_json_bytes": _json_size(payload),
        "read_seconds": round(read_seconds, 6),
        "artifact_kind": identity.kind,
        "package_type": identity.package_type,
        "contract_version": identity.contract_version,
    }
    if identity.kind == "projected_temporal_activation_graph":
        activations = payload.get("projected_activations") or []
        states = [
            state
            for activation in activations
            for state in (activation.get("temporal_facts") or {}).get("observation_states") or []
        ]
        summary = payload.get("summary") or {}
        row.update({
            "materialization_mode": (payload.get("metadata") or {}).get("materialization_mode"),
            "projected_activator_count": len(payload.get("projected_activators") or []) or int(summary.get("projected_activator_count") or 0),
            "projected_activation_count": len(activations) or int(summary.get("projected_activation_count") or 0),
            "projected_sequence_count": len(payload.get("projected_sequences") or []) or int(summary.get("projected_sequence_count") or 0),
            "projected_state_count": len(states) or int(summary.get("projected_observation_state_count") or 0),
            "projected_target_graph_bytes": _json_size(payload.get("projected_target_graph") or {}),
            "projected_activation_bytes": _json_size(activations),
            "audit_bytes": _json_size(payload.get("audit") or {}),
            "diagnostics_bytes": _json_size(payload.get("diagnostics") or {}),
            "registry_bytes": _json_size(payload.get("projected_term_registry") or {}),
            "activator_hash": stable_hash(payload.get("projected_activators") or []),
            "activation_hash": stable_hash(activations),
            "sequence_hash": stable_hash(payload.get("projected_sequences") or []),
            "state_hash": stable_hash(states),
        })
    elif identity.kind in {"projection_qa_result", "temporal_projection_qa_result", "projection_forensic_audit"}:
        row["administrative_artifact"] = True
    return row


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Profile projection artifacts without misclassifying QA/admin JSON.")
    parser.add_argument("paths", nargs="+")
    parser.add_argument("--out", required=True)
    args = parser.parse_args(argv)
    rows = [profile(Path(value)) for value in args.paths]
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({"artifact_count": len(rows), "artifacts": rows}, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
