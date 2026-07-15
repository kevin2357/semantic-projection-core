# Chunk 2 Standalone Projection API and CLI

## Status

Chunk 2.5 makes semantic projection independently callable from saved full SDK packages.

No natal, Synastry, transit, return, or other astrology calculation is rerun.

```text
saved full SDK package
→ extract canonical + structural boundary
→ build generic ProjectionRequest
→ execute profile
→ standalone projected semantic graph
```

## Python API

The embedded SDK exposes:

```python
from astro_analysis_sdk import project_dataset

result = project_dataset(
    source_package,
    profile_id="orthodox_astrology.v1",
    context=projection_context,
)
```

The convenience function lives at the SDK boundary rather than inside the generic projection core because extracting SDK package registries and metadata is adapter-specific.

The generic projection engine remains package-agnostic.

## CLI

Full output:

```bat
python -m astro_analysis_sdk.cli project ^
  --source-dataset outputs\kevin_natal_dataset.json ^
  --projection-profile orthodox_astrology.v1 ^
  --projection-context examples\contexts\orthodox_general_context.json ^
  --output-mode full ^
  --out outputs\kevin_natal_orthodox_projection.json
```

Summary output:

```bat
python -m astro_analysis_sdk.cli project ^
  --source-dataset outputs\kevin_natal_dataset.json ^
  --projection-profile orthodox_astrology.v1 ^
  --output-mode summary ^
  --out outputs\kevin_natal_orthodox_projection.summary.json
```

## Context input

Contexts may be supplied through a JSON file or a minimal set of inline flags.

A context file is preferred for reproducibility.

Included examples:

```text
examples/contexts/orthodox_general_context.json
examples/contexts/orthodox_relationship_professional_context.json
```

## Execution controls

Supported options include:

- profile and exact profile version;
- full or summary output;
- audit inclusion;
- diagnostics inclusion;
- unmapped policy;
- fail-on-unmapped fraction threshold.

Semantic context and engine execution options remain separate.

## Source requirements

The command requires a full SDK package containing:

```text
canonical_astrology_graph
```

Compact analysis and streaming views are rejected because they do not contain the complete source graph required for standalone reprojection.

## Summary materialization

The summary output contains:

- projection/profile/context metadata;
- source identity and source graph reference;
- target ontology;
- projection summary;
- audit coverage;
- diagnostic counts.

It omits:

- projected object rows;
- projected relationship rows;
- mapping execution records;
- full diagnostics.

## Decoupling rule

The public SDK convenience API is exported from:

```text
astro_analysis_sdk
```

while generic contracts and engine code remain under:

```text
astro_analysis_sdk.projection
```

The projection core does not import the SDK adapter. This preserves the later repository-extraction boundary.
