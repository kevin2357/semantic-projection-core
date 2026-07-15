from __future__ import annotations

import hashlib
import json
import os
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
        raise RuntimeError(
            f"Command returned {result.returncode}, expected {expected}: {' '.join(command)}"
        )
    return result


def artifact_identity(path: Path) -> tuple[str | None, str | None]:
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

    pytest_log = OUTPUTS / "pytest.log"
    run([sys.executable, "-m", "pytest", "-q"], pytest_log)

    candidates = []
    inventory = []
    for path in sorted(FIXTURES.glob("*.json")):
        package_type, contract_version = artifact_identity(path)
        inventory.append({
            "path": str(path.relative_to(ROOT)),
            "package_type": package_type,
            "contract_version": contract_version,
        })
        if package_type == "temporal_projection_source_bundle":
            candidates.append(path)
    (OUTPUTS / "fixture_inventory.json").write_text(
        json.dumps(inventory, indent=2) + "\n", encoding="utf-8"
    )
    if len(candidates) != 1:
        raise RuntimeError(
            "Expected exactly one temporal_projection_source_bundle fixture; "
            f"found {len(candidates)}."
        )

    bundle = candidates[0]
    request = OUTPUTS / "temporal_request.json"
    log_file = OUTPUTS / "semantic_projection.log"
    run([
        sys.executable, "-m", "semantic_projection.temporal_cli",
        "--bundle", str(bundle),
        "--projection-profile", "cognitive_architecture_demo.v0",
        "--projection-profile-version", "0.2.0",
        "--projection-context", str(ROOT / "examples/contexts/cognitive_architecture_general_context.json"),
        "--log-file", str(log_file),
        "--out", str(request),
    ], OUTPUTS / "intake.log")

    run1 = OUTPUTS / "projected_temporal_run1.json"
    run2 = OUTPUTS / "projected_temporal_run2.json"
    base = [
        sys.executable, "-m", "semantic_projection.temporal_projection_cli",
        "--request", str(request),
        "--log-file", str(log_file),
    ]
    run(base + ["--out", str(run1)], OUTPUTS / "projection_run1.log")
    run(base + ["--out", str(run2)], OUTPUTS / "projection_run2.log")

    bytes1, bytes2 = run1.read_bytes(), run2.read_bytes()
    determinism = {
        "byte_identical": bytes1 == bytes2,
        "bytes": len(bytes1),
        "sha256_run1": hashlib.sha256(bytes1).hexdigest(),
        "sha256_run2": hashlib.sha256(bytes2).hexdigest(),
    }
    (OUTPUTS / "determinism_result.json").write_text(
        json.dumps(determinism, indent=2) + "\n", encoding="utf-8"
    )
    if not determinism["byte_identical"]:
        raise RuntimeError("Projected temporal outputs are not byte-identical.")

    wrong_out = OUTPUTS / "wrong_artifact_should_not_exist.json"
    wrong = run([
        sys.executable, "-m", "semantic_projection.temporal_projection_cli",
        "--request", str(bundle),
        "--log-file", str(log_file),
        "--out", str(wrong_out),
    ], OUTPUTS / "wrong_artifact.log", expected=2)

    graph = json.loads(run1.read_text(encoding="utf-8"))
    coverage = graph["summary"]["coverage"]
    qa_summary = {
        "status": "passed",
        "pytest": "passed",
        "fixture_count": len(candidates),
        "temporal_projection_id": graph["metadata"]["temporal_projection_id"],
        "projected_activator_count": len(graph["projected_activators"]),
        "projected_activation_count": len(graph["projected_activations"]),
        "projected_sequence_count": len(graph["projected_sequences"]),
        "projected_observation_state_count": graph["summary"]["projected_observation_state_count"],
        "activator_coverage": coverage["activators"],
        "activation_coverage": coverage["activations"],
        "determinism": determinism,
        "wrong_artifact_exit_code": wrong.returncode,
        "wrong_artifact_output_absent": not wrong_out.exists(),
    }
    (OUTPUTS / "qa_summary.json").write_text(
        json.dumps(qa_summary, indent=2) + "\n", encoding="utf-8"
    )
    print("Chunk 3.beta.4 QA passed.")
    print(f"Wrote outputs to {OUTPUTS}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
