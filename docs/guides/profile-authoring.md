# Profile authoring

A profile is versioned executable policy over SPC's generic contracts. It supplies target-domain drafts; the engine supplies projection infrastructure.

## Required structure

Bundled profiles conventionally contain:

```text
profile_name/
  __init__.py
  manifest.json
  ontology.json
  projected_term_registry.json
  object_mappings.py
  relationship_mappings.py
  context.py
  profile.py
```

The exact module layout is conventional, not contractual. The `ProjectionProfile` protocol is contractual:

- `manifest`
- `validate_context(context)`
- `project_object(source_object, request)`
- `project_relationship(source_relationship, projected_object_index, request)`
- `finalize(graph, request)`

## Manifest

Declare an exact profile ID/version, engine contract version, source and target ontologies, implementation entry point, supported source graph types, context fields, mapping-rule namespace, output contract, deterministic status, and any explicit exclusions or guardrails.

Change the profile version when mapping semantics change materially. Generated artifacts retain both profile and context versions.

## Mapping drafts

Object and relationship methods return zero or more plain dictionaries. Drafts describe target identity keys, semantic attributes, source references, mapping rules, and relevance inputs. They must not assign final SPC IDs or mutate the request.

Classify eligibility explicitly. Deliberate alias/source-selection exclusions are different from unsupported families and mapping failures.

Relationships run after projected objects exist. Resolve endpoints through the supplied projected-object index rather than assuming source and target IDs are interchangeable.

## Term registry

Every production-quality profile should define and validate a projected term registry. All semantic keys emitted by drafts must resolve through it. Include definitions and composition guidance sufficient for consumers to understand the vocabulary without importing profile source code.

## Context

Validate fields and supported context IDs deliberately. Context may adjust semantic emphasis but should not become a bag of transient application state. Volatile game state, report style, and final audience prose belong downstream.

## Registration

Register directly for embedded execution:

```python
from semantic_projection import ProjectionProfileRegistry

registry = ProjectionProfileRegistry()
registry.register(MyProfile())
```

Installed packages can expose profiles through the `semantic_projection.profiles` Python entry-point group. `discover_entry_points()` loads them; the general tools do this when `--profile custom` is selected.

SPC does not yet provide a polished CLI argument that loads an arbitrary source directory as a profile. Active consumers may use their own adapter or packaging workflow, but should not copy consumer-owned semantics into SPC.

## Acceptance checklist

- Exact-version registration and resolution tests.
- Request immutability and deterministic output tests.
- Object and relationship mapping tests over representative source rows.
- Context validation and cross-context tests.
- Eligibility, exclusion, and coverage reconciliation tests.
- Projected-term-registry validation and used-subset tests.
- Static and temporal tests when the profile claims both routes.
- No source-domain constants added to the generic engine.
