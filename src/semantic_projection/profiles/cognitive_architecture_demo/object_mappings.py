from __future__ import annotations

OBJECT_MAPPINGS = {
    "Sun": {
        "target_name": "identity_organization",
        "object_type": "cognitive_process_primitive",
        "operators": ["organize", "prioritize", "stabilize"],
        "domains": ["central_coherence", "identity_priority", "self_model"],
        "salience": 1.00,
    },
    "Moon": {
        "target_name": "emotional_regulation",
        "object_type": "cognitive_process_primitive",
        "operators": ["regulate", "retain", "signal_need"],
        "domains": ["affect_regulation", "safety_memory", "habit"],
        "salience": 1.00,
    },
    "Mercury": {
        "target_name": "communication_processing",
        "object_type": "cognitive_process_primitive",
        "operators": ["encode", "compare", "translate", "exchange"],
        "domains": ["symbolic_processing", "attention_switching", "communication"],
        "salience": 0.94,
    },
    "Venus": {
        "target_name": "valuation_preference",
        "object_type": "cognitive_process_primitive",
        "operators": ["evaluate", "prefer", "weight", "harmonize"],
        "domains": ["preference_weighting", "value_assignment", "affiliative_tuning"],
        "salience": 0.92,
    },
    "Mars": {
        "target_name": "action_selection",
        "object_type": "cognitive_process_primitive",
        "operators": ["mobilize", "select_action", "assert", "defend"],
        "domains": ["action_selection", "effort_allocation", "boundary_response"],
        "salience": 0.94,
    },
    "Jupiter": {
        "target_name": "meaning_abstraction",
        "object_type": "cognitive_process_primitive",
        "operators": ["generalize", "expand", "contextualize", "forecast"],
        "domains": ["abstraction", "possibility_generation", "meaning_modeling"],
        "salience": 0.84,
    },
    "Saturn": {
        "target_name": "constraint_management",
        "object_type": "cognitive_process_primitive",
        "operators": ["constrain", "sequence", "inhibit", "stabilize"],
        "domains": ["constraint_management", "durability", "error_control"],
        "salience": 0.90,
    },
    "Uranus": {
        "target_name": "change_adaptation",
        "object_type": "cognitive_process_primitive",
        "operators": ["disrupt", "differentiate", "update", "novelize"],
        "domains": ["novelty_detection", "change_adaptation", "model_revision"],
        "salience": 0.78,
    },
    "Neptune": {
        "target_name": "imagination_permeability",
        "object_type": "cognitive_process_primitive",
        "operators": ["simulate", "blur", "associate", "idealize"],
        "domains": ["imagination", "ambiguity_processing", "boundary_permeability"],
        "salience": 0.76,
    },
    "Pluto": {
        "target_name": "intensity_transformation",
        "object_type": "cognitive_process_primitive",
        "operators": ["intensify", "transform", "expose", "control"],
        "domains": ["deep_reorganization", "control_processing", "salience_intensity"],
        "salience": 0.82,
    },
    "North Node": {
        "target_name": "developmental_orientation",
        "object_type": "cognitive_orientation_primitive",
        "operators": ["orient", "develop", "approach"],
        "domains": ["developmental_pull", "learning_direction"],
        "salience": 0.68,
    },
    "South Node": {
        "target_name": "default_pattern_memory",
        "object_type": "cognitive_orientation_primitive",
        "operators": ["default", "revert", "reuse"],
        "domains": ["familiar_strategy", "fallback_pattern"],
        "salience": 0.62,
    },
    "Part of Fortune": {
        "target_name": "resource_ease_convergence",
        "object_type": "cognitive_orientation_primitive",
        "operators": ["converge", "resource", "ease"],
        "domains": ["resource_availability", "low_friction_gain"],
        "salience": 0.56,
    },
    "Vertex": {
        "target_name": "external_trigger_interface",
        "object_type": "cognitive_interface_primitive",
        "operators": ["trigger", "encounter", "externalize"],
        "domains": ["externally_evoked_change", "encounter_channel"],
        "salience": 0.52,
    },
    "ASC": {
        "target_name": "active_interface",
        "object_type": "cognitive_interface_primitive",
        "operators": ["interface", "initiate_response", "present"],
        "domains": ["first_response_policy", "system_boundary"],
        "salience": 0.98,
    },
    "DSC": {
        "target_name": "counterpart_model",
        "object_type": "cognitive_interface_primitive",
        "operators": ["model_other", "complement", "negotiate"],
        "domains": ["dyadic_modeling", "external_complement"],
        "salience": 0.93,
    },
    "IC": {
        "target_name": "internal_foundation",
        "object_type": "cognitive_interface_primitive",
        "operators": ["root", "baseline", "privatize"],
        "domains": ["private_state_baseline", "foundational_memory"],
        "salience": 0.93,
    },
    "MC": {
        "target_name": "executive_output_direction",
        "object_type": "cognitive_interface_primitive",
        "operators": ["direct", "prioritize_output", "externalize"],
        "domains": ["visible_objective", "executive_direction"],
        "salience": 0.96,
    },
}

