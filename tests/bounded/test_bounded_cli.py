from __future__ import annotations

import json

from semantic_projection.bounded_cli import main
from tests.paths import FIXTURES_ROOT


def test_bounded_cli_projects_with_exact_bundled_context(tmp_path):
    output = tmp_path / "projected.json"
    exit_code = main(
        [
            "--source",
            str(FIXTURES_ROOT / "agf" / "bounded_natal_v1_tiny.json"),
            "--context-id",
            "woofmapped.doghouse.general.v0",
            "--context-version",
            "0.1.0",
            "--out",
            str(output),
        ]
    )

    assert exit_code == 0
    artifact = json.loads(output.read_text(encoding="utf-8"))
    assert artifact["metadata"]["output_contract"] == (
        "projected_bounded_semantic_graph.v1"
    )
    assert artifact["metadata"]["context_id"] == (
        "woofmapped.doghouse.general.v0"
    )
    assert artifact["metadata"]["engine_version"] == "0.11.0"


def test_bounded_cli_rejects_wrong_context_version_without_writing(tmp_path, capsys):
    output = tmp_path / "projected.json"
    exit_code = main(
        [
            "--source",
            str(FIXTURES_ROOT / "agf" / "bounded_natal_v1_tiny.json"),
            "--context-id",
            "woofmapped.doghouse.general.v0",
            "--context-version",
            "9.9.9",
            "--out",
            str(output),
        ]
    )

    assert exit_code == 2
    assert not output.exists()
    assert "does not resolve uniquely" in capsys.readouterr().err
