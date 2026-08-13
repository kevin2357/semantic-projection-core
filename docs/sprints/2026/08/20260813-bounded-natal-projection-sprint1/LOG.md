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

## 2026-08-13 — Slice 1 approval and publication

- User approved Slice 1 using the commit/push/continue boundary.
- Committed the Slice 1 audit as `e30cddf` (`Audit bounded natal projection
  contract`) and pushed `main` to `origin`.
- Began Slice 2 only after the approved evidence was immutable upstream.

## 2026-08-13 — Slice 2 bounded wire intake

- Added `BoundedNatalProjectionRequest`, a dedicated
  `bounded_natal_projection_request.v1` schema, and an SPC-owned consumer schema
  for the exact AGF 0.8 bounded fields and identities SPC consumes.
- Added `validate_foundry_bounded_natal_dataset` and
  `adapt_foundry_bounded_natal_dataset`. Intake accepts one full source artifact,
  deep-copies it, validates cross-section consistency, and produces deterministic
  request and source-artifact identities without importing AGF.
- Validation pins package 1.0.0, graph 1.7.0, evidence 1.0.0, calculation profile
  1.12.0, and interval proof 1.0.0. It reconciles chart identity, package/graph
  capabilities, invariant-subgraph basis, counts, IDs, endpoints, ownership,
  direct evidence refs, family metadata, and epistemic classifications.
- Validation rejects exact positional/scoring fields prohibited by bounded
  semantics. Missing structural strength remains absent rather than receiving an
  exact-profile default.
- Capability reconciliation intentionally permits the canonical graph to expose
  the post-finalization structural capability additions that are absent from the
  package-level pre-finalization capability copy; all shared keys must agree.
- Added explicit wrong-route detection before the existing static graph-version
  check so callers receive bounded-route guidance rather than a generic version
  error. Existing temporal behavior was not changed.
- Added artifact recognition for the AGF bounded dataset and prepared bounded
  request.
- Added a compact, schema-shaped fixture owned by SPC tests. It is not represented
  as a full AGF native-schema fixture or as qualification evidence for AGF itself.

## 2026-08-13 — Slice 2 defects found and resolved

- The first cross-repository generated-artifact probe showed that AGF finalizes
  three structural capabilities only on the canonical graph, after the package
  level initially copies graph capabilities. Requiring the two maps to be
  byte-identical would reject valid release-shaped output. The validator now
  requires all package-declared keys to agree and reads structural capability
  assertions from the finalized graph.
- The older AGF unit assessment helper predates mandatory generalized evidence
  identity and omits `evidence_contract_version`. The cross-repository probe added
  the released evidence identity to that synthetic assessment; the SPC boundary
  correctly remains strict for the qualified 1.12.0 profile.

## 2026-08-13 — Slice 2 verification and gate disposition

- Focused bounded/contract suite: 28 passed during initial integration.
- Final bounded intake suite: 15 passed.
- Full SPC suite: 172 passed in 60.79 seconds.
- Ruff on all touched Python modules and the bounded tests: passed.
- Cross-repository source-shaped probe generated an AGF bounded package through
  the current builder and adapted it through SPC successfully after supplying
  the released evidence identity to the older synthetic assessment helper.
- `git diff --check` and Markdown/JSON checks were run after result documentation.
- No bounded semantic projection, output artifact, profile mapping, installed
  CLI, or release version change is included in Slice 2.
- Slice 2 gate disposition: ready for review. Slice 3 has not begun.

## 2026-08-13 — Slice 2 approval and publication

- User approved Slice 2 using the commit/push/continue boundary.
- Committed the atomic intake boundary as `b63be2e` (`Add bounded natal intake
  boundary`) and pushed `main` to `origin`.
- Began Slice 3 only after the approved intake contract was immutable upstream.

## 2026-08-13 — Slice 3 projected bounded contract and provenance

- Added `projected_bounded_semantic_graph.v1` as a separate package contract.
  The existing `projected_semantic_graph.v1` file was not modified.
- Added bounded-specific projected object and relationship schemas. Every row
  requires an invariant epistemic basis, direct source-evidence refs, evidence
  family groups, proof scope, source refs, mapping refs, and a context-independent
  correspondence ID. Structural strength is prohibited by schema.
- Added `ProjectedBoundedSemanticGraph`, contract construction, validation,
  artifact recognition, and public correspondence/evidence helpers.
- Added artifact-scoped evidence closure. Direct evidence is mandatory;
  prerequisite records are recursively included only when their identifiers
  exactly resolve in the source registry; non-registry prerequisites remain
  verbatim in an unresolved-reference list rather than being guessed or dropped.
- The output preserves source capabilities and feature dispositions verbatim,
  records source and runtime identities, and hashes the evidence subset,
  capabilities, and dispositions into an epistemic identity.
- Projection artifact identity remains context-specific. Correspondence identity
  excludes context and is derived from kind, exact profile, semantic key, and
  source refs so parallel context artifacts can be compared safely.
