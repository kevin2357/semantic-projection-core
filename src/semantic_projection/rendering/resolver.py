from __future__ import annotations

from typing import Any

JsonDict = dict[str, Any]


class ProjectedTermResolutionError(ValueError):
    pass


class ProjectedTermResolver:
    """Resolve terms from an embedded projected-term registry."""

    def __init__(self, registry: JsonDict):
        self.registry = registry
        self.terms: JsonDict = registry.get("terms") or {}
        if not self.terms:
            raise ProjectedTermResolutionError("projected term registry has no terms")

    def resolve_key(self, key: str | None) -> JsonDict | None:
        if key is None:
            return None
        entry = self.terms.get(key)
        if entry is None:
            raise ProjectedTermResolutionError(f"unresolved projected term: {key}")
        return entry

    def label(self, key: str | None) -> str | None:
        entry = self.resolve_key(key)
        return str(entry.get("canonical_label")) if entry else None

    def friendly_label(self, key: str | None) -> str | None:
        entry = self.resolve_key(key)
        if entry is None:
            return None
        labels = entry.get("friendly_labels") or []
        return str(labels[0]) if labels else str(entry.get("canonical_label"))

    def output_guidance(self, key: str | None) -> JsonDict:
        entry = self.resolve_key(key)
        return dict(entry.get("output_guidance") or {}) if entry else {}

    def term_ref(self, key: str | None) -> str | None:
        if key is None:
            return None
        self.resolve_key(key)
        return (
            f"{self.registry['registry_id']}:"
            f"{self.registry['registry_version']}:{key}"
        )


def object_index(graph: JsonDict) -> dict[str, JsonDict]:
    return {str(row["id"]): row for row in graph.get("objects") or []}
