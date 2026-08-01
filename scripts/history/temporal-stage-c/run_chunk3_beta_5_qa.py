from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "outputs" / "fixture_test_files"
OUTPUTS = ROOT / "outputs" / "fixture_outputs"


def run(command: list[str], log_path: Path, expected: int = 0) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, encoding="utf-8")
    log_path.write_text(
        "$ " + " ".join(command) + "\n\nSTDOUT\n" + result.stdout +
        "\nSTDERR\n" + result.stderr + f"\nEXIT_CODE={result.returncode}\n",
        encoding="utf-8",
    )
    if result.returncode != expected:
        raise RuntimeError(f"Command returned {result.returncode}, expected {expected}: {' '.join(command)}")
    return result


def identity(path: Path) -> tuple[str | None, str | None]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    metadata = payload.get("metadata") or {}
    return metadata.get("package_type"), metadata.get("contract_version")


def main() -> int:
    OUTPUTS.mkdir(parents=True, exist_ok=True)
    for path in OUTPUTS.iterdir():
        if path.is_file():
            path.unlink()
        elif path.is_dir():
            shutil.rmtree(path)

    run([sys.executable, "-m", "pytest", "-q"], OUTPUTS / "pytest.log")
    candidates = []
    inventory = []
    for path in sorted(FIXTURES.glob("*.json")):
        package_type, contract_version = identity(path)
        inventory.append({"path": str(path.relative_to(ROOT)), "package_type": package_type, "contract_version": contract_version})
        if package_type == "temporal_projection_source_bundle":
            candidates.append(path)
    (OUTPUTS / "fixture_inventory.json").write_text(json.dumps(inventory, indent=2) + "\n", encoding="utf-8")
    if len(candidates) != 1:
        raise RuntimeError(f"Expected exactly one temporal_projection_source_bundle fixture; found {len(candidates)}.")

    bundle = candidates[0]
    request = OUTPUTS / "temporal_request.json"
    core_log = OUTPUTS / "semantic_projection.log"
    run([
        sys.executable, "-m", "semantic_projection.temporal_cli",
        "--bundle", str(bundle),
        "--projection-profile", "cognitive_architecture_demo.v0",
        "--projection-profile-version", "0.2.0",
        "--projection-context", str(ROOT / "examples/contexts/cognitive_architecture_general_context.json"),
        "--log-file", str(core_log),
        "--out", str(request),
    ], OUTPUTS / "intake.log")

    outputs = {}
    full_out = OUTPUTS / "projected_temporal.full.json"
    run([
        sys.executable, "-m", "semantic_projection.temporal_projection_cli",
        "--request", str(request), "--output-mode", "full",
        "--log-file", str(core_log), "--out", str(full_out),
    ], OUTPUTS / "projection_full.log")
    outputs["full"] = full_out

    from semantic_projection.materialization import materialize_projected_temporal_graph
    full_payload = json.loads(full_out.read_text(encoding="utf-8"))
    for mode in ("standard", "summary", "forensic"):
        out = OUTPUTS / f"projected_temporal.{mode}.json"
        materialized = materialize_projected_temporal_graph(full_payload, mode=mode)
        out.write_text(json.dumps(materialized, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        outputs[mode] = out

    repeat = OUTPUTS / "projected_temporal.standard.run2.json"
    repeat_payload = materialize_projected_temporal_graph(full_payload, mode="standard")
    repeat.write_text(json.dumps(repeat_payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    b1, b2 = outputs["standard"].read_bytes(), repeat.read_bytes()
    determinism = {
        "byte_identical": b1 == b2,
        "bytes": len(b1),
        "sha256_run1": hashlib.sha256(b1).hexdigest(),
        "sha256_run2": hashlib.sha256(b2).hexdigest(),
    }
    (OUTPUTS / "determinism_result.json").write_text(json.dumps(determinism, indent=2) + "\n", encoding="utf-8")
    if not determinism["byte_identical"]:
        raise RuntimeError("Standard materializations are not byte-identical.")

    profile_paths = [str(path) for path in outputs.values()]
    profile_out = OUTPUTS / "artifact_profile.json"
    run([sys.executable, str(ROOT / "scripts/profile_projection_artifacts.py"), *profile_paths, "--out", str(profile_out)], OUTPUTS / "profiler.log")

    full = json.loads(outputs["full"].read_text(encoding="utf-8"))
    standard = json.loads(outputs["standard"].read_text(encoding="utf-8"))
    forensic = json.loads(outputs["forensic"].read_text(encoding="utf-8"))
    qa = {
        "metadata": {"package_type": "temporal_projection_qa_result", "contract_version": "1.0.0"},
        "status": "passed",
        "pytest": "passed",
        "temporal_projection_id": full["metadata"]["temporal_projection_id"],
        "coverage": full["summary"]["coverage"],
        "reconciliation": full["summary"]["reconciliation"],
        "diagnostics_summary": full["diagnostics"]["summary"],
        "materialization_bytes": {mode: path.stat().st_size for mode, path in outputs.items()},
        "semantic_hash_reconciliation": {
            "full_vs_standard_activations": hashlib.sha256(json.dumps(full["projected_activations"], sort_keys=True).encode()).hexdigest() == hashlib.sha256(json.dumps(standard["projected_activations"], sort_keys=True).encode()).hexdigest(),
            "full_vs_forensic_activations": hashlib.sha256(json.dumps(full["projected_activations"], sort_keys=True).encode()).hexdigest() == hashlib.sha256(json.dumps(forensic["projected_activations"], sort_keys=True).encode()).hexdigest(),
        },
        "determinism": determinism,
    }
    (OUTPUTS / "qa_summary.json").write_text(json.dumps(qa, indent=2) + "\n", encoding="utf-8")
    print("Chunk 3.beta.5 QA passed.")
    print(f"Wrote outputs to {OUTPUTS}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
