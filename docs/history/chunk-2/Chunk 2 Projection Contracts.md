# Chunk 2 Projection Contracts

## Status

Chunk 2.1 establishes extraction-ready plain-data contracts. It intentionally does **not** implement the projection engine or any orthodox/cognitive mapping semantics.

## Package boundary

The temporary internal package is:

```text
astro_analysis_sdk.projection
```

It is designed to become the independent Python package:

```text
semantic_projection
```

Generic projection modules must not import SDK pipelines, ephemeris providers, or Swiss Ephemeris.

## Data flow

```text
canonical_astrology_graph
+ structural_evidence_graph
+ ProjectionProfileManifest
+ ProjectionContext
+ source registries
→ ProjectionRequest
→ later projection engine
→ ProjectedSemanticGraph
```

## Implemented contracts

- `ProjectionProfileManifest`
- `ProjectionContext`
- `ProjectionRequest`
- `ProjectedObject`
- `ProjectedRelationship`
- `MappingExecution`
- `ProjectionAudit`
- `ProjectionDiagnostics`
- `ProjectedSemanticGraph`

All contracts are dependency-free dataclasses that serialize to ordinary dictionaries and JSON.

## Deterministic identity

`projection.ids` provides stable identifiers for requests, packages, objects, relationships, and mapping executions. Inputs are normalized through sorted compact JSON and SHA-256. Timestamps are intentionally excluded from identity.

## Validation

The package owns its JSON schemas in:

```text
astro_analysis_sdk/projection/schemas/
```

Validation uses JSON Schema when the optional `jsonschema` dependency is installed. A minimal required-field fallback keeps production imports dependency-free.

Chunk 2.1 accepts canonical source graph version `1.3.0`. Supporting another source contract must be an explicit compatibility change.

## Diagnostics and audit

Chunk 2.1 provides empty audit and diagnostics constructors. Mapping execution population, coverage updates, merge behavior, and unmapped policies arrive in Chunk 2.2.

## Fixtures

Tiny fixtures live under:

```text
tests/fixtures/projection/
```

They prove contract serialization, deterministic identifiers, schema validity, and package extraction readiness without invoking astrology pipelines.

## Dependency inspection

Run:

```bat
python scripts\inspect_projection_dependencies.py
```

The report must show zero imports from:

- `astro_analysis_sdk.pipelines`
- `astro_analysis_sdk.ephemeris`
- `swisseph`
- `pyswisseph`

## Deferred to 2.2+

- profile protocol and registry;
- projection engine;
- mapping and merge execution;
- actual orthodox semantics;
- context-dependent behavior;
- standalone projection CLI;
- cognitive reference profile.

## Chunk 2.2 execution update

The contracts are now exercised by the generic engine described in `Chunk 2 Generic Projection Engine.md`.

A concrete output is included at:

```text
examples/outputs/chunk22_demo_projection.json
```

It demonstrates object merging, relationship endpoint resolution, mapping-execution audit records, unmapped-source diagnostics, stable ordering, and schema-valid projected output.

## Projection options

Chunk 2.3 formalizes `ProjectionOptions` as separate from `ProjectionContext`.

```text
context = what the projection means under these circumstances
options = how the engine executes and materializes the request
```

Current options include audit/diagnostic inclusion, unmapped policy, and future compact-audit extensions.
