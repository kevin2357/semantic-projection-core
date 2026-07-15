from __future__ import annotations

OBJECT_MAPPINGS = {
    "Sun": {
        "target_name": "pack_role_identity",
        "object_type": "woofmapped_operator",
        "operators": ["coordinate_whole_dog", "express_pack_role", "vitalize"],
        "domains": ["pack_identity", "whole_dog_coordination", "vitality"],
        "salience": 1.00,
    },
    "Moon": {
        "target_name": "comfort_safety_regulation",
        "object_type": "woofmapped_operator",
        "operators": ["regulate_body_state", "seek_safety", "retain_comfort_memory"],
        "domains": ["comfort", "safety", "body_state", "attachment"],
        "salience": 1.00,
    },
    "Mercury": {
        "target_name": "scent_signal_interpretation",
        "object_type": "woofmapped_operator",
        "operators": ["decode_cue", "interpret_scent", "predict_routine", "signal"],
        "domains": ["scent_ecology", "cue_processing", "routine_prediction"],
        "salience": 0.94,
    },
    "Venus": {
        "target_name": "bonding_preference",
        "object_type": "woofmapped_operator",
        "operators": ["bond", "prefer", "enjoy", "affiliate"],
        "domains": ["favorite_humans", "treats", "toys", "affection_style"],
        "salience": 0.94,
    },
    "Mars": {
        "target_name": "chase_play_defense_drive",
        "object_type": "woofmapped_operator",
        "operators": ["chase", "play_attack", "assert", "defend", "execute"],
        "domains": ["pursuit", "play", "immediate_action", "defense"],
        "salience": 0.96,
    },
    "Jupiter": {
        "target_name": "adventure_optimism",
        "object_type": "woofmapped_operator",
        "operators": ["explore", "expand_radius", "encourage", "roam"],
        "domains": ["curiosity_radius", "adventure", "confidence"],
        "salience": 0.84,
    },
    "Saturn": {
        "target_name": "training_rule_structure",
        "object_type": "woofmapped_operator",
        "operators": ["train", "limit", "sequence", "inhibit_impulse", "routinize"],
        "domains": ["training", "rules", "routine", "impulse_control"],
        "salience": 0.92,
    },
    "Uranus": {
        "target_name": "novelty_zoomie_response",
        "object_type": "woofmapped_operator",
        "operators": ["startle", "disrupt", "individuate", "zoom"],
        "domains": ["novelty", "surprise", "independence", "weirdness"],
        "salience": 0.78,
    },
    "Neptune": {
        "target_name": "atmosphere_dream_permeability",
        "object_type": "woofmapped_operator",
        "operators": ["dream", "absorb_atmosphere", "blur_signal", "drift"],
        "domains": ["dreaming", "scent_memory_haze", "emotional_atmosphere"],
        "salience": 0.76,
    },
    "Pluto": {
        "target_name": "primal_trust_intensity",
        "object_type": "woofmapped_operator",
        "operators": ["fixate", "intensify", "guard", "transform_trust"],
        "domains": ["primal_drive", "territory", "hierarchy", "deep_trust_fear"],
        "salience": 0.84,
    },
    "North Node": {
        "target_name": "training_development_vector",
        "object_type": "woofmapped_orientation",
        "operators": ["develop", "learn_toward", "practice"],
        "domains": ["growth_direction", "training_path"],
        "salience": 0.68,
    },
    "South Node": {
        "target_name": "instinctive_fallback_pattern",
        "object_type": "woofmapped_orientation",
        "operators": ["fallback", "revert", "default"],
        "domains": ["stress_default", "familiar_instinct"],
        "salience": 0.62,
    },
    "Part of Fortune": {
        "target_name": "easy_good_thing_channel",
        "object_type": "woofmapped_orientation",
        "operators": ["resource", "reward", "ease"],
        "domains": ["treat_flow", "comfort_resource", "easy_success"],
        "salience": 0.56,
    },
    "Vertex": {
        "target_name": "unexpected_encounter_trigger",
        "object_type": "woofmapped_interface",
        "operators": ["encounter", "trigger", "externalize"],
        "domains": ["surprise_meeting", "externally_evoked_behavior"],
        "salience": 0.52,
    },
    "ASC": {
        "target_name": "behavioral_doorway",
        "object_type": "woofmapped_interface",
        "operators": ["meet_world", "present", "first_respond"],
        "domains": ["first_impression", "visible_temperament", "doorway_behavior"],
        "salience": 0.98,
    },
    "DSC": {
        "target_name": "primary_companion_interface",
        "object_type": "woofmapped_interface",
        "operators": ["bond_with_other", "receive_companion", "mirror"],
        "domains": ["favorite_human", "one_to_one_bond", "counterpart_style"],
        "salience": 0.94,
    },
    "IC": {
        "target_name": "safe_den_baseline",
        "object_type": "woofmapped_interface",
        "operators": ["root", "retreat", "secure_den"],
        "domains": ["private_safety", "home_base", "base_camp"],
        "salience": 0.94,
    },
    "MC": {
        "target_name": "visible_pack_function",
        "object_type": "woofmapped_interface",
        "operators": ["perform_pack_role", "be_known_for", "direct_function"],
        "domains": ["guardian_role", "greeter_role", "helper_role", "couch_supervision"],
        "salience": 0.96,
    },
}

SIGN_MODES = {
    "Aries": "immediate_chase_mode",
    "Taurus": "nap_spot_loyalty_mode",
    "Gemini": "information_sniffing_mode",
    "Cancer": "pack_security_focus_mode",
    "Leo": "attention_seeking_display_mode",
    "Virgo": "patrol_inspection_mode",
    "Libra": "social_harmony_maintenance_mode",
    "Scorpio": "obsessive_investigation_mode",
    "Sagittarius": "adventure_dog_mode",
    "Capricorn": "working_dog_seriousness_mode",
    "Aquarius": "pattern_breaking_oddball_mode",
    "Pisces": "emotional_sponge_dream_dog_mode",
}

DOGHOUSE_DOMAINS = {
    1: "doghouse_1_body_temperament_presence",
    2: "doghouse_2_food_toys_bones_resources",
    3: "doghouse_3_smells_barks_cues_local_data",
    4: "doghouse_4_den_home_base_safety",
    5: "doghouse_5_play_zoomies_tricks",
    6: "doghouse_6_training_routine_care",
    7: "doghouse_7_favorite_human_primary_bond",
    8: "doghouse_8_deep_trust_vulnerability",
    9: "doghouse_9_adventure_territory",
    10: "doghouse_10_visible_pack_role",
    11: "doghouse_11_social_pack_network",
    12: "doghouse_12_deep_instinct_hidden_fear",
}

ALIASES = {
    "Ascendant": "ASC", "Descendant": "DSC", "Midheaven": "MC", "Imum Coeli": "IC",
    "True Node": "North Node", "True_Node": "North Node",
    "Mean Node": "North Node", "Mean_Node": "North Node",
    "North_Node": "North Node", "South_Node": "South Node",
    "Fortune": "Part of Fortune", "Part_of_Fortune": "Part of Fortune",
}


def canonical_object_name(source_object: dict) -> str:
    raw = str(source_object.get("name") or source_object.get("source_key") or source_object.get("id") or "")
    for token in ("natal:", "transit:", "composite:", "davison:", "solar_return:", "person_a:", "person_b:"):
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
