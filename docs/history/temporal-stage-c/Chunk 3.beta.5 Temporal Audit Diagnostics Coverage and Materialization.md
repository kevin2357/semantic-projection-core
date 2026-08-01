# Chunk 3.beta.5 — Temporal Audit, Diagnostics, Coverage, and Materialization

## Status

Implemented in Semantic Projection Core 0.5.0.

## Scope

This pass promotes the Stage C4 temporal graph from an experimental full artifact into an operationally mature projection contract with:

- refined target-resolution classifications;
- component-level state-composition availability;
- audit reconciliation;
- structured diagnostic summaries;
- full, standard, summary, and forensic materializations;
- deterministic integrity hashes;
- temporal artifact profiling;
- richer completion logging;
- one-command QA.

## Coverage

Temporal targets are now distinguished as:

- mapped;
- excluded by profile scope;
- excluded by source-selection policy;
- eligible but unmapped;
- missing from the static source graph.

Missing optional sign/house data remains an availability fact rather than a projection failure.

## Materialization policy

`full` preserves all mapping executions and diagnostics.

`standard` preserves the projected graph and all defining temporal facts while compacting audit, diagnostics, and the embedded static target graph.

`summary` contains identity, period, counts, coverage, reconciliation, diagnostic summaries, hashes/refs, provenance, and limitations without graph rows.

`forensic` preserves the full graph and adds deterministic hashes for target graph, activators, activations, sequences, observation states, temporal facts, audit, diagnostics, and used terms.

## Non-goals

This pass does not add temporal interpretation, ranking, claim synthesis, report planning, or rendering.
