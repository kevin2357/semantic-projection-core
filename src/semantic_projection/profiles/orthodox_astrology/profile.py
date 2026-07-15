from __future__ import annotations

from pathlib import Path
import json
from typing import Any

from ...contracts import (
    ProjectionContext,
    ProjectionProfileManifest,
    ProjectionRequest,
    ProjectedSemanticGraph,
)
from .context import (
    GENERAL_CONTEXT_ID,
    PROFESSIONAL_CONTEXT_ID,
    context_salience,
    house_domain,
    is_professional,
    map_themes,
    object_name,
)
from .object_mappings import (
    OBJECT_MAPPINGS,
    canonical_object_name,
    house_number,
)
from .relationship_mappings import (
    ASPECT_MAPPINGS,
    canonical_aspect,
    source_operator_strings,
)


def _load_manifest() -> ProjectionProfileManifest:
    path = Path(__file__).with_name("manifest.json")
    return ProjectionProfileManifest.from_dict(
        json.loads(path.read_text(encoding="utf-8"))
    )


def _score(
    structural: float | None,
    profile_salience: float,
    context_component: float = 1.0,
) -> tuple[float, dict[str, float]]:
    structural_component = 1.0 if structural is None else max(0.0, min(1.0, float(structural)))
    components = {
        "structural_strength": round(structural_component, 6),
        "profile_salience": round(profile_salience, 6),
        "context_salience": round(context_component, 6),
    }
    return round(structural_component * profile_salience * context_component, 6), components


def _registry_values(request: ProjectionRequest, registry_name: str, key: Any) -> list[Any]:
    if key is None:
        return []
    registry = request.source_registries.get(registry_name) or {}
    return list(registry.get(str(key)) or [])


def _theme_evidence(
    *,
    object_themes: list[str],
    aspect_themes: list[str],
    registry_themes: list[str],
    theme_key: Any,
    context: dict[str, Any],
) -> list[dict[str, Any]]:
    rows = []
    for theme in sorted(set(object_themes)):
        rows.append({"theme": theme, "origin": "object_mapping"})
    for theme in sorted(set(aspect_themes)):
        rows.append({"theme": theme, "origin": "aspect_mapping"})
    for theme in sorted(set(registry_themes)):
        rows.append({
            "theme": theme,
            "origin": "source_registry",
            "source_ref": f"theme_registry:{theme_key}",
        })
    if is_professional(context):
        for row in rows:
            mapped = map_themes([row["theme"]], context)[0]
            if mapped != row["theme"]:
                row["source_theme"] = row["theme"]
                row["theme"] = mapped
                row["context_transform"] = PROFESSIONAL_CONTEXT_ID
    deduped = {}
    for row in rows:
        key = (row["theme"], row["origin"], row.get("source_ref"))
        deduped[key] = row
    return [deduped[key] for key in sorted(deduped)]


