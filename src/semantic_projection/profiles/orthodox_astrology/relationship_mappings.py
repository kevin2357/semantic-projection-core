from __future__ import annotations

ASPECT_MAPPINGS = {
    "conjunction": {
        "relationship_type": "fuses_and_amplifies",
        "operators": ["merge", "amplify", "co_activate"],
        "themes": ["fusion_intensity"],
        "salience": 1.00,
    },
    "opposition": {
        "relationship_type": "polarizes_and_mirrors",
        "operators": ["polarize", "mirror", "negotiate"],
        "themes": ["growth_edge"],
        "salience": 0.96,
    },
    "square": {
        "relationship_type": "pressures_and_develops",
        "operators": ["stress", "activate", "develop"],
        "themes": ["growth_edge"],
        "salience": 0.98,
    },
    "trine": {
        "relationship_type": "supports_and_facilitates",
        "operators": ["flow", "support", "facilitate"],
        "themes": ["ease_support"],
        "salience": 0.88,
    },
    "sextile": {
        "relationship_type": "enables_and_coordinates",
        "operators": ["cooperate", "enable", "coordinate"],
        "themes": ["ease_support"],
        "salience": 0.82,
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
        if isinstance(hint, dict):
            value = hint.get("operator")
        else:
            value = hint
        if value:
            values.append(str(value))
    return sorted(set(values))
