# Semantic Projection Core Release Engineering Sprint 1

```yaml
status: active
owner: semantic-projection-core
scope: release qualification and publication
started: 2026-08-05
candidate_distribution: semantic-projection-core
candidate_version: 0.10.0
```

## 1. Sprint outcome

Qualify the current Semantic Projection Core runtime as an installable,
reproducible, immutable Python wheel; prove its installed static and temporal
behavior across the AGF-to-SPC-to-SBE boundary; and, only after explicit
approval, publish an annotated component-scoped tag and GitHub release whose
assets are pinned by SHA-256.

The release identity must cover executable semantic policy as well as Python
code: schemas, profiles, contexts, manifests, source-selection policy, mapping
rules, ontologies, projected-term registries, deterministic behavior, supported
routes, source contracts, and console entry points.

## 2. Candidate release names and version assumptions

Initial candidate, subject to Slice 1 audit:

- distribution: `semantic-projection-core`
- import package: `semantic_projection`
- distribution/engine candidate version: `0.10.0`
- wheel: `semantic_projection_core-0.10.0-py3-none-any.whl`
- annotated tag: `semantic-projection-core-v0.10.0`
- GitHub release title: `Semantic Projection Core v0.10.0`

The existing `v0.1.0` tag is immutable historical state and will not be moved,
overwritten, or reused. A version or tag change requires an explicit audit
finding and approval.

## 3. Explicit slice sequence

### Slice 1 — Packaging and dependency audit

Inventory packaging, package data, version sources, resources, contracts,
profiles, contexts, public interfaces, entry points, QA, documentation, and Git
release history. Identify installed-wheel blockers and define the required
runtime resource manifest. Produce no implementation fixes.

### Slice 2 — Installable package boundary

Correct approved packaging/resource defects, add or stabilize installed-runtime
inspection/smoke behavior, build a wheel, install it outside the checkout, and
exercise every supported console command and profile discovery path.

### Slice 3 — Stable release and compatibility contracts

Freeze the supported consumer boundary for Python, AGF contracts, SPC contracts,
profiles, contexts, CLI routes, failure behavior, and intentionally unsupported
operations. Add AGF and AstroWoof API handoffs without promising internal module
layout as public API unintentionally.

### Slice 4 — Provenance and release identity

Create and expose a deterministic installed resource manifest and semantic
resource-set fingerprint. Ensure artifacts identify the runtime, contracts,
profile, context, route, and policy bundle sufficiently for release traceability.

### Slice 5 — Packaged deterministic QA

From a clean wheel-only environment, run deterministic static projection for all
bundled profiles, all four AstroWoof Woofmapping contexts, a supported temporal
route, registry checks, repeatability checks, negative compatibility tests, and
the appropriate full QA suite without checkout imports.

### Slice 6 — Controlled downstream compatibility candidate

Pin the candidate wheel locally by exact SHA-256 and prove the real
AGF-to-SPC-to-SBE boundary on a representative natal fixture, preferably Ella
when available and compatible. Record lineage, coverage, registry, deterministic
identity, and downstream acceptance evidence without reader-facing authorship.

### Slice 7 — Reproducibility, release handoff, and publication

Build twice under a fixed reproducibility control, prove byte identity, prepare
the final wheel/checksums/manifest/compatibility guide/handoff/release notes,
run final installed smoke, and stop for approval. Only after explicit approval:
create and push the annotated tag, publish assets, download through the real
release path, and verify remote tag and asset hashes.

Each slice ends at its gate for review. Later slices may be refined by an earlier
finding but may not silently waive an exit condition.

## 4. Controls and safety constraints

- Preserve pre-existing work and inspect repository state before every slice.
- Make no destructive Git changes and never move or overwrite an existing tag.
- Do not modify AGF, SBE, AstroWoof API, or project repositories unless separately
  requested; cross-repository checks are read-only.
- Keep credentials and sensitive paths out of code, wheels, manifests, logs,
  requirements, images, and sprint evidence.
- Use wheel-only environments outside the source tree for installed-boundary
  proof; ensure the checkout is absent from `sys.path` and resource resolution.
- Pin production consumption by exact wheel SHA-256, not branch state or a
  permissive version range.
- Prefer deterministic/local tests before cross-repository or live tests.
- Retain only compact evidence under `results/`; keep environments, build trees,
  caches, expanded fixtures, and downloaded assets in temporary storage.
- Run relevant tests and `git diff --check` before each proposed commit.
- Keep slice changes uncommitted for review; commit only after approval.
- Do not tag, push, create a release, upload assets, or download private release
  assets without explicit approval and least-privilege credentials.
- Treat a qualification defect as a successful finding that blocks the gate
  until fixed and rerun; never waive a failed gate implicitly.

## 5. Exit criteria

The sprint exits only when:

1. two controlled builds produce byte-identical wheels;
2. the wheel installs and runs outside the source tree;
3. every supported console entry point passes a meaningful installed smoke;
4. all required schemas, profiles, mappings, ontologies, registries, manifests,
   and supported contexts are packaged and fingerprinted;
5. distribution, engine, contract, profile, registry, and context versions are
   internally reconciled;
6. installed deterministic static projection passes for every bundled profile;
7. all four AstroWoof Woofmapping contexts pass;
8. at least one supported installed temporal route passes;
9. installed negative compatibility/version/resource/input tests pass;
10. the installed AGF-to-SPC boundary passes;
11. resulting projected artifacts pass the agreed SBE acceptance boundary;
12. release manifest, compatibility guide, consumer handoff, release notes, and
    checksums exist;
13. the annotated tag resolves to the exact qualified commit;
14. published assets verify after download against local recorded hashes;
15. large temporary artifacts are removed;
16. the release commit working tree is clean; and
17. cross-project documentation records the released baseline.

## 6. Deferred work and non-goals

- No new projection ontology, mappings, source graph families, or product
  semantics are added merely to produce a release.
- No broad refactor, lint cleanup, API redesign, or schema generation change is
  in scope unless qualification proves it is a release blocker.
- No PyPI publication is assumed; the initial private distribution target is a
  GitHub release unless a later approved decision changes it.
- No reader-facing AstroWoof prose generation is required for compatibility.
- No temporal synastry support is implied; unsupported routes remain explicit.
- No compatibility promise is made for private Python modules unless Slice 3
  intentionally promotes one.
- No existing release tag or historical artifact will be rewritten.

