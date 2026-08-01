# Chunk 2 Orthodox Astrology Profile

## Status

Chunk 2.3 introduces the first real semantic projection profile:

```text
orthodox_astrology.v1
```

This profile is implemented through the generic Chunk 2.2 engine. The engine contains no astrology-specific mapping constants.

## Current scope

The initial profile supports:

- Sun;
- Moon;
- Mercury;
- Venus;
- Mars;
- Jupiter;
- Saturn;
- Uranus;
- Neptune;
- Pluto;
- Ascendant;
- Descendant;
- Midheaven;
- Imum Coeli;
- conjunction;
- opposition;
- square;
- trine;
- sextile.

Expanded points, minor aspects, timing-specific rules, Synastry registries, house overlays, and professional relationship contexts remain intentionally deferred.

## Projection model

A canonical source object becomes an orthodox semantic primitive.

Example:

```text
canonical Venus
→ value_attraction_harmony
```

The projected object retains:

- canonical source reference;
- mapping-rule reference;
- source operators;
- orthodox operators;
- semantic domains;
- orthodox theme tags;
- structural strength;
- projection relevance components;
- context reference.

A canonical source relationship is reasoned between projected endpoints.

Example:

```text
canonical Mars square Venus
        ↓ object projection
action_assertion_drive
square
value_attraction_harmony
        ↓ relationship projection
pressures_and_develops
```

The projected relationship contains structured operators and themes, not report prose.

## Projection relevance

Chunk 2.3 uses an initial transparent heuristic:

```text
structural strength
× profile salience
× context salience
```

The result is called `projection_relevance_score`, not confidence.

Every component is retained under:

```text
attributes.projection_relevance_components
```

This formula is a reference implementation to make profile-specific salience explicit and auditable. It is expected to evolve through real fixture analysis.

## Projection options versus context

Chunk 2.3 adds an explicit `ProjectionOptions` contract.

Context describes semantic interpretation conditions:

```text
natal interpretation
professional relationship
age/life-stage context
target domain
```

Options describe engine execution and materialization:

```text
include audit
include diagnostics
unmapped policy
compact audit
```

The two are intentionally separate.

## Merge behavior

The demonstration profile now uses:

```json
"source_names": ["Input A", "Input B"]
```

when multiple sources merge into one projected primitive.

Generic attribute merging preserves list-valued attributes and exposes conflicting scalar values under:

```text
merged_attribute_values
```

instead of silently retaining the last processed value.

## Example

Run:

```bat
python examples\projection_orthodox_chunk23.py
```

The output includes:

- projected Mars and Venus objects;
- a projected Mars-square-Venus relationship;
- an intentionally unmapped calculated point;
- complete mapping executions;
- coverage and diagnostics;
- deterministic projected IDs.

## Boundary rule

The orthodox profile never writes themes back into:

```text
canonical_astrology_graph
```

Orthodox semantics exist only in the projected graph.

## Next step

Chunk 2.4 will make the profile registry-aware for Synastry and add controlled relationship contexts, including general and professional interpretations.

## Chunk 2.4 relationship extension

The profile now resolves Synastry registries, maps house overlays, and supports general versus professional relationship contexts.

Registry themes, object themes, aspect themes, and context transformations remain separately traceable under `attributes.theme_evidence`.
