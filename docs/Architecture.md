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
