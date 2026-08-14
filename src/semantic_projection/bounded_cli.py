from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .bounded import adapt_foundry_bounded_natal_dataset
from .bounded_projection import project_bounded_natal
from .contracts import ProjectionContext
from .resources import load_bundled_context


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Project an AGF bounded natal dataset through Woofmapping."
    )
    parser.add_argument("--source", required=True, help="AGF bounded natal JSON file")
    parser.add_argument("--out", required=True, help="Projected bounded JSON file")
    parser.add_argument("--context-id", required=True, help="Exact bundled context ID")
    parser.add_argument(
        "--context-version", required=True, help="Exact bundled context version"
    )
    parser.add_argument(
        "--profile-id", default="woofmapped_bounded_astrology.v0"
    )
    parser.add_argument("--profile-version", default="0.1.0")
    parser.add_argument("--debug", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        source = json.loads(Path(args.source).read_text(encoding="utf-8"))
        context = ProjectionContext.from_dict(
            load_bundled_context(args.context_id, args.context_version)
        )
        request = adapt_foundry_bounded_natal_dataset(
            source,
            profile_id=args.profile_id,
            profile_version=args.profile_version,
            context=context,
        )
        result = project_bounded_natal(request).to_dict()
        output = Path(args.out)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(
            json.dumps(result, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        print(f"Wrote {output}")
        return 0
    except Exception as exc:
        if args.debug:
            raise
        print(f"ERROR semantic_bounded_projection: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
