"""Release and per-artifact identity for installed executable semantic policy."""

from __future__ import annotations

import json
from collections.abc import Mapping
from hashlib import sha256
from importlib import metadata, resources
from typing import Any

from ._version import __version__
from .resources import (
    bundled_contexts,
    release_compatibility,
    resource_set_manifest,
    runtime_package_records,
    semantic_resource_manifest,
)

DISTRIBUTION_NAME = "semantic-projection-core"
RUNTIME_IDENTITY_CONTRACT = "semantic_projection.runtime_identity.v1"
RELEASE_MANIFEST_CONTRACT = "semantic_projection.runtime_release_manifest.v1"


def _subset(prefix: str, *, suffix: str | None = None) -> dict[str, Any]:
    return resource_set_manifest(
        record
        for record in runtime_package_records()
        if str(record["path"]).startswith(prefix)
        and (suffix is None or str(record["path"]).endswith(suffix))
    )


def _installed_runtime_manifest() -> dict[str, Any]:
    distribution = metadata.distribution(DISTRIBUTION_NAME)
    records = runtime_package_records()
    for name in ("METADATA", "WHEEL", "entry_points.txt"):
        content = distribution.read_text(name)
        if content is not None:
            encoded = content.encode("utf-8")
            records.append({
                "path": f"distribution/{name}",
                "sha256": sha256(encoded).hexdigest(),
                "size": len(encoded),
            })
    return resource_set_manifest(records)


def _profile_resource_set(profile_id: str, profile_version: str) -> dict[str, Any]:
    root = resources.files("semantic_projection.profiles")
    for child in root.iterdir():
        if not child.is_dir():
            continue
        manifest_resource = child.joinpath("manifest.json")
        if not manifest_resource.is_file():
            continue
        manifest = json.loads(manifest_resource.read_text(encoding="utf-8"))
        if manifest.get("profile_id") == profile_id and manifest.get("profile_version") == profile_version:
            return {"bundled": True, **_subset(f"profiles/{child.name}/")}
    return {
        "bundled": False,
        "algorithm": None,
        "sha256": None,
        "resource_count": 0,
        "resources": [],
    }


def _context_identity(context: Mapping[str, Any]) -> dict[str, Any]:
    canonical = json.dumps(dict(context), sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    identity = {
        "context_id": context.get("context_id"),
        "context_version": context.get("context_version"),
        "content_sha256": sha256(canonical).hexdigest(),
        "bundled": False,
        "resource_path": None,
        "resource_sha256": None,
    }
    matching = [
        item for item in bundled_contexts()
        if item["context_id"] == context.get("context_id")
        and item["context_version"] == context.get("context_version")
    ]
    if len(matching) == 1:
        path = f"contexts/{matching[0]['resource']}"
        packaged = json.loads(resources.files("semantic_projection.contexts").joinpath(matching[0]["resource"]).read_text(encoding="utf-8"))
        if dict(context) == packaged:
            record = next(item for item in runtime_package_records() if item["path"] == path)
            identity.update({"bundled": True, "resource_path": path, "resource_sha256": record["sha256"]})
    return identity


def runtime_release_manifest() -> dict[str, Any]:
    """Return the full installed runtime manifest used for release evidence."""
    compatibility = release_compatibility()
    profiles = []
    for profile in compatibility["profiles"]:
        profiles.append({
            "profile_id": profile["profile_id"],
            "profile_version": profile["profile_version"],
            "policy_resource_set": _profile_resource_set(profile["profile_id"], profile["profile_version"]),
        })
    contexts = []
    context_root = resources.files("semantic_projection.contexts")
    for item in bundled_contexts():
        value = json.loads(context_root.joinpath(item["resource"]).read_text(encoding="utf-8"))
        contexts.append(_context_identity(value))
    compatibility_record = next(
        record for record in runtime_package_records() if record["path"] == "release/compatibility.json"
    )
    return {
        "manifest_contract": RELEASE_MANIFEST_CONTRACT,
        "distribution": {
            "name": DISTRIBUTION_NAME,
            "version": metadata.version(DISTRIBUTION_NAME),
            "package_version": __version__,
        },
        "release_compatibility": {
            "contract_id": compatibility["contract_id"],
            "resource_sha256": compatibility_record["sha256"],
        },
        "runtime_package": _installed_runtime_manifest(),
        "semantic_resources": semantic_resource_manifest(),
        "schemas": _subset("schemas/", suffix=".json"),
        "profiles": profiles,
        "contexts": contexts,
    }


def projection_runtime_identity(
    *,
    profile_id: str,
    profile_version: str,
    context: Mapping[str, Any],
    route: str,
    output_contract: str,
) -> dict[str, Any]:
    """Return compact runtime and policy identity suitable for artifact provenance."""
    release_manifest = runtime_release_manifest()
    profile_resources = _profile_resource_set(profile_id, profile_version)
    return {
        "identity_contract": RUNTIME_IDENTITY_CONTRACT,
        "distribution": release_manifest["distribution"],
        "release_compatibility": release_manifest["release_compatibility"],
        "runtime_package": {
            key: release_manifest["runtime_package"][key]
            for key in ("algorithm", "sha256", "resource_count")
        },
        "semantic_resources": {
            key: release_manifest["semantic_resources"][key]
            for key in ("algorithm", "sha256", "resource_count")
        },
        "schemas": {
            key: release_manifest["schemas"][key]
            for key in ("algorithm", "sha256", "resource_count")
        },
        "profile": {
            "profile_id": profile_id,
            "profile_version": profile_version,
            "policy_resource_set": {
                key: profile_resources[key]
                for key in ("bundled", "algorithm", "sha256", "resource_count")
            },
        },
        "context": _context_identity(context),
        "route": route,
        "output_contract": output_contract,
    }
