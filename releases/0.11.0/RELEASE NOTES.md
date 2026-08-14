# Semantic Projection Core 0.11.0

Status: published 2026-08-14.

## Added

- Dedicated AGF bounded-natal intake and validation.
- Separate `projected_bounded_semantic_graph.v1` output contract.
- `woofmapped_bounded_astrology.v0@0.1.0` bundled profile.
- Installed `semantic-bounded-project` command.
- Four-context bounded projection with correspondence validation and certainty
  invariance.
- Source evidence closure, capability/limitation preservation, and
  family-aware non-inflating relevance allocation.

## Compatibility

Existing exact static and temporal contracts are unchanged. The bounded route
is qualified against immutable AGF 0.8.0. SBE 0.3.0 can load and merge the
qualification family, but its candidate builder remains exact-chart-specific;
bounded authorship is therefore not yet an end-to-end supported product route.

See [COMPATIBILITY.md](COMPATIBILITY.md) and
[CONSUMER INTEGRATION.md](CONSUMER%20INTEGRATION.md).

## Qualification

- 228 source tests passed before release-document preparation.
- Two fixed-epoch candidate builds were byte-identical.
- The exact wheel installed non-editably outside the checkout.
- All seven installed commands passed meaningful smoke/help checks.
- AGF 0.8.0 intake, four bounded contexts, deterministic QA, negative QA, and
  SBE shallow-boundary acceptance passed during the bounded sprint.
