# Chunk 3.beta.7 — Production Temporal Routing and Integration Closure

## Status

Implemented in Semantic Projection Core 0.7.0.

## Purpose

C7 closes Stage C by turning the previously separate intake and projection commands into one supported production route:

```text
Foundry temporal_projection_source_bundle.v1
        ↓ validate and adapt
Core temporal_projection_request.v1
        ↓ deterministic projection
projected_temporal_activation_graph.v1
        ↓ materialize
full | standard | summary | forensic
        ↓
temporal_projection_route_receipt.v1
```

The route is composition, not a new engine. It delegates to the already-tested C1–C6 contracts and therefore preserves the same validation, IDs, audit, diagnostics, coverage, temporal-fact invariants, and materialization semantics.

## Public API

```python
from semantic_projection import project_foundry_temporal_bundle

result = project_foundry_temporal_bundle(
    bundle,
    profile_id="cognitive_architecture_demo.v0",
    profile_version="0.2.0",
    context=context,
    output_mode="standard",
)
```

The result contains:

- the normalized temporal request;
- the selected projected artifact;
- a deterministic routing receipt.

## Production CLI

```bat
semantic-temporal-run ^
  --bundle temporal_projection_source.json ^
  --projection-profile cognitive_architecture_demo.v0 ^
  --projection-profile-version 0.2.0 ^
  --projection-context examples\contexts\cognitive_architecture_general_context.json ^
  --output-mode standard ^
  --out projected_temporal.standard.json ^
  --request-out temporal_request.json ^
  --receipt-out temporal_route_receipt.json
```

`--request-out` and `--receipt-out` are optional. The projected artifact is required.

## Routing receipt

`temporal_projection_route_receipt.v1` records the complete identity chain without duplicating graph payloads:

- Foundry source bundle ID;
- canonical temporal graph ID;
- Core request ID;
- projected temporal graph ID;
- profile and context identity;
- target family;
- materialization mode;
- summary semantic hashes;
- compact coverage;
- deterministic route hash.

This receipt is suitable for integration logs, catalogs, batch manifests, and cross-repository QA.

## Target-family classification

C7 adds a conservative target classifier for QA and routing metadata:

- natal;
- composite;
- Davison;
- explicit upstream target types;
- natal-or-unspecified fallback.

Classification does not alter projection behavior. Composite and Davison bundles use the same generic route and are tested whenever such fixtures are placed in `outputs/fixture_test_files`.

## Architectural conclusion preserved from C6

> **Temporal projection is not a second semantic compiler. It is the same semantic compiler operating over a time-indexed canonical graph while preserving an invariant temporal fact layer. Cross-profile and cross-context comparisons demonstrate that semantic variability is orthogonal to canonical temporal structure.**

C7 turns that conclusion into the production integration boundary.

## QA

Run one command:

```bat
scripts\run_chunk3_beta_7_qa.bat
```

The runner:

- executes pytest;
- inventories every fixture semantically;
- processes every Foundry temporal bundle found in `outputs/fixture_test_files`;
- supports natal, Composite, and Davison fixtures without filename assumptions;
- runs the complete production route twice per fixture;
- verifies byte and SHA-256 determinism;
- writes request, standard artifact, routing receipt, production route manifest, and QA summary under `outputs/fixture_outputs`.

## Stage C closure

C1–C7 now provide:

1. frozen Foundry intake validation;
2. Core temporal request contract;
3. static-target and activator reuse;
4. directional projected activation arcs;
5. audit, diagnostics, coverage, and materializations;
6. cross-profile and cross-context invariance proof;
7. supported end-to-end production routing and cross-repository QA.

Temporal claim synthesis, narrative interpretation, report rendering, and lifecycle labels remain downstream.
