from __future__ import annotations

from typing import Any

from .contracts import ProjectionDiagnostics


def diagnostic(code: str, message: str, *, path: str | None = None, details: dict[str, Any] | None = None) -> dict[str, Any]:
    value: dict[str, Any] = {"code": code, "message": message}
    if path is not None:
        value["path"] = path
    if details:
        value["details"] = details
    return value


def empty_diagnostics() -> ProjectionDiagnostics:
    return ProjectionDiagnostics()
