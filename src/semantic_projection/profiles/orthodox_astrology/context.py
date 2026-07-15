from __future__ import annotations

from typing import Any

GENERAL_CONTEXT_ID = "orthodox.relationship.general.v1"
PROFESSIONAL_CONTEXT_ID = "orthodox.relationship.professional.v1"

PROFESSIONAL_THEME_MAP = {
    "romance_affection": "professional_rapport",
    "values_resources": "values_alignment_resources",
    "conflict_drive": "initiative_tension",
    "home_family": "team_foundation",
    "emotional_safety": "team_climate_support",
    "partnership_mirroring": "collaboration_mirroring",
    "growth_meaning": "professional_growth_meaning",
    "commitment_structure": "role_commitment_structure",
    "freedom_change": "innovation_change",
    "dream_idealization": "vision_idealization",
    "depth_power": "power_influence",
}

PROFESSIONAL_OBJECT_NAMES = {
    "communication_interpretation": "professional_communication_coordination",
    "value_attraction_harmony": "values_alignment_diplomacy",
    "action_assertion_drive": "initiative_execution",
    "emotional_regulation": "team_climate_regulation",
    "partnership_mirror": "collaboration_mirror",
    "public_direction": "professional_direction",
}

HOUSE_DOMAINS = {
    1: ("identity_presence", "role_presence"),
    2: ("values_resources", "resource_stewardship"),
    3: ("communication_learning", "information_exchange"),
    4: ("home_foundation", "team_foundation"),
    5: ("creativity_expression", "creative_contribution"),
    6: ("work_routine_service", "workflow_service"),
    7: ("partnership_contract", "collaboration_contract"),
    8: ("shared_resources_depth", "shared_resources_risk"),
    9: ("meaning_learning_worldview", "strategy_learning"),
    10: ("public_direction_status", "career_direction_status"),
    11: ("community_future", "network_future"),
    12: ("private_unconscious", "hidden_processes"),
}


def is_professional(context: dict[str, Any]) -> bool:
    return (
        context.get("context_id") == PROFESSIONAL_CONTEXT_ID
        or context.get("application_context") == "professional_relationship"
        or context.get("relationship_type") in {"manager_employee", "coworkers", "professional"}
    )


def context_salience(context: dict[str, Any], themes: list[str]) -> float:
    if not is_professional(context):
        return 1.0
    professional_priority = {
        "communication", "values_resources", "commitment_structure",
        "growth_meaning", "conflict_drive", "identity_visibility",
    }
    return 1.05 if professional_priority.intersection(themes) else 0.95


def map_themes(themes: list[str], context: dict[str, Any]) -> list[str]:
    if not is_professional(context):
        return sorted(set(themes))
    return sorted({PROFESSIONAL_THEME_MAP.get(theme, theme) for theme in themes})


def object_name(name: str, context: dict[str, Any]) -> str:
    if not is_professional(context):
        return name
    return PROFESSIONAL_OBJECT_NAMES.get(name, name)


def house_domain(house: int, context: dict[str, Any]) -> str:
    general, professional = HOUSE_DOMAINS.get(house, (f"house_{house}_domain", f"house_{house}_domain"))
    return professional if is_professional(context) else general
