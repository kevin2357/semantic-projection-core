# Bounded Source-Selection Repair Sprint 1 Log

Append-only chronological record. Commands, findings, decisions, changes,
verification, approvals, commits, release identities, and publication evidence
belong here as slices proceed.

## 2026-08-18 - Initial repository state and defect report

- Repository began clean on `main` at `da688c6` (`Document AGF 0.8.1 bounded
  compatibility`).
- A first downstream bounded authoring cycle produced both True Node and Mean
  Node claims. SBE QA correctly classified the resulting content as duplicate.
- Exact Woofmapped static projection already prefers True Node, excludes Mean
  Node through `excluded_by_source_selection_policy`, and excludes relationships
  touching the removed row. Existing regression coverage proves that behavior.
- The bounded profile declares `node_variant: true` and
  `fortune_variant: part_of_fortune`, but its object classifier currently checks
  only source shape and mapping availability. Both node variants therefore map
  to the same North Node semantic primitive under distinct source identities.
- The same implementation gap can affect the declared Fortune preference,
  derived rows owned by excluded aliases, dependent relationships, coverage,
  family accounting, registries, and all four contexts.
- No implementation change has begun. Candidate version 0.11.1 is a planning
  recommendation pending Slice 1 audit.

## 2026-08-18 - Planning gate

- Created the sprint plan, append-only log, and results index.
- Current gate is plan review. Implementation is not authorized.

## 2026-08-18 - Plan approval

- User approved the sprint plan and authorized commit, push, and Slice 1 work.
- Marked the sprint active and opened the reproduction/policy-closure audit.

## 2026-08-18 - Slice 1 exact and bounded policy audit

- Confirmed exact Woofmapped selection classifies Mean Node and the exact legacy
  Fortune alias as `excluded_by_source_selection_policy`; True Node and Part of
  Fortune remain eligible. Dependent exact relationships inherit the exclusion.
- Confirmed AGF 0.8.1 emits both `True Node` and `Mean Node` as
  `bounded_natal_body` rows using space-bearing names and underscore-bearing IDs.
  Its transforms retain `owner_object_ref` to the corresponding body.
- Confirmed AGF's bounded terrestrial calculation emits one
  `bounded_calculated_point` named `Fortune`. It does not emit the exact graph's
  legacy `lot` alias alongside a separate bounded Part of Fortune row. Applying
  the exact name-only helper wholesale would delete a valid bounded fact.
- Built a controlled current-runtime reproduction with True Node, Mean Node,
  calculated Fortune, synthetic Part of Fortune, True/Mean harmonic descendants,
  and direct/ownership relationships. Every row classified `eligible`, every row
  projected, and both node variants mapped to `training_development_vector`.
- The bounded artifact audit simultaneously declared `node_variant: true`,
  proving policy metadata and execution disagree.
- Bounded coverage currently has only mapped and outside-scope buckets. It needs
  separate object and relationship policy-exclusion counts and IDs.

## 2026-08-18 - Slice 1 decisions

- Implement a bounded type-aware selection helper rather than directly reusing
  exact name-only selection.
- Direct Mean Node is policy-excluded using normalized source name. True Node is
  eligible; Mean Node is not promoted when True Node is absent.
- Every transform whose owner status is policy-excluded inherits the same status.
- Every relationship touching a policy-excluded endpoint inherits the same status.
- Preserve AGF's `bounded_calculated_point` Fortune and its relationships as the
  canonical bounded representation of Part of Fortune semantics.
- Add explicit policy-excluded IDs/counts for objects and relationships while
  retaining outside-scope accounting for genuinely unsupported rows.
- No schema, profile ID/version, ontology, context, or registry version change is
  required. Retain candidate distribution/engine version 0.11.1 because runtime
  semantic behavior and fingerprints change.
- Slice 1 gate is ready for review. No runtime implementation has begun.

## 2026-08-18 - Slice 1 approval and Slice 2 start

- User approved the Slice 1 audit using the commit/push/continue boundary.
- Committed and pushed the audit as `3eaa44c` (`Audit bounded source-selection
  closure`).
- Opened bounded policy enforcement only after the audit became immutable.

## 2026-08-18 - Slice 2 bounded policy enforcement

- Added bounded-type-aware source selection to the Woofmapped bounded profile.
  `bounded_natal_body` records named Mean Node are now excluded; True Node and
  the single canonical bounded calculated point named Fortune remain eligible.
- Closed selection over bounded derived objects through `owner_object_ref`.
- Closed selection over relationships whenever either endpoint is policy
  excluded.
- Kept policy exclusions distinct from `outside_declared_scope` in the bounded
  audit and added deterministic object/relationship exclusion ledgers plus an
  informational diagnostic.
- Added focused regression coverage for direct nodes, normalized source names,
  derived families, relationship closure, bounded Fortune preservation,
  registry non-expansion, and no Mean Node promotion when True Node is absent.
- Ran 21 focused bounded tests under Python 3.11 in the existing Linux QA image
  with the checkout mounted read-only: all passed. The sole warning was pytest's
  expected inability to write its cache into the read-only mount.
