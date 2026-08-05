# Semantic Projection Core Release Engineering Sprint 1 Log

This is an append-only chronological record. Corrections are added as later
entries rather than rewriting prior observations.

## 2026-08-05 — Sprint initialization

- User authorized Slice 1 only: read-only release-readiness audit plus sprint
  planning and evidence documents. Slice 2 implementation is not authorized.
- Repository: `C:\dev\github\semantic-projection-core`.
- Initial branch: `main`.
- Initial HEAD: `fa0f2ce` (`Link AstroWoof downstream integration guidance`).
- `origin/main` and `origin/HEAD` pointed to the same commit.
- Initial tracked working tree was clean. Ignored local development artifacts
  were present, including cache directories and `semantic_projection.log`; they
  are not release inputs.
- Existing tags: `v0.1.0` only.
- Candidate asserted by the request: distribution and engine `0.10.0`, Python
  `>=3.10`, five console entry points, and three bundled profiles. Every item
  remains subject to audit.
- No `docs/sprints/2026/08/` directory existed, so the sprint directory selected
  under the per-day naming rule was
  `20260805-release-engineering-sprint1`.
- Safety boundary recorded: no package fixes, wheel build, tag, push, release,
  publication, or cross-repository writes during Slice 1.

## 2026-08-05 — Slice 1 repository and packaging audit

- Read `pyproject.toml`, package discovery/data declarations, public exports,
  profile registry, all five CLI modules, static/temporal execution paths,
  validation, materialization, profile manifests/ontologies/registries/mapping
  code, context resources, schemas, current QA, and current documentation.
- Confirmed declared distribution `semantic-projection-core` 0.10.0, Python
  `>=3.10`, five console scripts, three profile entry points, and no declared
  runtime dependencies.
- Counted 48 package Python files, 19 packaged schemas, 9 profile JSON resources,
  and 13 context JSON files outside the package boundary.
- Finding: current default/context discovery in repository convenience tools
  depends on `examples/contexts`; those contexts are not installed package data.
- Finding: `jsonschema` is dev-only. Without it, contract validation performs
  shallow top-level required-field checks; with it, full Draft 2020-12
  validation runs. Demonstrated the same forbidden context property being
  accepted without `jsonschema` and rejected with `jsonschema` 4.26.0.
- Finding: distribution version and `ENGINE_VERSION` both read 0.10.0 but are
  independent hard-coded sources with no equality test.
- Finding: static artifacts do not emit an explicit static contract version and
  neither static nor temporal outputs identify the wheel/release/resource set.
- Finding: profile manifest `supported_source_graph_types` is not enforced by the
  engine.
- Finding: Orthodox `ontology.json` lacks `profile_version`; no ontology schema
  currently enforces identity.
- Finding: supported context metadata is incomplete/inconsistent with actual
  examples and AstroWoof usage, including omission of the general Woofmapping
  natal context from `supported_context_ids`.
- Finding: current installed-entry-point tests mock metadata; current CLI tests
  execute source modules/functions rather than wheel-installed wrappers.
- Finding: no installed smoke command, runtime resource manifest, release
  manifest, compatibility bundle, checksums, release notes, reproducible-build
  control, or publication automation exists.

## 2026-08-05 — Version and remote release audit

- Inspected local Git history and tags. The only tag is lightweight `v0.1.0` at
  `538b627e9769158455a85f0e000fa537b5bf7635`, predating the current temporal,
  synastry, documentation, and QA baseline.
- Read-only `git ls-remote --tags origin` confirmed the same sole remote tag.
- GitHub CLI is not installed, so the GitHub release-list inventory could not be
  queried in this environment. No publication action was attempted.
- Proposed retaining candidate version 0.10.0 and using a new annotated,
  component-scoped tag `semantic-projection-core-v0.10.0`, conditional on later
  qualification not requiring a meaning-changing release increment.
- Existing `v0.1.0` will not be moved, overwritten, or reused.

## 2026-08-05 — Resource and contract validation

- The sandbox had no generic `python` command on `PATH`; interpreter identity was
  resolved explicitly. This reinforced the requirement that installed QA record
  and invoke an exact interpreter rather than inherit shell ambiguity.
- Used CPython 3.12.13 in the existing editable dev environment.
- Editable distribution metadata and imported engine both reported 0.10.0.
- Actual editable entry-point discovery loaded exactly the three expected
  profiles and exact versions.
- Parsed 41 package/context JSON files successfully.
- Checked all 19 packaged schemas against the Draft 2020-12 metaschema.
- Validated all three manifests, all three term registries, and all 13 contexts
  with full validation available.
- Registry inventories: Orthodox 68 terms; Cognitive 56; Woofmapping 56.
- Computed a non-release source audit over 89 candidate semantic files. Aggregate
  `22eb5a11c10c33cb81c18a3785c99491e3cc7bac2b64570c63c40f4a3c423607`.
  It is explicitly not a release fingerprint because installed paths and context
  packaging must change.

## 2026-08-05 — Cross-repository read-only audit

- AGF HEAD observed at `259058d`; no AGF files were modified.
- AGF 0.5.0 declares `semantic-projection-core>=0.10.0`, documents canonical
  graph 1.3.0 and temporal bundle/graph 1.0.0 compatibility, and imports several
  SPC internal modules/profile mapping helpers in addition to top-level APIs.
