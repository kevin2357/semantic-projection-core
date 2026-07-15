from __future__ import annotations

import re
from typing import Any

from .composition import _operator_phrase, _subject_possessive, _words
from .models import RenderedSentence
from .resolver import ProjectedTermResolver

JsonDict = dict[str, Any]


def _relation_phrase(key: str, resolver: ProjectedTermResolver) -> str:
    entry = resolver.resolve_key(key) or {}
    guidance = entry.get("output_guidance") or {}
    raw = str(guidance.get("verb_phrase") or resolver.friendly_label(key) or key)
    raw = _words(raw)
    substitutions = {
        "co activates and fuses": "runs together with",
        "polarizes and alternates": "pulls against and alternates with",
        "interferes and forces adaptation": "creates friction with and forces adaptation in",
        "facilitates and automates": "naturally supports",
        "enables optional coordination": "can coordinate with",
        "mismatches and requires recalibration": "requires repeated recalibration with",
        "adjacent low bandwidth coordination": "maintains a subtle coordination channel with",
        "subsystems run together": "runs together with",
        "drives face off": "pulls against",
        "drive conflict requires outlet": "creates drive conflict with",
        "natural behavioral channel": "naturally supports",
        "trainable usable channel": "can be deliberately coordinated with",
        "awkward system recalibration": "requires repeated adjustment with",
        "subtle adjacent nudge": "maintains a subtle influence on",
    }
    return substitutions.get(raw, raw)


def render_relationship_sentence(
    row: JsonDict,
    objects: dict[str, JsonDict],
    registry: JsonDict,
    *,
    subject: str,
    style: str = "natural",
    focus_id: str | None = None,
) -> RenderedSentence:
    resolver = ProjectedTermResolver(registry)
    source = objects[str(row["source_id"])]
    target = objects[str(row["target_id"])]
    if focus_id is not None and str(target["id"]) == focus_id:
        source, target = target, source
    source_key = str(source["name"])
    target_key = str(target["name"])
    relation_key = str(row["relationship_type"])
    source_phrase = _operator_phrase(source_key, resolver)
    target_phrase = _operator_phrase(target_key, resolver)
    relation_phrase = _relation_phrase(relation_key, resolver)

    if style == "technical":
        text = f"{source_phrase.title()} {relation_phrase} {target_phrase}."
        template = "relationship.technical.explicit.v1"
    else:
        text = (
            f"{_subject_possessive(subject)} {source_phrase} {relation_phrase} "
            f"the {target_phrase}."
        )
        template = "relationship.natural.active.v1"
    text = re.sub(r"\s+", " ", text)
    return RenderedSentence(
        text=text,
        template_id=template,
        source_term_refs=[
            resolver.term_ref(source_key),
            resolver.term_ref(relation_key),
            resolver.term_ref(target_key),
        ],
        semantic_components={
            "source": source_key,
            "relation": relation_key,
            "target": target_key,
        },
    )
