# Slice 2 — Bounded Wire Intake and Validation

```yaml
status: gate_candidate
date: 2026-08-13
scope: atomic AGF bounded dataset intake
projection_execution: not_implemented
```

## Outcome

SPC now has a dedicated, deterministic intake boundary for the qualified AGF
0.8 bounded natal artifact. It accepts the source as one atomic dataset,
validates the source sections and semantic invariants SPC relies upon, and emits
a prepared `bounded_natal_projection_request.v1` without mutating the input or
executing target-domain projection.

Existing exact and temporal routes remain separate. Supplying a bounded graph to
the exact static validator now fails with explicit bounded-route guidance.

## Public intake boundary

The new SDK surface is:

- `BoundedNatalProjectionRequest`;
- `BoundedNatalSourceContractError`;
- `validate_foundry_bounded_natal_dataset`;
- `adapt_foundry_bounded_natal_dataset`;
- `validate_bounded_natal_projection_request`;
- `BOUNDED_REQUEST_CONTRACT`; and
- `SUPPORTED_BOUNDED_SOURCE`.

The prepared request contains:

- exact request, profile, and context identities;
- a deep-copied complete source artifact;
- reconciled chart and sensor identity;
- a deterministic SHA-256 over canonical JSON of the complete source artifact;
- exact upstream package, graph, evidence, calculation, and proof identities;
- explicit limitations; and
- `execution_status: validated_intake_only`.

No CLI is added yet because the selected `semantic-bounded-project` command is an
execution route and projection/output semantics begin in later slices. Adding an
intake-only command under that name would create a misleading installed contract.

## Consumer-owned validation

SPC packages `bounded_natal_source_v1.schema.json`, a consumer boundary rather
than a copy of AGF's complete schema. AGF remains authoritative for generation
and native package validation. SPC's schema and semantic validator freeze the
fields and relationships required to execute projection safely.

The boundary pins:

| Contract | Supported identity |
| --- | --- |
| Package | `bounded_natal_dataset` 1.0.0 |
| Canonical graph | `bounded_canonical_astrology_graph` 1.7.0 |
| Canonical graph contract | `bounded_canonical_astrology_graph.v1` |
| Evidence | `agf.bounded_uncertainty_evidence.v1.0.0` |
| Calculation provenance | `agf.bounded_natal.calculation_provenance.v1.0.0` |
| Calculation profile | `agf.bounded_natal.calculation_profile.v1.12.0` |
| Proof profile | `agf.interval_proof.v1.0.0` |

There is no AGF runtime import or dependency. This preserves the projection-
neutral wire boundary established by AGF 0.8.

## Semantic and cross-section checks

Intake verifies:

- package, graph, evidence, calculation, and proof identities;
- metadata, canonical graph, structural graph, and semantic-boundary chart
  identity agreement;
- one-source bounded natal identity;
- `pre_projection` graph status;
- package capability agreement with the corresponding finalized graph keys;
- explicit absence of exact-longitude, structural-score, canonical-claim, and
  semantic-activation capabilities;
- bounded-invariant-subgraph basis and non-weighting raw counts;
- unique object and relationship IDs;
- relationship endpoint closure;
- derived owner closure;
- required evidence-family identity on every canonical row;
- direct evidence-reference closure;
- known epistemic classifications; and
- summary count reconciliation.

The validator deliberately preserves availability and status-reason values as
opaque upstream vocabulary, consistent with the Slice 1 finding. It does not
reinterpret them as epistemic classifications.

## Forbidden precision and unsafe fallbacks

Objects are rejected if they contain exact `longitude`, `pretty`, `sign_degree`,
or `structural_strength_score` fields. Relationships are rejected if they
contain `orb`, `distance`, `applying_delta`, `strength`, or
`structural_strength_score`.

This is stronger than relying on the graph version alone and prevents a caller
from laundering exact or scored content into the bounded route. Projection does
not yet occur, so no relevance, salience, coverage, or target term is synthesized
in this slice.

## Identity behavior

`source_artifact_sha256` covers the complete input artifact using SPC canonical
JSON. Request identity covers the request contract, exact profile, source
identity, context, and options. Consequently:

- repeated identical adaptation is deterministic;
- changing context changes request identity but not source identity;
- changing source evidence changes source artifact identity; and
- prepared requests cannot detach a graph from the evidence/provenance package
  that established its meaning.

## Cross-repository probe finding

AGF's finalization adds `supports_invariant_subgraph_summary`,
`supports_structural_strength_scores`, and `supports_canonical_claims` to the
canonical graph after the package-level capability map has already been copied.
Valid artifacts therefore have a graph capability superset rather than two
identical maps.

SPC now requires every package-declared capability to agree with the graph and
uses the finalized graph for the structural capability assertions it consumes.
This preserves strictness without rejecting valid release-shaped output.

## Verification

- Focused integration run: 28 tests passed.
- Final bounded intake suite: 15 tests passed.
- Full SPC regression suite: 172 tests passed.
- Ruff over all touched Python modules and bounded tests: passed.
- A source-shaped package generated through AGF's current bounded builder adapted
  successfully through SPC.
- Machine-readable Slice 2 evidence parses as JSON.
- `git diff --check`, Markdown whitespace, and fence checks pass.

## Gate decision

Slice 2 is ready for review. Slice 3 may define the separate projected bounded
artifact, evidence closure, context-independent correspondence identity, and
provenance model. No mapping or projected output has been implemented early.

