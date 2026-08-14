# SBE Bounded Projection Acceptance Handoff

## Status and authority

This handoff records an observed installed-runtime boundary between SPC 0.11.0
candidate artifacts and the published `astrowoof-natal-authoring` 0.3.0 wheel.
It does not prescribe AstroWoof product behavior or claim that SBE has accepted
a bounded authoring design.

## What already works

SBE's current four-context loader accepts the bounded files' source identity,
target ontology, context markers, object/relationship source-ref topology, and
artifact-scoped projected-term registries. Strict registry merge produced six
terms for the tiny fixture without conflict.

This is useful compatibility, but it is only the shallow input boundary.

## First observed blocker

`build_candidates` computes:

```text
projection_relevance_score / 0.55
```

Bounded objects intentionally carry `projection_relevance_score: null`. SPC has
not established a bounded object-relevance measure, and the contract prohibits
substituting an exact-chart structural score. SBE must define bounded selection
semantics explicitly before authoring from these artifacts.

Safe options include a separate bounded basis route, an explicit bounded
eligibility/selection policy, or deferring bounded authoring. Treating `null` as
zero, one, 0.55, or another convenient default is not safe.

## Contract differences SBE must handle deliberately

1. **Source reference:** bounded output uses `source_artifact_ref`, not
   `source_graph_ref`. The package-level ref carries the bounded package,
   canonical graph, schema, and source artifact hash.
2. **Epistemic evidence:** each row has an invariant `epistemic_basis`; the
   artifact embeds direct evidence plus prerequisite closure in
   `source_evidence`. This is not confidence or structural strength.
3. **Capabilities and dispositions:** `source_capabilities`,
   `source_feature_dispositions`, and `limitations` constrain downstream use
   and must survive basis extraction.
4. **No structural strength:** bounded relationships omit orb, exact geometry,
   application delta, and structural strength. Missing values must not receive
   old fallbacks.
5. **Object completeness:** a bounded invariant subgraph need not contain SBE's
   exact-chart mandatory object set. Absence can mean variable, unavailable,
   inconclusive, unsupported, or simply outside the invariant subgraph—not a
   malformed full natal chart.
6. **Family accounting:** derived siblings share one evidence family and one
   relevance budget. Raw row count is not an independence weight.
7. **Cross-context identity:** compare `correspondence_id`, source refs, and the
   parallel-context validation result. Context-specific materialized IDs are
   expected to differ.
8. **Registry preservation:** preserve every used-term definition and qualified
   ref through filtering, synthesis, and delivery. The registry remains
   artifact-scoped.
9. **No canonical context:** general, handler, direct-to-dog, and hybrid are
   parallel projection contexts. General is not the epistemic master file.
10. **No finished reading:** SPC output is a projected semantic artifact, not a
    selected basis, synthesis, card deck, or reader-facing claim.

## Required SBE decision

SBE/product owners need to decide whether bounded natal authoring should:

- produce a distinct bounded reading/card product;
- select only invariant projected material with explicit omissions;
- supplement it with uncertainty-aware authoring constructs; or
- remain unsupported until a richer product contract exists.

SPC cannot choose among these product/authoring policies. It can provide fixtures,
schema guidance, provenance, and semantic invariants once the downstream policy
is selected.

## Reproduction basis

The failure was observed using:

- SPC candidate wheel SHA-256
  `b28786325e3a37ea511f2e1f265d14f98ec0ecc963ff725fadf7a1e9f52cc44a`;
- SBE 0.3.0 wheel SHA-256
  `377c48ed37d337e42dc9392cc7b5e07a81c3b12c2e0638a50bf33ad1b18cd3b0`;
- checked-in source fixture
  `tests/fixtures/agf/bounded_natal_v1_tiny.json`, SHA-256
  `097266ac8ae463822a75ad71dbc873cf445c05d5aeeef2e19a02182ee705fa6b`;
- the four exact bundled context pairs declared in release compatibility; and
- `semantic-bounded-project` followed by SBE
  `load_and_validate_contexts` and `build_candidates`.

The generated four files are reproducible from that fixture and command set, so
expanded duplicate artifacts are not checked into the sprint directory.
