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

## 2026-08-05 - Slice 2 approval and commit boundary

- User approved Slice 2 and authorized continuation.
- Committed Slice 2 as `114906d5e6c6fe67095cc757a023b70b99b437f7`
  (`Establish installable SPC runtime boundary`).
- Began only the approved Slice 3 stable release and compatibility contract.

## 2026-08-05 - Slice 3 compatibility freeze

- Added packaged `semantic_projection.release_compatibility.v1` describing the
  0.10.0 runtime, source/output contracts, profiles, commands,
  materializations, failure policy, and supported four-context natal set.
- Added consistency tests tying the machine contract to implementation
  constants, manifests, bundled contexts, materialization modes, and installed
  distribution entry points.
- Added the release compatibility reference and consumer handoff. Clarified
  high-level Python/CLI support, unsupported internal imports/routes, exact-hash
  installation, preservation requirements, and failure behavior.
- Formally declared the general, handler, direct-to-dog, and hybrid context
  identities as supported static Woofmapped natal contexts. This is projection
  compatibility, not downstream audience or prose policy.
- Recorded that graph versions are enforced while manifest graph-type lists are
  qualified support declarations rather than a generic type-rejection check.

## 2026-08-05 - Slice 3 downstream reconciliation and QA

- Read-only AGF inspection at `259058d` confirmed its permissive
  `semantic-projection-core>=0.10.0` dependency and internal SPC imports. The
  consumer handoff marks both unsuitable for immutable production integration.
- Read-only AstroWoof API inspection at `e0d171d` confirmed its proposed 0.10.0
  compatibility set and unresolved exact-context question. SPC's contract now
  answers the identity/version portion; materialization promotion remains a
  downstream decision.
- Observed pre-existing untracked API path `src/astrowoof_api/storage/`; made no
  downstream changes.
- Focused compatibility/resource tests passed: 10 tests.
- Full SPC suite passed: 150 tests in 92.04 seconds. Focused Ruff passed.
- Wrote `results/compatibility-contract-verification.json` and
  `results/SLICE 3 - Stable Release and Compatibility Contracts.md`.
- Slice 3 gate passed. Changes remain uncommitted pending review; Slice 4 has
  not begun.

## 2026-08-05 - Slice 3 final gate verification

- The first relative-link command mishandled repository-root Markdown files and
  emitted PowerShell path errors; its apparent pass line was discarded as an
  invalid check result.
- Re-ran the corrected checker with terminating errors and an explicit root
  base. All relative links in the eight created or materially updated
  entry-point documents passed.
- Parsed the packaged release compatibility contract and compact evidence JSON.
- `git diff --check` passed.

## 2026-08-05 - Slice 3 approval and commit boundary

- User approved Slice 3 and authorized continuation.
- Committed Slice 3 as `bc49739f2084e007e28cd62ca5fdb6b4f9527e4a`
  (`Freeze SPC 0.10.0 compatibility contract`).
- Began only the approved Slice 4 provenance and release-identity work.

## 2026-08-05 - Slice 4 runtime and policy identity

- Determined that the Slice 2 semantic-resource fingerprint covered JSON
  resources but not executable profile mappings or source-selection policy.
- Added complete installed runtime inventory covering SPC Python/JSON content
  plus distribution `METADATA`, `WHEEL`, and `entry_points.txt`.
- Added schema-only, profile-policy, and exact context identity sets. Modified
  contexts with a bundled ID/version no longer claim bundled resource identity
  unless their complete parsed content matches.
- Added `semantic_projection.runtime_release_manifest.v1`, its schema, Python
  API, and `semantic-runtime-smoke --release-manifest-out` generation route.
- Added compact `semantic_projection.runtime_identity.v1` receipts to static,
  temporal-foundations, temporal projection, materialization, forensic audit,
  and temporal receipt paths.
- Added native runtime-identity schema requirements and updated the static
  contract fixture accordingly.

## 2026-08-05 - Slice 4 defect and QA

