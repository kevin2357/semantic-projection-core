from __future__ import annotations

import importlib.util
import sys

from tests.paths import REPO_ROOT


def load_runner():
    path = REPO_ROOT / "scripts" / "run_qa.py"
    spec = importlib.util.spec_from_file_location("spc_run_qa", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_qa_runner_uses_capability_paths_and_optional_coverage():
    runner = load_runner()
    command = runner.command_for("temporal", coverage=True)
    assert command[:4] == [sys.executable, "-m", "pytest", "-q"]
    assert "tests/temporal" in command
    assert "--cov-branch" in command
    assert all("chunk" not in part.lower() for part in command)


def test_qa_runner_exposes_all_durable_suites():
    runner = load_runner()
    assert set(runner.SUITES) == {"all", "static", "temporal", "woofmapped", "cli", "integration"}