- Slice 2 gate is ready for review. Versioning, manifests, full-suite
  qualification, release work, and downstream replay remain later slices.

## 2026-08-18 - Slice 2 approval and Slice 3 start

- User approved the Slice 2 implementation using the commit/push/continue
  boundary.
- Committed and pushed the bounded policy repair as `bf714f0` (`Enforce bounded
  node source selection`).
- Opened four-context, determinism, and regression qualification only after the
  implementation slice became immutable.

## 2026-08-18 - Slice 3 four-context and regression qualification

- Added a four-context regression proving general, handler, direct-to-dog, and
  hybrid projections make identical source-selection decisions, retain matching
  True Node families, exclude matching Mean Node families and dependent
  relationships, remain structurally parallel, and reproduce identical output
  on repeat execution.
- The first full-suite container run passed 228 tests and failed four for harness
  reasons: the read-only repository root prevented two default CLI log writes,
  while the preinstalled 0.11.0 wheel caused two tests that intentionally expect
  editable-install metadata to observe installed-release metadata instead.
- A first correction attempt confirmed PEP 660 editable installation cannot
  update checkout-local egg-info through a read-only mount. A minimal writable
  copy initially omitted repository tools and durable output fixtures, producing
  expected missing-file failures rather than product failures.
- The final source-suite harness copied the required source, tests, examples,
  tools, scripts, and durable fixtures to ephemeral writable container storage;
  uninstalled the released wheel; installed the candidate editable with dev
  dependencies; and ran from the copied repository root.
- Final full source suite: 232 passed in 56.08 seconds.
- Whole-tree Ruff is not a valid clean gate for the current Windows checkout:
  Docker observes NTFS-mounted Python files as executable and the repository has
  pre-existing lint debt outside this slice. Focused Ruff with `EXE002` ignored
  passed on every Python file changed by this sprint.
- Final focused four-context, bounded source-selection, exact static
  node/Fortune, and temporal Mean Node regression set: 22 passed in 119.57
  seconds. Changed-file Ruff passed in the same command.
- Slice 3 gate is ready for review. No package, engine, profile, schema, ontology,
  context, or registry version has changed yet.

## 2026-08-18 - Slice 3 approval and Slice 4 start

- User approved the Slice 3 qualification using the commit/push/continue
  boundary.
- Committed and pushed four-context and regression evidence as `4d165a5`
  (`Qualify bounded source selection across contexts`).
- Opened release identity, installed candidate, compatibility, and downstream
  handoff work only after regression qualification became immutable.
- Advanced distribution and engine identity to candidate 0.11.1. Retained
  bounded profile 0.1.0 and `projected_bounded_semantic_graph.v1`: execution now
  conforms to already-declared policy, so neither semantic policy declaration
  nor wire contract changed.

## 2026-08-18 - Slice 4 installed candidate and release handoff

- Updated packaged compatibility identity, current release references, bounded
  consumer guidance, runtime/provenance sentinels, and release-local handoff
  material for candidate 0.11.1.
- Corrected the obsolete SBE 0.3.0 bounded-blocker statement. Current SBE owns a
  dedicated bounded admission, selection, authoring, QA, authority-hydration,
  and lifecycle route; SPC still owns upstream source-selection closure.
- Corrected the obsolete AGF dependency warning: AGF is now runtime-decoupled
  from SPC, leaving the production orchestrator responsible for independently
  pinning both immutable wheels and retaining both runtime receipts.
- Documented the 0.11.0 affected-artifact rule: regenerate from immutable AGF
  source using 0.11.1 rather than deduplicating projected rows in SBE.
- Built the wheel twice under Linux/Python 3.11.15 with
  `SOURCE_DATE_EPOCH=1787090400`. Both 161706-byte artifacts were byte-identical
  at SHA-256 `dc345cd3253de333a5428e4fc7e24816447a065215ef288ba76527960a7da612`.
- Installed that candidate non-editably outside the source checkout. Runtime
  smoke confirmed aligned distribution/package/engine 0.11.1, four profile
  entry points, seven installed commands, 13 contexts, and non-editable status.
- Installed runtime fingerprint:
  `38de395c5089289fb025dc93888d26f64e1c315daaed98bafd069e950d95aa44`;
  semantic-resource fingerprint:
  `464b91889b5146abc92a74ac477ea9b7ac469d0b7c7783700264195e01615b0a`.
- Executed `semantic-bounded-project` from the installed wheel through general,
  handler, direct-to-dog, and hybrid against the checked-in AGF 0.8.1-shaped
  bounded fixture. All commands succeeded.
- Initial focused release tests exposed four expected hard-coded 0.11.0
  sentinels. Advanced them to 0.11.1; the corrected release/provenance set passed
  17 tests.
- A repository search found one additional bounded CLI 0.11.0 sentinel. Advanced
  it and reran the complete final candidate source suite: 232 passed in 57.31
  seconds.
- Prepared release notes, compatibility guide, consumer instructions,
  hash-pinned requirements, SHA256SUMS, and external release manifest under
  `releases/0.11.1/`.
- Slice 4 is ready for review. No commit, tag, push, GitHub release, downstream
  pin mutation, or publication has occurred for 0.11.1.
