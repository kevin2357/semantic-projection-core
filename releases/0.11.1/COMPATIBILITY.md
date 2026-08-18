# Semantic Projection Core 0.11.1 Compatibility

SPC 0.11.1 is a semantic-policy bug-fix release over 0.11.0.

## Stable identities

- Python: 3.10 or newer.
- Static source graph: 1.3.0.
- Bounded dataset: 1.0.0.
- Bounded canonical graph: 1.7.0.
- Bounded evidence: `agf.bounded_uncertainty_evidence.v1.0.0`.
- Bounded calculation profile: 1.12.0.
- Bounded interval-proof profile: 1.0.0.
- Bounded profile: `woofmapped_bounded_astrology.v0@0.1.0`.
- Bounded output: `projected_bounded_semantic_graph.v1`.
- Qualified upstream distribution: AGF 0.8.1.

## Intentional output difference

Mean Node, derived objects owned by Mean Node, and relationships touching that
family are excluded before projection. True Node remains preferred even when it
is absent; Mean Node is never promoted as a fallback. Bounded calculated
`Fortune` remains eligible.

This changes affected output content and runtime/resource fingerprints without
changing the declared profile policy or wire contract.

The full consumer boundary remains authoritative in
[`docs/reference/release-compatibility.md`](../../docs/reference/release-compatibility.md).