- Found that Slice 3 declared temporal foundations contract 1.0.0 while the
  implemented artifact and schema use 0.1.0. Corrected compatibility JSON and
  reference documentation; added a regression assertion.
- Added tests proving executable mapping changes affect both runtime and profile
  fingerprints, semantic resource changes affect their aggregate, and altered
  context content cannot impersonate a bundled context.
- Initial full run: 151 passed and six temporal contract-skeleton fixture
  failures because the fixture lacked newly required runtime identity. Execution
  provenance tests were already passing.
- Updated the standalone temporal contract fixture with a valid real identity.
- Corrected full run: 157 passed in 132.53 seconds.
- Focused temporal/provenance suite: 19 passed. Focused Ruff passed.
- Source-checkout preview identities: runtime package 101 records at
  `ac8dd4b0beca9b2946837a93f9dcb72d86650f810fc4577c18f24e41a8a41eab`;
  semantic resources 44 records at
  `2262689d70b38e3319a7f19a6431462a863acbb68bc8f1da31550c0a9fc72773`;
  schemas 21 records at
  `051c3e2814c7ac4bb75e15bfd7361049b6d267374059b393c51d8c3e7ab72c84`.
  These are explicitly not final installed-wheel release identities.
- Wrote `results/provenance-identity-verification.json` and
  `results/SLICE 4 - Provenance and Release Identity.md`.
- Slice 4 gate passed. Changes remain uncommitted pending review; Slice 5 has
  not begun.

## 2026-08-05 - Slice 4 runtime-cost correction and final verification

- Observed that the corrected 157-test run took 132.53 seconds because each
  artifact identity re-read all installed code and semantic resources.
- Added process-lifetime caching of immutable installed inventory records.
  Editable processes must restart after file changes and remain ineligible for
  release qualification.
- The final full suite passed all 157 tests in 91.63 seconds; focused Ruff
  passed. Runtime identity overhead no longer materially increased suite time.
- Final source-checkout preview runtime package identity changed with the cache
  implementation to 101 records at
  `8ab92812c14f03d574fdb88e83d5b6c83a06e7dcd32e26f8fc49dd282dd9aee0`.
  Semantic, schema, compatibility, and profile-policy fingerprints were
  unchanged. All preview values remain non-release evidence.
- Relative links across eight created/materially updated entry documents and
  `git diff --check` passed.

## 2026-08-05 - Slice 4 approval and commit boundary

- User approved Slice 4 and authorized continuation.
- Committed Slice 4 as `a5777a7dd5d028b76b6822e0bedb75d39607848b`
  (`Embed exact SPC runtime provenance`).
- Began only the approved Slice 5 packaged deterministic QA work.

## 2026-08-05 - Slice 5 harness and clean-environment defect

- Added an installed-wheel qualification harness independent of repository test
  helpers and designed to run beside copied AGF boundary fixtures.
- Created a fresh Python 3.12 environment and installed the repository with its
  development dependencies for source-suite qualification.
- First full suite run: 156 passed and one failed. The failure was an obsolete
  test allowance that deliberately excluded `semantic-runtime-smoke` from
  installed editable metadata. The fresh environment correctly installed it.
- Removed the allowance so release compatibility now requires exact equality
  with installed command metadata.
- Corrected full suite: 157 passed in 94.60 seconds. Focused Ruff passed.

## 2026-08-05 - Slice 5 installed candidate QA

- Built `semantic_projection_core-0.10.0-py3-none-any.whl` and installed it into
  a new environment outside the checkout.
- Copied the standalone harness and two compact AGF boundary fixtures outside
  the checkout, cleared `PYTHONPATH`, and confirmed the module resolved from
  the clean environment's `site-packages`.
- Six static cases passed canonical-byte repetition and schema validation:
  Orthodox, cognitive demonstration, Woofmapping general, handler,
  direct-to-dog, and hybrid.
