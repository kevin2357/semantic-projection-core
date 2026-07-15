from __future__ import annotations

from pathlib import Path
import json
from typing import Any

from ...contracts import ProjectionContext, ProjectionProfileManifest, ProjectionRequest, ProjectedSemanticGraph
from .context import CONTEXT_ID, context_salience
from .object_mappings import (
    DOGHOUSE_DOMAINS,
    OBJECT_MAPPINGS,
    SIGN_MODES,
    canonical_object_name,
    house_cusp_number,
    source_house,
    source_sign,
    source_selection_status,
)
from .relationship_mappings import ASPECT_MAPPINGS, canonical_aspect, source_operator_strings


GUARDRAILS = [
    "playful_experimental_projection",
    "not_veterinary_advice",
    "not_behavioral_diagnosis",
    "not_empirically_validated",
]


def _load_manifest() -> ProjectionProfileManifest:
    return ProjectionProfileManifest.from_dict(
        json.loads(Path(__file__).with_name("manifest.json").read_text(encoding="utf-8"))
    )


def _score(structural: float | None, profile_salience: float, context_component: float) -> tuple[float, dict[str, float]]:
    structural_component = 1.0 if structural is None else max(0.0, min(1.0, float(structural)))
    components = {
        "structural_strength": round(structural_component, 6),
        "profile_salience": round(profile_salience, 6),
        "context_salience": round(context_component, 6),
    }
    return round(structural_component * profile_salience * context_component, 6), components


