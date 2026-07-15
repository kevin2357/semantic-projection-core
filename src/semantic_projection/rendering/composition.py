from __future__ import annotations

import re
from typing import Any

from .models import RenderedSentence
from .resolver import ProjectedTermResolver

JsonDict = dict[str, Any]


_ARTICLES = {"a", "an", "the"}


def _words(value: str) -> str:
    return re.sub(r"\s+", " ", value.replace("_", " ")).strip()


def _strip_suffix(value: str, suffix: str) -> str:
    words = _words(value)
    return words[: -len(suffix)].strip() if words.endswith(suffix) else words


def _subject_possessive(subject: str) -> str:
    return subject + "'" if subject.lower().endswith("s") else subject + "'s"


def _operator_phrase(key: str, resolver: ProjectedTermResolver) -> str:
    entry = resolver.resolve_key(key) or {}
    guidance = entry.get("output_guidance") or {}
    phrase = guidance.get("noun_phrase") or resolver.friendly_label(key) or key
    phrase = _words(str(phrase))
    return phrase.removeprefix("the subject's ").strip()


def _facet_phrase(key: str | None, resolver: ProjectedTermResolver, *, excluded: set[str]) -> str | None:
    if not key:
        return None
    entry = resolver.resolve_key(key) or {}
    facets = [
        _words(str(value)) for value in entry.get("semantic_facets") or []
        if _words(str(value)).lower() not in excluded
    ]
    if not facets:
        return None
    if len(facets) == 1:
        return facets[0]
    return ", ".join(facets[:-1]) + f", and {facets[-1]}"


def _mode_phrase(key: str | None, resolver: ProjectedTermResolver) -> str | None:
    if not key:
        return None
    resolver.resolve_key(key)
    raw = _strip_suffix(_words(key), " mode")
    raw = raw.replace("self amplification", "self-amplification")
    raw = raw.replace("attention seeking", "attention-seeking")
    raw = raw.replace("dream dog", "dream-dog")
    return raw


def _domain_phrase(key: str | None, resolver: ProjectedTermResolver) -> str | None:
    if not key:
        return None
    resolver.resolve_key(key)
    number = None
    raw_key = key
    match = re.match(r"doghouse_(\d+)_(.+)", key)
    if match:
        number, raw_key = match.group(1), match.group(2)
    tokens = raw_key.split("_")
    if len(tokens) == 3:
        concept = f"{tokens[0]} {tokens[1]} and {tokens[2]}"
    elif len(tokens) == 4:
        concept = f"{tokens[0]} {tokens[1]} and {tokens[2]} {tokens[3]}"
    elif len(tokens) == 5 and tokens[-3:] == ["long", "range", "learning"]:
        concept = " ".join(tokens[:2]) + " and long-range learning"
    else:
        concept = " ".join(tokens)
    return f"Doghouse {number} contexts involving {concept}" if number else f"situations involving {concept}"

def _gerund(phrase: str) -> str:
    parts = phrase.split(" ", 1)
    verb = parts[0]
    rest = f" {parts[1]}" if len(parts) > 1 else ""
    if verb.endswith("ie"):
        verb = verb[:-2] + "ying"
    elif verb.endswith("e") and not verb.endswith(("ee", "ye")):
        verb = verb[:-1] + "ing"
    elif verb.endswith("ing"):
        pass
    else:
        verb += "ing"
    return verb + rest


def _list_phrase(values: list[str]) -> str:
    if not values:
        return ""
    if len(values) == 1:
        return values[0]
    return ", ".join(values[:-1]) + f", and {values[-1]}"


def _operator_verbs(row: JsonDict, entry: JsonDict) -> list[str]:
    values = list(entry.get("core_operators") or []) or list(row.get("operators") or [])
    cleaned = []
    for value in values:
        word = _words(str(value))
        if word and word not in cleaned:
            cleaned.append(word)
    return cleaned[:4]


def render_object_sentence(
    row: JsonDict,
    registry: JsonDict,
    *,
    subject: str,
    style: str = "natural",
    variant: int = 0,
) -> RenderedSentence:
    resolver = ProjectedTermResolver(registry)
    attrs = row.get("attributes") or {}
    term_key = str(row.get("name") or "")
    mode_key = attrs.get("projected_mode")
    domain_key = attrs.get("projected_domain")
    term = resolver.resolve_key(term_key) or {}
    operator = _operator_phrase(term_key, resolver)
    mode = _mode_phrase(mode_key, resolver)
    domain = _domain_phrase(domain_key, resolver)
    verbs = _operator_verbs(row, term)
    activity_text = _list_phrase([_gerund(value) for value in verbs])

    refs = [resolver.term_ref(term_key)]
    if mode_key:
        refs.append(resolver.term_ref(str(mode_key)))
    if domain_key:
        refs.append(resolver.term_ref(str(domain_key)))
    refs = [ref for ref in refs if ref]

    if style == "technical":
        text = f"{_subject_possessive(subject)} {operator}"
        if mode:
            text += f" operates through {mode}"
        if domain:
            text += f" in {domain}"
        text += "."
        template = "object.technical.explicit_composition.v1"
    elif variant % 2 == 1 and domain:
        text = f"{_subject_possessive(subject)} {operator} is most active in {domain}"
        if activity_text:
            text += f", where it supports {activity_text}"
        if mode:
            text += f" with an emphasis on {mode}"
        text += "."
        template = "object.natural.domain_emphasis.v1"
    else:
        text = f"{_subject_possessive(subject)} {operator}"
        if activity_text:
            text += f" is organized around {activity_text}"
        if mode:
            text += f", with an emphasis on {mode}"
        if domain:
            text += f", especially in {domain}"
        text += "."
        template = "object.natural.subject_mode_domain.v1"

    text = re.sub(r"\ba ([aeiouAEIOU])", r"an \1", text)
    return RenderedSentence(
        text=text,
        template_id=template,
        source_term_refs=refs,
        semantic_components={
            "operator": term_key,
            "mode": mode_key,
            "domain": domain_key,
            "verbs": verbs,
        },
    )
