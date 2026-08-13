from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class ArtifactIdentity:
    kind: str
    package_type: str | None
    contract_version: str | None
    recognized: bool

    def to_dict(self) -> dict[str, Any]:
        return {
            "kind": self.kind,
            "package_type": self.package_type,
            "contract_version": self.contract_version,
            "recognized": self.recognized,
        }


_KIND_BY_PACKAGE_TYPE = {
    "bounded_natal_dataset": "foundry_bounded_natal_dataset",
    "temporal_projection_source_bundle": "foundry_temporal_projection_source_bundle",
    "canonical_temporal_activation_graph": "canonical_temporal_activation_graph",
    "projected_temporal_activation_graph": "projected_temporal_activation_graph",
    "projected_semantic_graph": "projected_static_graph",
    "projected_bounded_semantic_graph": "projected_bounded_graph",
    "projection_forensic_audit": "projection_forensic_audit",
    "projection_qa_result": "projection_qa_result",
    "temporal_projection_qa_result": "temporal_projection_qa_result",
    "temporal_projection_route_receipt": "temporal_projection_route_receipt",
}


def identify_artifact(value: Mapping[str, Any]) -> ArtifactIdentity:
    metadata = value.get("metadata") if isinstance(value.get("metadata"), Mapping) else {}
    package_type = metadata.get("package_type")
    contract_version = metadata.get("contract_version")
    if value.get("request_contract") == "bounded_natal_projection_request.v1":
        return ArtifactIdentity(
            kind="bounded_natal_projection_request",
            package_type="bounded_natal_projection_request",
            contract_version="1.0.0",
            recognized=True,
        )
    if metadata.get("analysis_type") == "bounded_natal_dataset":
        return ArtifactIdentity(
            kind="foundry_bounded_natal_dataset",
            package_type="bounded_natal_dataset",
            contract_version=str(metadata.get("schema_version") or ""),
            recognized=True,
        )
    if value.get("request_contract") == "temporal_projection_request.v1":
        return ArtifactIdentity(
            kind="temporal_projection_request",
            package_type="temporal_projection_request",
            contract_version="1.0.0",
            recognized=True,
        )
    if all(key in value for key in ("request_id", "profile_id", "source_graph", "context")):
        return ArtifactIdentity(
            kind="projection_request",
            package_type="projection_request",
            contract_version="1.0.0",
            recognized=True,
        )
    kind = _KIND_BY_PACKAGE_TYPE.get(str(package_type))
    return ArtifactIdentity(
        kind=kind or "unknown",
        package_type=str(package_type) if package_type is not None else None,
        contract_version=str(contract_version) if contract_version is not None else None,
        recognized=kind is not None,
    )
