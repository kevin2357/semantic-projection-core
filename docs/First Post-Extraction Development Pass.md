# First Post-Extraction Development Pass

## Primary feature

Implement the arc-oriented `projected_temporal_activation_graph.v1` design described in `Projected Timing and Temporal Activation Design.md`. Reuse profile object/aspect mappings while representing directionality, activation arcs, dated states, applying/exact/separating phases, repeated passes, and projection-neutral timing facts.

## Ergonomic corrections carried from Chunk 2.7

### Friendly expected-error CLI handling

Catch known user-facing exceptions such as temporal projection rejection at CLI boundaries. Print a concise structured error containing source type, reason, remediation, and future contract. Return a nonzero exit code without a traceback unless debug/verbose mode is enabled. Log the intentional rejection with source path/type, profile, context, and future contract.

### Artifact-profiler classification

Detect true projection artifacts by package type. Skip administrative QA JSON by default or classify rejection/admin artifacts explicitly rather than treating them as legacy/full projected graphs. Preserve an opt-in include-all mode.

### Single authoritative QA profiling run

Remove duplicate profiling invocation from bundled QA. Produce one authoritative profile artifact and one write log entry, while keeping the standalone manual profiler command available and idempotent.
