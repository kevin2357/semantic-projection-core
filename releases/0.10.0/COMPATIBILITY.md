# Semantic Projection Core 0.10.0 Compatibility

This release supports Python 3.10 or newer and requires `jsonschema>=4,<5`.
The authoritative machine-readable contract is packaged as
`semantic_projection.release/compatibility.json`; the consumer-readable
contract is [Release compatibility](../../docs/reference/release-compatibility.md).

Supported source boundaries are canonical static graph 1.3.0 and Foundry
temporal source bundle / canonical temporal activation graph 1.0.0. Supported
native outputs are `projected_semantic_graph.v1`, projected temporal activation
graph 1.0.0, projected temporal foundations 0.1.0, and temporal route receipt
1.0.0.

Bundled profiles are:

- `orthodox_astrology.v1@1.0.0`;
- `cognitive_architecture_demo.v0@0.2.0`; and
- `woofmapped_astrology.v0@0.1.0`.

AstroWoof natal integration is qualified for the exact general, handler,
direct-to-dog, and hybrid context versions in `release-manifest.json`. Summary
materialization is not a row-bearing SBE input. Temporal synastry, reconstructed
canonical graphs, reader-facing prose, and internal mapping-module imports are
not supported release routes.

Consumers must pin the wheel SHA-256, resolve profiles and contexts by exact
version, verify the installed runtime manifest, preserve projected-term
definitions and provenance, and reject drift rather than guessing.
