# Temporal projection

Temporal projection consumes an Astrology Graph Foundry `temporal_projection_source_bundle.v1`. It does not accept a raw transit report or flatten a temporal package into a natal graph.

## Command-line route

```powershell
python tools/project_temporal.py `
  --bundle path/to/temporal_projection_source_bundle.json `
  --profile orthodox `
  --context examples/contexts/orthodox_general_context.json `
  --output-mode standard `
  --out outputs/projected-temporal.standard.json `
  --request-out outputs/projected-temporal.request.json `
  --receipt-out outputs/projected-temporal.receipt.json
```

Omit profile or context flags to select them interactively. `--options` accepts a JSON-serialized `TemporalProjectionOptions` object.

## Python route

```python
from semantic_projection import project_foundry_temporal_bundle

result = project_foundry_temporal_bundle(
    bundle,
    profile_id="orthodox_astrology.v1",
    profile_version="1.0.0",
    context=context,
    output_mode="standard",
)

artifact = result.artifact
request = result.request
receipt = result.receipt
```

The production function validates, adapts, projects, materializes, and issues the receipt. Pass an explicit registry when executing a consumer-owned profile.

## What is preserved

Each projected activation is directional from temporary activator to enduring target. Foundry-owned facts remain under `temporal_facts`, including source activation identity, timestamps, sampled phase, orb, motion, pass/sequence identity, observations, and provenance.

Profiles supply target operators, domains, and relationship vocabulary. Context can change relevance and audience framing. Neither is permitted to rewrite timing facts.

## Output interpretation

The projected graph is an activation substrate, not a forecast. It does not select the most important event, combine arcs into advice, infer a narrative lifecycle, or write horoscope prose. Those decisions belong downstream.

Summary materialization omits rows but retains semantic hashes. Standard retains the graph with compact audit. Forensic adds integrity hashes and detailed counts.

## Compatibility note

`project_temporal()` is executable when supplied a valid `TemporalProjectionRequest` and registry. Calling it without a request intentionally raises `TemporalProjectionNotImplementedError`; this preserves the earlier guard against treating an unprepared transit package as a static projection.
