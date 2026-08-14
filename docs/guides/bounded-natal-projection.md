# Bounded natal projection

## Purpose

The bounded route consumes an AGF artifact describing the invariant semantic
subgraph of a natal chart when birth time is known only within an interval. It
does not choose a representative instant or turn uncertain features into exact
placements.

The supported installed profile is
`woofmapped_bounded_astrology.v0@0.1.0`; the native output is
`projected_bounded_semantic_graph.v1`.

## Command

```powershell
semantic-bounded-project `
  --source bounded-natal.json `
  --context-id woofmapped.doghouse.general.v0 `
  --context-version 0.1.0 `
  --out bounded.general.json
```

Use the exact context pairs:

| Context | Version |
| --- | --- |
| `woofmapped.doghouse.general.v0` | `0.1.0` |
| `woofmapped.handler_guidance.v1` | `1.0.0` |
| `woofmapped.dog_direct.v1` | `1.0.0` |
| `woofmapped.hybrid_horoscope.v1` | `1.0.0` |

Run the command once per context when a downstream workflow needs the parallel
set. Context can own explicit target framing and relevance; it cannot alter
source certainty, evidence, capabilities, limitations, family identity,
semantic primitives, mappings, operators, or term definitions.

## Consumer obligations

Preserve:

- `source_artifact_ref` and `source_identity`;
- `source_capabilities`, `source_feature_dispositions`, and `limitations`;
- every row's `epistemic_basis`, source refs, mapping refs, and
  `correspondence_id`;
- the embedded `source_evidence` closure;
- evidence-family grouping and non-inflating relevance accounting;
- the complete artifact-scoped projected-term registry; and
- runtime, profile, context, route, and contract provenance.

Do not infer exact degrees, houses, orbs, strengths, probabilities, confidence,
or absent mandatory objects. A `null` relevance or unavailable capability is
not permission to substitute an exact-route default.

Use `validate_parallel_bounded_contexts()` when combining the four outputs. It
requires the exact set and versions, verifies common epistemic and structural
semantic hashes, and confirms distinct context-specific projection IDs. No
context is canonical.

## Downstream authoring status

SPC produces projected semantic artifacts, not finished readings. The published
SBE 0.3.0 loader can recognize and merge the four tiny qualification artifacts,
but its candidate-building policy remains exact-chart-specific. Bounded
authoring therefore requires a separate downstream decision and must not be
enabled by replacing missing scores with convenient defaults.

See the [release compatibility contract](../reference/release-compatibility.md)
and [consumer handoff](../integration/release-consumer-handoff.md).
