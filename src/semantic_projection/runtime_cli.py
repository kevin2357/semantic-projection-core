"""Installed-runtime inspection command used by release qualification."""

from __future__ import annotations

import argparse
import json
import sys
from importlib import metadata
from pathlib import Path
from typing import Any

from . import ENGINE_VERSION, __version__
from .profiles import builtin_projection_registry
from .resources import bundled_contexts, semantic_resource_manifest
from .validation import validate_contract

DISTRIBUTION_NAME = "semantic-projection-core"


def _entry_points(group: str) -> list[dict[str, str]]:
    return [
        {"name": item.name, "value": item.value}
        for item in sorted(metadata.entry_points().select(group=group), key=lambda entry: entry.name)
        if item.dist and item.dist.metadata["Name"] == DISTRIBUTION_NAME
    ]


def _installation_metadata() -> tuple[str, bool]:
    distribution = metadata.distribution(DISTRIBUTION_NAME)
    editable = False
    direct_url = distribution.read_text("direct_url.json")
    if direct_url:
        editable = bool(json.loads(direct_url).get("dir_info", {}).get("editable"))
    return distribution.version, editable


def runtime_report() -> dict[str, Any]:
    distribution_version, editable = _installation_metadata()
    contexts = bundled_contexts()
    for context in contexts:
        from .resources import load_bundled_context
        validate_contract(
            load_bundled_context(context["context_id"], context["context_version"]),
            "projection_context_v1.schema.json",
        )

    discovered = builtin_projection_registry()
    discovered_count = discovered.discover_entry_points(replace=True)
    versions_aligned = distribution_version == ENGINE_VERSION == __version__
    return {
        "report_contract": "semantic_projection.runtime_smoke.v1",
        "status": "ok" if versions_aligned else "error",
        "distribution": {"name": DISTRIBUTION_NAME, "version": distribution_version, "editable": editable},
        "engine_version": ENGINE_VERSION,
        "package_version": __version__,
        "python": {"version": ".".join(map(str, sys.version_info[:3])), "executable": sys.executable},
        "module_file": str(Path(__file__).resolve()),
        "profiles": discovered.manifests(),
        "profile_entry_points_discovered": discovered_count,
        "contexts": contexts,
        "console_entry_points": _entry_points("console_scripts"),
        "profile_entry_points": _entry_points("semantic_projection.profiles"),
        "semantic_resources": semantic_resource_manifest(),
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Inspect and verify the installed SPC runtime.")
    parser.add_argument("--json", action="store_true", help="Emit the deterministic JSON report.")
    parser.add_argument("--require-installed", action="store_true", help="Reject editable installations.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        report = runtime_report()
    except Exception as exc:  # noqa: BLE001 - convert command-boundary failures to stable exit status
        print(f"semantic-runtime-smoke: {exc}", file=sys.stderr)
        return 2
    if args.require_installed and report["distribution"]["editable"]:
        print("semantic-runtime-smoke: editable installation is not an immutable runtime", file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        resources = report["semantic_resources"]
        print(
            f"semantic-projection-core {report['distribution']['version']}: {report['status']} "
            f"({resources['resource_count']} resources, {resources['sha256']})"
        )
    return 0 if report["status"] == "ok" else 2


if __name__ == "__main__":
    raise SystemExit(main())
