# Architecture

## System boundary

```text
canonical source graph + structural evidence + source registries
                              |
versioned profile + context + execution options
                              |
                              v
                 Semantic Projection Core
                              |
                              v
projected semantic graph + used-term registry + audit + diagnostics
```

SPC is a semantic compiler. The engine is domain-neutral; profiles own mappings and target vocabulary. Inputs and outputs are plain data, deterministic IDs are derived from semantic inputs, and source evidence is never mutated.

SPC currently supports three execution shapes:

1. Static projection, including natal and other chart-like canonical graphs supported by the selected profile.
2. Temporal projection from a Foundry temporal source bundle into a directional, arc-first projected temporal graph.
3. Synastry projection through a participant-preparation layer followed by the ordinary static compiler.

## Ownership boundaries

Astrology Graph Foundry (AGF) owns astrological calculation, canonical source graphs, structural evidence, source identity, canonical temporal activation graphs, observations, timing facts, and the adapter into SPC's temporal source bundle.

SPC owns projection requests, target-domain mappings, projected contracts, deterministic projection identity, audit and diagnostics, coverage classification, materialization, and temporal route receipts.

Consumers own application reasoning after projection: claims, recommendations, numeric game effects, report organization, final prose, UI, and publishing.

SPC does not import AGF calculation pipelines. AGF hands it saved plain-data artifacts.

## Static execution

The generic engine:

1. Validates the request and resolves the exact profile ID and version.
2. Validates the projection context through that profile.
3. Classifies source objects as eligible, excluded by policy, or unsupported.
4. Requests projected object drafts from the profile.
5. Assigns stable IDs, source references, mapping-rule references, provenance, and relevance components.
6. Merges equivalent target objects deterministically.
7. Projects eligible relationships after resolving their projected endpoints.
8. Attaches the used subset of the profile's projected term registry.
9. Reconciles coverage, audit records, diagnostics, indexes, and summary counts.
10. Validates the resulting `projected_semantic_graph.v1` artifact.

The engine contains no astrology or Woofmapping constants.

## Temporal execution

The supported production flow is:

```text
AGF temporal_projection_source_bundle.v1
    -> TemporalProjectionRequest
    -> static target projection
    -> persistent activator projection
    -> directional projected activation arcs and observation states
    -> materialization + deterministic route receipt
```

Temporal projection reuses the same profile object and relationship mappings as static projection. It adds a time-indexed activation envelope; it is not a second ontology engine.

Canonical timing facts remain nested under `temporal_facts`. Profile and context changes may alter projected operators, domains, relationships, relevance, and audience framing, but may not rewrite source activation identity, timestamps, phase observations, orb, motion, pass identity, or provenance.

The bare compatibility call `project_temporal()` without a request remains an intentional error. Use `project_foundry_temporal_bundle()`, `project_temporal(request, registry=...)`, or the supported temporal tools.

## Synastry execution

Synastry adds ownership rather than time. `prepare_synastry_source_graph()` annotates source objects and relationships with participant ownership, endpoint roles, relationship kind, and cross-participant status. The result then passes through the ordinary static engine.

Synastry does not imply temporal activation. Temporal synastry awaits an upstream canonical temporal-synastry source contract.

## Identity and immutability

Requests, projected packages, objects, relationships, mapping executions, temporal graphs, activators, sequences, activations, and states use deterministic, namespaced IDs. Input mappings are copied before preparation or execution. Audit hashes let consumers verify the source graph, context, and request used to create an artifact.

## Coverage

Coverage is profile-aware. Canonical rows may be mapped, deliberately excluded by source-selection policy, or outside a profile's declared scope. Eligible-scope coverage is therefore distinct from total canonical-source coverage. An unsupported source row is not silently relabeled as a failed mapping.
