from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "outputs" / "fixture_test_files"
OUTPUTS = ROOT / "outputs" / "fixture_outputs"
CONTEXT = ROOT / "examples" / "contexts" / "cognitive_architecture_general_context.json"


def run(command: list[str], *, log_name: str, expected_codes: set[int] = {0}) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        command,
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
    )
    (OUTPUTS / log_name).write_text(
        "$ " + " ".join(command) + "\n\nSTDOUT\n" + result.stdout +
        "\nSTDERR\n" + result.stderr + f"\nEXIT_CODE={result.returncode}\n",
        encoding="utf-8",
    )
    if result.returncode not in expected_codes:
        raise RuntimeError(f"Command failed ({result.returncode}): {' '.join(command)}")
    return result


def find_bundle() -> Path:
    candidates = sorted(FIXTURES.glob("*temporal_projection_source*.json"))
    if not candidates:
        candidates = sorted(FIXTURES.glob("*.json"))
    if not candidates:
        raise FileNotFoundError(
            f"Place a Foundry temporal_projection_source_bundle.v1 JSON under {FIXTURES}"
        )
    return candidates[0]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    OUTPUTS.mkdir(parents=True, exist_ok=True)
    for path in OUTPUTS.iterdir():
        if path.is_file():
            path.unlink()
        elif path.is_dir():
            shutil.rmtree(path)

    summary: dict[str, object] = {
        "qa_contract": "chunk3.beta.2",
        "started_at_epoch": time.time(),
        "fixture_directory": str(FIXTURES),
        "output_directory": str(OUTPUTS),
    }

    pytest_result = run(
        [sys.executable, "-m", "pytest", "-q"],
        log_name="pytest.log",
    )
    summary["pytest_passed"] = pytest_result.returncode == 0

    bundle = find_bundle()
    summary["bundle"] = str(bundle.relative_to(ROOT))
    run1 = OUTPUTS / "temporal_request_run1.json"
    run2 = OUTPUTS / "temporal_request_run2.json"
    core_log = OUTPUTS / "semantic_projection.log"

    base = [
        sys.executable, "-m", "semantic_projection.temporal_cli",
        "--bundle", str(bundle),
        "--projection-profile", "cognitive_architecture_demo.v0",
        "--projection-profile-version", "0.2.0",
        "--projection-context", str(CONTEXT),
        "--log-file", str(core_log),
    ]
    run(base + ["--out", str(run1)], log_name="positive_run1.log")
    run(base + ["--out", str(run2)], log_name="positive_run2.log")

    determinism = {
        "byte_identical": run1.read_bytes() == run2.read_bytes(),
        "bytes_run1": run1.stat().st_size,
        "bytes_run2": run2.stat().st_size,
        "sha256_run1": sha256(run1),
        "sha256_run2": sha256(run2),
    }
    (OUTPUTS / "determinism_result.json").write_text(
        json.dumps(determinism, indent=2) + "\n", encoding="utf-8"
    )
    summary["determinism"] = determinism

    bad = OUTPUTS / "temporal_source_bad_version.json"
    payload = json.loads(bundle.read_text(encoding="utf-8"))
    payload["metadata"]["contract_version"] = "9.0.0"
    bad.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    bad_out = OUTPUTS / "bad_version_should_not_exist.json"
    negative = run(
        [
            sys.executable, "-m", "semantic_projection.temporal_cli",
            "--bundle", str(bad),
            "--projection-profile", "cognitive_architecture_demo.v0",
            "--projection-profile-version", "0.2.0",
            "--projection-context", str(CONTEXT),
            "--out", str(bad_out),
            "--log-file", str(core_log),
        ],
        log_name="negative_version.log",
        expected_codes={2},
    )
    negative_result = {
        "exit_code": negative.returncode,
        "rejected_as_expected": negative.returncode == 2,
        "output_absent": not bad_out.exists(),
        "error_mentions_version": "Unsupported Foundry temporal bundle contract version" in negative.stderr,
    }
    (OUTPUTS / "negative_version_result.json").write_text(
        json.dumps(negative_result, indent=2) + "\n", encoding="utf-8"
    )
    summary["negative_version"] = negative_result

    # Contract-only C2 artifact. No temporal mappings are executed.
    from semantic_projection import projected_temporal_contract_skeleton
    request = json.loads(run1.read_text(encoding="utf-8"))
    static_graph = request["static_source_graph"]
    skeleton = projected_temporal_contract_skeleton(
        metadata={
            "package_type": "projected_temporal_activation_graph",
            "contract_version": "1.0.0",
            "temporal_projection_id": "temporal_projection:contract_skeleton",
            "static_projection_id": "projection:not_executed_in_c2",
            "engine_version": "0.6.0",
            "profile_id": request["profile_id"],
            "profile_version": request["profile_version"],
            "context_id": request["context"]["context_id"],
            "context_version": request["context"]["context_version"],
            "materialization_mode": "full",
        },
        source_identity=request["source_identity"],
        target_identity=request["target_identity"],
        period=request["temporal_source_graph"].get("period") or {},
        projected_target_graph={
            "metadata": {
                "package_type": "projected_semantic_graph",
                "projection_id": "projection:not_executed_in_c2",
            },
            "objects": [],
            "relationships": [],
            "source_graph_ref": {"graph_id": static_graph.get("graph_id")},
        },
        upstream_source_limitations=request.get("limitations") or [],
    ).to_dict()
    (OUTPUTS / "projected_temporal_contract_skeleton.json").write_text(
        json.dumps(skeleton, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    summary["contract_skeleton_valid"] = True
    summary["core_log_present"] = core_log.exists()
    summary["completed_at_epoch"] = time.time()
    summary["passed"] = bool(
        summary["pytest_passed"]
        and determinism["byte_identical"]
        and negative_result["rejected_as_expected"]
        and negative_result["output_absent"]
    )
    (OUTPUTS / "qa_summary.json").write_text(
        json.dumps(summary, indent=2) + "\n", encoding="utf-8"
    )
    print(f"Chunk 3.beta.2 QA complete. Attach: {OUTPUTS}")
    return 0 if summary["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
