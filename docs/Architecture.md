# Architecture

```text
canonical source graph + structural evidence + profile + context
→ projected semantic graph + audit + diagnostics
```

The engine is generic. Domain semantics belong to versioned profiles. Projected term registries define profile vocabulary and composition guidance. Claims, narrative synthesis, and consumer publishing remain downstream.

Astrology Graph Foundry adapts saved astrology packages into `ProjectionRequest`; Semantic Projection Core never imports astrology calculation pipelines.


## Temporal source intake

Semantic Projection Core now accepts the frozen Foundry 0.4.2 temporal handoff through an adapter:

```text
temporal_projection_source_bundle.v1
        ↓ validation and referential integrity
temporal_projection_request.v1
```

This is an intake boundary only. The generic static engine remains unchanged, and temporal execution remains disabled until the Core-owned projected temporal contract and engine are completed.

## Projected temporal contract

Stage C2 defines `projected_temporal_activation_graph.v1` as an extension of the static architecture. The projected target graph remains an ordinary projected semantic graph. Temporal activators and activation arcs reference that graph while preserving Foundry-owned timing facts under explicit `temporal_facts` envelopes. Static and temporal IDs use separate namespaces.

## Stage C3 temporal reuse boundary

Temporal projection now reuses the ordinary static projection engine for the target graph and delegates persistent activator mapping to each profile's existing object mapper. The temporal layer orchestrates role and time; it does not duplicate object, sign, house, or projected-term vocabularies. Activation arcs remain a Stage C4 responsibility.

## Stage C4 temporal execution

Temporal execution reuses the ordinary static projection engine for the target
graph, existing object mappings for persistent activators, and existing
relationship mappings for activation contacts. Core adds a directional
activation envelope around those semantics while preserving Foundry timing
facts under `temporal_facts`.

This is an extension of the static pipeline, not a parallel temporal ontology
engine.

## Stage C5 temporal operational layer

Temporal projection now shares the static materialization policy and adds temporal coverage, reconciliation, diagnostic summaries, and deterministic section hashes. Foundry timing facts remain nested under `temporal_facts`; Core-owned semantic fields remain separate.