- All four Woofmapping contexts preserved identical source topology, resolved
  every projected-term reference, and merged without registry conflicts.
- A repeated full Woofmapping handler temporal route produced identical
  artifacts and receipts and passed native validation.
- Negative QA rejected unsupported source/profile versions, an unavailable
  context version, a physically removed installed context resource, a
  conflicting projected-term definition, and malformed output.
- All six installed console scripts passed safe invocation. All three declared
  profile entry points resolved from installed distribution metadata.
- Candidate wheel: 129379 bytes at
  `0c4b64932a1a5b717b108e1637ecde9222ddd017f31c4fd9647ff6adc3715bf2`.
  Installed runtime package set:
  `a3408e8032d6a65d74716ba5e1e2fd7baa7c47aebfdbe7b196e9c3b17cd4ae48`.
  Semantic resource set:
  `2262689d70b38e3319a7f19a6431462a863acbb68bc8f1da31550c0a9fc72773`.
- Wrote `results/deterministic-fixture-summary.json` and
  `results/SLICE 5 - Packaged Deterministic QA.md`.
- Slice 5 gate passed. Changes remain uncommitted pending review; Slice 6 has
  not begun.

## 2026-08-05 - Slice 5 approval and commit boundary

- User approved Slice 5 and authorized continuation.
- Committed Slice 5 as `06a605b066fcb57eae7b205f563e994f851575e5`
  (`Qualify deterministic installed SPC runtime`).
- Began only the approved Slice 6 controlled downstream compatibility work.

## 2026-08-05 - Slice 6 installed candidate preparation

- Confirmed clean AGF and SBE working trees at commits
  `259058db9861d867a6c747c31eb1297c6be2a023` and
  `06dcb3c81bf4c6f38540f92b4346d4675b0642b8` respectively.
- Built AGF 0.5.0 from a clean Git archive and SPC 0.10.0 from the approved
  Slice 5 commit. Selected the released SBE 0.1.0 wheel whose SHA-256 matches
  its exact-hash consumer requirement.
- The first combined install attempted AGF's optional live dependency. PyPI
  exposed `pyswisseph` source but no compatible CPython 3.12 binary, and the
  host lacked MSVC 14 or newer. No candidate incompatibility was implicated.
- Installed the three wheel artifacts without AGF's optional live extra and
  installed SPC's declared `jsonschema` dependency. All three distributions
  resolved from the isolated environment's `site-packages`.
- Ella's params and prior projected artifacts were available, but her original
  canonical AGF package was not. Declined to infer or reconstruct it from
  downstream artifacts. Switched to the slice's permitted replay route using
  AGF's current checked-in full natal fixture.

## 2026-08-05 - Slice 6 cross-repository compatibility result

- Added a standalone installed-artifact harness that copies no code from AGF
  or SBE and imports SPC only from `site-packages`.
- Replayed the AGF 1.3.0 `natal:kevin` fixture containing 189 objects and 4,239
  relationships through all four Woofmapping natal contexts twice.
- Every context was deterministic and schema-valid with 17 projected objects,
  75 relationships, 47 closed projected-term definitions, identical source
  topology, and reconciled embedded runtime/policy identities.
- Invoked installed `astrowoof-build-natal-basis` using the preferred
  `astrowoof.projected_natal_input.v0.1` manifest. SBE exited 0 with batch and
  subject status `pass`, retained all 47 term keys, and selected 50 claims from
  108 candidates including 13 syntheses.
- Repeated installed SBE extraction into a separate output tree; the selected
  authoring packet was byte-identical at
  `495ae4894e1275e661f7e653de55bf51af1efba48627af2356b554874214e28c`.
- Compared the packet with SBE's checked-in Kevin reference: selection
  statistics and registry term keys were unchanged; 40 of 50 canonical claim
  wordings matched. Ten changed with current AGF canonical relationship
  identities. Exact golden identity is not a compatibility requirement.
