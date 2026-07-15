from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs" / "fixture_outputs"
CTX = ROOT / "examples" / "contexts"


def dump(path, value):
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_graph():
    return {
        "metadata": {"graph_type": "synastry"},
        "objects": [
            {"id": "human:saturn", "name": "Saturn", "object_type": "planet", "subject_owner": "human", "sign": "Libra", "house": 6},
            {"id": "dog:mars", "name": "Mars", "object_type": "planet", "subject_owner": "dog", "sign": "Aries", "house": 1},
            {"id": "dog:moon", "name": "Moon", "object_type": "luminary", "subject_owner": "dog", "sign": "Cancer", "house": 4},
        ],
        "relationships": [
            {"id": "syn:1", "source_id": "human:saturn", "target_id": "dog:mars", "aspect": "square", "orb": 1.2},
            {"id": "syn:2", "source_id": "dog:moon", "target_id": "human:saturn", "aspect": "trine", "orb": 2.0},
        ],
    }


def context(name):
    return json.loads((CTX / name).read_text(encoding="utf-8"))


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for p in OUT.iterdir():
        if p.is_file():
            p.unlink()

    env = dict(os.environ)
    env["PYTHONPATH"] = str(ROOT / "src") + os.pathsep + env.get("PYTHONPATH", "")
    test = subprocess.run([sys.executable, "-m", "pytest", "-q"], cwd=ROOT, env=env, capture_output=True, text=True)
    (OUT / "pytest.log").write_text(test.stdout + test.stderr, encoding="utf-8")
    if test.returncode:
        raise SystemExit(test.returncode)

    sys.path.insert(0, str(ROOT / "src"))
    from semantic_projection import project_synastry
    from semantic_projection.profiles import builtin_projection_registry

    participants = [
        {"participant_id": "human", "role": "handler", "species": "human"},
        {"participant_id": "dog", "role": "dog", "species": "canine"},
    ]
    routes = [
        ("woofmapped_human_dog", "woofmapped_astrology.v0", "0.1.0", "human_dog", "woofmapped_human_dog_synastry_context.json"),
        ("orthodox_synastry", "orthodox_astrology.v1", "1.0.0", "synastry", "orthodox_synastry_general_context.json"),
    ]
    summary = {"chunk": "3.beta.10", "pytest": "passed", "routes": {}}
    for name, pid, pver, kind, ctx in routes:
        values = []
        for run in (1, 2):
            result = project_synastry(
                source_graph=source_graph(), structural_evidence={},
                source_identity={"source_chart_ids": ["human", "dog"]},
                participants=participants, relationship_kind=kind,
                profile_id=pid, profile_version=pver, context=context(ctx),
                registry=builtin_projection_registry(),
            )
            path = OUT / f"{name}.run{run}.json"
            dump(path, result.artifact)
            values.append(path)
        summary["routes"][name] = {
            "byte_identical": values[0].read_bytes() == values[1].read_bytes(),
            "sha256_run1": sha(values[0]), "sha256_run2": sha(values[1]),
            "object_count": len(json.loads(values[0].read_text())["objects"]),
            "relationship_count": len(json.loads(values[0].read_text())["relationships"]),
        }

    dump(OUT / "context_inventory.json", {
        "hybrid": context("woofmapped_hybrid_horoscope_context.json"),
        "human_dog": context("woofmapped_human_dog_synastry_context.json"),
        "dog_dog": context("woofmapped_dog_dog_synastry_context.json"),
    })
    summary["overall_status"] = "passed" if all(v["byte_identical"] for v in summary["routes"].values()) else "failed"
    dump(OUT / "qa_summary.json", summary)
    return 0 if summary["overall_status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
