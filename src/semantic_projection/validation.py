from __future__ import annotations

import json
from importlib.resources import files
from typing import Any

SCHEMA_PACKAGE = "semantic_projection.schemas"
SUPPORTED_SOURCE_GRAPH_VERSIONS = {"1.3.0"}


class ProjectionValidationError(ValueError):
    pass


def load_schema(schema_name: str) -> dict[str, Any]:
    resource = files(SCHEMA_PACKAGE).joinpath(schema_name)
    return json.loads(resource.read_text(encoding="utf-8"))


def _manual_required_check(value: dict[str, Any], schema: dict[str, Any]) -> None:
    missing = [key for key in schema.get("required", []) if key not in value]
    if missing:
        raise ProjectionValidationError(f"Missing required fields: {', '.join(missing)}")


def validate_contract(value: dict[str, Any], schema_name: str) -> None:
    schema = load_schema(schema_name)
    try:
        from jsonschema import Draft202012Validator
    except ImportError:
        _manual_required_check(value, schema)
        return
    try:
        from referencing import Registry, Resource
        registry = Registry()
        schema_root = files(SCHEMA_PACKAGE)
        for resource in schema_root.iterdir():
            if resource.name.endswith(".schema.json"):
                content = json.loads(resource.read_text(encoding="utf-8"))
                registry = registry.with_resource(
                    resource.name, Resource.from_contents(content)
                )
        validator = Draft202012Validator(schema, registry=registry)
    except ImportError:
        validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(value), key=lambda error: list(error.path))
    if errors:
        first = errors[0]
        path = ".".join(str(part) for part in first.path) or "<root>"
        raise ProjectionValidationError(f"{schema_name} validation failed at {path}: {first.message}")


def validate_projection_request(request: dict[str, Any]) -> None:
    validate_contract(request, "projection_request_v1.schema.json")
    graph = request.get("source_graph") or {}
    graph_version = graph.get("graph_version")
    if graph_version not in SUPPORTED_SOURCE_GRAPH_VERSIONS:
        raise ProjectionValidationError(
            f"Unsupported canonical source graph version {graph_version!r}; "
            f"supported versions: {sorted(SUPPORTED_SOURCE_GRAPH_VERSIONS)}"
        )
    context = request.get("context") or {}
    if context.get("target_domain") and request.get("profile_id", "").split(".")[0] == "":
        raise ProjectionValidationError("profile_id must be non-empty")


def validate_projected_graph_ids(graph: dict[str, Any]) -> None:
    for field in ("objects", "relationships"):
        ids = [row.get("id") for row in graph.get(field) or []]
        duplicates = sorted({value for value in ids if value is not None and ids.count(value) > 1})
        if duplicates:
            raise ProjectionValidationError(f"Duplicate {field} IDs: {duplicates[:5]}")
