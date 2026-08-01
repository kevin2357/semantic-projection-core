# Profiles and contexts

## Bundled profiles

| Alias | Profile | Version | Status | Declared static source types |
|---|---|---:|---|---|
| `orthodox` | `orthodox_astrology.v1` | 1.0.0 | Expanded reference profile | Natal, synastry, composite, Davison, solar return, lunar return |
| `cognitive` | `cognitive_architecture_demo.v0` | 0.2.0 | Experimental architecture demonstration | Natal |
| `woofmapped` | `woofmapped_astrology.v0` | 0.1.0 | Playful experimental reference profile | Natal, synastry |

Temporal execution reuses static mapping capabilities and applies its own activator/target scope classification. The Cognitive and Woofmapped profiles currently exclude `Spirit` as a temporal target. Orthodox declares no temporal activator or target exclusions.

The Cognitive profile is not a clinical, diagnostic, or empirically validated model. Woofmapped projection is not veterinary advice or behavioral diagnosis. Both exist as rich demonstrations of projection into a non-orthodox ontology.

## What a profile owns

A profile owns:

- its versioned manifest and target ontology;
- source eligibility and selection policy;
- object and relationship mapping behavior;
- projected term registry;
- context validation and context-sensitive semantic emphasis;
- final profile-specific graph annotations.

The engine owns identifiers, provenance, deterministic merging, audit records, diagnostics, ordering, indexes, and contract validation.

Profiles are resolved by exact `(profile_id, profile_version)`. A version mismatch is an error, not an invitation to select whatever happens to be nearby.

## Contexts

A `ProjectionContext` is versioned plain data. Common fields include:

- `context_id` and `context_version`;
- `subject_scope`;
- `target_domain`;
- `application_context`;
- optional audience, relationship type, constraints, and parameters.

Context can change relevance, audience framing, or target-domain emphasis. It must not mutate the canonical source graph or alter projection-neutral timing facts. Context is also distinct from output voice: a handler-facing context can declare guidance intent without SPC inventing recommendations or prose.

Bundled contexts live under `examples/contexts`. The general tools filter this directory by target domain and route. Explicit `--context` input always supplies the complete selected context.

## Woofmapped context families

Woofmapped currently provides:

- general Doghouse natal framing;
- handler-facing temporal guidance intent;
- dog-facing direct temporal framing;
- hybrid horoscope framing;
- human-dog synastry;
- symmetric and asymmetric dog-dog synastry.

These contexts reuse one primitive profile. They are not separate astrologies hiding in a trench coat.
