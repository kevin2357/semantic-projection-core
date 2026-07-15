from __future__ import annotations

import ast
from pathlib import Path


def test_core_has_no_astrology_graph_foundry_imports():
    root = Path(__file__).parents[1] / "src" / "semantic_projection"
    offenders = []
    for path in root.rglob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            names = []
            if isinstance(node, ast.Import):
                names = [alias.name for alias in node.names]
            elif isinstance(node, ast.ImportFrom) and node.module:
                names = [node.module]
            for name in names:
                if name.startswith("astro_analysis_sdk"):
                    offenders.append(f"{path.relative_to(root)}:{name}")
    assert offenders == []
