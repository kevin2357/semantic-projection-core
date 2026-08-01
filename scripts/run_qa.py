#!/usr/bin/env python3
"""Run stable Semantic Projection Core QA suites by capability."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SUITES = {
    "all": ["tests"],
    "static": [
        "tests/contracts",
        "tests/engine",
        "tests/materialization",
        "tests/profiles",
        "tests/rendering",
        "tests/synastry",
    ],
    "temporal": ["tests/temporal"],
    "woofmapped": ["tests/profiles/woofmapped", "tests/synastry", "tests/cli/test_woofmapping_tools.py"],
    "cli": ["tests/cli"],
    "integration": ["tests/integration"],
}


def command_for(suite: str, *, coverage: bool = False) -> list[str]:
    command = [sys.executable, "-m", "pytest", "-q", *SUITES[suite]]
    if coverage:
        command.extend(["--cov=semantic_projection", "--cov-branch", "--cov-report=term-missing"])
    return command


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--suite", choices=tuple(SUITES), default="all")
    parser.add_argument("--coverage", action="store_true", help="Measure branch coverage for the selected suite")
    args = parser.parse_args(argv)
    completed = subprocess.run(command_for(args.suite, coverage=args.coverage), cwd=REPO_ROOT, check=False)
    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())
