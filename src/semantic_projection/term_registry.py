from __future__ import annotations

from copy import deepcopy
from typing import Any

JsonDict = dict[str, Any]

TERM_TYPES = {"operator", "mode", "domain", "interface", "relation", "theme", "orientation"}


def term_ref(registry: JsonDict, key: str) -> str:
    return f"{registry['registry_id']}:{registry['registry_version']}:{key}"


def validate_projected_term_registry(registry: JsonDict) -> list[str]:
    errors: list[str] = []
    for field in ("registry_id", "registry_version", "target_ontology", "terms"):
        if field not in registry:
            errors.append(f"missing registry field: {field}")
    terms = registry.get("terms") or {}
    for key, entry in terms.items():
        if entry.get("term_type") not in TERM_TYPES:
            errors.append(f"{key}: invalid term_type")
        for field in ("canonical_label", "short_description"):
            if not entry.get(field):
                errors.append(f"{key}: missing {field}")
        for related in entry.get("related_terms") or []:
            if related not in terms:
                errors.append(f"{key}: dangling related term {related}")
    return errors


def used_term_keys(graph: Any, registry: JsonDict) -> set[str]:
    terms = registry.get("terms") or {}
    used: set[str] = set()
    def add(value: Any) -> None:
        if isinstance(value, str) and value in terms:
            used.add(value)
        elif isinstance(value, list):
            for item in value:
                add(item)
    for row in graph.objects:
        add(row.get("name"))
        attrs = row.get("attributes") or {}
        for key in ("projected_mode", "projected_domain"):
            add(attrs.get(key))
    for row in graph.relationships:
        add(row.get("relationship_type"))
        attrs = row.get("attributes") or {}
        add(attrs.get("interaction_mode"))
        add(row.get("theme_tags"))
    return used


def attach_registry_refs_and_subset(graph: Any, registry: JsonDict) -> JsonDict:
    errors = validate_projected_term_registry(registry)
    if errors:
        raise ValueError("Invalid projected term registry: " + "; ".join(errors))
    terms = registry["terms"]
    def ref(value: Any) -> str | None:
        return term_ref(registry, value) if isinstance(value, str) and value in terms else None

    for row in graph.objects:
        attrs = row.setdefault("attributes", {})
        if ref(row.get("name")):
            attrs["term_ref"] = ref(row["name"])
        if ref(attrs.get("projected_mode")):
            attrs["mode_ref"] = ref(attrs["projected_mode"])
        if ref(attrs.get("projected_domain")):
            attrs["domain_ref"] = ref(attrs["projected_domain"])
    for row in graph.relationships:
        attrs = row.setdefault("attributes", {})
        if ref(row.get("relationship_type")):
            attrs["relation_ref"] = ref(row["relationship_type"])
        if ref(attrs.get("interaction_mode")):
            attrs["interaction_mode_ref"] = ref(attrs["interaction_mode"])

    keys = used_term_keys(graph, registry)
    return {
        "registry_id": registry["registry_id"],
        "registry_version": registry["registry_version"],
        "target_ontology": registry["target_ontology"],
        "materialization": "used_terms_subset",
        "terms": {key: deepcopy(terms[key]) for key in sorted(keys)},
    }
