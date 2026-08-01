# Chunk 3.beta.1 — Stage C1 Temporal Intake and Adapter Contract

## Status

Implemented.

This pass establishes the Semantic Projection Core side of the frozen Astrology Graph Foundry 0.4.2 temporal handoff. It validates and adapts Foundry temporal source bundles but intentionally does not emit projected temporal graphs.

## Supported upstream contracts

Core currently accepts:

```text
temporal_projection_source_bundle.v1
canonical_temporal_activation_graph.v1
```

Concrete frozen versions:

```text
bundle contract_version:         1.0.0
temporal graph contract_version: 1.0.0
```

The upstream schemas are packaged with Core as compatibility snapshots for boundary validation. Material changes require explicit version support rather than silent reinterpretation.

## New generic Core contract

```text
temporal_projection_request.v1
```

The request contains:

- source and target identity;
- static canonical source graph;
- structural evidence;
- canonical temporal source graph;
- source registries;
- existing `ProjectionContext`;
- temporal execution options;
- explicit upstream contract identity;
- propagated source limitations.

The request is generic Core input. The Foundry bundle is consumed through an adapter and does not become the internal temporal engine contract.

## Public API

```python
from semantic_projection import (
    ProjectionContext,
    adapt_foundry_temporal_source_bundle,
)

request = adapt_foundry_temporal_source_bundle(
    bundle,
    profile_id="cognitive_architecture_demo.v0",
    profile_version="0.2.0",
    context=context,
)
```

Validation-only CLI:

```bat
semantic-temporal-intake ^
  --bundle temporal_projection_source.json ^
  --projection-profile cognitive_architecture_demo.v0 ^
  --projection-profile-version 0.2.0 ^
  --projection-context cognitive_architecture_general_context.json ^
  --out temporal_projection_request.json
```

This command does not project timing semantics.

## Validation performed

The adapter validates:

- bundle package type, version, projection-neutral flag, and consumer status;
- temporal graph package type, version, projection-neutral flag, and arc-first authoritative unit;
- JSON Schema validity;
- target identity agreement across bundle, temporal graph, and static graph;
- activator reference resolution;
- activation-target resolution against static source objects;
- target-chart agreement;
- observation-count reconciliation;
- unique activation and state IDs;
- summary count reconciliation;
- index reference integrity;
- supported static canonical graph version;
- deterministic temporal request identity;
- input immutability.

## Safety boundary

Temporal execution remains disabled:

```python
project_temporal(...)
```

raises:

```text
TemporalProjectionNotImplementedError
```

The old safety principle remains active: Core must not emit a plausible static result for temporal input, and it must not claim `projected_temporal_activation_graph.v1` exists until Stages C2–C7 are complete.

## Real-corpus smoke result

The January 2026 Kevin Foundry bundle adapted successfully with:

```text
189 static source objects
4,239 static source relationships
12 temporal activators
88 activation arcs
640 observation states
```

No source object was mutated.
