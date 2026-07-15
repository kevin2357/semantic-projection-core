# Semantic Projection Core

Semantic Projection Core is a generic Python library and SDK for **deterministic projection of structured source graphs into auditable target-domain semantic graphs**.

Rather than interpreting source data directly, the engine performs explicit structural projection using projection profiles, contexts, registries, and deterministic graph transformations.

The result is a projected semantic graph that is:

- Deterministic
- Explainable
- Auditable
- Provenance-preserving
- Independent of any specific source domain

Originally developed alongside **Astrology Graph Foundry**, the engine is intentionally domain-agnostic and already includes multiple reference projection profiles demonstrating the same infrastructure across very different target ontologies.

---

## Philosophy

> **Project structure, not interpretation.**

Projection profiles define explicit correspondences between semantic structures.

Semantic Projection Core transforms graphs.

Interpretation, reasoning, narrative generation, visualization, publication, and domain-specific advice are intentionally downstream concerns built on top of projected structure.

In short:

> **Semantic Projection Core projects structure—not meaning. Meaning emerges downstream from projected structure.**

---

## Design Principles

- Deterministic
- Explicit
- Auditable
- Provenance-preserving
- Domain-independent
- Schema-driven
- Context-aware
- Registry-backed
- Structural rather than interpretive

---

## Responsibilities

Semantic Projection Core owns:

- projection request, context, profile, and registry contracts;
- deterministic projection engine and stable IDs;
- audit, diagnostics, scope-aware coverage, and materialization;
- projected term registries;
- deterministic rendering primitives;
- standalone generic CLI;
- Foundry temporal source-bundle validation and generic temporal request intake;
- reserved `projected_temporal_activation_graph.v1` contracts.

It intentionally **does not** calculate astrology charts. **Astrology Graph Foundry** is one upstream producer of canonical source graphs and one integration client of this library.

---

## Included Reference Profiles

Current built-in reference profiles include:

- ✅ Orthodox Astrology
- ✅ Cognitive Architecture *(experimental reference ontology)*
- ✅ Woofmapped Astrology *(demonstration reference ontology)*

These demonstrate that the projection engine itself is generic rather than astrology-specific.

---

## Current Status

**Implemented**

- Generic projection engine
- Profile registry
- Context system
- Deterministic IDs
- Materialization modes
- Projected term registries
- Deterministic rendering primitives
- Standalone static projection CLI
- Validation-only temporal intake CLI
- `temporal_projection_request.v1`

**Planned**

- Temporal activation projection
- Plugin-discovered projection profiles
- Richer deterministic rendering
- Claim compiler integration
- Publication / report layer

---

## Local Development

```bat
python -m pip install -e .[dev]
python -m pytest -q
```

---

## Generic API

```python
from semantic_projection import (
    ProjectionRequest,
    project_with_builtin_profiles,
)

result = project_with_builtin_profiles(request)
```

---

## Temporal Intake

Stage C1 can validate and adapt Astrology Graph Foundry's frozen temporal handoff without yet executing temporal projection:

```bat
semantic-temporal-intake ^
  --bundle temporal_projection_source.json ^
  --projection-profile cognitive_architecture_demo.v0 ^
  --projection-profile-version 0.2.0 ^
  --projection-context examples\contexts\cognitive_architecture_general_context.json ^
  --out temporal_projection_request.json
```

Temporal execution remains intentionally disabled until `projected_temporal_activation_graph.v1` is implemented and validated.

---

## Generic CLI

```bat
semantic-project ^
  --request request.json ^
  --output-mode standard ^
  --out projected.json
```

---

## Documentation

See:

- `docs/Architecture.md`
- `docs/Profile Authoring Guide.md`
- `docs/Installation and Integration.md`
- `docs/Extraction History.md`
- `docs/Ideas and Future Work.md`
- `docs/Chunk 3.beta.1 Temporal Intake and Adapter Contract.md`

