from __future__ import annotations

from typing import Any, Protocol, runtime_checkable

from .contracts import ProjectionContext, ProjectionProfileManifest, ProjectionRequest, ProjectedSemanticGraph

JsonDict = dict[str, Any]


@runtime_checkable
class ProjectionProfile(Protocol):
    """Extraction-ready interface implemented by all projection profiles.

    Profiles return plain-data drafts. The engine owns identifiers, provenance,
    merge behavior, audit records, diagnostics, ordering, and validation.
    """

    manifest: ProjectionProfileManifest

    def validate_context(self, context: ProjectionContext) -> list[JsonDict]:
        ...

    def project_object(
        self,
        source_object: JsonDict,
        request: ProjectionRequest,
    ) -> list[JsonDict]:
        ...

    def project_relationship(
        self,
        source_relationship: JsonDict,
        projected_object_index: dict[str, list[JsonDict]],
        request: ProjectionRequest,
    ) -> list[JsonDict]:
        ...

    def finalize(
        self,
        graph: ProjectedSemanticGraph,
        request: ProjectionRequest,
    ) -> None:
        ...
