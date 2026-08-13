# Slice 3 — Projected Bounded Contract and Provenance

```yaml
status: gate_candidate
date: 2026-08-13
output_contract: projected_bounded_semantic_graph.v1
mapping_execution: not_implemented
existing_static_contract_changed: false
```

## Outcome

SPC now defines and validates a distinct projected-bounded artifact. The
contract preserves the bounded source's epistemic basis and executable runtime
identity without pretending that a validated intake has already acquired
Woofmapping semantics. A valid empty artifact can be built today; populated rows
must satisfy the bounded evidence, correspondence, and provenance rules that
later mapping slices will use.

The existing `projected_semantic_graph.v1` schema is unchanged.

## Contract shape

`projected_bounded_semantic_graph.v1` contains:

- output, engine, profile, context, and runtime identity;
- complete bounded source identity and artifact hash;
- exact source package and graph contract references;
- target ontology identity;
- source capabilities and feature dispositions preserved verbatim;
- an artifact-scoped source-evidence registry;
- bounded projected objects and relationships;
- context-independent correspondence indexes;
- non-weighting counts and bounded-invariant-subgraph summary semantics;
- projected-term registry, audit, and diagnostics locations;
- upstream/runtime/epistemic provenance; and
- explicit source limitations.

It is neither substitutable for the exact projected graph nor independently a
finished reading.

## Projected row requirements

Every projected object and relationship requires:

- a context-specific artifact row ID;
- a context-independent `correspondence_id`;
- target semantic type/name/operators;
- exact source refs;
- exact mapping-rule refs;
- context refs;
- `epistemic_basis.classification = invariant`;
- one or more materialized evidence refs;
- one or more preserved evidence-family groups;
- source proof scope; and
- provenance.

Relationships additionally require projected endpoints that exist in the same
artifact. Correspondence IDs must be unique across both object and relationship
rows.

`structural_strength_score` is prohibited. A nullable target-domain
`projection_relevance_score` is available for later profile use, but it is not
source certainty, evidence strength, confidence, or an independence weight.

## Evidence closure

`bounded_evidence_closure` starts from evidence refs attached to emitted rows.
It validates every direct ref, recursively follows prerequisite identifiers that
exactly match source-registry keys, and embeds a deterministic, sorted subset.

Prerequisite identifiers that refer to provider features, coordinate features,
or another upstream namespace are preserved verbatim as
`unresolved_prerequisite_refs`. SPC does not guess namespace translations. A
missing direct evidence ref is fatal; an opaque prerequisite is retained and
diagnosed by the contract.

The evidence block records:

- source evidence contract;
- materialization policy;
- embedded records;
- direct refs;
- resolved prerequisite refs;
- unresolved prerequisite refs;
- source and materialized record counts; and
- SHA-256 of the embedded semantic evidence subset.

This makes evidence difficult to discard accidentally while avoiding automatic
duplication of every source evidence record into every context artifact.

## Identity and cross-context correspondence

Projection IDs remain context-specific because each context produces a distinct
artifact. Correspondence IDs deliberately omit context and include:

- row kind;
- exact bounded profile ID;
- target semantic key; and
- sorted source refs.

Two structurally parallel context artifacts therefore have different projection
and row IDs but stable correspondence IDs. The contract indexes correspondence
IDs directly.

The provenance `epistemic_identity` hashes:

- complete source artifact identity;
- embedded evidence subset;
- source capabilities; and
- source feature dispositions.

Tests prove that general and handler artifacts built from parallel rows have
identical correspondence and epistemic identities despite distinct projection
IDs. Later Slice 6 tests will extend this to all four configured contexts and
fully mapped artifacts.

## Provenance boundary

Runtime provenance uses the existing installed runtime identity contract with:

- route `bounded_natal_projection`;
- output `projected_bounded_semantic_graph.v1`;
- exact profile and context identity;
- distribution/runtime/schema/semantic-resource fingerprints; and
- bundled-resource status.

Before the bounded profile is packaged in Slice 4, its policy resource set is
correctly represented as not bundled. This is a truthful transitional state,
not release provenance for a qualified mapping runtime.

## Validation behavior

Validation rejects:

- use of the exact projected schema shape;
- missing or duplicate row IDs;
- duplicate correspondence IDs;
- non-invariant projected epistemic classifications;
- structural strength fields;
- dangling projected endpoints;
- evidence refs absent from the materialized subset; and
- malformed runtime/source/evidence identities.

Artifact construction deep-copies inputs and sorts rows, evidence, and indexes
deterministically.

## Verification

- Focused bounded intake/contract tests: 26 passed.
- Full SPC suite: 183 passed in 60.75 seconds.
- Ruff passed on the new contract and focused changed modules/tests.
- Public export assertions cover all new supported SDK surfaces.
- Existing `projected_semantic_graph_v1.schema.json` has no diff.
- Machine-readable result evidence parses as JSON.
- Markdown whitespace/fence and `git diff --check` validation pass.

## Gate decision

Slice 3 is ready for review. Slice 4 may add the independently versioned bounded
Woofmapping profile and object mappings against this contract. No object mapping
has been implemented early.

