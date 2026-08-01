# Chunk 3.beta.6 — Cross-Profile Temporal Projection and Context Behavior

## Status

Implemented in Semantic Projection Core 0.6.0.

## Purpose

Stage C6 proves that one Foundry-owned temporal fact layer can be projected through multiple target ontologies and contexts without changing the underlying timing facts.

The same `temporal_projection_source_bundle.v1` is projected through:

- `orthodox_astrology.v1`;
- `cognitive_architecture_demo.v0`;
- `woofmapped_astrology.v0`;
- orthodox general and professional contexts.

## Architectural invariant

```text
same canonical temporal activation
        ↓
same preserved temporal facts
        +
profile/context-specific projected semantics
```

Profiles may change:

- projected activator vocabulary;
- projected target vocabulary;
- projected relationship type;
- projected mode/domain terms;
- used projected-term registry.

Profiles and contexts must not change:

- source activation identity;
- timing envelope;
- pass identity;
- observation states;
- orb, phase, exactness, or motion;
- Foundry provenance.

## C6 refinements

### Cognitive Spirit scope

`Spirit` is now explicitly classified as outside the current Cognitive temporal target scope. Temporal arcs to Spirit are profile-scope exclusions rather than eligible-but-unmapped failures. This records the current profile boundary without inventing a Cognitive mapping.

### Summary semantic hashes

Summary materializations now retain hashes for:

- projected activators;
- projected activations;
- projected sequences;
- projected states;
- temporal facts.

This allows catalogs and profilers to reconcile summary artifacts with graph-bearing materializations without hashing intentionally absent arrays.

### Upstream limitation annotations

Foundry limitation text remains unchanged, but Core annotates each limitation with:

- source contract;
- active or superseded status;
- the Core contract that supersedes an obsolete handoff limitation.

This preserves provenance without presenting “Core does not yet execute this bundle” as an active limitation of an executed temporal graph.

### Completion logging

Temporal completion logs now include `target_eligible_but_unmapped` for complete coverage visibility.

## QA

Run:

```bat
scripts\run_chunk3_beta_6_qa.bat
```

Inputs:

```text
outputs/fixture_test_files/
```

All logs and artifacts:

```text
outputs/fixture_outputs/
```

The runner performs:

- pytest;
- four profile/context projections;
- standard and summary materialization;
- deterministic Cognitive repeat;
- temporal-fact invariance comparison;
- projected-semantic divergence comparison;
- orthodox general/professional context comparison;
- limitation and summary-hash checks.

## Non-goals

C6 does not add:

- consumer-facing transit interpretation;
- cross-activation claim synthesis;
- temporal narrative rendering;
- monthly weather summaries;
- interpretive retrograde/pass labels.
