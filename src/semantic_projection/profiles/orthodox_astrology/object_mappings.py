from __future__ import annotations

OBJECT_MAPPINGS = {
    "Sun": {
        "target_name": "identity_vitality",
        "operators": ["illuminate", "prioritize", "express"],
        "themes": ["identity_visibility"],
        "domains": ["identity", "vitality", "purpose", "visibility"],
        "salience": 1.00,
    },
    "Moon": {
        "target_name": "emotional_regulation",
        "operators": ["regulate", "need", "remember"],
        "themes": ["emotional_safety", "home_family"],
        "domains": ["emotion", "security", "memory", "habit"],
        "salience": 1.00,
    },
    "Mercury": {
        "target_name": "communication_interpretation",
        "operators": ["represent", "translate", "interpret", "compare"],
        "themes": ["communication"],
        "domains": ["communication", "thought", "exchange", "interpretation"],
        "salience": 0.92,
    },
    "Venus": {
        "target_name": "value_attraction_harmony",
        "operators": ["connect", "attract", "value", "bond"],
        "themes": ["romance_affection", "values_resources"],
        "domains": ["values", "attraction", "harmony", "relationship"],
        "salience": 0.94,
    },
    "Mars": {
        "target_name": "action_assertion_drive",
        "operators": ["act", "assert", "defend", "initiate"],
        "themes": ["conflict_drive"],
        "domains": ["action", "assertion", "desire", "conflict"],
        "salience": 0.94,
    },
    "Jupiter": {
        "target_name": "growth_meaning_expansion",
        "operators": ["contextualize", "expand", "synthesize", "encourage"],
        "themes": ["growth_meaning"],
        "domains": ["growth", "meaning", "belief", "opportunity"],
        "salience": 0.84,
    },
    "Saturn": {
        "target_name": "structure_constraint_commitment",
        "operators": ["stabilize", "constrain", "endure", "structure"],
        "themes": ["commitment_structure"],
        "domains": ["structure", "constraint", "commitment", "durability"],
        "salience": 0.90,
    },
    "Uranus": {
        "target_name": "freedom_change_disruption",
        "operators": ["differentiate", "liberate", "disrupt", "individuate"],
        "themes": ["freedom_change"],
        "domains": ["change", "freedom", "novelty", "disruption"],
        "salience": 0.78,
    },
    "Neptune": {
        "target_name": "imagination_idealization_permeability",
        "operators": ["imagine", "dissolve", "idealize", "spiritualize"],
        "themes": ["dream_idealization"],
        "domains": ["imagination", "idealization", "permeability", "ambiguity"],
        "salience": 0.76,
    },
    "Pluto": {
        "target_name": "depth_power_transformation",
        "operators": ["intensify", "transform", "expose", "empower"],
        "themes": ["depth_power"],
        "domains": ["power", "depth", "transformation", "intensity"],
        "salience": 0.82,
    },
    "ASC": {
        "target_name": "identity_interface",
        "operators": ["interface", "present", "enter"],
        "themes": ["identity_visibility"],
        "domains": ["presentation", "interface", "approach"],
        "salience": 0.98,
    },
    "DSC": {
        "target_name": "partnership_mirror",
        "operators": ["mirror", "partner", "externalize"],
        "themes": ["partnership_mirroring"],
        "domains": ["partnership", "mirroring", "other"],
        "salience": 0.93,
    },
    "MC": {
        "target_name": "public_direction",
        "operators": ["publicize", "aspire", "direct"],
        "themes": ["identity_visibility"],
        "domains": ["career", "public role", "direction"],
        "salience": 0.96,
    },
    "IC": {
        "target_name": "private_roots",
        "operators": ["root", "secure", "privatize"],
        "themes": ["home_family"],
        "domains": ["roots", "home", "private foundation"],
        "salience": 0.93,
    },
}

ALIASES = {
    "Ascendant": "ASC",
    "Descendant": "DSC",
    "Midheaven": "MC",
    "Imum Coeli": "IC",
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
    raw = raw.split(":")[-1].split("_H")[0]
    return ALIASES.get(raw, raw)



def house_number(source_object: dict) -> int | None:
    if source_object.get("object_type") != "house_cusp":
        return None
    facts = source_object.get("facts") or {}
    value = facts.get("house") or source_object.get("house")
    try:
        return int(value)
    except (TypeError, ValueError):
        return None
