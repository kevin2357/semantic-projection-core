from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping


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
    "temporal_projection_source_bundle": "foundry_temporal_projection_source_bundle",
    "canonical_temporal_activation_graph": "canonical_temporal_activation_graph",
    "projected_temporal_activation_graph": "projected_temporal_activation_graph",
    "projected_semantic_graph": "projected_static_graph",
    "projection_forensic_audit": "projection_forensic_audit",
    "projection_qa_result": "projection_qa_result",
    "temporal_projection_qa_result": "temporal_projection_qa_result",
}


def identify_artifact(value: Mapping[str, Any]) -> ArtifactIdentity:
    metadata = value.get("metadata") if isinstance(value.get("metadata"), Mapping) else {}
    package_type = metadata.get("package_type")
    contract_version = metadata.get("contract_version")
    if value.get("request_contract") == "temporal_projection_request.v1":
        return ArtifactIdentity(
            kind="temporal_projection_request",
            package_type="temporal_projection_request",
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
