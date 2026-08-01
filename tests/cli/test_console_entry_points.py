from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

from semantic_projection import (
    ProjectionContext,
    adapt_foundry_temporal_source_bundle,
    temporal_cli,
    temporal_foundations_cli,
    temporal_pipeline_cli,
    temporal_projection_cli,
)
from semantic_projection import cli as static_cli
from tests.paths import EXAMPLES_ROOT, FIXTURES_ROOT, REPO_ROOT

MODULE_ENTRY_POINTS = (
    "semantic_projection.cli",
    "semantic_projection.temporal_cli",
    "semantic_projection.temporal_foundations_cli",
    "semantic_projection.temporal_projection_cli",
    "semantic_projection.temporal_pipeline_cli",
)
TOOL_ENTRY_POINTS = (
    "tools/project_natal.py",
    "tools/project_synastry.py",
    "tools/project_temporal.py",
    "tools/woofmap_natal.py",
    "tools/woofmap_synastry.py",
    "tools/woofmap_transit.py",
)


def run_help(command: list[str]) -> subprocess.CompletedProcess[str]:
    environment = os.environ.copy()
    environment["PYTHONIOENCODING"] = "cp1252:strict"
    return subprocess.run(
        command,
        cwd=REPO_ROOT,
        env=environment,
        text=True,
        capture_output=True,
        timeout=30,
        check=False,
    )


@pytest.mark.subprocess
@pytest.mark.parametrize("module", MODULE_ENTRY_POINTS)
def test_installed_module_help_is_cp1252_safe(module):
    completed = run_help([sys.executable, "-m", module, "--help"])
    assert completed.returncode == 0, completed.stderr
    assert "usage:" in completed.stdout.lower()
    assert "Traceback" not in completed.stderr


@pytest.mark.subprocess
@pytest.mark.parametrize("tool", TOOL_ENTRY_POINTS)
def test_repository_tool_help_is_cp1252_safe(tool):
    completed = run_help([sys.executable, tool, "--help"])
    assert completed.returncode == 0, completed.stderr
    assert "usage:" in completed.stdout.lower()
    assert "Traceback" not in completed.stderr


def temporal_request(tmp_path: Path) -> Path:
    bundle = json.loads((FIXTURES_ROOT / "foundry_temporal_source_bundle_v1_tiny.json").read_text(encoding="utf-8"))
    context = ProjectionContext.from_dict(
        json.loads((EXAMPLES_ROOT / "contexts" / "cognitive_architecture_general_context.json").read_text(encoding="utf-8"))
    )
    request = adapt_foundry_temporal_source_bundle(
        bundle,
        profile_id="cognitive_architecture_demo.v0",
        profile_version="0.2.0",
        context=context,
    )
    path = tmp_path / "temporal-request.json"
    path.write_text(json.dumps(request.to_dict()), encoding="utf-8")
    return path


@pytest.mark.integration
def test_static_cli_writes_requested_materialization(monkeypatch, tmp_path):
    payload = json.loads((FIXTURES_ROOT / "projection" / "empty_projection_request.json").read_text(encoding="utf-8"))
    payload["context"]["target_domain"] = "orthodox_astrology.v1"
    request = tmp_path / "request.json"
    request.write_text(json.dumps(payload), encoding="utf-8")
    output = tmp_path / "static-summary.json"
    monkeypatch.setattr(sys, "argv", ["semantic-project", "--request", str(request), "--output-mode", "summary", "--out", str(output)])
    assert static_cli.main() == 0
    artifact = json.loads(output.read_text(encoding="utf-8"))
    assert artifact["metadata"]["materialization_mode"] == "summary"


@pytest.mark.integration
def test_temporal_foundations_and_projection_clis(tmp_path):
    request = temporal_request(tmp_path)
    foundations = tmp_path / "foundations.json"
    projected = tmp_path / "projected.json"
    assert temporal_foundations_cli.main(["--request", str(request), "--out", str(foundations)]) == 0
    assert temporal_projection_cli.main(["--request", str(request), "--output-mode", "summary", "--out", str(projected)]) == 0
    assert json.loads(foundations.read_text(encoding="utf-8"))["metadata"]["package_type"] == "projected_temporal_foundations"
    assert json.loads(projected.read_text(encoding="utf-8"))["metadata"]["materialization_mode"] == "summary"


@pytest.mark.integration
def test_temporal_intake_cli_writes_request(monkeypatch, tmp_path):
    bundle = FIXTURES_ROOT / "foundry_temporal_source_bundle_v1_tiny.json"
    context = EXAMPLES_ROOT / "contexts" / "cognitive_architecture_general_context.json"
    output = tmp_path / "request.json"
    log = tmp_path / "intake.log"
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "semantic-temporal-intake",
            "--bundle",
            str(bundle),
            "--projection-profile",
            "cognitive_architecture_demo.v0",
            "--projection-profile-version",
            "0.2.0",
            "--projection-context",
            str(context),
            "--out",
            str(output),
            "--log-file",
            str(log),
        ],
    )
    assert temporal_cli.main() == 0
    assert json.loads(output.read_text(encoding="utf-8"))["request_contract"] == "temporal_projection_request.v1"
    assert "temporal_intake_complete" in log.read_text(encoding="utf-8")


def test_static_and_temporal_intake_clis_reject_malformed_json_cleanly(tmp_path, capsys):
    bad = tmp_path / "bad.json"
    bad.write_text("not-json", encoding="utf-8")
    output = tmp_path / "output.json"
    assert static_cli.main(["--request", str(bad), "--out", str(output)]) == 2
    static_error = capsys.readouterr().err
    assert "ERROR semantic_projection" in static_error
    assert "Traceback" not in static_error

    context = EXAMPLES_ROOT / "contexts" / "cognitive_architecture_general_context.json"
    assert (
        temporal_cli.main(
            [
                "--bundle",
                str(bad),
                "--projection-profile",
                "cognitive_architecture_demo.v0",
                "--projection-profile-version",
                "0.2.0",
                "--projection-context",
                str(context),
                "--out",
                str(output),
                "--log-file",
                str(tmp_path / "intake.log"),
            ]
        )
        == 2
    )
    temporal_error = capsys.readouterr().err
    assert "ERROR temporal_source_contract" in temporal_error
    assert "Traceback" not in temporal_error


@pytest.mark.integration
def test_temporal_pipeline_cli_success_and_clean_rejection(tmp_path, capsys):
    bundle = FIXTURES_ROOT / "foundry_temporal_source_bundle_v1_tiny.json"
    context = EXAMPLES_ROOT / "contexts" / "cognitive_architecture_general_context.json"
    output = tmp_path / "projected.json"
    receipt = tmp_path / "receipt.json"
    args = [
        "--bundle",
        str(bundle),
        "--projection-profile",
        "cognitive_architecture_demo.v0",
        "--projection-profile-version",
        "0.2.0",
        "--projection-context",
        str(context),
        "--out",
        str(output),
        "--receipt-out",
        str(receipt),
    ]
    assert temporal_pipeline_cli.main(args) == 0
    assert output.exists() and receipt.exists()

    bad = tmp_path / "bad.json"
    bad.write_text("{}", encoding="utf-8")
    assert temporal_pipeline_cli.main([*args[:1], str(bad), *args[2:]]) == 2
    captured = capsys.readouterr()
    assert "ERROR temporal_pipeline" in captured.err
    assert "Traceback" not in captured.err
