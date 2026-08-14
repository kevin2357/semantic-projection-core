# Slice 7 — Deterministic, Negative, Scale, and Regression QA

## Outcome

The bounded route now has explicit QA for interval-shape diversity, rich source
evidence, fail-closed compatibility behavior, source-order independence, large
derived families, and all legacy SPC routes.

This slice treats AGF's interval facts at the correct boundary. Narrow,
whole-day, and maximum-duration inputs do not select different SPC algorithms.
Their invariant subgraphs are projected normally, while circular/disjoint
ranges, transitions, counterexamples, unavailable features, and inconclusive
features remain structured source proof or source dispositions. They are never
converted into representative positions, confidence, or claims.

## Positive matrix

| Case | Expected SPC behavior | Result |
| --- | --- | --- |
| 1-hour / 61 evaluations | project invariant subgraph; no representative values | passed |
| 24-hour / 1,441 evaluations | same semantic route | passed |
| 48-hour / 2,881 evaluations | same semantic route | passed |
| circular/disjoint prerequisite evidence | preserve exact structured record | passed |
| transition witnesses and counterexamples | preserve as evidence, not rows | passed |
| unavailable feature | preserve disposition; emit no unsupported row | passed |
| inconclusive feature | preserve disposition; emit no unsupported row | passed |
| reordered source rows and registry | semantically equivalent output | passed |
| identical repeated request | byte-equivalent contract value | passed |

## Negative matrix

The combined bounded suite rejects unsupported package, graph, evidence,
calculation-profile, proof-profile, bounded-profile, and context versions;
missing or conflicting evidence refs; duplicate source IDs; unknown endpoints;
forbidden exact/scored fields; capability disagreement; promoted non-invariant
evidence; invalid output correspondence; context-set drift; and missing
projected-term definitions.

Unknown object and relationship semantics remain explicitly outside declared
scope and appear in coverage diagnostics. Eligible rows that cannot map are
fatal rather than silent omissions.

## Defects found by qualification

### Registry completeness failed open for missing terms

The artifact-scoped registry builder validated the registry itself but only
attached refs for terms that happened to exist. A damaged policy resource could
therefore emit a bare semantic label without its definition. It now requires a
definition for every emitted primary semantic term and for every present
mode/domain term. Missing definitions stop projection.

### Per-member rounding could inflate large families

Equal allocation previously rounded each member independently. At 300 siblings,
a `0.98` family summed to `0.9801`. Allocation now uses deterministic integer
millionth units and apportions the remainder by sorted source relationship ID.
The 300-member total is exactly `0.98`; allocation shares total exactly `1.0`.
This preserves deterministic ordering and avoids quadratic family lookup.

## Scale evidence

The compact synthetic case deliberately exaggerates one derived evidence family:

- 8 source objects;
- 306 source relationships;
- 315 source evidence records;
- 6 projected objects;
- 305 projected relationships;
- 312 materialized evidence records;
- 21 artifact-scoped projected terms;
- 300 scored siblings in one family;
- conserved family relevance: `0.98`;
- conserved member allocation: `1.0`;
- observed single-projection time: 0.299 seconds.

The automated test uses a deliberately loose 10-second ceiling as a pathological
regression guard. The observed workstation time is evidence, not a released
latency guarantee.

## Verification

- focused Slice 7 QA: 12 passed;
- bounded suite: 69 passed;
- complete SPC suite: 226 passed in 69.49 seconds;
- Ruff: passed for changed implementation and tests;
- compact JSON evidence: [`bounded-qa-summary.json`](bounded-qa-summary.json);
- JSON and whitespace validation: passed.

Installed-wheel resource discovery and source-checkout isolation are intentionally
not claimed here. They remain the principal Slice 8 gate.

## Gate disposition

Slice 7 is ready for review. Slice 8 installed-runtime and cross-repository
acceptance has not begun.
