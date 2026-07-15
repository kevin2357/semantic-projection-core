from __future__ import annotations

ASPECT_MAPPINGS = {
    "conjunction": {
        "relationship_type": "co_activates_and_fuses",
        "operators": ["co_activate", "fuse", "amplify"],
        "interaction_mode": "shared_activation",
        "salience": 1.00,
    },
    "opposition": {
        "relationship_type": "polarizes_and_alternates",
        "operators": ["polarize", "alternate", "mirror"],
        "interaction_mode": "competitive_alternation",
        "salience": 0.96,
    },
    "square": {
        "relationship_type": "interferes_and_forces_adaptation",
        "operators": ["interfere", "pressure", "force_adaptation"],
        "interaction_mode": "frictional_coordination",
        "salience": 0.98,
    },
    "trine": {
        "relationship_type": "facilitates_and_automates",
        "operators": ["facilitate", "automate", "support"],
        "interaction_mode": "low_friction_support",
        "salience": 0.88,
    },
    "sextile": {
        "relationship_type": "enables_optional_coordination",
        "operators": ["enable", "coordinate", "offer_pathway"],
        "interaction_mode": "available_coordination",
        "salience": 0.82,
    },
    "quincunx": {
        "relationship_type": "mismatches_and_requires_recalibration",
        "operators": ["misalign", "recalibrate", "adapt_repeatedly"],
        "interaction_mode": "recurrent_recalibration",
        "salience": 0.74,
    },
    "semisextile": {
        "relationship_type": "adjacent_low_bandwidth_coordination",
        "operators": ["adjacent_signal", "weakly_coordinate", "incrementally_adjust"],
        "interaction_mode": "low_bandwidth_adjacency",
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