- Exact wheel hashes: AGF
  `d1dad0b36a4529ff2c161f0a7de9696525fcf30a313b12bdcc4713e1d71c00f5`;
  SPC `127a4ccbc589d738d526f6e0be848a0e304845d297131ff482062e8bbafd6a62`;
  SBE `58f8d93066cce040ebfc07bc89ffb11254895f0768965aa305296a722aa39dfe`.
- Full SPC suite passed all 157 tests in 95.11 seconds. Focused Ruff passed.
- Wrote `results/cross-repository-compatibility.json` and
  `results/SLICE 6 - Controlled Downstream Compatibility Candidate.md`.
- Slice 6 gate passed. Changes remain uncommitted pending review; Slice 7 has
  not begun.

## 2026-08-05 - Slice 6 approval and commit boundary

- User approved Slice 6 and authorized continuation.
- Committed Slice 6 as `caa4e3c5243b226d914b8c36ca5dcbeaeb885232`
  (`Prove installed AGF SPC SBE compatibility`).
- Began the approved local/reproducibility portion of Slice 7. Retained the
  separate explicit boundary against tag, push, GitHub release, or upload.

## 2026-08-05 - Slice 7 reproducible build

- Fixed `SOURCE_DATE_EPOCH` to qualified commit time `1785958444` and pinned
  CPython 3.12.13, build 1.5.0, setuptools 80.9.0, and wheel 0.45.1.
- Built two independent clean Git archives with PEP 517 isolation disabled so
  the pinned build backend remained authoritative.
- Both outputs were byte-identical 130243-byte wheels at
  `60bd0f18d3b183d2f4c6375447f90881ab6c22c6138b8f9b8ffe69a246015150`.
- A third identical build populated the ignored local `dist/` publication
  asset. A fourth identical build was installed directly into the protected
  smoke environment to work around Windows ACL inheritance on generated files.

## 2026-08-05 - Slice 7 final exact-wheel QA

- Found that clean Git archive line-ending normalization changes exact packaged
  JSON resource hashes relative to working-checkout candidate builds. Parsed
  semantic content and canonical context content hashes were unchanged.
- Treated the change as provenance-significant: discarded earlier resource
  hashes as final identities and reran all installed QA against the exact
  archive-built wheel.
- Final installed identities: runtime package 101 records at
  `209be10ee879312293d7955f76dc7d9c0ade2dcb4e3a2fead11d424483f80611`;
  semantic resources 44 records at
  `74ba2450c20e4b8c636ba2ffcb0a8b6db8ae3e0964f552cfdfbf78bde1145afd`;
  schemas 21 records at
  `559ca31adc4e718b247defc90044ecb0cb5ca113d76ddc5581fe3955449e6963`.
- Final installed smoke passed six commands, three profile entry points, 13
  contexts, exact version alignment, and non-editable installation.
- Final installed deterministic QA passed all six static cases, four
  Woofmapping contexts, temporal projection, registry checks, and six negative
  cases without checkout imports.
- Rebuilt and installed AGF 0.5.0 beside the exact final SPC wheel and pinned
  SBE 0.1.0. The AGF-to-SPC-to-SBE boundary passed; SBE selected 50 claims and
  returned status `pass` with packet SHA-256
  `ad664768088644cdd8f584e587c4e16308d2aed2d865433a348686ce808f417f`.

## 2026-08-05 - Slice 7 local release handoff

- Added release-specific checksum, external manifest, exact-hash requirement,
  compatibility guide, consumer integration guide, and release notes under
  `releases/0.10.0/`.
- Updated the general consumer handoff with the final qualified hash and real
  future private-release URL while marking that URL inactive until publication.
- Wrote `results/reproducible-build-verification.json`,
  `results/final-installed-smoke.json`, and
  `results/SLICE 7 - Reproducibility and Publication Candidate.md`.
- Local release gate passed. Tag creation, push, GitHub release, asset upload,
  private-path download verification, publication evidence, and project-level
  released-baseline update remain pending explicit approval.
