from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
import traceback
from pathlib import Path
from typing import Any

from semantic_projection import ProjectionContext, project_foundry_temporal_bundle
from semantic_projection.artifact_identity import identify_artifact

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "outputs" / "fixture_test_files"
OUTPUTS = ROOT / "outputs" / "fixture_outputs"


def write_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_context(name: str) -> ProjectionContext:
    return ProjectionContext.from_dict(
        json.loads((ROOT / "examples" / "contexts" / name).read_text(encoding="utf-8"))
    )


def run_pytest() -> dict[str, Any]:
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "-q"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        encoding="utf-8",
    )
    (OUTPUTS / "pytest.log").write_text(
        result.stdout + result.stderr + f"\nEXIT_CODE={result.returncode}\n",
        encoding="utf-8",
    )
    return {"exit_code": result.returncode, "passed": result.returncode == 0}


def find_bundle() -> Path:
    rows = []
    found = []
    for path in sorted(FIXTURES.glob("*.json")):
        payload = json.loads(path.read_text(encoding="utf-8"))
        identity = identify_artifact(payload)
        rows.append({"path": str(path.relative_to(ROOT)), **identity.to_dict()})
        if identity.kind == "foundry_temporal_projection_source_bundle":
            found.append(path)
    write_json(OUTPUTS / "fixture_inventory.json", {"artifacts": rows})
    if len(found) != 1:
        raise RuntimeError(f"Expected exactly one Foundry temporal source bundle; found {len(found)}.")
    return found[0]


def project_profile(bundle: dict[str, Any], profile_id: str, profile_version: str, context_name: str, stem: str, *, repeat: bool):
    context = load_context(context_name)
    first = project_foundry_temporal_bundle(
        bundle,
        profile_id=profile_id,
        profile_version=profile_version,
        context=context,
        output_mode="standard",
    )
    second = (
        project_foundry_temporal_bundle(
            bundle,
            profile_id=profile_id,
            profile_version=profile_version,
            context=context,
            output_mode="standard",
        )
        if repeat
        else None
    )
    out1 = OUTPUTS / f"{stem}.standard.json"
    out2 = OUTPUTS / f"{stem}.standard.run2.json"
    write_json(out1, first.artifact)
    if second is not None:
        write_json(out2, second.artifact)
    write_json(OUTPUTS / f"{stem}.summary.json", {
        "profile_id": profile_id,
        "profile_version": profile_version,
        "receipt": first.receipt,
        "target_object_count": len(first.artifact["projected_target_graph"]["objects"]),
        "target_relationship_count": len(first.artifact["projected_target_graph"]["relationships"]),
        "projected_activator_count": len(first.artifact["projected_activators"]),
        "projected_activation_count": len(first.artifact["projected_activations"]),
        "coverage": first.artifact["audit"]["coverage"],
    })
    same = None if second is None else out1.read_bytes() == out2.read_bytes()
    return {
        "profile_id": profile_id,
        "profile_version": profile_version,
        "byte_identical": same,
        "sha256_run1": sha256(out1),
        "sha256_run2": sha256(out2) if second is not None else None,
        "determinism_repeat_executed": second is not None,
        "size_bytes": out1.stat().st_size,
        "target_object_count": len(first.artifact["projected_target_graph"]["objects"]),
        "target_relationship_count": len(first.artifact["projected_target_graph"]["relationships"]),
        "projected_activator_count": len(first.artifact["projected_activators"]),
        "projected_activation_count": len(first.artifact["projected_activations"]),
        "route_hash": first.receipt["metadata"]["route_hash"],
    }


def main() -> int:
    shutil.rmtree(OUTPUTS, ignore_errors=True)
    OUTPUTS.mkdir(parents=True, exist_ok=True)
    summary = {"stage": "C8", "status": "failed"}
    try:
        summary["pytest"] = run_pytest()
        if not summary["pytest"]["passed"]:
            raise RuntimeError("pytest failed")
        fixture = find_bundle()
        bundle = json.loads(fixture.read_text(encoding="utf-8"))
        orthodox = project_profile(
            bundle,
            "orthodox_astrology.v1",
            "1.0.0",
            "orthodox_general_context.json",
            "orthodox_expanded",
            repeat=True,
        )
        woof = project_profile(
            bundle,
            "woofmapped_astrology.v0",
            "0.1.0",
            "woofmapped_doghouse_general_context.json",
            "woofmapped_temporal",
            repeat=False,
        )
        if orthodox["byte_identical"] is not True:
            raise RuntimeError("Orthodox deterministic repeat failed.")
        if orthodox["target_object_count"] < 188 or orthodox["projected_activation_count"] != 88:
            raise RuntimeError("Orthodox expanded coverage did not meet the C8 reference-fixture contract.")
        if woof["projected_activation_count"] != 54:
            raise RuntimeError("Woofmapped temporal reference coverage changed unexpectedly.")
        summary.update({
            "status": "passed",
            "fixture": str(fixture.relative_to(ROOT)),
            "orthodox": orthodox,
            "woofmapped": woof,
            "all_executed_determinism_checks_passed": True,
            "all_routes_determinism_tested": all(
                row["determinism_repeat_executed"] for row in (orthodox, woof)
            ),
        })
        write_json(OUTPUTS / "qa_summary.json", summary)
        return 0
    except Exception as exc:
        summary["error"] = str(exc)
        summary["traceback"] = traceback.format_exc()
        write_json(OUTPUTS / "qa_summary.json", summary)
        print(summary["traceback"], file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
