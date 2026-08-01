from __future__ import annotations

from copy import deepcopy
from typing import Any

from semantic_projection import ProjectionOptions, ProjectionRequest, project, projection_request_id
from semantic_projection.profiles import builtin_projection_registry

TARGET_DOMAINS = {
    "orthodox_astrology.v1": "orthodox_astrology.v1",
    "cognitive_architecture_demo.v0": "cognitive_architecture_demo.v0",
    "woofmapped_astrology.v0": "woofmapped_astrology.v0",
}


def default_context(profile_id: str) -> dict[str, Any]:
    return {
        "context_id": "tests.default",
        "context_version": "1.0.0",
        "subject_scope": "dog" if profile_id == "woofmapped_astrology.v0" else "individual",
        "target_domain": TARGET_DOMAINS[profile_id],
        "application_context": "test",
        "constraints": {"house_mapping_policy": "doghouse"} if profile_id == "woofmapped_astrology.v0" else {},
        "parameters": {},
        "extensions": {},
    }


def projection_request_from_package(
    source_package: dict[str, Any],
    *,
    profile_id: str = "orthodox_astrology.v1",
    profile_version: str = "1.0.0",
    context: Any = None,
    options: Any = None,
) -> ProjectionRequest:
    graph = deepcopy(source_package.get("canonical_astrology_graph") or source_package.get("source_graph") or {})
    metadata = source_package.get("metadata") or {}
    identity = {
        "source_chart_id": metadata.get("source_chart_id"),
        "source_chart_ids": metadata.get("source_chart_ids") or [],
        "sensor_instance_id": metadata.get("sensor_instance_id"),
    }
    context_dict = context.to_dict() if hasattr(context, "to_dict") else deepcopy(context or default_context(profile_id))
    options_dict = options.to_dict() if hasattr(options, "to_dict") else deepcopy(options or ProjectionOptions().to_dict())
    return ProjectionRequest(
        request_id=projection_request_id(
            profile_id=profile_id,
            profile_version=profile_version,
            source_identity=identity,
            context=context_dict,
            options=options_dict,
        ),
        profile_id=profile_id,
        profile_version=profile_version,
        source_graph=graph,
        structural_evidence=deepcopy(source_package.get("structural_evidence_graph") or {}),
        source_identity=identity,
        context=context_dict,
        source_registries=deepcopy(source_package.get("source_registries") or {}),
        options=options_dict,
    )


def project_dataset(source_package: dict[str, Any], **kwargs: Any) -> dict[str, Any]:
    request = projection_request_from_package(source_package, **kwargs)
    return project(request, registry=builtin_projection_registry()).to_dict()


def enforce_unmapped_threshold(projected: dict[str, Any], threshold: float | None, *, scope: str = "canonical") -> None:
    if threshold is None:
        return
    if scope == "eligible":
        profile_scope = (projected.get("summary") or {}).get("profile_scope_coverage") or {}
        groups = [profile_scope.get("objects") or {}, profile_scope.get("relationships") or {}]
        total = sum(int(group.get("eligible_count") or 0) for group in groups)
        unmapped = sum(int(group.get("eligible_but_unmapped_count") or 0) for group in groups)
    else:
        coverage = (projected.get("audit") or {}).get("coverage") or {}
        total = int(coverage.get("source_object_count") or 0) + int(coverage.get("source_relationship_count") or 0)
        unmapped = int(coverage.get("unmapped_source_object_count") or 0) + int(coverage.get("unmapped_source_relationship_count") or 0)
    fraction = (unmapped / total) if total else 0.0
    if fraction > threshold:
        raise ValueError(f"{scope} unmapped source fraction exceeds threshold")
