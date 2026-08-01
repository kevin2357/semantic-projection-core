from __future__ import annotations

import json
import logging

import pytest

from semantic_projection import configure_logging, identify_artifact, log_event
from semantic_projection.io import read_json, write_json


def test_json_io_round_trip_and_rejects_non_object(tmp_path):
    path = tmp_path / "nested" / "value.json"
    write_json(path, {"woof": "mapped"})
    assert read_json(path) == {"woof": "mapped"}
    path.write_text("[1, 2, 3]", encoding="utf-8")
    with pytest.raises(ValueError, match="JSON object"):
        read_json(path)


def test_utf8_logging_replaces_handlers_and_emits_structured_fields(tmp_path):
    path = tmp_path / "projection.log"
    logger = configure_logging(log_path=path, level=logging.DEBUG)
    first_handlers = tuple(logger.handlers)
    log_event(logger, "projection_complete", dog="Bré", count=2)
    logger = configure_logging(log_path=path, level=logging.INFO)
    assert tuple(logger.handlers) == first_handlers
    for handler in logger.handlers:
        handler.flush()
    text = path.read_text(encoding="utf-8")
    assert "projection_complete" in text
    assert "Bré" in text
    assert "count=2" in text


def test_logging_can_add_one_idempotent_console_handler(tmp_path, capsys):
    logger = configure_logging(log_path=tmp_path / "console.log", console=True)
    logger = configure_logging(log_path=tmp_path / "console.log", console=True)
    console_handlers = [handler for handler in logger.handlers if getattr(handler, "_semantic_projection_console", False)]
    assert len(console_handlers) == 1
    log_event(logger, "console_event", value=1)
    for handler in console_handlers:
        handler.flush()
    assert "console_event" in capsys.readouterr().err


@pytest.mark.parametrize(
    ("artifact", "kind"),
    [
        ({"metadata": {"package_type": "projected_semantic_graph"}}, "projected_static_graph"),
        ({"metadata": {"package_type": "projected_temporal_activation_graph"}}, "projected_temporal_activation_graph"),
        ({"metadata": {"package_type": "temporal_projection_route_receipt"}}, "temporal_projection_route_receipt"),
        (
            {"request_id": "projection_request:test", "profile_id": "test", "source_graph": {}, "context": {}},
            "projection_request",
        ),
        ({"unexpected": True}, "unknown"),
    ],
)
def test_artifact_identity_matrix(artifact, kind):
    assert identify_artifact(artifact).kind == kind
    assert isinstance(json.loads(json.dumps(identify_artifact(artifact).to_dict())), dict)
