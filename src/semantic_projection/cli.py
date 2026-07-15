from __future__ import annotations

import argparse
import json
from pathlib import Path

from .contracts import ProjectionRequest
from .materialization import materialize_projected_graph
from .profiles import builtin_projection_registry
from .engine import project


def main() -> None:
    parser = argparse.ArgumentParser(description="Project a generic semantic projection request.")
    parser.add_argument("--request", required=True, help="ProjectionRequest JSON file")
    parser.add_argument("--out", required=True, help="Output JSON file")
    parser.add_argument("--output-mode", choices=("full", "standard", "summary", "forensic"), default="standard")
    args = parser.parse_args()
    payload = json.loads(Path(args.request).read_text(encoding="utf-8"))
    request = ProjectionRequest.from_dict(payload)
    result = project(request, registry=builtin_projection_registry()).to_dict()
    materialized = materialize_projected_graph(result, mode=args.output_mode)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(materialized, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
