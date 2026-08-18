# Slice 1 - Reproduction and policy-closure audit

## Outcome

The downstream duplicate is reproduced as an SPC bounded-profile defect. The
profile declares True Node preference but classifies and projects True Node,
Mean Node, both transform families, and all dependent relationships as eligible.

The repair boundary is narrower than the initial plan's Fortune hypothesis. AGF
0.8.1 emits a single bounded calculated point named `Fortune`; that row is the
canonical bounded representation of the calculated lot and must remain eligible.

## Current versus required node behavior

| Source row | Current | Required |
| --- | --- | --- |
| True Node | eligible and emitted | eligible and emitted |
| Mean Node | eligible and emitted | policy-excluded |
| True Node-owned transform | eligible and emitted | eligible and emitted |
| Mean Node-owned transform | eligible and emitted | policy-excluded |
| relationship touching True Node family | eligible and emitted | eligible when otherwise supported |
| relationship touching Mean Node family | eligible and emitted | policy-excluded |

Both direct nodes currently map to `training_development_vector`; their distinct
source refs produce distinct projected and correspondence IDs, so downstream
selection sees two semantically duplicate candidates.

## Fortune distinction

Exact canonical graphs contain a legacy `Fortune` alias and a preferred
`Part of Fortune` object. Exact source selection removes the former.

AGF bounded graphs instead produce one `bounded_calculated_point` named
`Fortune`, derived from the bounded terrestrial-frame calculation. There is no
parallel bounded Part of Fortune row in the qualified producer. Name alone is
therefore insufficient for cross-route selection. The bounded calculated point
must remain eligible and maps to `easy_good_thing_channel`.

## Implementation boundary

The bounded profile needs a type-aware selection path:

1. Normalize direct source identity using name first, then source key/ID fallback.
2. Classify direct Mean Node as `excluded_by_source_selection_policy`.
3. For coordinate transforms, inspect the owner's already-computed status and
   propagate policy exclusion before checking mapping availability.
4. For relationships, propagate policy exclusion from either endpoint before
   evaluating supported relationship semantics.
5. Track policy-excluded object and relationship IDs/counts separately from
   outside-scope rows.
6. Build projected IDs, registries, evidence-family coverage, and relevance only
   from eligible rows, as the existing execution order already permits.

The exact helper should not be called blindly because its name-only Fortune rule
has different meaning on the bounded object type.

## Version disposition

- Distribution/engine candidate: 0.11.1.
- Bounded profile: remains `woofmapped_bounded_astrology.v0@0.1.0`.
- Output: remains `projected_bounded_semantic_graph.v1` / 1.0.0.
- Contexts, ontology, registry identity, and upstream bounded contracts: unchanged.

This is a patch repair aligning execution with an already-published node policy.
The immutable 0.11.0 artifact remains valid against its schema but is
semantically nonconforming when a projected Mean Node family is present.

## Gate disposition

Ready for review. No implementation change has begun.
