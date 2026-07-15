from __future__ import annotations

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Any

DEFAULT_LOG_NAME = "semantic_projection.log"


def configure_logging(
    *,
    log_path: str | Path | None = None,
    level: int = logging.INFO,
    console: bool = False,
) -> logging.Logger:
    """Configure Core logging without requiring an external config file.

    Repeated calls are idempotent for the same resolved file path.
    """
    logger = logging.getLogger("semantic_projection")
    logger.setLevel(level)
    logger.propagate = False

    resolved = Path(log_path or DEFAULT_LOG_NAME).resolve()
    resolved.parent.mkdir(parents=True, exist_ok=True)
    marker = f"semantic_projection_file:{resolved}"
    if not any(getattr(handler, "_semantic_projection_marker", None) == marker for handler in logger.handlers):
        handler = RotatingFileHandler(
            resolved,
            maxBytes=5_000_000,
            backupCount=3,
            encoding="utf-8",
        )
        handler.setLevel(level)
        handler.setFormatter(logging.Formatter(
            "%(asctime)s %(levelname)s [%(name)s] %(message)s"
        ))
        handler._semantic_projection_marker = marker  # type: ignore[attr-defined]
        logger.addHandler(handler)

    if console and not any(getattr(h, "_semantic_projection_console", False) for h in logger.handlers):
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        console_handler.setFormatter(logging.Formatter("%(levelname)s %(message)s"))
        console_handler._semantic_projection_console = True  # type: ignore[attr-defined]
        logger.addHandler(console_handler)

    logger.debug("Logging configured: %s", resolved)
    return logger


def log_event(logger: logging.Logger, event: str, **fields: Any) -> None:
    payload = " ".join(f"{key}={value!r}" for key, value in sorted(fields.items()))
    logger.info("%s%s", event, f" {payload}" if payload else "")