- SBE's published `astrowoof-natal-authoring` 0.1.0 release records SPC 0.10.0
  and AGF graph 1.3.0 as its controlled input baseline.
- SBE's input contract requires general, direct-to-dog, handler, and hybrid
  context files. Its registry merger requires identical duplicate definitions,
  matching SPC's downstream contract.
- No cross-repository writes or LLM authorship runs were performed.

## 2026-08-05 — Source-tree QA baseline

- An initial short-timeout QA invocation was terminated before execution could
  complete; it produced no qualification result. The suite was immediately
  rerun with a bounded long timeout.
- Ran `scripts/run_qa.py --suite all --coverage` with CPython 3.12.13.
- Result: 139 passed in 173.95 seconds; branch-aware coverage 89.01%; required
  85% floor passed.
- `pip check` reported no broken requirements in the editable dev environment.
- `compileall -q src` passed.
- Ruff source audit reported 82 findings: 38 F401, 18 I001, 10 C405, 6 UP035,
  5 RUF022, 2 RUF012, and one each PIE800, TRY004, UP006. Broad lint cleanup was
  not authorized; two mutable class-level source-selection dictionaries were
  recorded for bounded hardening review.
- This run is explicitly source-tree evidence, not installed-wheel evidence.

## 2026-08-05 — Slice 1 decision

- Wrote `results/SLICE 1 - Packaging and Dependency Audit.md`.
- Wrote `results/runtime-package-manifest.json` as compact machine-readable
  source-audit evidence, explicitly marked non-release.
- Slice 1 gate: audit complete; current candidate blocked pending approved fixes
  assigned to Slices 2–7.
- No Slice 2 implementation has begun. Awaiting user review and approval.

## 2026-08-05 - Slice 1 approval and commit boundary

- User approved the Slice 1 audit and plan.
- Committed Slice 1 as `b8bd1b17ab7cd82f84a2c2713781c2e9b02d7035`
  (`Audit SPC release readiness`).
- Began only the approved Slice 2 installable-package boundary.

## 2026-08-05 - Slice 2 implementation

- Moved the 13 versioned context JSON resources into the installed
  `semantic_projection.contexts` package. Retained repository examples as
  non-authoritative compatibility copies and added equality tests.
- Declared `jsonschema>=4,<5` as a runtime dependency and removed conditional
  shallow contract validation.
- Established `semantic_projection._version.__version__` as the single version
  source for distribution metadata, package identity, and `ENGINE_VERSION`.
- Added exact installed context resolution, deterministic semantic-resource
  inventory/fingerprinting, and `semantic-runtime-smoke`.
- Added tests for version alignment, complete packaged contexts, exact-version
  failure, fingerprint stability/change sensitivity, entry-point discovery,
  and editable-install rejection.

## 2026-08-05 - Slice 2 source and wheel verification

- Focused tests initially found that the pre-existing editable distribution
  metadata did not hot-reload the newly declared console script. The test was
  corrected to reserve that assertion for a fresh install; the fresh wheel did
  expose the command as required.
- Full source suite passed: 146 tests in 86.95 seconds.
- Focused Ruff check passed after import-order and command-boundary annotation
  cleanup.
- Built the wheel through PEP 517 isolation, then rebuilt after the final source
  adjustments and installed the rebuilt wheel into a second fresh environment.
- Final Slice 2 candidate wheel:
  `semantic_projection_core-0.10.0-py3-none-any.whl`, 123,402 bytes,
  SHA-256 `264dd80c29cc9b3ceacf42dd7c472979d18b0ceec6185893693066f5c2340d98`.
- Archive inspection found 98 members: 13 context JSON files, 19 schemas, nine
  profile semantic resources, runtime smoke code, and distribution entry-point
  metadata.
- Installed smoke ran with `--require-installed --json`: non-editable 0.10.0
  distribution, 0.10.0 engine/package, three discovered profile entry points,
  41 semantic resources, aggregate resource SHA-256
  `4ddcbc98bda8af59563a37ab73608b08d4991d4b0d81d00a4b732f2260187912`.
- Cleared `PYTHONPATH` and ran all five previously supported commands from a
  directory outside the checkout through representative static, temporal
  intake, foundations, temporal projection, and complete temporal pipeline
  routes. All passed; import inspection resolved the fresh environment's
  `site-packages`.
- Wrote `results/installed-smoke.json` and
  `results/SLICE 2 - Installable Package Boundary.md`.
- Slice 2 gate passed. Changes are uncommitted pending review; Slices 3 and
  later have not begun.

## 2026-08-05 - Slice 2 cleanup and review boundary

- Re-ran focused resource/CLI tests: 23 passed. Focused Ruff and
  `git diff --check` passed.
- Parsed the 13 packaged contexts and compact installed-smoke evidence as JSON.
- Deleted the exact temporary build, wheel-install, fixture, and generated-output
  directories after preserving compact evidence and hashes. No candidate wheel
  is retained in the repository; later slices must rebuild from reviewed source.
- Working tree intentionally contains only the uncommitted Slice 2 source,
  tests, documentation, and compact evidence for user review.
