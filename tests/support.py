from __future__ import annotations
from copy import deepcopy
from semantic_projection import ProjectionOptions, ProjectionRequest, projection_request_id, project
from semantic_projection.profiles import builtin_projection_registry


def project_dataset(source_package, *, profile_id="orthodox_astrology.v1", profile_version="1.0.0", context=None, options=None):
    graph=deepcopy(source_package.get("canonical_astrology_graph") or {})
    identity={
        "source_chart_id": (source_package.get("metadata") or {}).get("source_chart_id"),
        "source_chart_ids": (source_package.get("metadata") or {}).get("source_chart_ids") or [],
        "sensor_instance_id": (source_package.get("metadata") or {}).get("sensor_instance_id"),
    }
    
    if context is None:
        target_domain = {
            "orthodox_astrology.v1": "orthodox_astrology.v1",
            "cognitive_architecture_demo.v0": "cognitive_architecture_demo.v0",
            "woofmapped_astrology.v0": "woofmapped_astrology.v0",
        }[profile_id]
        context_dict={
            "context_id": "tests.default",
            "context_version": "1.0.0",
            "subject_scope": "dog" if profile_id == "woofmapped_astrology.v0" else "individual",
            "target_domain": target_domain,
            "application_context": "test",
            "constraints": {"house_mapping_policy":"doghouse"} if profile_id == "woofmapped_astrology.v0" else {},
            "parameters": {},
            "extensions": {},
        }
    else:
        context_dict=context.to_dict() if hasattr(context,"to_dict") else deepcopy(context)
    options_dict=options.to_dict() if hasattr(options,"to_dict") else deepcopy(options or ProjectionOptions().to_dict())
    request=ProjectionRequest(
        request_id=projection_request_id(profile_id=profile_id, profile_version=profile_version, source_identity=identity, context=context_dict, options=options_dict),
        profile_id=profile_id, profile_version=profile_version, source_graph=graph,
        structural_evidence=deepcopy(source_package.get("structural_evidence_graph") or {}),
        source_identity=identity, context=context_dict, source_registries={}, options=options_dict,
    )
    return project(request, registry=builtin_projection_registry()).to_dict()


def enforce_unmapped_threshold(projected, threshold, *, scope="canonical"):
    if threshold is None: return
    if scope == "eligible":
        ps=(projected.get("summary") or {}).get("profile_scope_coverage") or {}
        groups=[ps.get("objects") or {}, ps.get("relationships") or {}]
        total=sum(int(g.get("eligible_count") or 0) for g in groups)
        unmapped=sum(int(g.get("eligible_but_unmapped_count") or 0) for g in groups)
    else:
        cov=(projected.get("audit") or {}).get("coverage") or {}
        total=int(cov.get("source_object_count") or 0)+int(cov.get("source_relationship_count") or 0)
        unmapped=int(cov.get("unmapped_source_object_count") or 0)+int(cov.get("unmapped_source_relationship_count") or 0)
    fraction=(unmapped/total) if total else 0.0
    if fraction > threshold: raise ValueError(f"{scope} unmapped source fraction exceeds threshold")
