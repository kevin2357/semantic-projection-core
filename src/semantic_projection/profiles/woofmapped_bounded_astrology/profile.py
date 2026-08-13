from __future__ import annotations

import json
from importlib.resources import files
from typing import Any, ClassVar

from ...contracts import ProjectionContext, ProjectionProfileManifest
from ..woofmapped_astrology.object_mappings import (
    ALIASES,
    DOGHOUSE_DOMAINS,
    OBJECT_MAPPINGS,
    SIGN_MODES,
)

PROFILE_ID = "woofmapped_bounded_astrology.v0"
PROFILE_VERSION = "0.1.0"
TARGET_ONTOLOGY = "woofmapped_astrology.v0"
SIGNS = (
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces",
)
DERIVED_TYPES = {
    "bounded_antiscia_point",
    "bounded_contra_antiscia_point",
    "bounded_harmonic_point",
}
SUPPORTED_CONTEXT_IDS = {
    "woofmapped.doghouse.general.v0",
    "woofmapped.handler_guidance.v1",
    "woofmapped.dog_direct.v1",
    "woofmapped.hybrid_horoscope.v1",
}


def _resource_json(name: str) -> dict[str, Any]:
    return json.loads(
        files(__package__).joinpath(name).read_text(encoding="utf-8")
    )


def _canonical_name(value: str) -> str:
    return ALIASES.get(value, value)


def _sign(source_object: dict[str, Any]) -> str | None:
    value = source_object.get("sign_index")
    if isinstance(value, int) and 0 <= value < len(SIGNS):
        return SIGNS[value]
    return None


def _house(source_object: dict[str, Any]) -> int | None:
    value = source_object.get("house_number")
    return value if isinstance(value, int) and 1 <= value <= 12 else None