- The contract records
  `context_epistemic_policy=certainty_invariant_across_contexts`. Tests prove two
  contexts have different projection IDs but identical source evidence,
  epistemic identity, and correspondence IDs for structurally parallel rows.
- The contract builder is mapping-neutral. Slice 3 can produce a valid empty
  bounded artifact or validate supplied projected rows, but it does not map an
  AGF object or relationship into Woofmapping semantics.

## 2026-08-13 — Slice 3 verification and gate disposition

- Focused bounded intake/contract suite: 26 passed.
- Full SPC suite after contract implementation: 183 passed in 60.75 seconds.
- Ruff passed for the new contract implementation, changed contract/ID/validation
  modules, and focused tests. The legacy top-level export module retains broader
  pre-existing Ruff noise and was checked through public API tests plus manual
  import ordering for the changed block.
- Public API coverage now asserts the bounded request, output, intake, evidence,
  builder, and validator exports.
- Exact static output schema diff against HEAD: empty.
- JSON, Markdown, schema, and `git diff --check` validation were run after result
  documentation.
- No Woofmapping object/relationship mapping, projected-term registry, execution
  CLI, profile entry point, version bump, or release change is included.
- Slice 3 gate disposition: ready for review. Slice 4 has not begun.

## 2026-08-13 — Slice 3 approval and publication

- User approved Slice 3 using the commit/push/continue boundary.
- Committed the bounded output contract as `15186db` (`Define projected bounded
  graph contract`) and pushed `main` to `origin`.
- Began Slice 4 only after the contract and provenance boundary were immutable
  upstream.

## 2026-08-13 — Slice 4 Woofmapping bounded object projection

- Added independently versioned profile policy
  `woofmapped_bounded_astrology.v0` 0.1.0 with its own manifest, source-selection
  policy, mapping namespace, ontology resource, and projected-term registry.
- The target ontology remains `woofmapped_astrology.v0`. The profile reuses the
  established canine primitive meanings while keeping bounded source policy and
  registry identity separately fingerprintable.
- Added deterministic object-only execution through
  `project_bounded_natal_objects`. It resolves only the exact bounded profile,
  validates one of the four supported contexts, maps declared object families,
  builds artifact-scoped evidence closure, attaches a used-term registry subset,
  and emits the Slice 3 bounded contract.
- Mapped known bounded bodies, angles, calculated points, house cusps, and
  coordinate-derived objects. Sign indexes become established Woofmapping modes;
  invariant houses become Doghouse domains. No sign or house is manufactured
  when absent.
- Derived antiscia, contra-antiscia, and harmonic objects preserve their root
  owner's target operator and add an explicit coordinate-transform role,
  transform kind/qualifier, owner reference, and owner-family provenance. They
  remain separate source-supported objects and do not become independent votes.
- House cusp objects map directly to the corresponding Doghouse domain while
  preserving source sign and ruler facts as source attributes.
- Bounded sect state and calculated points without an established primitive are
  classified outside declared scope and listed in audit coverage. They are not
  passed through or assigned decorative new meanings.
- Projection relevance remains `null` for every Slice 4 object. Structural
  strength is absent. Relationship projection remains explicitly deferred to
  Slice 5.
- The bounded projected-term registry is an artifact-scoped used-term subset
  with bounded profile identity. Emitted object, mode, and domain refs all
  resolve to embedded definitions.

## 2026-08-13 — Slice 4 intake hardening finding

- Object mapping made visible that promoted `house_number` and
  `triplicity_ruler` fields can have distinct evidence refs beyond the object's
  primary uncertainty evidence.
- Hardened bounded intake so non-cusp house promotions require
  `house_uncertainty_evidence_ref` and triplicity promotions require
  `triplicity_uncertainty_evidence_ref`. Both refs must resolve in the source
  registry and become part of projected epistemic closure.
- House cusp `house_number` is intrinsic cusp identity rather than a promoted
  placement and therefore correctly does not require a separate house-membership
  evidence ref.

## 2026-08-13 — Slice 4 packaging boundary

- The bounded profile resources are included by existing package-data rules and
  receive a bundled policy-resource fingerprint in runtime identity.
- The profile is not yet added to installed entry-point discovery or the 0.10.0
  release-compatibility declaration. Advertising a new installed supported
  profile while distribution compatibility still identifies immutable 0.10.0
  would be false. Installed exposure and release declaration remain Slice 8/9
  work after relationship and QA gates.

## 2026-08-13 — Slice 4 verification and gate disposition

- Bounded suite: 34 passed.
- Full SPC suite: 191 passed in 61.04 seconds.
- Ruff on bounded intake/execution/profile modules and focused tests: passed.
- Manifest schema and projected-term registry semantic validation: passed.
- Runtime identity reports the bounded profile policy resource set as bundled
  and content-addressed.
- Existing exact and temporal release declarations and routes remain unchanged.
- JSON, Markdown, and `git diff --check` validation were run after result
  documentation.
- Slice 4 gate disposition: ready for review. Slice 5 has not begun.