SIGN_MODES = {
    "Aries": "initiation_mode",
    "Taurus": "stabilization_persistence_mode",
    "Gemini": "differentiation_exchange_mode",
    "Cancer": "protective_attachment_mode",
    "Leo": "expressive_self_amplification_mode",
    "Virgo": "error_correction_refinement_mode",
    "Libra": "comparative_balancing_mode",
    "Scorpio": "deep_search_guarded_transformation_mode",
    "Sagittarius": "abstraction_exploration_mode",
    "Capricorn": "hierarchical_goal_constraint_mode",
    "Aquarius": "system_revision_differentiation_mode",
    "Pisces": "associative_permeable_integration_mode",
}

HOUSE_DOMAINS = {
    1: "self_interface_response_initiation",
    2: "resource_valuation_stability",
    3: "local_information_exchange",
    4: "foundational_memory_internal_base",
    5: "generative_expression_play",
    6: "maintenance_routine_error_correction",
    7: "dyadic_modeling_counterpart_interaction",
    8: "shared_risk_deep_integration",
    9: "abstraction_worldview_long_range_learning",
    10: "executive_direction_public_output",
    11: "network_coordination_future_modeling",
    12: "latent_processing_hidden_state_integration",
}

ALIASES = {
    "Ascendant": "ASC",
    "Descendant": "DSC",
    "Midheaven": "MC",
    "Imum Coeli": "IC",
    "True Node": "North Node",
    "True_Node": "North Node",
    "Mean Node": "North Node",
    "Mean_Node": "North Node",
    "North_Node": "North Node",
    "South_Node": "South Node",
    "Fortune": "Part of Fortune",
    "Part_of_Fortune": "Part of Fortune",
}


def canonical_object_name(source_object: dict) -> str:
    raw = str(
        source_object.get("name")
        or source_object.get("source_key")
        or source_object.get("id")
        or ""
    )
    for token in (
        "natal:", "transit:", "composite:", "davison:", "solar_return:",
        "person_a:", "person_b:",
    ):
        raw = raw.replace(token, "")
    raw = raw.split(":")[-1].split("_H")[0].replace("_", " ")
    return ALIASES.get(raw, raw)


def source_sign(source_object: dict) -> str | None:
    facts = source_object.get("facts") or {}
    value = source_object.get("sign") or facts.get("sign")
    return str(value) if value else None


def source_house(source_object: dict) -> int | None:
    facts = source_object.get("facts") or {}
    value = source_object.get("house") or facts.get("house")
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def house_cusp_number(source_object: dict) -> int | None:
    if source_object.get("object_type") != "house_cusp":
        return None
    return source_house(source_object)



def raw_source_name(source_object: dict) -> str:
    raw = str(
        source_object.get("name")
        or source_object.get("source_key")
        or source_object.get("id")
        or ""
    )
    for token in (
        "natal:", "transit:", "composite:", "davison:", "solar_return:",
        "person_a:", "person_b:",
    ):
        raw = raw.replace(token, "")
    return raw.split(":")[-1].split("_H")[0].replace("_", " ")


def source_selection_status(source_object: dict) -> str:
    raw = raw_source_name(source_object)
    if raw in {"Mean Node", "Mean_Node"}:
        return "excluded_by_source_selection_policy"
    if raw == "Fortune":
        return "excluded_by_source_selection_policy"
    return "eligible"
