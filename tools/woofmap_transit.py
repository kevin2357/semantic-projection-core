#!/usr/bin/env python3
"""Woofmap a Foundry temporal bundle for a handler, dog, or hybrid audience."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from _projection_cli import run_main
from project_temporal import main as project_temporal_main

CONTEXT_FILES = {
    "handler": "woofmapped_handler_guidance_context.json",
    "dog": "woofmapped_dog_direct_context.json",
    "hybrid": "woofmapped_hybrid_horoscope_context.json",
}


def projection_argv(argv: list[str]) -> list[str]:
    if "--help" in argv or "-h" in argv:
        print("Woofmapped Transit option: --audience {handler,dog,hybrid} (default: handler)\n")
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--audience", choices=tuple(CONTEXT_FILES), default="handler")
    known, remaining = parser.parse_known_args(argv)
    context = (
        Path(__file__).resolve().parents[1]
        / "examples"
        / "contexts"
        / CONTEXT_FILES[known.audience]
    )
    return ["--context", str(context), *remaining, "--profile", "woofmapped"]


def main(argv: list[str] | None = None) -> int:
    return project_temporal_main(projection_argv(list(argv if argv is not None else sys.argv[1:])))


if __name__ == "__main__":
    raise SystemExit(run_main(main))
