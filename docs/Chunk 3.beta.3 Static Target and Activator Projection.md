# Chunk 3.beta.3 — Static Target and Temporal Activator Projection

## Status

Stage C3 is implemented.

This pass proves that temporal projection can reuse the existing static projection engine and reference-profile object mappings. It deliberately stops before activation-arc mapping.

## Implemented flow

```text
temporal_projection_request.v1
        ├── static_source_graph
        │       ↓ ordinary static projection engine
        │   projected_semantic_graph.v1
        │
        └── canonical persistent activators
                ↓ existing profile.project_object mappings
            projected temporal activators
```

No separate temporal body ontology or duplicate sign/house/aspect mapping tables were introduced.

## Stage C3 artifact

The inspection artifact is:

```text
projected_temporal_foundations
contract_version: 0.1.0
```

Schema:

```text
projected_temporal_foundations_v1.schema.json
```

It contains:

- the complete ordinary static projected target graph;
- persistent projected activators;
- source-to-projected target resolution index;
- activator coverage;
- the used projected-term registry;
- explicit limitations stating that activation arcs begin in C4.

This is an intermediate development artifact, not the final `projected_temporal_activation_graph.v1`.

## Artifact identification

Core now exposes:

```python
identify_artifact(...)
```

It distinguishes:

- Foundry temporal source bundles;
- canonical temporal graphs;
- temporal projection requests;
- static projected graphs;
- projected temporal graphs;
- unknown artifacts.

The QA runner uses semantic artifact identity rather than filename guessing.

## Activator semantics

Each canonical transiting body is represented once as a persistent temporal activator. Dated sign, house, motion, and position facts remain observation-state data and are not duplicated into dated activator objects.

The default mapping delegates to the existing profile object mapper:

```text
Mars
→ orthodox Mars
→ Cognitive Action Selection
→ Woofmapped Chase-Play-Defense Drive
```

depending on profile.

## Deferred to C4

- projected activation arcs;
- temporal relationship mappings;
- projected observation states;
- sequence and pass materialization;
- activation coverage;
- final temporal graph execution.

## Documentation policy

Every Stage C pass must update code contracts, JSON Schemas, architecture documentation, pass notes, and future-work documentation when relevant.
