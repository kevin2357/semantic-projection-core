# Semantic Projection Core

Semantic Projection Core is a Python SDK for deterministic, auditable transformation of canonical source graphs into target-domain semantic graphs.

It owns:

- projection request/context/profile contracts;
- deterministic projection engine and IDs;
- audit, diagnostics, scope-aware coverage, and materialization;
- projected term registries and canonical deterministic rendering primitives;
- reference profiles for orthodox astrology, cognitive architecture, and Woofmapped astrology;
- the reserved `projected_temporal_activation_graph.v1` contract.

It does **not** calculate astrology charts. Astrology Graph Foundry is one upstream source-graph producer and integration client.

## Local development

```bat
python -m pip install -e .[dev]
python -m pytest -q
```

## Generic API

```python
from semantic_projection import ProjectionRequest, project_with_builtin_profiles

result = project_with_builtin_profiles(request)
```

## Generic CLI

```bat
semantic-project --request request.json --output-mode standard --out projected.json
```

See `docs/Architecture.md`, `docs/Profile Authoring Guide.md`, and `docs/Extraction History.md`.
