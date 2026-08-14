# Contracts

SPC's public contracts are Python dataclasses that serialize to plain dictionaries and are backed by packaged JSON Schemas under `src/semantic_projection/schemas`.

## Static request

`ProjectionRequest` contains:

- deterministic `request_id`;
- exact `profile_id` and `profile_version`;
- complete canonical `source_graph`;
- optional `structural_evidence`;
- `source_identity`;
- versioned `context`;
- optional `source_registries`;
- execution `options`.

`ProjectionOptions` controls audit and diagnostic inclusion, unmapped-source behavior, and optional coverage thresholds. Context describes what the projection is for; options describe how execution behaves.

## Static result

`projected_semantic_graph.v1` contains metadata, source identity and graph reference, target ontology, projected objects and relationships, indexes, summary, a used-term registry, audit, diagnostics, and provenance.

Generated metadata includes `semantic_projection.runtime_identity.v1`, which
binds the artifact to installed code, declarative semantic resources, schemas,
profile policy, context content, route, and output contract. See
[Runtime and release identity](runtime-and-release-identity.md).

Projected rows retain `source_refs`, `mapping_rule_refs`, context references, and deterministic identity. They are target-domain semantic units, not final claims or prose.

## Bounded natal request and result

`bounded_natal_projection_request.v1` accepts the exact supported AGF bounded
natal package boundary and retains the complete source artifact, immutable
source hash, upstream contract identities, context, options, and limitations.
It is a sibling route, not a relaxed static request.

`projected_bounded_semantic_graph.v1` contains only source-supported invariant
objects and relationships selected by the bounded profile. It preserves source
capabilities and feature dispositions, direct evidence plus prerequisite
closure, evidence-family identity, proof scope, correspondence IDs, an
artifact-scoped term registry, and installed runtime provenance. It cannot
represent an exact longitude, orb, structural strength, confidence, or
representative state as a bounded projected fact.

The four Woofmapping outputs have context-specific materialized IDs and stable
`correspondence_id` values. `validate_parallel_bounded_contexts()` verifies
their structural correspondence and certainty invariance. No context has
canonical epistemic priority.

## Temporal source and request

SPC accepts AGF's frozen `temporal_projection_source_bundle.v1` version 1.0.0. The adapter validates supported contract versions, arc-first authority, projection neutrality, cross-field counts, and referential integrity before producing `temporal_projection_request.v1`.

The request combines:

- a static target source graph;
- a canonical temporal source graph;
- source and target identity;
- upstream contract metadata;
- a profile, context, and temporal options.

## Temporal result

`projected_temporal_activation_graph.v1` contains:

- an ordinary projected static target graph;
- persistent projected activators;
- directional projected activation arcs;
- projected sequence summaries;
- observation states nested in preserved `temporal_facts`;
- indexes and summary;
- audit, diagnostics, limitations, and provenance;
- the used projected-term registry.

Source and projected limitations are separate fields. Upstream omissions are annotated, never repaired by inventing facts.

The production route also emits `temporal_projection_route_receipt.v1`, which records the source bundle, request, projected graph, profile, context, target family, output mode, semantic hashes, coverage, and deterministic route hash.

Temporal artifacts and route receipts carry the same runtime identity; temporal
foundations carry a foundations-specific receipt. The foundations contract is
currently 0.1.0, while the projected temporal graph and route receipt are 1.0.0.

## Synastry preparation

`project_synastry()` accepts a canonical relationship graph, structural evidence, source identity, at least two participant records, relationship kind, profile, context, options, registry, and optional source registries. It returns the prepared `ProjectionRequest`, projected artifact, and participant index.

Participant records require `participant_id`; role, species, and label are optional. Owners discovered on source objects are retained in the participant index with an `unspecified` role when they were not supplied explicitly.

## Validation

`validate_contract()` performs full Draft 2020-12 JSON Schema validation.
`jsonschema` is a required runtime dependency so validation depth cannot vary
with the ambient environment. Specialized validators additionally enforce
deterministic and reference-integrity rules that JSON Schema alone cannot
express. The rationale is preserved in
[ADR-0002](../decisions/ADR-0002%20-%20Require%20Invariant%20Full%20Schema%20Validation%20at%20Runtime.md).

The schemas are the field-level authority. This page describes their role and composition rather than duplicating every property.
