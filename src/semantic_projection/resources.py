"""Installed semantic-resource discovery and deterministic fingerprinting."""

from __future__ import annotations

import json
from collections.abc import Iterable, Mapping
from functools import lru_cache
from hashlib import sha256
from importlib import resources
from typing import Any

RESOURCE_ROOTS = ("contexts", "profiles", "release", "schemas")
RUNTIME_SUFFIXES = (".json", ".py")


def _walk_json(root, prefix: str) -> Iterable[tuple[str, bytes]]:
    for child in sorted(root.iterdir(), key=lambda item: item.name):
        path = f"{prefix}/{child.name}"
        if child.is_dir():
            yield from _walk_json(child, path)
        elif child.name.endswith(".json"):
            yield path, child.read_bytes()


def _walk_runtime(root, prefix: str = "") -> Iterable[tuple[str, bytes]]:
    for child in sorted(root.iterdir(), key=lambda item: item.name):
        path = f"{prefix}/{child.name}" if prefix else child.name
        if child.is_dir():
            if child.name != "__pycache__":
                yield from _walk_runtime(child, path)
        elif child.name.endswith(RUNTIME_SUFFIXES):
            yield path, child.read_bytes()


def _records(rows: Iterable[tuple[str, bytes]]) -> list[dict[str, Any]]:
    return [
        {"path": path, "sha256": sha256(content).hexdigest(), "size": len(content)}
        for path, content in rows
    ]


@lru_cache(maxsize=1)
def _semantic_resource_values() -> tuple[tuple[str, str, int], ...]:
    package_root = resources.files("semantic_projection")
    records = []
    for root_name in RESOURCE_ROOTS:
        records.extend(_records(_walk_json(package_root.joinpath(root_name), root_name)))
    return tuple((record["path"], record["sha256"], record["size"]) for record in records)


def semantic_resource_records() -> list[dict[str, Any]]:
    """Describe every packaged semantic-policy JSON resource in stable order."""
    return [
        {"path": path, "sha256": content_sha256, "size": size}
        for path, content_sha256, size in _semantic_resource_values()
    ]


@lru_cache(maxsize=1)
def _runtime_package_values() -> tuple[tuple[str, str, int], ...]:
    records = _records(_walk_runtime(resources.files("semantic_projection")))
    return tuple((record["path"], record["sha256"], record["size"]) for record in records)


def runtime_package_records() -> list[dict[str, Any]]:
    """Describe installed executable Python and semantic JSON package content."""
    return [
        {"path": path, "sha256": content_sha256, "size": size}
        for path, content_sha256, size in _runtime_package_values()
    ]


def aggregate_resource_records(records: Iterable[Mapping[str, Any]]) -> str:
    """Hash ordered resource identity records without depending on filesystem metadata."""
    digest = sha256()
    for record in sorted(records, key=lambda item: str(item["path"])):
        digest.update(str(record["path"]).encode("utf-8"))
        digest.update(b"\0")
        digest.update(str(record["sha256"]).encode("ascii"))
        digest.update(b"\n")
    return digest.hexdigest()


def semantic_resource_manifest() -> dict[str, Any]:
    return resource_set_manifest(semantic_resource_records())


def runtime_package_manifest() -> dict[str, Any]:
    return resource_set_manifest(runtime_package_records())


def resource_set_manifest(records: Iterable[Mapping[str, Any]]) -> dict[str, Any]:
    normalized = [dict(record) for record in records]
    return {
        "algorithm": "sha256(path + NUL + content_sha256 + LF)",
        "sha256": aggregate_resource_records(normalized),
        "resource_count": len(normalized),
        "resources": sorted(normalized, key=lambda item: str(item["path"])),
    }


def bundled_contexts() -> list[dict[str, Any]]:
    root = resources.files("semantic_projection.contexts")
    contexts = []
    for resource in sorted(root.iterdir(), key=lambda item: item.name):
        if resource.name.endswith(".json"):
            value = json.loads(resource.read_text(encoding="utf-8"))
            contexts.append({
                "resource": resource.name,
                "context_id": value["context_id"],
                "context_version": value["context_version"],
                "target_domain": value["target_domain"],
            })
    return contexts


def load_bundled_context(context_id: str, context_version: str) -> dict[str, Any]:
    """Resolve a bundled context by exact ID and version."""
    matches = [
        item for item in bundled_contexts()
        if item["context_id"] == context_id and item["context_version"] == context_version
    ]
    if len(matches) != 1:
        available = sorted(
            f"{item['context_id']}@{item['context_version']}" for item in bundled_contexts()
            if item["context_id"] == context_id
        )
        raise LookupError(
            f"Bundled context {context_id!r} does not resolve uniquely at version {context_version!r}; "
            f"available versions: {available}"
        )
    resource = resources.files("semantic_projection.contexts").joinpath(matches[0]["resource"])
    return json.loads(resource.read_text(encoding="utf-8"))


def release_compatibility() -> dict[str, Any]:
    """Load the machine-readable compatibility contract for this distribution."""
    resource = resources.files("semantic_projection.release").joinpath("compatibility.json")
    return json.loads(resource.read_text(encoding="utf-8"))
