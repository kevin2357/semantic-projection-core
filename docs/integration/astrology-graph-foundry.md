# Astrology Graph Foundry integration

Astrology Graph Foundry (AGF) is SPC's upstream source compiler. The repositories communicate through saved, versioned plain-data artifacts; SPC does not import AGF's ephemeris providers or calculation pipelines.

## Ownership

AGF owns:

- astronomical and astrological calculation;
- `canonical_astrology_graph` and `structural_evidence_graph`;
- chart, sensor, and source identity;
- canonical object and relationship topology;
- `canonical_temporal_activation_graph.v1`;
- activation arcs, observations, timing facts, and provenance;
- `temporal_projection_source_bundle.v1` adaptation.
- bounded-birth-time calculation, uncertainty evidence, capabilities, and the
  `bounded_canonical_astrology_graph.v1` invariant subgraph.

SPC owns:

- projection requests and projected output contracts;
- profiles, contexts, and projected vocabularies;
- mapping execution, projected IDs, audit, diagnostics, and coverage;
- static, temporal, and synastry projection behavior;
- materializations and temporal route receipts.

## Static handoff

A full AGF chart-like package supplies `canonical_astrology_graph`, optional `structural_evidence_graph`, source identity, and source registries. SPC's natal/static tool extracts those fields without recalculating the chart.

Synastry additionally requires participant declarations so SPC can preserve ownership and endpoint roles. Compact registry references must accompany the graph when their values are needed by a profile.

## Temporal handoff

The frozen supported boundary is:

```text
canonical_temporal_activation_graph.v1 1.0.0
    -> temporal_projection_source_bundle.v1 1.0.0
    -> temporal_projection_request.v1
    -> projected_temporal_activation_graph.v1
```

SPC validates arc-first authority, projection neutrality, reference integrity, counts, and supported versions. Contract changes should be versioned explicitly on both sides rather than inferred from filenames.

## Bounded natal handoff

SPC 0.11.0 accepts AGF's bounded natal package schema 1.0.0, canonical bounded
graph 1.7.0, uncertainty evidence contract 1.0.0, calculation profile 1.12.0,
and interval-proof profile 1.0.0. The dedicated bounded route rejects other
versions rather than passing them through the exact static engine.

AGF decides what is invariant, variable, unavailable, or inconclusive across
the birth-time interval. SPC may reinterpret only promoted invariant semantics.
It preserves evidence and limitations and never selects a midpoint,
representative chart, most-likely state, or default house.

## Development installation

From an AGF sibling checkout:

```powershell
python -m pip install -e ..\semantic-projection-core
python -m pip install -e ".[dev]"
```

AGF's own documentation remains authoritative for generating canonical packages and temporal bundles.

Editable sibling installation is development-only. Production AGF integration
must pin the published SPC wheel by exact SHA-256 and use the public artifact or
top-level runtime boundary. Imports from SPC profile mapping modules are not a
supported release interface. See the
[release consumer handoff](release-consumer-handoff.md).
