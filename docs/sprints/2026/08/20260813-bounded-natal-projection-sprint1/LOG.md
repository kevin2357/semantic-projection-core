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

## 2026-08-13 — Slice 1 released-contract audit

- User approved the sprint scaffold, committed as `1d28af3` and pushed to
  `origin/main`, then authorized beginning the audit.
- Read the released AGF bounded package, graph, evidence, calculation-provenance,
  evidence-provenance, and structural-evidence schemas; bounded package builder;
  interval/evidence construction paths; semantic-boundary finalization; bounded
  tests; release manifests; installed qualification; oracle summaries; and the
  four bounded/decoupling sprint histories.
- Read SPC's static request and output schemas, validation, contracts, engine,
  audit/coverage calculation, artifact identity, deterministic IDs, profile
  registry, runtime provenance, term-registry materialization, Woofmapping
  manifest/mappings/context behavior, all four natal contexts, package resources,
  release compatibility, and relevant tests.
- Confirmed that accepting graph version 1.7.0 through the existing static route
  would be unsafe: its request separates sections that must remain mutually
  consistent, its validator knows only graph version rather than bounded package
  identity, its profile expects exact-source shapes, and its score fallback turns
  intentionally absent bounded strength into `1.0`.
- Selected an atomic full-package intake. Callers provide the released
  `bounded_natal_dataset`; SPC extracts and cross-validates its graph, evidence,
  structural, identity, capability, and provenance sections.
- Selected dependency-neutral consumer validation: SPC will package an SPC-owned
  schema for the fields and invariants it consumes and add semantic/reference
  validators. It will not import AGF at runtime and will not copy or claim
  ownership of AGF's complete native schemas.
- Selected additive identities for implementation: request
  `bounded_natal_projection_request.v1`, output
  `projected_bounded_semantic_graph.v1`, CLI `semantic-bounded-project`, and
  sibling profile `woofmapped_bounded_astrology.v0` version 0.1.0. The target
  ontology and four existing context IDs remain Woofmapping identities.
- Retained 0.11.0 as the candidate distribution/engine version. This is an
  additive public feature release; qualification and publication remain later
  approval boundaries.
- Selected artifact-scoped evidence materialization: preserve verbatim every
  directly used evidence record plus recursively resolvable prerequisites,
  retain unresolved prerequisite identifiers as opaque source references, and
  record the source artifact hash and closure diagnostics. Do not copy the full
  source registry merely because it exists.
- Selected a context-independent correspondence identity in addition to each
  context-specific projected ID, because the current static ID algorithm includes
  `context_id` and therefore cannot itself correlate parallel context artifacts.
- Selected family-aware coverage alongside ordinary record coverage. Raw record
  counts remain diagnostic topology counts and must be labelled non-weighting.

## 2026-08-13 — Upstream contract inconsistency found during Slice 1

- AGF's published generalized evidence schema enumerates availability values
  `available`, `disabled_by_configuration`, `unsupported_provider_field`,
  `missing_provider_field`, `nonfinite_provider_value`, and `provider_failure`.
- Released AGF 0.8 implementation also emits values including `disabled`,
  `prerequisite_unavailable`, `prerequisite_variable_or_unavailable`, and
  `unsupported_profile` for some terrestrial, triplicity, calculated-point, and
  optional-external-feature evidence.
- The bounded package schema does not apply the generalized evidence schema to
  every `evidence_registry` value, so package-level schema validation does not
  detect that vocabulary difference. Some evidence families also use specialized
  shapes rather than the generalized envelope.
- SPC will not guess that these reasons are equivalent or reject an otherwise
  released artifact solely because a reason token is outside the standalone
  schema enum. It will treat `classification` as the epistemic state, preserve
  `availability` and `status_reason` verbatim as source reason vocabulary, and
  validate the fields needed for each consumed feature family. The mismatch is
  recorded as an upstream compatibility warning for AGF reconciliation.

## 2026-08-13 — Slice 1 verification and gate disposition

- Created `results/SLICE 1 - Released Contract and Semantic Audit.md` and
  `results/bounded-contract-compatibility.json`.
- Parsed the machine-readable compatibility evidence as JSON.
- Ran Markdown trailing-whitespace and fence-balance checks and `git diff
  --check`.
- No implementation source, runtime schema, profile, CLI, test, version, or
  package resource changed in Slice 1.
- Slice 1 gate disposition: ready for review. Slice 2 has not begun.
