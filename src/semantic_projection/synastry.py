from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from typing import Any

from .contracts import ProjectionOptions, ProjectionRequest
from .engine import project
from .ids import projection_request_id
from .registry import ProjectionProfileRegistry

JsonDict = dict[str, Any]


@dataclass(slots=True)
class SynastryProjectionResult:
    request: ProjectionRequest
    artifact: JsonDict
    participant_index: JsonDict


def _owner(row: JsonDict) -> str | None:
    for key in ("subject_owner", "chart_owner", "participant_id", "owner_id"):
        value = row.get(key)
        if value is not None:
            return str(value)
    attrs = row.get("attributes") or {}
    for key in ("subject_owner", "chart_owner", "participant_id", "owner_id"):
        value = attrs.get(key)
        if value is not None:
            return str(value)
    return None


def _participant_index(source_graph: JsonDict, participants: list[JsonDict]) -> JsonDict:
    declared = {str(p["participant_id"]): deepcopy(p) for p in participants}
    object_owners: dict[str, str] = {}
    for obj in source_graph.get("objects") or []:
        owner = _owner(obj)
        if owner:
            object_owners[str(obj.get("id"))] = owner
            declared.setdefault(owner, {"participant_id": owner, "role": "unspecified"})
    return {
        "participants": [declared[key] for key in sorted(declared)],
        "object_owners": dict(sorted(object_owners.items())),
    }


def prepare_synastry_source_graph(
    source_graph: JsonDict,
    *,
    participants: list[JsonDict],
    relationship_kind: str,
) -> tuple[JsonDict, JsonDict]:
    """Attach participant ownership and endpoint-role facts without changing astrology."""
    graph = deepcopy(source_graph)
    index = _participant_index(graph, participants)
    owners = index["object_owners"]
    participant_by_id = {str(p["participant_id"]): p for p in index["participants"]}

    for obj in graph.get("objects") or []:
        owner = owners.get(str(obj.get("id")))
        if owner:
            obj["subject_owner"] = owner
            obj.setdefault("attributes", {})["participant_role"] = participant_by_id.get(owner, {}).get("role", "unspecified")
            obj["attributes"]["relationship_kind"] = relationship_kind

    for rel in graph.get("relationships") or []:
        source_id = str(rel.get("source_id") or rel.get("source_object_id") or "")
        target_id = str(rel.get("target_id") or rel.get("target_object_id") or "")
        source_owner = owners.get(source_id)
        target_owner = owners.get(target_id)
        attrs = rel.setdefault("attributes", {})
        attrs["relationship_kind"] = relationship_kind
        attrs["source_owner"] = source_owner
        attrs["target_owner"] = target_owner
        attrs["source_participant_role"] = participant_by_id.get(source_owner or "", {}).get("role")
        attrs["target_participant_role"] = participant_by_id.get(target_owner or "", {}).get("role")
        attrs["inter_participant"] = bool(source_owner and target_owner and source_owner != target_owner)
        rel["source_owner"] = source_owner
        rel["target_owner"] = target_owner

    graph["graph_type"] = "synastry"
    graph.setdefault("graph_version", "1.3.0")
    graph.setdefault("metadata", {})["graph_type"] = "synastry"
    graph["metadata"]["relationship_kind"] = relationship_kind
    graph["metadata"]["participants"] = deepcopy(index["participants"])
    return graph, index


def project_synastry(
    *,
    source_graph: JsonDict,
    structural_evidence: JsonDict,
    source_identity: JsonDict,
    participants: list[JsonDict],
    relationship_kind: str,
    profile_id: str,
    profile_version: str,
    context: JsonDict,
    registry: ProjectionProfileRegistry,
    options: JsonDict | None = None,
    source_registries: JsonDict | None = None,
) -> SynastryProjectionResult:
    graph, participant_index = prepare_synastry_source_graph(
        source_graph,
        participants=participants,
        relationship_kind=relationship_kind,
    )
    context_copy = deepcopy(context)
    context_copy["subject_scope"] = "synastry"
    context_copy["relationship_type"] = relationship_kind
    context_copy.setdefault("parameters", {})["participants"] = deepcopy(participant_index["participants"])
    options_dict = deepcopy(options or ProjectionOptions().to_dict())
    identity = deepcopy(source_identity)
    identity.setdefault("source_chart_ids", [])
    identity.setdefault("sensor_instance_id", None)
    identity["source_graph_type"] = "synastry"
    identity["relationship_kind"] = relationship_kind
    request = ProjectionRequest(
        request_id=projection_request_id(
            profile_id=profile_id,
            profile_version=profile_version,
            source_identity=identity,
            context=context_copy,
            options=options_dict,
        ),
        profile_id=profile_id,
        profile_version=profile_version,
        source_graph=graph,
        structural_evidence=deepcopy(structural_evidence),
        source_identity=identity,
        context=context_copy,
        source_registries=deepcopy(source_registries or {}),
        options=options_dict,
    )
    artifact = project(request, registry=registry).to_dict()
    artifact.setdefault("summary", {})["synastry"] = {
        "relationship_kind": relationship_kind,
        "participants": deepcopy(participant_index["participants"]),
        "participant_count": len(participant_index["participants"]),
        "inter_participant_relationship_count": sum(
            1 for row in artifact.get("relationships") or []
            if (row.get("attributes") or {}).get("inter_participant")
        ),
    }
    artifact.setdefault("indexes", {})["participants"] = deepcopy(participant_index)
    return SynastryProjectionResult(request=request, artifact=artifact, participant_index=participant_index)
