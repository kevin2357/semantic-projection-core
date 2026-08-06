# ADR-0001 — Include Executable Semantic Policy in Release Identity

```yaml
status: accepted
date: 2026-08-05
owner: semantic-projection-core
scope: runtime provenance and release engineering
```

## Context

SPC packages more than a generic projection algorithm. Bundled mappings,
source-selection rules, contexts, ontologies, term registries, schemas, profile
manifests, and entry points determine the semantics of its outputs. Some
profile policy is declarative JSON, while current bundled mappings and
selection behavior are executable Python.

A manifest covering only JSON resources can remain unchanged while executable
mapping behavior changes. A version string alone also cannot identify the exact
wheel installed by a consumer.

## Decision

An SPC release identifies both:

1. the semantic resource set, covering packaged declarative policy; and
2. the runtime package set, covering installed SPC Python and JSON plus relevant
   distribution metadata and entry points.

Artifacts embed compact runtime, resource, schema, profile-policy, context,
route, and output-contract identity. Release orchestration separately records
the wheel SHA-256 because an extracted installation cannot reconstruct the
original wheel bytes.

Production consumers must pin the exact wheel hash and reject drift. Profile
ID/version alone is necessary but insufficient release provenance.

## Consequences

- Changes to executable mappings or source-selection policy alter runtime and
  profile-policy fingerprints.
- Formatting or line-ending changes to covered packaged resources alter byte
  identity even when parsed semantic content is equivalent.
- Reproducible qualification must build from controlled source archives and run
  installed-wheel QA against the exact candidate bytes.
- Third-party profiles require their own pinned distribution identity; SPC
  cannot claim a policy hash for code owned by another installed package.
- Editable installations are useful for development but are not qualified
  release runtimes.