class WoofmappedAstrologyProfile:
    """Doghouse-based Natal projection and operator-preservation stress test."""

    manifest = _load_manifest()
    temporal_target_scope_exclusions = frozenset({"spirit"})
    source_selection_policy = {
        "node_variant": "true",
        "fortune_variant": "part_of_fortune",
    }

    def validate_context(self, context: ProjectionContext) -> list[dict[str, Any]]:
        policy = (
            context.constraints.get("house_mapping_policy")
            or context.parameters.get("house_mapping_policy")
        )
        if policy is None:
            raise ValueError(
                "woofmapped_astrology.v0 requires explicit "
                "house_mapping_policy=doghouse"
            )
        if policy != "doghouse":
            raise ValueError(
                "woofmapped_astrology.v0 does not implement "
                f"house_mapping_policy={policy}"
            )
        warnings = []
        if context.context_id != CONTEXT_ID:
            warnings.append({
                "code": "woofmapped.context.nonstandard",
                "message": "Context accepted, but this profile uses Doghouses as its reference policy.",
                "details": {"expected": CONTEXT_ID, "received": context.context_id},
            })
        if context.subject_scope not in {"individual", "natal", "dog", "synastry"}:
            warnings.append({
                "code": "woofmapped.scope.experimental",
                "message": "Woofmapped v0.1 supports individual and explicit synastry contexts.",
                "details": {"subject_scope": context.subject_scope},
            })
        return warnings

    def project_object(self, source_object: dict[str, Any], request: ProjectionRequest) -> list[dict[str, Any]]:
        if source_selection_status(source_object) == "excluded_by_source_selection_policy":
            return []
        doghouse = house_cusp_number(source_object)
        if doghouse is not None:
            domain = DOGHOUSE_DOMAINS.get(doghouse)
            if domain is None:
                return []
            return [{
                "target_key": f"woof:doghouse:{doghouse}:{source_object.get('id')}",
                "object_type": "woofmapped_doghouse_domain",
                "name": domain,
                "operators": ["locate_behavior", "organize_dog_life", "contextualize"],
                "attributes": {
                    "source_house": doghouse,
                    "doghouse_number": doghouse,
                    "projected_domain": domain,
                    "house_mapping_policy": "doghouse",
                    "source_names": [str(source_object.get("name") or f"House {doghouse}")],
                    "guardrails": GUARDRAILS,
                },
                "structural_strength_score": source_object.get("structural_strength_score"),
                "projection_relevance_score": 0.76,
                "mapping_rule_id": f"woofmapped_astrology.v0.doghouse.{doghouse}.{domain}",
                "mapping_rule_version": "0.1.0",
                "conditions_evaluated": [{"condition": "doghouse_domain_supported", "result": True, "value": doghouse}],
                "provenance": {"profile_layer": "woofmapped_doghouse_mapping"},
            }]

        canonical_name = canonical_object_name(source_object)
        mapping = OBJECT_MAPPINGS.get(canonical_name)
        if mapping is None:
            return []

        sign = source_sign(source_object)
        house = source_house(source_object)
        projected_mode = SIGN_MODES.get(sign) if sign else None
        projected_domain = DOGHOUSE_DOMAINS.get(house) if house else None
        structural = source_object.get("structural_strength_score")
        relevance, components = _score(
            structural,
            float(mapping["salience"]),
            context_salience(request.context, list(mapping["domains"])),
        )
        source_ops = source_operator_strings(source_object)

        return [{
            "target_key": f"woof:{mapping['target_name']}:{source_object.get('id')}",
            "object_type": mapping["object_type"],
            "name": mapping["target_name"],
            "operators": sorted(set([*source_ops, *mapping["operators"]])),
            "attributes": {
                "canonical_object_name": canonical_name,
                "source_names": [str(source_object.get("name") or canonical_name)],
                "subject_owner": source_object.get("subject_owner") or (source_object.get("attributes") or {}).get("subject_owner"),
                "participant_role": (source_object.get("attributes") or {}).get("participant_role"),
                "relationship_kind": (source_object.get("attributes") or {}).get("relationship_kind"),
                "canine_domains": list(mapping["domains"]),
                "source_sign": sign,
                "projected_mode": projected_mode,
                "source_house": house,
                "doghouse_number": house,
                "projected_domain": projected_domain,
                "house_mapping_policy": "doghouse",
                "projection_composition": {
                    "operator": mapping["target_name"],
                    "mode": projected_mode,
                    "domain": projected_domain,
                },
                "projection_relevance_components": components,
                "guardrails": GUARDRAILS,
            },
            "structural_strength_score": structural,
            "projection_relevance_score": relevance,
            "mapping_rule_id": (
                f"woofmapped_astrology.v0.object."
                f"{canonical_name.lower().replace(' ', '_')}.{mapping['target_name']}"
            ),
            "mapping_rule_version": "0.1.0",
            "conditions_evaluated": [
                {"condition": "woofmapped_object_supported", "result": True, "value": canonical_name},
                {"condition": "sign_mode_resolved", "result": projected_mode is not None, "value": sign},
                {"condition": "doghouse_domain_resolved", "result": projected_domain is not None, "value": house},
            ],
            "provenance": {
                "profile_layer": "woofmapped_object_mapping",
                "source_object_type": source_object.get("object_type"),
                "operator_preservation_policy": "preserve_core_verb_change_species_domain",
            },
        }]

    def project_relationship(
        self,
        source_relationship: dict[str, Any],
        projected_object_index: dict[str, list[dict[str, Any]]],
        request: ProjectionRequest,
    ) -> list[dict[str, Any]]:
        aspect = canonical_aspect(source_relationship)
        mapping = ASPECT_MAPPINGS.get(aspect)
        if mapping is None:
            return []

        source_id = str(source_relationship.get("source_id") or source_relationship.get("source_object_id") or "")
        target_id = str(source_relationship.get("target_id") or source_relationship.get("target_object_id") or "")
        if not projected_object_index.get(source_id) or not projected_object_index.get(target_id):
            return []

        source_projected = projected_object_index[source_id][0]
        target_projected = projected_object_index[target_id][0]
        structural = source_relationship.get("structural_strength_score")
        relevance, components = _score(structural, float(mapping["salience"]), 1.0)
        source_ops = source_operator_strings(source_relationship)

        return [{
            "relationship_type": mapping["relationship_type"],
            "source_source_id": source_id,
            "target_source_id": target_id,
            "operators": sorted(set([*source_ops, *mapping["operators"]])),
            "theme_tags": [
                mapping["interaction_mode"],
                source_projected["name"],
                target_projected["name"],
            ],
            "attributes": {
                "canonical_aspect": aspect,
                "orb": source_relationship.get("orb"),
                "relationship_kind": (source_relationship.get("attributes") or {}).get("relationship_kind") or request.context.get("relationship_type"),
                "source_owner": source_relationship.get("source_owner") or (source_relationship.get("attributes") or {}).get("source_owner"),
                "target_owner": source_relationship.get("target_owner") or (source_relationship.get("attributes") or {}).get("target_owner"),
                "source_participant_role": (source_relationship.get("attributes") or {}).get("source_participant_role"),
                "target_participant_role": (source_relationship.get("attributes") or {}).get("target_participant_role"),
                "inter_participant": bool((source_relationship.get("attributes") or {}).get("inter_participant")),
                "relational_role_composition": {
                    "source_role": (source_relationship.get("attributes") or {}).get("source_participant_role"),
                    "target_role": (source_relationship.get("attributes") or {}).get("target_participant_role"),
                    "asymmetric": (source_relationship.get("attributes") or {}).get("source_participant_role") != (source_relationship.get("attributes") or {}).get("target_participant_role"),
                },
                "source_canine_subsystem": source_projected["name"],
                "target_canine_subsystem": target_projected["name"],
                "source_mode": source_projected.get("attributes", {}).get("projected_mode"),
                "target_mode": target_projected.get("attributes", {}).get("projected_mode"),
                "source_doghouse": source_projected.get("attributes", {}).get("projected_domain"),
                "target_doghouse": target_projected.get("attributes", {}).get("projected_domain"),
                "interaction_mode": mapping["interaction_mode"],
                "projection_relevance_components": components,
                "projection_first_reasoning": {
                    "source_mapping": source_projected["name"],
                    "source_mode": source_projected.get("attributes", {}).get("projected_mode"),
                    "relationship_mapping": mapping["relationship_type"],
                    "target_mapping": target_projected["name"],
                    "target_mode": target_projected.get("attributes", {}).get("projected_mode"),
                },
                "guardrails": GUARDRAILS,
            },
            "projection_relevance_score": relevance,
            "mapping_rule_id": f"woofmapped_astrology.v0.aspect.{aspect}.{mapping['relationship_type']}",
            "mapping_rule_version": "0.1.0",
            "conditions_evaluated": [
                {"condition": "sdk_aspect_supported", "result": True, "value": aspect},
                {"condition": "projected_endpoints_available", "result": True},
            ],
            "provenance": {
                "profile_layer": "woofmapped_relationship_mapping",
                "operator_preservation_policy": "relationship_geometry_preserved",
            },
        }]

    def projected_term_registry(self) -> dict[str, Any]:
        return json.loads(
            Path(__file__).with_name("projected_term_registry.json").read_text(
                encoding="utf-8"
            )
        )

    def classify_source_object(self, source_object: dict[str, Any]) -> str:
        selection = source_selection_status(source_object)
        if selection != "eligible":
            return selection
        if house_cusp_number(source_object) is not None:
            return "eligible"
        return (
            "eligible"
            if canonical_object_name(source_object) in OBJECT_MAPPINGS
            else "outside_declared_scope"
        )

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
        endpoint_statuses = {
            object_status.get(source_id, "outside_declared_scope"),
            object_status.get(target_id, "outside_declared_scope"),
        }
        if "excluded_by_source_selection_policy" in endpoint_statuses:
            return "excluded_by_source_selection_policy"
        if endpoint_statuses != {"eligible"}:
            return "outside_declared_scope"
        return (
            "eligible"
            if canonical_aspect(source_relationship) in ASPECT_MAPPINGS
            else "outside_declared_scope"
        )

    def finalize(self, graph: ProjectedSemanticGraph, request: ProjectionRequest) -> None:
        interaction_counts: dict[str, int] = {}
        mode_counts: dict[str, int] = {}
        doghouse_counts: dict[str, int] = {}
        for obj in graph.objects:
            attributes = obj.get("attributes", {})
            if attributes.get("projected_mode"):
                mode_counts[attributes["projected_mode"]] = mode_counts.get(attributes["projected_mode"], 0) + 1
            if attributes.get("projected_domain"):
                doghouse_counts[attributes["projected_domain"]] = doghouse_counts.get(attributes["projected_domain"], 0) + 1
        for relationship in graph.relationships:
            mode = relationship.get("attributes", {}).get("interaction_mode")
            if mode:
                interaction_counts[mode] = interaction_counts.get(mode, 0) + 1
        graph.summary["profile_scope"] = "natal_and_synastry_operators_sign_modes_doghouses_angles_and_aspects"
        graph.summary["synastry_mode"] = request.context.get("subject_scope") == "synastry"
        graph.summary["relationship_type"] = request.context.get("relationship_type")
        graph.summary["playful_experimental_projection"] = True
        graph.summary["veterinary_advice"] = False
        graph.summary["behavioral_diagnosis_permitted"] = False
        graph.summary["house_mapping_policy"] = "doghouse"
        graph.summary["supported_object_names"] = sorted(OBJECT_MAPPINGS)
        graph.summary["supported_sign_modes"] = dict(sorted(SIGN_MODES.items()))
        graph.summary["supported_doghouses"] = {str(k): v for k, v in sorted(DOGHOUSE_DOMAINS.items())}
        graph.summary["supported_aspects"] = sorted(ASPECT_MAPPINGS)
        graph.summary["interaction_mode_counts"] = dict(sorted(interaction_counts.items()))
        graph.summary["projected_mode_counts"] = dict(sorted(mode_counts.items()))
        graph.summary["projected_doghouse_counts"] = dict(sorted(doghouse_counts.items()))
