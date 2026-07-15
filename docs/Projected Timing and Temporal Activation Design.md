# Projected Timing and Temporal Activation Design

## Status

**Design status:** approved post-extraction priority  
**Implementation status:** Stage C1 implemented; projected temporal execution remains unimplemented  
**Current safety policy:** Foundry temporal source bundles can be validated and adapted into `temporal_projection_request.v1`, but temporal execution still fails explicitly until `projected_temporal_activation_graph.v1` is implemented.

This document records the intended design for timing-aware projection after the projection layer is extracted into its own repository.

---

## 1. Why static projection is insufficient

A saved Transit package may contain:

```text
top-level target/radix canonical graph
+ transiting object states
+ dated aspect snapshots
+ exact events
+ continuous activation arcs
+ applying/separating phases
+ repeated retrograde passes
+ period summaries and indexes
```

The current static projection operation consumes:

```text
canonical_astrology_graph
→ projected_semantic_graph.v1
```

When applied naively to a Transit package, it sees the top-level target chart and can produce a valid-looking static Natal projection while ignoring the nested timing structures that make the package a Transit package.

That behavior is dangerous because it looks successful.

Current policy therefore rejects:

```text
transit_dataset
transit_range_dataset
transit_period_dataset
```

with `TemporalProjectionNotImplementedError`.

Static chart-like packages such as Natal, Synastry, Composite, Davison, and return charts are not blanket-rejected merely because they are associated with a date. The guard is specifically for packages whose defining meaning is a nested temporal activation sequence.

---

## 2. What can be reused

Most target-domain semantic mappings already exist.

For example:

```text
transiting Mars
→ action_selection

target Venus
→ valuation_preference

square
→ interferes_and_forces_adaptation
```

Or in Woofmapped terms:

```text
transiting Mars
→ chase_play_defense_drive

target Venus
→ bonding_preference

square
→ drive_conflict_requires_outlet
```

The semantic question “what kind of operator and interaction is this?” is largely solved by the static profile.

The new work concerns temporal structure:

```text
when
for how long
in which direction
at what phase
with how many passes
represented at what granularity
```

---

## 3. Proposed architectural operation

The preferred architecture is:

```text
static projected target graph
+
canonical temporal activation graph
+
projection profile
+
projection context
→
projected_temporal_activation_graph.v1
```

It is explicitly not:

```text
full Transit package
→ pretend it is another static chart
```

The temporal graph should reference an existing target projected graph rather than duplicate its entire semantic model.

---

## 4. Primary temporal unit

The recommended primary unit is an **activation arc**:

```text
starts
→ applies
→ reaches exactness
→ separates
→ ends
```

Daily snapshots should be materializations of arcs, not the primary semantic identity.

Why:

- projecting every daily snapshot creates repetition;
- one underlying Transit can appear in many snapshots;
- exact-event rows and period summaries may represent the same process;
- arc identity supports deduplication and recurrence tracking;
- later daily or monthly “weather” views can be generated from the same arc.

A narrow first implementation could support snapshots, but the project should prefer a moderately richer arc-based implementation from the beginning.

---

## 5. Directionality

Static relationships can often be read as durable relationships between two subsystems.

Transit relationships are directional:

```text
temporary activator
→ enduring target subsystem
```

The contract must preserve distinct roles:

```text
activator_id
target_id
temporal_role = current_activation
```

A projected transit must not imply:

```text
action_selection and valuation_preference are permanently in friction
```

when the source means:

```text
current action pressure temporarily activates or stresses valuation/preference
```

Directionality is mandatory.

---

## 6. Transient object identity

The design should avoid creating a new projected object for the same transiting operator every day.

Preferred model:

```text
one transient projected operator identity
+ dated temporal-state records
+ one or more activation relationships
```

Example:

```json
{
  "transient_object": "projected:...:transiting_action_selection",
  "states": [
    {
      "observed_at": "2026-07-14T12:00:00-06:00",
      "longitude": 123.4,
      "retrograde": false
    }
  ]
}
```

This avoids object-count explosion and separates semantic identity from dated state.

---

## 7. Timing facts that remain projection-neutral

The projection layer should preserve, not reinterpret:

- timestamps;
- activation start/end;
- exact time;
- orb;
- applying/separating state;
- direct/retrograde state;
- station state where present;
- pass number;
- source Transit IDs;
- source target-chart identity;
- source sensor/provider identity.

Profiles may add target-domain concepts such as:

```text
temporary support
current pressure
recalibration window
activation emphasis
```

but must not rewrite the underlying timing facts.

---

## 8. Repeated passes

A retrograde sequence may contain:

```text
first direct pass
retrograde pass
final direct pass
```

The contract should preserve those as related passes within one broader activation sequence.

A safe first implementation should record:

```text
sequence_id
pass_index
motion_state
exact_at
```

It should not assume interpretive labels such as:

```text
introduction
review
closure
```

unless a specific projection profile explicitly declares and audits those mappings.

---

## 9. Proposed contracts

The repository now reserves:

```text
ProjectedTemporalState
ProjectedTemporalActivation
ProjectedTemporalActivationGraph
```

and schema:

```text
projected_temporal_activation_graph_v1.schema.json
```

