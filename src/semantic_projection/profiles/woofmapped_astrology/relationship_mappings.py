from __future__ import annotations

ASPECT_MAPPINGS = {
    "conjunction": {
        "relationship_type": "subsystems_run_together",
        "operators": ["fuse_impulses", "co_activate", "amplify"],
        "interaction_mode": "inseparable_dog_impulse",
        "salience": 1.00,
    },
    "opposition": {
        "relationship_type": "drives_face_off",
        "operators": ["polarize", "alternate", "mirror"],
        "interaction_mode": "bond_freedom_axis_tension",
        "salience": 0.96,
    },
    "square": {
        "relationship_type": "drive_conflict_requires_outlet",
        "operators": ["frustrate", "activate", "require_training_or_outlet"],
        "interaction_mode": "behavioral_friction",
        "salience": 0.98,
    },
    "trine": {
        "relationship_type": "natural_behavioral_channel",
        "operators": ["flow", "support", "habitualize"],
        "interaction_mode": "easy_habit_or_talent",
        "salience": 0.88,
    },
    "sextile": {
        "relationship_type": "trainable_usable_channel",
        "operators": ["enable", "practice", "coordinate"],
        "interaction_mode": "developable_coordination",
        "salience": 0.82,
    },
    "quincunx": {
        "relationship_type": "awkward_system_recalibration",
        "operators": ["misfit", "recalibrate", "manage"],
        "interaction_mode": "odd_behavior_needing_adjustment",
        "salience": 0.74,
    },
    "semisquare": {
        "relationship_type": "repeated_behavioral_irritant",
        "operators": ["irritate", "repeat", "require_small_adjustment"],
        "interaction_mode": "minor_repeating_friction",
        "salience": 0.64,
    },
    "sesquisquare": {
        "relationship_type": "persistent_adjustment_pressure",
        "operators": ["pressure", "persist", "adjust"],
        "interaction_mode": "persistent_behavioral_adjustment",
        "salience": 0.68,
    },
    "semisextile": {
        "relationship_type": "subtle_adjacent_nudge",
        "operators": ["nudge", "irritate_lightly", "incrementally_coordinate"],
        "interaction_mode": "minor_behavioral_nudge",
        "salience": 0.58,
    },
}


def canonical_aspect(source_relationship: dict) -> str:
    return str(source_relationship.get("aspect") or "").strip().lower()


def source_operator_strings(row: dict) -> list[str]:
    values = []
    for hint in (
        row.get("operator_hints")
        or row.get("source_operator_hints")
        or row.get("semantic_operator_hints")
        or []
    ):
        value = hint.get("operator") if isinstance(hint, dict) else hint
        if value:
            values.append(str(value))
    return sorted(set(values))
