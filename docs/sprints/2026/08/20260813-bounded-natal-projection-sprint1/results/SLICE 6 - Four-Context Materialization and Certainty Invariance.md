# Slice 6 — Four-Context Materialization and Certainty Invariance

## Outcome

The bounded Woofmapping route now has an executable four-context acceptance
rule rather than an informal expectation. One bounded source can be projected
through handler, direct-to-dog, hybrid, and general contexts and validated as a
parallel set.

The validator proves two independent properties:

1. **Epistemic invariance:** source identity, capabilities, feature
   dispositions, limitations, evidence records, proof scopes, evidence-family
   membership, and row evidence bases are identical.
2. **Structural-semantic correspondence:** objects, relationships, normalized
   endpoints, semantic primitives, operators, mappings, target ontology, and
   artifact-scoped projected-term definitions correspond exactly.

Context-specific materialized IDs are expected and required to differ. Stable
`correspondence_id` values provide comparison identity across the four files.

## Exact context set

| Context ID | Version |
| --- | --- |
| `woofmapped.dog_direct.v1` | `1.0.0` |
| `woofmapped.doghouse.general.v0` | `0.1.0` |
| `woofmapped.handler_guidance.v1` | `1.0.0` |
| `woofmapped.hybrid_horoscope.v1` | `1.0.0` |

The version difference is authoritative packaged state, not an error to hide.
Resolution and validation use the exact pair for each context.

## Permitted and prohibited variation

The cross-context contract permits `projection_relevance_score` and explicitly
owned `audience_framing`, `context_framing`, and `contextual_relevance`
attributes to vary. This records the intended extension boundary even though
the current bounded profile emits structurally equal target semantics in all
four contexts.

It prohibits context-owned changes to certainty, evidence, capability state,
limitations, source lineage, family identity, semantic primitive, operator,
mapping rule, target ontology, or projected-term definition.

No context has canonical or epistemic priority. In particular, `general` is a
named projection context, not a fallback truth file and not an instruction
about AstroWoof product audience.

## Public boundary

`validate_parallel_bounded_contexts` accepts the four already-projected
artifacts and returns a deterministic
`bounded_parallel_context_validation.v1` report. The report records exact
contexts and versions, distinct projection IDs, correspondence counts, and
SHA-256 identities for the common epistemic and structural-semantic views.

This is a candidate 0.11.0 API. It is not part of the immutable 0.10.0 release
and is not yet advertised through installed release compatibility metadata.

## Verification

- focused context and public API tests: 14 passed;
- bounded tests: 57 passed;
- complete SPC suite: 214 passed in 64.96 seconds;
- Ruff: passed for the new implementation and focused tests;
- positive assertions: exact four-context set, exact versions, distinct
  materialized identities, matching correspondence sets, deterministic report,
  and no canonical priority;
- adversarial assertions: drift in evidence, capabilities, limitations, family
  identity, semantics, operators, mappings, or registry definitions is rejected.

Compact machine-readable evidence is in
[`bounded-context-verification.json`](bounded-context-verification.json).

## Gate disposition

Slice 6 is ready for review. Slice 7 deterministic, negative, scale, and legacy
regression QA has not begun.
