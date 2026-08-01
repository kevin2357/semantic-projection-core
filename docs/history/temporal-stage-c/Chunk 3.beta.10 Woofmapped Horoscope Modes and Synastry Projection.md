# Chunk 3.beta.10 — Woofmapped Horoscope Modes and Synastry Projection

This pass adds relationship-aware static projection without inventing a second primitive ontology.

## New modes

- `woofmapped.hybrid_horoscope.v1`
- `woofmapped.synastry.human_dog.v1`
- `woofmapped.synastry.dog_dog.v1`
- `orthodox.synastry.general.v1`
- `orthodox.synastry.professional.v1`

Audience mode and forecast-selection policy remain orthogonal. The hybrid horoscope specifies the three canonical sections: dog internal experience, observable behavior, and suggested activities. Structural, daily-lunar, and blended forecast policies remain downstream selection policies rather than primitive mappings.

## Synastry architecture

`project_synastry()` preserves participant ownership, participant roles, endpoint direction, inter-participant status, relationship kind, aspect identity, and source provenance. It then delegates object and relationship semantics to the ordinary projection engine.

Woofmapped human–dog synastry is explicitly asymmetric: handler-side and dog-side endpoints retain their roles. Dog–dog synastry supports symmetric participant roles. Orthodox synastry remains an auditable identity-oriented projection with ownership attached.

Synastry is not timing. Temporal activation of a relationship graph is deferred until canonical temporal-synastry fixtures exist, at which point it should reuse the established temporal compiler.

## Boundaries

- No new veterinary or behavioral claims.
- No new pack-composite model.
- No prose generation in Core.
- No lunar weighting in primitive mappings.
- Doghouses remain the applied domain system; direct house mapping remains a future traceability layer.
