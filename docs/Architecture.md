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
