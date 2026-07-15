"""Deterministic semantic composition for projected graphs."""

from .composition import render_object_sentence
from .local_narrative import render_local_narrative
from .models import LocalNarrative, RenderedSentence
from .relationships import render_relationship_sentence
from .resolver import ProjectedTermResolutionError, ProjectedTermResolver, object_index

__all__ = [
    "LocalNarrative",
    "ProjectedTermResolutionError",
    "ProjectedTermResolver",
    "RenderedSentence",
    "object_index",
    "render_local_narrative",
    "render_object_sentence",
    "render_relationship_sentence",
]
