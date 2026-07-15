# Chunk 2 Registry-Aware Relationship Projection

## Status

Chunk 2.4 extends `orthodox_astrology.v1` to real relationship-oriented projection concerns:

- Synastry theme registries;
- operator registries;
- directional contacts;
- house overlays;
- general relationship context;
- professional relationship context;
- SDK batch projection for compact Synastry analysis views.

## Registry-aware theme resolution

Compact Synastry contacts preserve a `theme_key` while the repeated theme arrays live in a package-level `theme_registry`.

The SDK adapter now supplies that registry through:

```text
ProjectionRequest.source_registries
```

The orthodox profile resolves:

```text
contact.theme_key
→ source theme_registry
→ complete projected themes
```

Registry-origin themes remain individually auditable:

```json
{
  "theme": "home_family",
  "origin": "source_registry",
  "source_ref": "theme_registry:communication|ease_support|home_family"
}
```

Object-derived and aspect-derived themes remain separate origins.

## Context-aware relationship projection

Two reference contexts are implemented:

```text
orthodox.relationship.general.v1
orthodox.relationship.professional.v1
```

The same canonical source graph can therefore produce controlled differences.

Example:

```text
general:
value_attraction_harmony
romance_affection
home_family
supports_and_facilitates

professional:
values_alignment_diplomacy
professional_rapport
team_foundation
professional_supports_and_facilitates
```

Context transformations are recorded in `theme_evidence` rather than silently replacing source meaning.

## House overlays

Synthetic canonical Synastry graphs contain explicit target-house objects. The profile maps these into relationship-domain objects and maps `HOUSE_OVERLAY` relationships into:

```text
activates_relationship_domain
```

or, in professional context:

```text
activates_collaboration_domain
```

Projected overlays preserve:

- direction;
- source person;
- target person;
- target house;
- theme-key provenance;
- registry themes;
- projected relevance.

## SDK adapter

The generic projection core remains package-agnostic.

SDK-specific package extraction lives in:

```text
astro_analysis_sdk.projection_adapter
```

The adapter:

1. extracts canonical and structural graphs;
2. supplies Synastry registries;
3. constructs a generic request;
4. invokes the generic engine;
5. indexes projected relationships by canonical relationship ID;
6. reconstructs compact analysis rows.

## Batch projection

Synastry analysis no longer reconstructs orthodox semantics independently for every contact.

It selects the requested contact/overlay set, projects that source subset once, and reuses the resulting index to enrich report-facing rows.

The canonical source graph remains unchanged.

## Known scope boundary

Chunk 2.4 focuses on Synastry contacts and house overlays. Natal-context hints still use the earlier compatibility adapter and may migrate after the standalone dataset API stabilizes in Chunk 2.5.

## Chunk 2.4.1 representative selection and compact diagnostics

Real Synastry packages frequently rank expanded harmonic, antiscion, and contra-antiscion rows ahead of ordinary planet/angle overlays. A fixed first-N slice could therefore contain no rows supported by the current reference profile.

Analysis selection now preserves source order inside two groups:

```text
supported rows first
then expanded/unmapped rows
```

It fills the requested limit without deleting or rewriting source rows. The analysis view reports available, selected, projected, and unprojected counts for both aspects and overlays.

Embedded analysis diagnostics now summarize unmapped rows by source family with counts and sample references instead of duplicating every informational diagnostic row.

## Chunk 2.4.2 canonical relationship identity resolution

Compact Synastry rows and canonical graph rows may expose different endpoint-ID namespaces. The shared relationship ID is the stable bridge.

Representative selection now resolves:

```text
compact row relationship ID
→ canonical relationship
→ canonical endpoint IDs
→ profile support check
```

Unmapped-family summaries use the same canonical subset, so expanded objects retain their real families instead of collapsing into `unknown_object`.