- Removed approximately 180.8 MB of disposable Slice 7 environments and build
  trees. Windows ACLs prevented removal of the two reproducibility-proof wheel
  copies (260,486 bytes total) under the external temporary staging directory;
  no cache, environment, expanded fixture, or other large temporary artifact
  remains. The authoritative candidate wheel remains under the repository's
  ignored `dist/` directory.

## 2026-08-05 - Slice 7 publication

- Committed the qualified release package as
  `68f11c56ff1ad26873958cf955b7f3699895e870` and pushed `main`.
- Created and pushed annotated tag `semantic-projection-core-v0.10.0`; remote
  tag object `3cbdb620e24d52b4fb1dfb65903c2149cac80280` dereferences to the intended
  release commit. GitHub reports the annotated tag as unsigned.
- Published private GitHub release `365787784` at
  `https://github.com/kevin2357/semantic-projection-core/releases/tag/semantic-projection-core-v0.10.0`.
- Uploaded wheel asset `503035345`, checksum asset `503035349`, and external
  manifest asset `503035357`.
- Downloaded all three assets through GitHub's authenticated release-asset API.
  Each downloaded asset matched its qualified local SHA-256; the checksum file
  also named the exact wheel hash and filename.
- GitHub's optional release-object `immutable` flag is false. Consumer
  immutability is enforced by the non-moving annotated tag and mandatory exact
  wheel SHA-256 pin; no claim of signed-tag or platform-enforced release
  immutability is made.
- Reconciled `astrowoof-project` release-strategy documentation with the
  published SPC 0.10.0 baseline. API target-image installation remains a
  downstream integration gate, not an SPC publication guarantee.

## 2026-08-05 - End-of-day documentation retrospective

- Re-read the full sprint chronology, all slice results, current guides,
  reference documents, integration handoffs, release files, roadmap, and test
  documentation against the published release state.
- Corrected stale consumer instructions that still described the private
  release URL as inactive, the runtime identity manifest as future Slice 7
  work, and full JSON Schema validation as a development-only capability.
- Marked the sprint plan completed and reconciled the Slice 7 result with the
  actual tag, upload, authenticated download verification, publication-evidence
  commit, and project-level documentation update.
- Promoted three durable decisions into SPC's first ADR set: executable semantic
  policy participates in release identity; full schema validation is invariant
  runtime behavior; and immutable qualification evidence remains separate from
  post-publication receipts.
- Added a compact retrospective preserving the archive line-ending discovery,
  unavailable Ella source boundary, unsigned/non-platform-immutable release
  limitation, unexpectedly direct packaging path, and remaining AGF/API work.
- Updated the roadmap with production consumer migration, target-image smoke,
  reproducible-build automation, and optional future signing/platform
  immutability work. No new SPC feature or downstream product behavior was
  inferred.

## 2026-08-05 - SPC and AstroWoof project authority reconciliation

- Re-read the project control plane's SPC integration architecture, projected
  graph consumer contract, release strategy, milestone, vocabulary, lifecycle,
  and open questions against the published SPC 0.10.0 contract and runtime
  identity implementation.
- Corrected project text that still treated formal four-context natal support
  as unresolved; the exact general, handler, direct-to-dog, and hybrid
  ID/version pairs are packaged release compatibility facts.
- Corrected project text that said SPC emitted no whole-profile configuration
  hash. Native artifacts now carry the bundled profile's executable
  `policy_resource_set` fingerprint along with runtime, semantic-resource,
  schema, and context identities.
- Reframed the remaining project question as placement of existing SPC
  identities in AstroWoof-owned run/delivery schemas, not invention of a
  competing hash.
- Adopted one authoritative project decision into SPC's consumer guidance:
  AstroWoof currently selects `full` as its conservative initial SBE input even
  though SPC supports all row-bearing materializations.
- Found no project decision that required changing SPC projection semantics,
  profile configuration, release compatibility, or ownership boundaries.
