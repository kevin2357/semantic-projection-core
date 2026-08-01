# Chunk 3.beta.2 — Projected Temporal Contract and Operational Foundations

## Status

Implemented as Semantic Projection Core 0.3.0.

This pass completes Stage C2 of the cross-repository temporal projection plan. It defines and validates the Core-owned projected temporal output contract before activation mappings are executed.

## Boundary

Foundry continues to own:

- activation arcs and pass segmentation;
- activator/target directionality;
- dates, orb, distance, motion, and sampled phase;
- exactness status and limitations;
- source provenance.

Core now defines where projected semantic meaning will live:

- projected activator identity;
- projected target identity;
- projected relationship vocabulary;
- projected mode/domain composition;
- projected audit, diagnostics, coverage, and materialization.

No transit interpretation, claim synthesis, reporting, or temporal prose is implemented.

## Contract

The authoritative output contract is:

```text
projected_temporal_activation_graph.v1
```

Its top level contains:

```text
metadata
source_identity
target_identity
period
projected_target_graph
projected_activators
projected_activations
projected_sequences
indexes
summary
projected_term_registry
audit
diagnostics
provenance
upstream_source_limitations
projected_artifact_limitations
```

### Projected semantics versus source facts

Every activation separates:

```text
projected_* fields
```

from:

```text
temporal_facts
```

`temporal_facts` preserves the Foundry-owned envelope:

- start, closest-observed, exact, and end times;
- exactness;
- motion;
- observation count;
- nested observation states.

Core-owned projected fields describe:

- projected activator;
- projected target;
- projected relationship type;
- temporal role;
- directionality;
- optional projected activation domain;
- optional activator-state mode composition.

### Directionality

The initial contract requires:

```text
temporal_role = current_activation
directionality = activator_to_target
```

A temporary activation may not silently become a permanent symmetric relationship.

### Observation states

Observation states remain nested under their owning arc. They preserve:

- source state ID;
- timestamp;
- phase;
- orb and distance;
- categorical `strength_label`;
- activator position/motion state;
- optional projected state composition.

They are not emitted as independent semantic relationships.

### Limitations

The contract distinguishes:

```text
upstream_source_limitations
projected_artifact_limitations
```

This prevents a Foundry source limitation from being confused with a limitation of the eventual projected artifact.

## Deterministic IDs

Added namespaces:

```text
temporal_projection:
projected_temporal_activator:
projected_temporal_sequence:
projected_temporal_activation:
projected_temporal_state:
```

Static and temporal identities cannot collide.

## Validation

`validate_projected_temporal_activation_graph()` enforces:

- JSON Schema validity;
- unique activator, activation, sequence, and state IDs;
- target and activator referential integrity;
- sequence membership;
- state ownership;
- observation-count reconciliation;
- pass-count reconciliation.

C2 includes a schema-valid contract skeleton helper:

```python
projected_temporal_contract_skeleton(...)
```

It deliberately emits no projected activations and states that mapping execution is not yet implemented.

## Logging

Core now includes first-class UTF-8 operational logging:

```python
configure_logging(...)
log_event(...)
```

The temporal intake CLI records:

- intake start;
- input/profile/context/output identity;
- successful request identity and row counts;
- intentional contract rejection.

Expected validation failures remain concise on the console. Tracebacks remain opt-in through `--debug`.

Default log:

```text
semantic_projection.log
```

A custom path may be supplied through:

```text
--log-file
```

## QA convention

All future development-pass QA should assume:

```text
outputs/fixture_test_files
outputs/fixture_outputs
```

C2 adds:

```text
scripts/run_chunk3_beta_2_qa.py
scripts/run_chunk3_beta_2_qa.bat
```

One command runs:

- pytest;
- real positive temporal intake twice;
- byte-identicality and SHA-256 checks;
- automatic bad-version fixture creation;
- negative rejection test;
- contract-skeleton generation;
- Core log capture;
- structured QA summary.

The user should not need to reconstruct multiline commands or manually redirect output.

## Acceptance result

Local validation against the real Kevin January 2026 Foundry bundle produced:

```text
54 tests passed
request determinism: byte-identical
negative version: rejected with exit code 2
bad output: absent
Core log: present
contract skeleton: schema-valid
```

## Next pass

Stage C3 should reuse the static projection engine to produce:

- the projected target graph;
- source-object to projected-object resolution;
- persistent projected activators;
- sign/mode and house/domain state composition;
- activator and target coverage diagnostics.

It should not yet map full activation arcs unless the C3 contract reuse work proves clean.
