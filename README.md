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
- validated `projected_temporal_activation_graph.v1` contract and deterministic temporal ID namespaces.

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
- `projected_temporal_activation_graph.v1` schema and referential-integrity validation
- UTF-8 operational logging
- one-command fixture QA workflow

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

Temporal mapping execution remains intentionally disabled. The output contract is now implemented and validated; Stage C3 will begin reusing static target/object mappings.

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
- `docs/Chunk 3.beta.2 Projected Temporal Contract and Operational Foundations.md`

## Temporal projection development status

Stage C3 now supports validated Foundry intake plus a temporal-foundations inspection route that reuses the ordinary static projection engine and existing profile object mappings. Full projected activation arcs remain intentionally disabled until Stage C4.

```bat
semantic-temporal-foundations --request temporal_request.json --out temporal_foundations.json
```

## Temporal projection status

Stage C4 now supports experimental directional activation-arc projection from a
validated `temporal_projection_request.v1` into
`projected_temporal_activation_graph.v1`.

```bat
semantic-temporal-project --request request.json --out projected-temporal.json
```

The output projects structure only. Temporal reasoning, rendering, and
consumer-facing reports remain downstream.

## Temporal materializations

Projected temporal graphs support `full`, `standard`, `summary`, and `forensic` materializations. The standard view preserves all defining activation arcs and observation facts while compacting audit and diagnostic payloads.

## Temporal cross-profile projection

Stage C6 validates the same canonical temporal facts across Orthodox, Cognitive, and Woofmapped profiles, plus context-sensitive Orthodox variants. Run `scripts\\run_chunk3_beta_6_qa.bat` for the complete one-command QA flow.

## End-to-end temporal production route

Stage C7 provides one supported command from a Foundry source bundle to a projected temporal materialization:

```bat
semantic-temporal-run ^
  --bundle temporal_projection_source.json ^
  --projection-profile cognitive_architecture_demo.v0 ^
  --projection-profile-version 0.2.0 ^
  --projection-context examples\contexts\cognitive_architecture_general_context.json ^
  --output-mode standard ^
  --out projected_temporal.standard.json ^
  --receipt-out temporal_route_receipt.json
```

The route preserves the normalized request and deterministic identity chain without creating a second projection implementation. Run `scripts\run_chunk3_beta_7_qa.bat` for complete production-route QA over every Foundry temporal fixture in `outputs\fixture_test_files`.


### C8 profile expansion

Chunk 3.beta.8 expands the Orthodox reference profile to near-complete canonical object coverage through specialized mappings plus auditable identity projection. The real temporal fixture now projects all 12 activators and all 88 activation arcs. Woofmapped primitive scope is unchanged, but its temporal production route is now explicitly documented and regression-tested.
