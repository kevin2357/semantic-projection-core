# Semantic Projection Core

Semantic Projection Core (SPC) is a Python library for deterministic, auditable projection of canonical source graphs into target-domain semantic graphs.

```text
canonical graph + structural evidence + source registries
                     +
       versioned profile + context
                     |
                     v
 projected graph + term registry + audit + diagnostics
```

SPC projects structure through explicit mappings. It does not calculate astrology charts, synthesize final claims, prescribe advice, apply game mechanics, or publish reports. Those responsibilities belong upstream or downstream of the projection boundary.

## Current capabilities

- Generic profile-driven static projection engine
- Deterministic IDs, provenance, audit, diagnostics, and scope-aware coverage
- Exact-version profile registry with optional Python entry-point discovery
- Full, standard, summary, and forensic materializations
- Profile-owned projected term registries and used-term subsets
- Deterministic local rendering helpers
- Astrology Graph Foundry temporal-bundle validation and adaptation
- Directional, arc-first temporal projection with preserved timing facts
- End-to-end temporal materialization and route receipts
- Participant-aware synastry projection
- Bounded-birth-time natal intake and invariant-subgraph projection
- Four-context bounded Woofmapping correspondence and certainty validation
- Interactive and unattended natal, temporal, and synastry tools

Bundled profiles are:

- `orthodox_astrology.v1` 1.0.0 — expanded reference profile
- `cognitive_architecture_demo.v0` 0.2.0 — experimental architecture demonstration
- `woofmapped_astrology.v0` 0.1.0 — playful experimental reference profile
- `woofmapped_bounded_astrology.v0` 0.1.0 — bounded-natal Woofmapping profile

## Install and test

SPC requires Python 3.10 or newer. Full Draft 2020-12 JSON Schema validation is
a required runtime behavior and is provided through the declared `jsonschema`
dependency.

```powershell
python -m pip install -e ".[dev]"
python -m pytest -q
```

An installed distribution can verify its version alignment, entry points, and
packaged semantic-resource fingerprint without consulting a source checkout:

```powershell
semantic-runtime-smoke --require-installed --json --release-manifest-out release-manifest.json
```

## Common workflows

Project a static package:

```powershell
python tools/project_natal.py `
  --source path/to/natal-package.json `
  --profile orthodox `
  --context examples/contexts/orthodox_general_context.json `
  --out outputs/natal.standard.json
```

Project an Astrology Graph Foundry temporal source bundle:

```powershell
python tools/project_temporal.py `
  --bundle path/to/temporal_projection_source_bundle.json `
  --profile orthodox `
  --context examples/contexts/orthodox_general_context.json `
  --out outputs/temporal.standard.json `
  --receipt-out outputs/temporal.receipt.json
```

Project participant-aware synastry:

```powershell
python tools/project_synastry.py `
  --source path/to/synastry-package.json `
  --participants participants.json `
  --profile orthodox `
  --context examples/contexts/orthodox_synastry_general_context.json `
  --out outputs/synastry.standard.json
```

Project an AGF bounded natal package without inventing a representative chart:

```powershell
semantic-bounded-project `
  --source path/to/bounded-natal.json `
  --context-id woofmapped.doghouse.general.v0 `
  --context-version 0.1.0 `
  --out outputs/bounded.general.json
```

The tools prompt for omitted required values and support `--help`, explicit options, request output, and `full`, `standard`, `summary`, or `forensic` materialization.

## Woofmapping convenience tools

```powershell
python tools/woofmap_natal.py --source dog-natal.json --out dog-natal.woof.json
python tools/woofmap_transit.py --bundle dog-transits.json --audience handler --out dog-transits.woof.json
python tools/woofmap_synastry.py --source pair.json --kind human-dog --participant-a-id handler --participant-b-id dog --out pair.woof.json
```

Transit audiences are `handler`, `dog`, and `hybrid`. Synastry kinds are `human-dog` and `dog-dog`.

## Python API

```python
from semantic_projection import (
    ProjectionRequest,
    load_bundled_context,
    project_with_builtin_profiles,
)

request = ProjectionRequest.from_dict(request_data)
projected = project_with_builtin_profiles(request).to_dict()
context = load_bundled_context("orthodox.general.v1", "1.0.0")
```

Temporal integrations should use `project_foundry_temporal_bundle()`. Synastry integrations should use `project_synastry()`.

## Architecture boundary

Astrology Graph Foundry is SPC's upstream producer of canonical astrology graphs, structural evidence, source identities, and canonical temporal bundles. SPC owns target-domain projection and its artifacts. Consumers such as Mythos and AstroWoof own application semantics and publication after projection.

See the [documentation index](docs/README.md) for current guides, reference material, integration contracts, roadmap, and clearly separated implementation history.

Production consumers should start with the
[0.11.0 release compatibility contract](docs/reference/release-compatibility.md)
and [release consumer handoff](docs/integration/release-consumer-handoff.md).
