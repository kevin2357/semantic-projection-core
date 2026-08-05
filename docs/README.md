# Semantic Projection Core documentation

These pages describe the current `semantic-projection-core` 0.10.x codebase. Documents under [`history/`](history/README.md) are implementation records and are not normative.

Semantic Projection Core (SPC) deterministically compiles canonical source graphs into versioned target-domain semantic graphs. It preserves source identity, provenance, and structural relationships while profiles supply the target vocabulary and mapping behavior. Claims, recommendations, application rules, report planning, and publication remain downstream.

## Start here

- [Getting started](guides/getting-started.md) — install SPC and run a static projection.
- [Architecture](reference/architecture.md) — understand the compiler, ownership boundaries, and supported projection shapes.
- [Profiles and contexts](reference/profiles-and-contexts.md) — compare the bundled profiles and their current scope.
- [Temporal projection](guides/temporal-projection.md) — project an Astrology Graph Foundry temporal bundle.
- [Synastry projection](guides/synastry-projection.md) — prepare participant-aware relationship graphs.
- [Woofmapping](guides/woofmapping.md) — use the natal, transit, and synastry convenience tools.

## Concepts

- [Semantic projection](concepts/semantic-projection.md)
- [Projection, reasoning, and publication layers](concepts/semantic-and-publication-layers.md)

## Reference

- [Architecture](reference/architecture.md)
- [Contracts](reference/contracts.md)
- [Profiles and contexts](reference/profiles-and-contexts.md)
- [Projected term registries](reference/projected-term-registries.md)
- [Materialization and artifact identity](reference/materialization-and-artifacts.md)

## Integration and extension

- [Astrology Graph Foundry integration](integration/astrology-graph-foundry.md)
- [Downstream consumer contract](integration/downstream-consumers.md)
- [AstroWoof project integration](https://github.com/kevin2357/astrowoof-project/blob/main/docs/architecture/Semantic%20Projection%20Integration.md) — downstream architecture and consumer policy, not SPC implementation authority.
- [Profile authoring](guides/profile-authoring.md)
- [Roadmap](roadmap.md)

## Documentation authority

Current code and JSON Schemas are the executable contract. The reference pages explain that contract; guides show supported workflows. Historical documents retain design rationale and implementation chronology but may describe behavior that was incomplete at the time.