The contract includes:

```text
target_graph_ref
transient_objects
temporal_states
activations
indexes
summary
audit
diagnostics
```

A temporal activation includes:

```text
activation_id
activation_type
activator_id
target_id
relationship_type
start_at
exact_at
end_at
phase
pass_index
applying
orb
attributes
source_refs
mapping_rule_refs
provenance
```

These contracts are reserved design scaffolding, not a claim that timing projection works today.

---

## 10. SDK adapter responsibilities

The Astrology Analysis SDK must construct a projection-neutral temporal source request from its Transit package.

The adapter should:

1. identify the target TransitableChart;
2. resolve transient object identities;
3. deduplicate snapshots and exact events into activation arcs;
4. retain source row lineage;
5. group repeated passes;
6. preserve provider/sensor identity;
7. expose timing facts without orthodox interpretive language;
8. pass the temporal source contract to the standalone projection engine.

The generic projection engine should not understand the SDK’s internal Transit package layout.

---

## 11. Profile responsibilities

A profile should reuse static object and aspect mappings where possible.

It should additionally define:

- temporary-activation vocabulary;
- directional relationship realization;
- context-sensitive temporal salience;
- whether and how phases change projected semantics;
- which temporal source families it supports.

The engine should remain ignorant of Mars, Venus, squares, or astrology-specific timing doctrine.

---

## 12. Relationship-entity targets

The same temporal contract should work for:

```text
individual Natal targets
Composite relationship entities
Davison relationship entities
other TransitableChart targets
```

The target projected graph carries entity type and identity. The temporal activation points into that graph.

This enables future comparison of:

```text
individual climate
Composite relationship climate
Davison relationship climate
```

without inventing separate timing engines.

---

## 13. Materializations

A mature temporal projection should support multiple views from the same arcs:

```text
full activation arcs
exact-event list
daily weather
monthly activation index
streaming timeline
compact game/interactive view
```

These are materializations, not independent semantic projections.

---

## 14. Explicit non-goals for the first implementation

The first timing-aware implementation should not attempt:

- prose forecasts;
- claim synthesis;
- multi-Transit pattern detection;
- contradiction resolution;
- eclipse/return/profection unification;
- calibrated forecast confidence;
- narrative lifecycle stages;
- automatic “most important Transit” selection;
- relationship-climate synthesis across several target charts.

Those belong after a correct temporal substrate exists.

---

## 15. Recommended first post-extraction development sequence

### Pass T1 — Canonical temporal source contract

- inspect Transit full/analysis/streaming structures;
- define arc identity and deduplication;
- preserve snapshot/exact-event lineage;
- implement SDK adapter fixtures.

### Pass T2 — Projected temporal activation engine

- reuse static target graph;
- map transient objects;
- map directional activation relationships;
- preserve phase, orb, and pass data;
- emit deterministic IDs and audit records.

### Pass T3 — Materializations and rich QA

- exact-event view;
- arc view;
- daily snapshot view;
- one-month and eighteen-month fixtures;
- Natal, Composite, and Davison targets;
- deterministic and size profiling.

Only after those passes should work begin on semantic pattern synthesis or report weather.

---

## 16. Acceptance criteria

Timing projection is ready when:

1. one underlying Transit arc is represented once;
2. daily and exact-event views derive from that arc;
3. activator and target roles remain directional;
4. static source and target semantics are reused rather than redefined;
5. all timing facts and source lineage are preserved;
6. repeated passes are grouped deterministically;
7. individual and relationship-entity targets use the same contract;
8. a Transit package can never silently degrade into a Natal-only projection;
9. standard/full/forensic materializations remain practical;
10. no final prose or hidden orthodox timing doctrine is required.

---

## 17. Current repository behavior

Until this design is implemented:

```python
project_dataset(transit_package)
```

raises:

```text
TemporalProjectionNotImplementedError
```

The error explains that the static `projected_semantic_graph.v1` contract cannot faithfully represent the package and references:

```text
projected_temporal_activation_graph.v1
```

This is an intentional correctness guard, not a temporary generic failure.


---

## Stage C1 implementation note

Chunk 3.beta.1 added:

- frozen Foundry schema compatibility snapshots;
- `TemporalProjectionRequest`;
- `TemporalProjectionOptions`;
- deterministic temporal request IDs;
- `FoundryTemporalSourceAdapterV1` behavior through `adapt_foundry_temporal_source_bundle`;
- cross-field and referential-integrity validation;
- a validation-only `semantic-temporal-intake` CLI;
- an explicit non-executable `project_temporal` boundary.

See `Chunk 3.beta.1 Temporal Intake and Adapter Contract.md`.

## Stage C2 contract freeze

Semantic Projection Core 0.3.0 defines the initial `projected_temporal_activation_graph.v1` contract. The contract separates Core-owned `projected_*` semantic fields from Foundry-owned `temporal_facts`, preserves arc-first nesting, requires activator-to-target directionality, and separates upstream source limitations from projected-artifact limitations.

## Stage C3 implementation note

The static target graph is now projected through the existing engine, and persistent transiting activators are projected through existing profile object mappings. This confirms the intended design rule: temporal projection is static projection plus a preserved activation envelope, not a parallel ontology engine.
