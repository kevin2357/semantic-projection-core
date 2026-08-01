from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .contracts import ProjectionRequest
from .engine import project
from .materialization import materialize_projected_graph
from .profiles import builtin_projection_registry


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Project a generic semantic projection request.")
    parser.add_argument("--request", required=True, help="ProjectionRequest JSON file")
    parser.add_argument("--out", required=True, help="Output JSON file")
    parser.add_argument("--output-mode", choices=("full", "standard", "summary", "forensic"), default="standard")
    parser.add_argument("--debug", action="store_true", help="Show tracebacks for rejected input")
    args = parser.parse_args(argv)
    try:
        payload = json.loads(Path(args.request).read_text(encoding="utf-8"))
        request = ProjectionRequest.from_dict(payload)
        result = project(request, registry=builtin_projection_registry()).to_dict()
        materialized = materialize_projected_graph(result, mode=args.output_mode)
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(materialized, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"Wrote {out}")
        return 0
    except Exception as exc:
        if args.debug:
            raise
        print(f"ERROR semantic_projection: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
