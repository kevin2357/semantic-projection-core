# Chunk 2.7 Timing Guard Completion

Rich-fixture QA identified that the static projection adapter could accept a Transit package, project only its top-level target chart, and emit a plausible result indistinguishable from Natal projection.

This pass closes that correctness hole.

## Implemented

- explicit rejection of `transit_dataset`, `transit_range_dataset`, and `transit_period_dataset`;
- `TemporalProjectionNotImplementedError` with a targeted explanation;
- reserved temporal contracts:
  - `ProjectedTemporalState`;
  - `ProjectedTemporalActivation`;
  - `ProjectedTemporalActivationGraph`;
- JSON Schema:
  - `projected_temporal_activation_graph_v1.schema.json`;
- detailed post-extraction design document;
- orthodox manifest no longer claims executable Transit support;
- Chunk 2.7 QA generator records the expected rejection rather than producing misleading Transit artifacts.

## Deliberate boundary

Return charts are not blanket-rejected. A dated static return chart can still be represented as a static projected graph. The guard targets packages whose defining content is nested temporal activation.

## Validation

- 119 tests passed;
- projection dependency inspection remains clean;
- extraction-readiness inspection remains clean;
- schema inventory now includes the reserved temporal contract.

## Next project priority

After repository extraction, implement the arc-based timing design in `Projected Timing and Temporal Activation Design.md`.
