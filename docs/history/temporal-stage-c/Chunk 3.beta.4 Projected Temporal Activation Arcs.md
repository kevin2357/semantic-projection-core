# Chunk 3.beta.4 — Projected Temporal Activation Arcs

## Status

Stage C4 is implemented experimentally.

Semantic Projection Core now converts a validated `temporal_projection_request.v1`
into a schema-valid `projected_temporal_activation_graph.v1`.

## Pipeline

```text
Foundry temporal source bundle
→ Core temporal request
→ existing static target projection
→ persistent activator projection through existing object mappings
→ one canonical activation arc
→ at most one directional projected activation arc
```

No daily observation is promoted into an independent projected relationship.
Observation rows remain nested states of their owning activation arc.

## Mapping reuse

C4 deliberately introduces no second object or aspect ontology.

- activators delegate to `profile.project_object`;
- static targets come from the ordinary static projection engine;
- activation contacts delegate to `profile.project_relationship`;
- state sign and house composition delegates to `profile.project_object`.

The temporal layer adds directionality, persistence rules, timing envelopes,
source identities, and temporal provenance around those existing mappings.

## Directionality and ownership

Every projected activation is:

```text
projected activator
→ projected static target
```

with:

```text
temporal_role: current_activation
directionality: activator_to_target
```

Foundry-owned timing facts remain under `temporal_facts`. Core does not reinterpret:

- start, closest, exact, or end timestamps;
- exactness status;
- motion;
- observation phase;
- orb, distance, or source strength labels;
- sequence or pass identity.

## Source-selection policy

Temporal activators now mirror static source-selection policy.

For the reference Cognitive and Woofmapped profiles:

```text
Mean Node
→ excluded_by_source_selection_policy
```

when True Node is the preferred source variant.

This is not counted as an eligible-but-unmapped activator or a mapping failure.
Activation arcs using a policy-excluded activator are classified separately.

Targets excluded or not selected by static projection are likewise classified
separately from unsupported aspect mappings.

## Contract output

The C4 full graph contains:

- the ordinary projected static target graph;
- persistent projected temporal activators;
- directional projected activation arcs;
- projected sequence summaries;
- nested projected observation states;
- indexes by activator, target, sequence, and source aspect;
- initial coverage, audit, diagnostics, and provenance;
- upstream and projected-artifact limitations.

Final materialization and audit policies remain Stage C5 work.

## State composition

When source position information exists, Core may project:

- transiting sign into a target-domain mode;
- transit house in the target chart into a target-domain activation arena.

When optional position information is absent, the state records:

```text
availability: source_position_not_supplied
```

rather than guessing.

## Explicit non-goals

C4 does not perform:

- transit interpretation;
- temporal claim synthesis;
- event ranking;
- report planning;
- retrograde-pass interpretation;
- monthly weather summaries;
- deterministic temporal prose;
- exact-event solving.

## QA

Run:

```bat
scripts\run_chunk3_beta_4_qa.bat
```

Inputs:

```text
outputs/fixture_test_files
```

Outputs:

```text
outputs/fixture_outputs
```

The runner performs tests, bundle intake, two full C4 projections, byte/hash
determinism comparison, wrong-artifact rejection, and a structured QA summary.

## Next pass

Stage C5 should stabilize:

- complete temporal audit and diagnostics contracts;
- full, standard, summary, and forensic materializations;
- used-registry subset policy;
- artifact profiling;
- friendly expected-error behavior;
- authoritative QA profiling.
