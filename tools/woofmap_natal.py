#!/usr/bin/env python3
"""Woofmap a canonical Natal/static graph with practical defaults."""

from __future__ import annotations

import sys
from pathlib import Path

from _projection_cli import run_main
from project_natal import main as project_natal_main

DEFAULT_CONTEXT = (
    Path(__file__).resolve().parents[1]
    / "examples"
    / "contexts"
    / "woofmapped_doghouse_general_context.json"
)


def projection_argv(argv: list[str]) -> list[str]:
    """Apply Woofmapped Natal defaults while allowing an explicit context override."""
    return ["--context", str(DEFAULT_CONTEXT), *argv, "--profile", "woofmapped"]


def main(argv: list[str] | None = None) -> int:
    return project_natal_main(projection_argv(list(argv if argv is not None else sys.argv[1:])))


if __name__ == "__main__":
    raise SystemExit(run_main(main))
