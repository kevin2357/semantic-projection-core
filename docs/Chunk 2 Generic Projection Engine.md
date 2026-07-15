# Chunk 2 Generic Projection Engine

## Status

Chunk 2.2 implements the first executable projection engine. It remains deliberately domain-neutral: orthodox astrology and cognitive architecture mappings are not present yet.

## Concrete execution model

```text
ProjectionRequest
    ↓ validate source, profile, and context contracts
ProjectionProfileRegistry
    ↓ resolve exact profile ID and version
ProjectionProfile.project_object()
    ↓ return plain-data drafts
engine
    ↓ deterministic IDs, merge, provenance, audit
ProjectionProfile.project_relationship()
    ↓ return plain-data drafts using projected-object index
engine
    ↓ deterministic ordering, diagnostics, schema validation
ProjectedSemanticGraph
```

Profiles own target-domain meaning. The engine owns mechanics.

## Profile protocol

A profile exposes:

```python
manifest
validate_context(context)
project_object(source_object, request)
project_relationship(source_relationship, projected_object_index, request)
finalize(graph, request)
```

Object and relationship methods return dictionaries called **drafts**. Drafts contain mapping intent—target keys, operators, attributes, mapping rule IDs, and scores—but not final IDs or audit envelopes. This makes profile authoring direct while preserving a single deterministic implementation of identity and provenance.

## Engine-owned responsibilities

The engine performs:

- exact profile/version resolution;
- request and output validation;
- immutable handling of source inputs;
- deterministic projected IDs;
- source-ref and mapping-rule provenance;
- compatible object merging;
- relationship endpoint resolution;
- mapping execution records;
- mapped/unmapped coverage;
- diagnostics and fallback records;
- deterministic ordering and indexes.

No target ontology or astrology rule is hard-coded into the engine.

## Merge behavior

Multiple source objects may map to the same target key. When they do, the engine merges:

- source refs;
- mapping rule refs;
- context refs;
- operators;
- attributes and provenance;
- maximum available structural and projection-relevance scores.

The resulting projected object retains all contributing source references.

## Unmapped policies

The request option `unmapped_policy` supports:

```text
diagnostic   record the unmapped source; emit no target row
passthrough  create a placeholder projected object where possible
ignore       omit the source without an informational diagnostic
fail         stop projection immediately
```

`diagnostic` is the default and is recommended during profile development.

## Audit and diagnostics

Each applied draft creates a `MappingExecution` linking:

```text
mapping rule
source ref
context ref
result ref
```

The audit also records source graph/context/request hashes and mapped/unmapped coverage.

Diagnostics separately record unmapped source refs, informational messages, warnings, errors, and fallbacks. This separation keeps execution history distinct from execution problems.

## Demonstration profile

Chunk 2.2 includes `demonstration_projection.v0`, a tiny domain-neutral profile used only to prove engine behavior. It intentionally maps two source objects into one shared projected primitive, maps one relationship, and leaves another source unmapped.

It is not one of Chunk 2’s final reference profiles. `orthodox_astrology.v1` begins in 2.3 and `cognitive_architecture_demo.v0` begins in 2.6.

Run:

```bat
python examples\projection_engine_chunk22.py
```

The output provides the first concrete example of all Chunk 2.1 contracts operating together.

## Extraction readiness

Generic engine modules do not import astrology pipelines, ephemeris providers, or Swiss Ephemeris. Entry-point discovery is scaffolded under:

```text
semantic_projection.profiles
```

so independently packaged profiles can later register without editing engine code.

## Explicitly deferred

Chunk 2.2 does not implement:

- orthodox astrology semantics;
- cognitive semantics;
- context-driven domain vocabulary;
- SDK package adapters or CLI projection commands;
- claim or narrative reasoning;
- rich fixture projection.
