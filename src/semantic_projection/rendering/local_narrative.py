from __future__ import annotations

from typing import Any

from .composition import render_object_sentence
from .models import LocalNarrative
from .relationships import render_relationship_sentence
from .resolver import object_index

JsonDict = dict[str, Any]


def render_local_narrative(
    graph: JsonDict,
    object_id: str,
    *,
    subject: str,
    relationship_limit: int = 4,
    style: str = "natural",
) -> LocalNarrative:
    objects = object_index(graph)
    if object_id not in objects:
        raise KeyError(f"projected object not found: {object_id}")
    registry = graph.get("projected_term_registry") or {}
    central = render_object_sentence(objects[object_id], registry, subject=subject, style=style)
    connected = [
        row for row in graph.get("relationships") or []
        if row.get("source_id") == object_id or row.get("target_id") == object_id
    ]
    deduplicated = {}
    for row in connected:
        other_id = (
            str(row.get("target_id"))
            if str(row.get("source_id")) == object_id
            else str(row.get("source_id"))
        )
        key = (other_id, str(row.get("relationship_type")))
        existing = deduplicated.get(key)
        if existing is None or float(row.get("projection_relevance_score") or 0.0) > float(existing.get("projection_relevance_score") or 0.0):
            deduplicated[key] = row
    connected = list(deduplicated.values())
    connected.sort(
        key=lambda row: (
            -float(row.get("projection_relevance_score") or 0.0),
            str(row.get("id")),
        )
    )
    rendered = [
        render_relationship_sentence(
            row, objects, registry, subject=subject, style=style, focus_id=object_id
        )
        for row in connected[:relationship_limit]
    ]
    sentences = [central.text, *[row.text for row in rendered]]
    paragraph = " ".join(sentences)
    refs = sorted({ref for row in [central, *rendered] for ref in row.source_term_refs if ref})
    templates = [central.template_id, *[row.template_id for row in rendered]]
    return LocalNarrative(
        object_id=object_id,
        central_sentence=central,
        relationship_sentences=rendered,
        paragraph=paragraph,
        source_term_refs=refs,
        template_ids=templates,
    )