class OrthodoxAstrologyProfile:
    """Orthodox reference profile with registry-aware relationship contexts."""

    manifest = _load_manifest()
    temporal_activator_scope_exclusions = frozenset()
    temporal_target_scope_exclusions = frozenset()

    def validate_context(self, context: ProjectionContext) -> list[dict[str, Any]]:
        supported = {
            "general_interpretation",
            "natal_interpretation",
            "relationship_interpretation",
            "professional_relationship",
        }
        warnings = []
        if context.application_context not in supported:
            warnings.append({
                "code": "orthodox.context.unrecognized_application",
                "message": "Context is accepted but has no specialized orthodox rules",
                "details": {"application_context": context.application_context},
            })
        return warnings

    def project_object(
        self,
        source_object: dict[str, Any],
        request: ProjectionRequest,
    ) -> list[dict[str, Any]]:
        context = request.context
        house = house_number(source_object)
        if house is not None:
            domain = house_domain(house, context)
            themes = map_themes([domain], context)
            return [{
                "target_key": f"orthodox:house_domain:{source_object.get('id')}:{domain}",
                "object_type": "orthodox_relationship_domain",
                "name": domain,
                "operators": ["receive", "locate", "contextualize"],
                "attributes": {
                    "house": house,
                    "subject_owner": source_object.get("subject_owner"),
                    "semantic_domains": themes,
                    "theme_tags": themes,
                    "source_names": [source_object.get("name")],
                    "context_mode": "professional" if is_professional(context) else "general",
                },
                "structural_strength_score": source_object.get("structural_strength_score"),
                "projection_relevance_score": 0.8,
                "mapping_rule_id": f"orthodox_astrology.v1.house.{house}.{domain}",
                "mapping_rule_version": "1.0.0",
                "conditions_evaluated": [{"condition": "house_cusp_supported", "result": True, "value": house}],
                "provenance": {"profile_layer": "orthodox_house_domain_mapping"},
            }]

        canonical_name = canonical_object_name(source_object)
        # Foundry may emit a legacy Lot-of-Fortune alias alongside the canonical
        # calculated Part of Fortune object. Preserve the canonical object only.
        if source_object.get("object_type") == "lot" and canonical_name == "Fortune":
            return []

        mapping = OBJECT_MAPPINGS.get(canonical_name)
        if mapping is None:
            source_type = str(source_object.get("object_type") or "canonical_object")
            facts = dict(source_object.get("facts") or {})
            source_name = str(source_object.get("name") or canonical_name or source_object.get("id"))
            target_name = source_name.strip().lower().replace(" ", "_").replace("-", "_")
            generic_domains = [source_type, "orthodox_astrology"]
            structural = source_object.get("structural_strength_score")
            relevance, components = _score(structural, 0.64, 1.0)
            return [{
                "target_key": f"orthodox:canonical:{source_object.get('id')}",
                "object_type": f"orthodox_{source_type}",
                "name": target_name,
                "operators": sorted(set(source_operator_strings(source_object) or ["represent"])),
                "attributes": {
                    "canonical_object_name": canonical_name,
                    "source_names": [source_name],
                    "source_object_type": source_type,
                    "semantic_domains": generic_domains,
                    "theme_tags": [source_type],
                    "source_theme_tags": [source_type],
                    "sign": source_object.get("sign") or facts.get("sign"),
                    "house": source_object.get("house") or facts.get("house"),
                    "subject_owner": source_object.get("subject_owner"),
                    "canonical_facts": facts,
                    "identity_projection": True,
                    "context_mode": "professional" if is_professional(context) else "general",
                    "projection_relevance_components": components,
                },
                "structural_strength_score": structural,
                "projection_relevance_score": relevance,
                "mapping_rule_id": f"orthodox_astrology.v1.identity.{source_type}",
                "mapping_rule_version": "1.1.0",
                "conditions_evaluated": [
                    {"condition": "canonical_identity_projection", "result": True, "value": source_type},
                ],
                "provenance": {
                    "profile_layer": "orthodox_canonical_identity_mapping",
                    "source_object_type": source_type,
                },
            }]

        mapped_themes = map_themes(list(mapping["themes"]), context)
        context_component = context_salience(context, list(mapping["themes"]))
        structural = source_object.get("structural_strength_score")
        relevance, components = _score(structural, float(mapping["salience"]), context_component)
        source_ops = source_operator_strings(source_object)
        target_name = object_name(mapping["target_name"], context)

        return [{
            "target_key": f"orthodox:{target_name}:{source_object.get('id')}",
            "object_type": "orthodox_astrology_primitive",
            "name": target_name,
            "operators": sorted(set([*source_ops, *mapping["operators"]])),
            "attributes": {
                "canonical_object_name": canonical_name,
                "source_names": [str(source_object.get("name") or canonical_name)],
                "semantic_domains": list(mapping["domains"]),
                "theme_tags": mapped_themes,
                "source_theme_tags": list(mapping["themes"]),
                "sign": source_object.get("sign"),
                "house": source_object.get("house"),
                "subject_owner": source_object.get("subject_owner"),
                "context_mode": "professional" if is_professional(context) else "general",
                "projection_relevance_components": components,
            },
            "structural_strength_score": structural,
            "projection_relevance_score": relevance,
            "mapping_rule_id": (
                f"orthodox_astrology.v1.object.{canonical_name.lower()}.{target_name}"
            ),
            "mapping_rule_version": "1.0.0",
            "conditions_evaluated": [
                {"condition": "canonical_object_supported", "result": True, "value": canonical_name},
                {"condition": "context_mode", "result": True, "value": context.get("context_id")},
            ],
            "provenance": {
                "profile_layer": "orthodox_object_mapping",
                "source_object_type": source_object.get("object_type"),
            },
        }]

    def project_relationship(
        self,
        source_relationship: dict[str, Any],
        projected_object_index: dict[str, list[dict[str, Any]]],
        request: ProjectionRequest,
    ) -> list[dict[str, Any]]:
        context = request.context
        source_id = str(source_relationship.get("source_id") or source_relationship.get("source_object_id") or "")
        target_id = str(source_relationship.get("target_id") or source_relationship.get("target_object_id") or "")
        if not projected_object_index.get(source_id) or not projected_object_index.get(target_id):
            return []

        source_projected = projected_object_index[source_id][0]
        target_projected = projected_object_index[target_id][0]
        relationship_type = str(source_relationship.get("relationship_type") or "")
        theme_key = source_relationship.get("theme_key")
        registry_themes = [str(value) for value in _registry_values(request, "theme_registry", theme_key)]
        registry_operators = _registry_values(request, "operator_registry", source_relationship.get("operator_key"))
        registry_operator_strings = source_operator_strings({"operator_hints": registry_operators})
        source_ops = source_operator_strings(source_relationship)
        object_themes = [
            *(source_projected.get("attributes", {}).get("source_theme_tags") or source_projected.get("attributes", {}).get("theme_tags") or []),
            *(target_projected.get("attributes", {}).get("source_theme_tags") or target_projected.get("attributes", {}).get("theme_tags") or []),
        ]

        if relationship_type == "HOUSE_OVERLAY":
            raw_themes = sorted(set([*object_themes, *registry_themes]))
            mapped_themes = map_themes(raw_themes, context)
            context_component = context_salience(context, raw_themes)
            structural = source_relationship.get("structural_strength_score")
            relevance, components = _score(structural, 0.86, context_component)
            evidence = _theme_evidence(
                object_themes=object_themes,
                aspect_themes=[],
                registry_themes=registry_themes,
                theme_key=theme_key,
                context=context,
            )
            return [{
                "relationship_type": (
                    "activates_collaboration_domain"
                    if is_professional(context)
                    else "activates_relationship_domain"
                ),
                "source_source_id": source_id,
                "target_source_id": target_id,
                "operators": sorted(set([*source_ops, *registry_operator_strings, "activate", "locate"])),
                "theme_tags": mapped_themes,
                "attributes": {
                    "source_relationship_type": relationship_type,
                    "direction": source_relationship.get("direction"),
                    "source_person": source_relationship.get("source_person"),
                    "target_person": source_relationship.get("target_person"),
                    "target_house": source_relationship.get("target_house"),
                    "theme_key": theme_key,
                    "theme_evidence": evidence,
                    "projection_relevance_components": components,
                    "context_mode": "professional" if is_professional(context) else "general",
                },
                "projection_relevance_score": relevance,
                "mapping_rule_id": (
                    "orthodox_astrology.v1.house_overlay."
                    + ("professional" if is_professional(context) else "general")
                ),
                "mapping_rule_version": "1.0.0",
                "conditions_evaluated": [
                    {"condition": "house_overlay_supported", "result": True},
                    {"condition": "source_registry_resolved", "result": bool(registry_themes), "value": theme_key},
                ],
                "provenance": {"profile_layer": "orthodox_house_overlay_mapping"},
            }]

        aspect = canonical_aspect(source_relationship)
        mapping = ASPECT_MAPPINGS.get(aspect)
        if mapping is None:
            return []

        raw_themes = sorted(set([*object_themes, *mapping["themes"], *registry_themes]))
        mapped_themes = map_themes(raw_themes, context)
        context_component = context_salience(context, raw_themes)
        structural = source_relationship.get("structural_strength_score")
        relevance, components = _score(structural, float(mapping["salience"]), context_component)
        operators = sorted(set([*source_ops, *registry_operator_strings, *mapping["operators"]]))
        evidence = _theme_evidence(
            object_themes=object_themes,
            aspect_themes=list(mapping["themes"]),
            registry_themes=registry_themes,
            theme_key=theme_key,
            context=context,
        )
        projected_relationship_type = mapping["relationship_type"]
        if is_professional(context):
            projected_relationship_type = f"professional_{projected_relationship_type}"

        return [{
            "relationship_type": projected_relationship_type,
            "source_source_id": source_id,
            "target_source_id": target_id,
            "operators": operators,
            "theme_tags": mapped_themes,
            "attributes": {
                "canonical_aspect": aspect,
                "orb": source_relationship.get("orb"),
                "source_relationship_type": relationship_type,
                "direction": source_relationship.get("direction"),
                "source_person": source_relationship.get("source_person"),
                "target_person": source_relationship.get("target_person"),
                "source_object_name": source_projected.get("attributes", {}).get("canonical_object_name"),
                "target_object_name": target_projected.get("attributes", {}).get("canonical_object_name"),
                "theme_key": theme_key,
                "theme_evidence": evidence,
                "projection_relevance_components": components,
                "context_mode": "professional" if is_professional(context) else "general",
            },
            "projection_relevance_score": relevance,
            "mapping_rule_id": (
                f"orthodox_astrology.v1.aspect.{aspect}.{projected_relationship_type}"
            ),
            "mapping_rule_version": "1.0.0",
            "conditions_evaluated": [
                {"condition": "major_aspect_supported", "result": True, "value": aspect},
                {"condition": "projected_endpoints_available", "result": True},
                {"condition": "source_registry_resolved", "result": bool(registry_themes), "value": theme_key},
                {"condition": "context_mode", "result": True, "value": context.get("context_id")},
            ],
            "provenance": {"profile_layer": "orthodox_relationship_mapping"},
        }]

    def projected_term_registry(self) -> dict[str, Any]:
        return json.loads(
            Path(__file__).with_name("projected_term_registry.json").read_text(
                encoding="utf-8"
            )
        )

    def classify_source_object(self, source_object: dict[str, Any]) -> str:
        if house_number(source_object) is not None:
            return "eligible"
        canonical_name = canonical_object_name(source_object)
        if source_object.get("object_type") == "lot" and canonical_name == "Fortune":
            return "excluded_by_source_selection_policy"
        return "eligible"

    def classify_source_relationship(
        self,
        source_relationship: dict[str, Any],
        object_status: dict[str, str],
    ) -> str:
        source_id = str(
            source_relationship.get("source_id")
            or source_relationship.get("source_object_id")
            or ""
        )
        target_id = str(
            source_relationship.get("target_id")
            or source_relationship.get("target_object_id")
            or ""
        )
        if {
            object_status.get(source_id),
            object_status.get(target_id),
        } != {"eligible"}:
            return "outside_declared_scope"
        if source_relationship.get("relationship_type") == "HOUSE_OVERLAY":
            return "eligible"
        return (
            "eligible"
            if canonical_aspect(source_relationship) in ASPECT_MAPPINGS
            else "outside_declared_scope"
        )

    def finalize(
        self,
        graph: ProjectedSemanticGraph,
        request: ProjectionRequest,
    ) -> None:
        theme_counts: dict[str, int] = {}
        registry_theme_count = 0
        overlay_count = 0
        for relationship in graph.relationships:
            for theme in relationship.get("theme_tags") or []:
                theme_counts[theme] = theme_counts.get(theme, 0) + 1
            for row in relationship.get("attributes", {}).get("theme_evidence") or []:
                if row.get("origin") == "source_registry":
                    registry_theme_count += 1
            if relationship.get("attributes", {}).get("source_relationship_type") == "HOUSE_OVERLAY":
                overlay_count += 1
        graph.summary["orthodox_theme_counts"] = dict(sorted(theme_counts.items()))
        graph.summary["registry_resolved_theme_evidence_count"] = registry_theme_count
        graph.summary["projected_house_overlay_count"] = overlay_count
        graph.summary["context_mode"] = "professional" if is_professional(request.context) else "general"
        graph.summary["supported_object_names"] = sorted(OBJECT_MAPPINGS)
        graph.summary["supported_major_aspects"] = sorted(ASPECT_MAPPINGS)
        graph.summary["profile_scope"] = "core_objects_major_aspects_synastry_overlays_contexts"
