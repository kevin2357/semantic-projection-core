# Getting started

## Install

SPC requires Python 3.10 or newer and has no runtime dependencies. From a checkout:

```powershell
python -m pip install -e .
```

For development and full JSON Schema validation:

```powershell
python -m pip install -e ".[dev]"
python -m pytest -q
```

Capability-oriented QA can also be run through the stable wrapper:

```powershell
python scripts/run_qa.py --suite all --coverage
python scripts/run_qa.py --suite temporal
python scripts/run_qa.py --suite woofmapped
```

## Choose an entry point

The repository provides friendly tools for common saved-package workflows:

- `tools/project_natal.py` for a static canonical graph or full AGF package;
- `tools/project_synastry.py` for participant-aware relationship projection;
- `tools/project_temporal.py` for an AGF temporal source bundle.

All accept flags for unattended use and prompt for missing required values interactively. Common options are:

```text
--profile orthodox|cognitive|woofmapped|custom
--profile-id ID               required for custom profiles
--profile-version VERSION     required for custom profiles
--context FILE
--output-mode full|standard|summary|forensic
```

Run `python tools/<tool>.py --help` for route-specific options.

## First static projection

```powershell
python tools/project_natal.py `
  --source examples/requests/cognitive_tiny_request.json `
  --profile cognitive `
  --context examples/contexts/cognitive_architecture_general_context.json `
  --out outputs/cognitive-tiny.standard.json
```

The input may be a complete canonical graph or a package containing `canonical_astrology_graph`. The tool also extracts structural evidence and source identity when present. Use `--request-out` to retain the normalized request.

The bundled tiny file is request-shaped but contains a `source_graph`, which the convenience extractor accepts. For production use, prefer a saved AGF full package or an explicitly constructed request.

## Python API

```python
from semantic_projection import ProjectionRequest, project_with_builtin_profiles

request = ProjectionRequest.from_dict(request_data)
projected = project_with_builtin_profiles(request).to_dict()
```

For a custom registry, call `project(request, registry=registry)` instead. Requests resolve exact profile versions.

## Next steps

- Read [Contracts](../reference/contracts.md) before constructing requests directly.
- Read [Profiles and contexts](../reference/profiles-and-contexts.md) to select target semantics.
- Read [Materialization and artifact identity](../reference/materialization-and-artifacts.md) before choosing an output mode.
