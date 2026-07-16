from __future__ import annotations

import argparse
import json
from copy import deepcopy
from pathlib import Path
from typing import Any

from semantic_projection import (
    materialize_projected_graph,
    project_synastry,
)
from semantic_projection.profiles import builtin_projection_registry


JsonDict = dict[str, Any]


def read_json(path: Path) -> JsonDict:
    return json.loads(path.read_text(encoding="utf-8"))


def extract_graph(package: JsonDict) -> JsonDict:
    graph = (
        package.get("canonical_astrology_graph")
        or package.get("canonical_source_graph")
        or package.get("source_graph")
    )
    if not graph:
        raise ValueError(
            "The Synastry dataset does not contain a complete canonical graph. "
            "Expected canonical_astrology_graph, canonical_source_graph, or source_graph."
        )

    if not graph.get("objects") or "relationships" not in graph:
        raise ValueError(
            "The canonical Synastry graph is incomplete. "
            "A refs-only streaming artifact must be hydrated before projection."
        )

    return deepcopy(graph)


def extract_structural_evidence(package: JsonDict) -> JsonDict:
    return deepcopy(
        package.get("structural_evidence_graph")
        or package.get("structural_evidence")
        or {}
    )


def extract_source_identity(package: JsonDict, graph: JsonDict) -> JsonDict:
    metadata = package.get("metadata") or {}
    graph_metadata = graph.get("metadata") or {}

    source_chart_ids = (
        metadata.get("source_chart_ids")
        or graph_metadata.get("source_chart_ids")
        or []
    )

    source_chart_id = (
        metadata.get("source_chart_id")
        or graph_metadata.get("source_chart_id")
    )

    if source_chart_id and source_chart_id not in source_chart_ids:
        source_chart_ids = [source_chart_id, *source_chart_ids]

    return {
        "source_chart_id": source_chart_id,
        "source_chart_ids": source_chart_ids,
        "sensor_instance_id": (
            metadata.get("sensor_instance_id")
            or graph_metadata.get("sensor_instance_id")
        ),
        "source_graph_type": "synastry",
        "source_package_type": (
            metadata.get("package_type")
            or package.get("package_type")
            or package.get("analysis_type")
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Project a canonical Synastry dataset as dog–dog Woofmapped Synastry."
    )
    parser.add_argument("--source-dataset", required=True)
    parser.add_argument("--dog-a-id", required=True)
    parser.add_argument("--dog-a-label", required=True)
    parser.add_argument("--dog-b-id", required=True)
    parser.add_argument("--dog-b-label", required=True)
    parser.add_argument(
        "--context",
        default="examples/contexts/woofmapped_dog_dog_synastry_asymmetric_context.json",
    )
    parser.add_argument(
        "--output-mode",
        choices=("full", "standard", "summary", "forensic"),
        default="standard",
    )
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    source_path = Path(args.source_dataset)
    package = read_json(source_path)
    graph = extract_graph(package)
    context = read_json(Path(args.context))

    participants = [
        {
            "participant_id": args.dog_a_id,
            "role": "dog",
            "species": "canine",
            "label": args.dog_a_label,
        },
        {
            "participant_id": args.dog_b_id,
            "role": "dog",
            "species": "canine",
            "label": args.dog_b_label,
        },
    ]

    result = project_synastry(
        source_graph=graph,
        structural_evidence=extract_structural_evidence(package),
        source_identity=extract_source_identity(package, graph),
        participants=participants,
        relationship_kind="dog_dog",
        profile_id="woofmapped_astrology.v0",
        profile_version="0.1.0",
        context=context,
        registry=builtin_projection_registry(),
    )

    output = materialize_projected_graph(
        result.artifact,
        mode=args.output_mode,
    )

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(
        json.dumps(output, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()