# Chunk 2 Cognitive Architecture Demo Profile

## Status and guardrails

Chunk 2.6 introduces:

```text
cognitive_architecture_demo.v0
```

This profile exists to prove that the generic projection engine can produce a genuinely different target ontology from the same canonical astrology source.

It is:

- experimental;
- an architectural demonstration;
- not clinical;
- not empirically validated;
- not a diagnostic instrument;
- intentionally incomplete.

These guardrails are encoded in the manifest, ontology, projected objects and relationships, and projection summary.

## Scope

Version `0.2.0` supports Natal source graphs containing:

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
- conjunction;
- opposition;
- square;
- trine;
- sextile.

Angles, houses, expanded objects, minor aspects, relationship charts, and timing-specific semantics remain unmapped diagnostics.

## Target primitives

The initial ontology includes:

```text
identity_organization
emotional_regulation
communication_processing
valuation_preference
action_selection
meaning_abstraction
constraint_management
change_adaptation
imagination_permeability
intensity_transformation
```

These are structured target-domain primitives, not psychological diagnoses.

## Projection-first relationship reasoning

The profile maps endpoints before reasoning about their relationship.

Example:

```text
canonical Mars
→ action_selection

canonical Venus
→ valuation_preference

canonical square
→ interferes_and_forces_adaptation
```

The projected relationship stores:

```json
{
  "source_process": "action_selection",
  "relationship_type": "interferes_and_forces_adaptation",
  "target_process": "valuation_preference",
  "interaction_mode": "frictional_coordination"
}
```

It does not translate finished orthodox romance prose into cognitive vocabulary.

## Cross-profile proof

The same canonical graph can now produce:

```text
orthodox_astrology.v1
→ action_assertion_drive
→ pressures_and_develops
→ value_attraction_harmony
```

and:

```text
cognitive_architecture_demo.v0
→ action_selection
→ interferes_and_forces_adaptation
→ valuation_preference
```

Both outputs share:

- source graph identity;
- canonical source references;
- mapping execution contracts;
- deterministic IDs;
- audit and diagnostic structure.

They differ in:

- target ontology;
- projected primitive names;
- relationship vocabulary;
- operators;
- semantic domains.

## Context

The reference context is:

```text
cognitive_architecture.general.v0
```

It is supplied in:

```text
examples/contexts/cognitive_architecture_general_context.json
```

## CLI

Project a saved Natal package:

```bat
python -m astro_analysis_sdk.cli project ^
  --source-dataset scripts\outputs\kevin_bre_test\kevin_natal_dataset.json ^
  --projection-profile cognitive_architecture_demo.v0 ^
  --projection-profile-version 0.2.0 ^
  --projection-context examples\contexts\cognitive_architecture_general_context.json ^
  --output-mode full ^
  --out scripts\outputs\kevin_bre_test\kevin_natal_cognitive_projection.json
```

## Example

Run:

```bat
python examples\projection_cross_profile_chunk26.py
```

The output contains orthodox and cognitive projections of the same small canonical source graph.

## Boundary result

Chunk 2.6 demonstrates that the engine is not merely an orthodox astrology refactor wearing a cognitive-neuroscience novelty tie. The engine remains unchanged; the profile supplies a different ontology and mapping policy.

## Chunk 2.6.woof expansion to v0.2

The cognitive demo now maps:

- additional orientation/interface objects;
- all twelve signs into operating modes;
- all twelve houses into cognitive domains;
- all four angles into explicit interfaces;
- all seven aspect types implemented by the SDK.

Projected operator objects retain a `projection_composition` containing operator, mode, and domain. Relationships preserve endpoint modes and domains so later reasoning can occur inside the projected architecture.

This remains an experimental architecture proof rather than a validated psychological model.
