from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

JsonDict = dict[str, Any]


@dataclass(frozen=True)
class RenderedSentence:
    text: str
    template_id: str
    source_term_refs: list[str] = field(default_factory=list)
    semantic_components: JsonDict = field(default_factory=dict)

    def to_dict(self) -> JsonDict:
        return asdict(self)


@dataclass(frozen=True)
class LocalNarrative:
    object_id: str
    central_sentence: RenderedSentence
    relationship_sentences: list[RenderedSentence]
    paragraph: str
    source_term_refs: list[str]
    template_ids: list[str]

    def to_dict(self) -> JsonDict:
        return {
            "object_id": self.object_id,
            "central_sentence": self.central_sentence.to_dict(),
            "relationship_sentences": [row.to_dict() for row in self.relationship_sentences],
            "paragraph": self.paragraph,
            "source_term_refs": list(self.source_term_refs),
            "template_ids": list(self.template_ids),
        }