class WoofmappedBoundedAstrologyProfile:
    """Target policy for invariant categorical facts from AGF bounded natal."""

    manifest = ProjectionProfileManifest.from_dict(_resource_json("manifest.json"))
    source_selection_policy: ClassVar[dict[str, str]] = {
        "source_package": "bounded_natal_dataset@1.0.0",
        "source_graph": "bounded_canonical_astrology_graph@1.7.0",
        "epistemic_classification": "invariant_only",
        "node_variant": "true",
        "fortune_variant": "part_of_fortune",
        "structural_strength": "unavailable_no_default",
    }

    def validate_context(self, context: ProjectionContext) -> list[dict[str, Any]]:
        if context.context_id not in SUPPORTED_CONTEXT_IDS:
            raise ValueError(
                f"{PROFILE_ID} does not support context {context.context_id!r}"
            )
        if context.target_domain != TARGET_ONTOLOGY:
            raise ValueError("Bounded Woofmapping context target_domain mismatch")
        policy = context.constraints.get("house_mapping_policy")
        if policy != "doghouse":
            raise ValueError(
                f"{PROFILE_ID} requires house_mapping_policy=doghouse"
            )
        return []

    def classify_source_object(
        self, source_object: dict[str, Any], source_object_index: dict[str, dict[str, Any]]
    ) -> str:
        object_type = source_object.get("object_type")
        if object_type == "bounded_house_cusp":
            return "eligible" if _house(source_object) is not None else "invalid_supported_source"
        if object_type == "bounded_sect_state":
            return "outside_declared_scope"
        if object_type in DERIVED_TYPES:
            owner = source_object_index.get(str(source_object.get("owner_object_ref") or ""))
            return "eligible" if owner and self._mapping_for_named_object(owner) else "outside_declared_scope"
        if object_type in {"bounded_natal_body", "bounded_angle", "bounded_calculated_point"}:
            return "eligible" if self._mapping_for_named_object(source_object) else "outside_declared_scope"
        return "outside_declared_scope"

    def _mapping_for_named_object(self, source_object: dict[str, Any]) -> dict[str, Any] | None:
        return OBJECT_MAPPINGS.get(_canonical_name(str(source_object.get("name") or "")))

    def project_object(
        self,
        source_object: dict[str, Any],
        *,
        source_object_index: dict[str, dict[str, Any]],
        context: dict[str, Any],
    ) -> dict[str, Any] | None:
        object_type = str(source_object.get("object_type") or "")
        if object_type == "bounded_house_cusp":
            house = _house(source_object)
            if house is None:
                return None
            domain = DOGHOUSE_DOMAINS[house]
            return {
                "semantic_key": domain,
                "object_type": "woofmapped_doghouse_domain",
                "name": domain,
                "operators": ["contextualize", "locate_behavior", "organize_dog_life"],
                "attributes": {
                    "source_object_type": object_type,
                    "source_house": house,
                    "doghouse_number": house,
                    "projected_domain": domain,
                    "source_sign": _sign(source_object),
                    "source_traditional_ruler": source_object.get("traditional_ruler"),
                    "source_modern_ruler": source_object.get("modern_ruler"),
                    "house_mapping_policy": "doghouse",
                },
                "mapping_rule_id": f"{PROFILE_ID}.doghouse.{house}.{domain}",
                "mapping_rule_version": PROFILE_VERSION,
                "provenance": {"profile_layer": "bounded_doghouse_mapping"},
            }

        owner = None
        transform = object_type in DERIVED_TYPES
        semantic_source = source_object
        if transform:
            owner = source_object_index.get(str(source_object.get("owner_object_ref") or ""))
            if owner is None:
                return None
            semantic_source = owner
        canonical_name = _canonical_name(str(semantic_source.get("name") or ""))
        mapping = OBJECT_MAPPINGS.get(canonical_name)
        if mapping is None:
            return None

        sign = _sign(source_object)
        house = _house(source_object)
        projected_mode = SIGN_MODES.get(sign) if sign else None
        projected_domain = DOGHOUSE_DOMAINS.get(house) if house else None
        transform_key = None
        if transform:
            qualifier = source_object.get("harmonic_number")
            transform_key = str(source_object.get("transform_kind") or object_type)
            if qualifier is not None:
                transform_key += f":{qualifier}"
        semantic_key = mapping["target_name"]
        if transform_key:
            semantic_key = f"{semantic_key}:coordinate_transform:{transform_key}"

        operators = list(mapping["operators"])
        if transform:
            operators.append("reexpress_through_coordinate_transform")
        return {
            "semantic_key": semantic_key,
            "object_type": (
                "woofmapped_derived_operator" if transform else mapping["object_type"]
            ),
            "name": mapping["target_name"],
            "operators": sorted(set(operators)),
            "attributes": {
                "canonical_object_name": canonical_name,
                "source_object_type": object_type,
                "source_sign": sign,
                "projected_mode": projected_mode,
                "source_house": house,
                "doghouse_number": house,
                "projected_domain": projected_domain,
                "source_motion_state": source_object.get("motion_state"),
                "source_sign_dignity": source_object.get("sign_dignity"),
                "source_triplicity_ruler": source_object.get("triplicity_ruler"),
                "source_possible_formula_ids": list(
                    source_object.get("possible_formula_ids") or []
                ),
                "coordinate_transform": transform_key,
                "source_owner_object_ref": (
                    source_object.get("owner_object_ref") if transform else None
                ),
                "projection_composition": {
                    "operator": mapping["target_name"],
                    "mode": projected_mode,
                    "domain": projected_domain,
                    "coordinate_transform": transform_key,
                },
                "house_mapping_policy": "doghouse",
            },
            "mapping_rule_id": (
                f"{PROFILE_ID}.object."
                f"{canonical_name.lower().replace(' ', '_')}."
                f"{mapping['target_name']}"
                + (f".{transform_key.replace(':', '.')}" if transform_key else "")
            ),
            "mapping_rule_version": PROFILE_VERSION,
            "provenance": {
                "profile_layer": (
                    "bounded_coordinate_transform_mapping"
                    if transform else "bounded_object_mapping"
                ),
                "operator_preservation_policy": (
                    "preserve_owner_operator_and_transform_role"
                    if transform else "preserve_core_verb_change_species_domain"
                ),
            },
        }

    def projected_term_registry(self) -> dict[str, Any]:
        return _resource_json("projected_term_registry.json")
