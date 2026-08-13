# Bounded Natal Projection Sprint 1 Log

This is an append-only chronological record. Corrections are added as later
entries rather than rewriting prior observations.

## 2026-08-13 — Sprint initialization

- User requested a reviewable sprint directory, plan, log, and results scaffold.
  Implementation has not been authorized.
- Repository: `C:\dev\github\semantic-projection-core`.
- Initial branch: `main`.
- Initial HEAD: `52fa6b97da623c8257372c7c699aca46e3254a6c`
  (`Consolidate SPC release documentation`).
- Initial tracked working tree was clean.
- Existing August sprint directory:
  `20260805-release-engineering-sprint1`. No sprint existed on 2026-08-13, so
  this directory is `20260813-bounded-natal-projection-sprint1`.
- Planning evidence came from detailed review of AGF's foundational bounded
  birth-time sprint, coordinate-derived expansion sprint, terrestrial/time-frame
  expansion sprint, and the immediately following AGF/SPC decoupling sprint.
  The decoupling sprint was included because it changed the integration boundary
  that bounded projection must use.

## 2026-08-13 — Confirmed product and semantic decisions

- Bounded natal is a distinct representation and receives a distinct projected
  output contract.
- Existing `projected_semantic_graph.v1` must not change.
- Derived-object multiplicity requires both preservation and anti-inflation:
  preserve root-owner/evidence-family identity while preventing family members
  from becoming independent relevance, coverage, confidence, or salience votes.
- Projection context is orthogonal to epistemic certainty. The four Woofmapping
  contexts may vary target relevance or framing, but not what the source proved,
  its evidence, limitations, or capability state.
- No implementation work began. Candidate contract, command, profile, and
  0.11.0 release names are presented for review and will be confirmed or revised
  at the Slice 1 gate.

## 2026-08-13 — Upstream facts carried into planning

- AGF 0.8.0 publishes a `bounded_natal_dataset` 1.0.0 containing a
  `bounded_canonical_astrology_graph` 1.7.0 and bounded uncertainty evidence
  1.0.0.
- The bounded artifact describes categorical facts proved across an elapsed
  birth-time interval. It does not authorize treating a midpoint or another
  representative instant as the subject's chart.
- Canonical bounded rows intentionally prohibit exact longitudes, sign degrees,
  pretty positional strings, orbs, distances, applying deltas, and structural
  strength values where those values are not invariant.
- Structured evidence may contain circular or disjoint ranges, categorical
  possibilities, prerequisites, transition witnesses, counterexamples, proof
  scope, availability, and capability limits.
- Canonical graph topology can be large. A reviewed four-hour example was about
  15.7 MB with 105 objects, roughly 1,400 invariant derived/declination
  relationships, and more than 2,100 evidence records. Scale and family
  multiplicity are therefore semantic as well as performance concerns.
- AGF deliberately groups derived siblings by root owner/evidence family. Those
  groups are not independent observations, confidence boosts, or salience
  weights.
- AGF 0.8.0 removed its SPC runtime dependency and projection execution surface.
  SPC now owns intake and projection execution over projection-neutral serialized
  wire artifacts. The plan must not reverse that boundary accidentally.
- Independently installed AGF 0.8.0 and SPC 0.10.0 passed exact-chart wire
  compatibility, but SPC 0.10.0 correctly rejects bounded graph 1.7.0.
- Current SPC exact validation supports canonical source graph 1.3.0. Current
  source selection and mappings assume exact-chart object and relationship
  semantics, so merely allowing version 1.7.0 would be unsafe.
- Current Woofmapping behavior can default absent structural score to `1.0`.
  That behavior must not be applied to bounded graphs, which intentionally omit
  structural strength.
- AGF wire references may use qualified `canonical:object:<id>` and
  `canonical:relationship:<id>` namespaces while canonical rows store raw IDs.
  Slice 1 must freeze the documented normalization and closure rules from the
  released contract.

## 2026-08-13 — Initial planning decisions and uncertainties

- Proposed additive public identities are:
  `bounded_natal_projection_request.v1`,
  `projected_bounded_semantic_graph.v1`, and
  `semantic-bounded-project`.
- Proposed distribution/engine release is 0.11.0 because the change adds a new
  public route, schema, and executable semantic policy while retaining 0.10.0
  behavior.
- Leading profile option is a separately versioned bounded Woofmapping profile
  rather than modifying released `woofmapped_astrology.v0` in place. Slice 1
  must decide whether shared ontology/term resources retain identity or require
  new versions.
- Validation ownership remains an explicit Slice 1 decision. AGF owns its full
  native schemas, but SPC must reject unsafe wire input without reintroducing a
  runtime/execution dependency. Candidate approaches will be evaluated against
  installed-wheel operation and cross-project authority boundaries.
- SBE's acceptance of the future bounded output is not assumed. A complete
  handoff and fixture is an acceptable sprint result if downstream support must
  be implemented separately.

## 2026-08-13 — Planning verification

- Confirmed the pre-edit worktree was clean on `main`.
- Confirmed no same-day SPC sprint directory existed.
- Reviewed the prior SPC release sprint's plan/log/results organization and
  adopted its append-only log and gated-slice conventions.
- Created planning documents and an empty results-area explanation only.
- No source, schema, test, package, profile, CLI, release, tag, remote, or
  downstream repository change was made.

