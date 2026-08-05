# Slice 1 — Packaging and Dependency Audit

```yaml
status: complete
gate: blocked_pending_approved_later_slice_fixes
audit_date: 2026-08-05
audited_head: fa0f2ce1956927644e83e35735366a620ece1089
candidate_distribution: semantic-projection-core
candidate_version: 0.10.0
```

## Executive finding

The repository is healthy enough to continue release engineering, but current
HEAD is not yet an immutable release candidate. Source-tree QA is strong
(`139 passed`, 89.01% branch-aware coverage), the asserted distribution and
engine versions align at 0.10.0, all current JSON resources parse, all 19 schemas
pass JSON Schema metaschema checks, all three profile entry points discover in
the editable environment, and bundled profile/registry versions mostly
reconcile.

Qualification nevertheless found release blockers in installed context
resources, environment-dependent validation, runtime/policy provenance, context
declarations, source-type enforcement, version-source duplication, ontology
identity, installed-wheel testing, and downstream API boundaries. These are
bounded hardening/contract defects; no finding requires a new projection feature
or ontology redesign.

Slice 1 made no runtime, packaging, schema, profile, mapping, or CLI changes.

## Candidate release identity

The proposed identity remains:

| Item | Proposed value |
|---|---|
| Distribution | `semantic-projection-core` |
| Import package | `semantic_projection` |
| Release version | `0.10.0` |
| Engine version | `0.10.0` |
| Wheel | `semantic_projection_core-0.10.0-py3-none-any.whl` |
| Annotated tag | `semantic-projection-core-v0.10.0` |
| Release title | `Semantic Projection Core v0.10.0` |
| Initial publication channel | Private GitHub release |

Rationale:

- distribution metadata and `ENGINE_VERSION` already agree on 0.10.0;
- AGF 0.5.0 declares SPC 0.10.0 as its current compatibility baseline;
- SBE's published natal-authoring 0.1.0 release records successful inputs from
  SPC 0.10.0;
- no local or remote Git tag exists for SPC 0.10.0;
- the only local and remote tag is the historical lightweight `v0.1.0` at
  `538b627e9769158455a85f0e000fa537b5bf7635`;
- the required fixes can preserve intended 0.10.0 semantics while making the
  package boundary and provenance truthful.

This proposal is conditional on qualification not discovering a required
meaning-changing mapping or contract break in later slices. The historical
`v0.1.0` tag must remain untouched. The GitHub release inventory was not
confirmed because GitHub CLI is unavailable in the environment; remote Git tags
were confirmed directly with `git ls-remote`.

## Current packaging boundary

### Declared distribution

`pyproject.toml` declares:

- setuptools build backend (`setuptools>=68`, `wheel`);
- Python `>=3.10`;
- no runtime dependencies;
- `src`-layout package discovery;
- package data `schemas/*.json` and `profiles/**/*.json`;
- five console scripts; and
- three `semantic_projection.profiles` entry points.

The editable audit environment reports distribution 0.10.0 and engine 0.10.0.
This is alignment evidence, not wheel evidence: the environment points back to
the source checkout.

### Expected current wheel content

Package discovery should include 48 Python files and package-data patterns
should include 19 schemas plus 9 profile JSON resources. This exact wheel
content remains unproved until Slice 2 builds and inspects the wheel.

The 13 versioned context JSON files are under `examples/contexts`, outside the
discovered package and package-data declarations. Repository convenience tools
and tests resolve them from the checkout. They therefore cannot currently be
treated as installed runtime resources.

Repository `tools/`, `scripts/`, `examples/`, tests, and large tracked/ignored
fixtures are not Python packages under the current `src` discovery rule. That is
appropriate unless a route explicitly depends on one of them; the current
Woofmapping context defaults do depend on `examples`, which is not appropriate
for an installed runtime.

### Proposed semantic resource-set boundary

The release resource manifest should enumerate and hash installed paths, bytes,
and SHA-256 values for:

1. all installed `semantic_projection/**/*.py` engine and profile code;
2. all packaged JSON Schemas;
3. every profile manifest, ontology, and projected-term registry;
4. every supported packaged projection context;
5. installed console and profile entry-point declarations; and
6. distribution and engine identity.

Mapping tables, source-selection policy, temporal scope exclusions, and context
behavior currently live in Python, so a JSON-only fingerprint would be false
assurance. The wheel SHA-256 remains the identity of the complete immutable
artifact; the semantic resource-set fingerprint is a diagnostic/provenance
identity within that wheel.

The source-audit candidate currently spans 89 files and 496,708 bytes. Its
aggregate is not a release hash because context locations and runtime contents
must change before qualification. See `runtime-package-manifest.json`.

## Public and executable interface inventory

### Installed console scripts

The editable distribution exposes the five asserted commands:

- `semantic-project` → `semantic_projection.cli:main`
- `semantic-temporal-intake` → `semantic_projection.temporal_cli:main`
- `semantic-temporal-foundations` →
  `semantic_projection.temporal_foundations_cli:main`
- `semantic-temporal-project` →
  `semantic_projection.temporal_projection_cli:main`
- `semantic-temporal-run` → `semantic_projection.temporal_pipeline_cli:main`

Current tests exercise module functions and module `--help` from the source
checkout. They do not launch installed wrapper executables from a wheel-only
environment. `semantic-temporal-foundations` also retains Stage C language and a
0.1.0 intermediate contract; Slice 3 must classify it explicitly as supported
intermediate/diagnostic compatibility or remove it from the promised boundary.

### Profile entry points

Actual editable-distribution discovery returned all three profiles:

| Entry point | Profile ID | Version |
|---|---|---:|
| `orthodox_astrology` | `orthodox_astrology.v1` | 1.0.0 |
| `cognitive_architecture_demo` | `cognitive_architecture_demo.v0` | 0.2.0 |
| `woofmapped_astrology` | `woofmapped_astrology.v0` | 0.1.0 |

The existing discovery test mocks Python metadata rather than proving entry
points from a built wheel. Slice 2 must test real installed metadata.

### Python API

`semantic_projection.__all__` currently contains 71 names. Current tests assert
only a small subset of supported routes. Slice 3 must intentionally freeze a
narrow public boundary rather than accidentally promise every exported contract,
ID helper, rendering helper, intermediate temporal type, and implementation
detail forever.

AGF currently imports intended top-level APIs but also imports:

- `semantic_projection.engine.ProjectionExecutionError`;
- `semantic_projection.validation.ProjectionValidationError`;
- `semantic_projection.registry.ProjectionProfileRegistryError`;
- `semantic_projection.profiles.builtin_projection_registry`; and
- Orthodox `object_mappings` constants/helpers directly.

AGF also declares `semantic-projection-core>=0.10.0`. That is acceptable as a
development compatibility range but not an immutable production pin. Slice 3
must decide whether a narrow adapter surface is intentionally public or whether
AGF should stop depending on profile internals before its production pin is
qualified. No AGF change is authorized in this sprint.

## Version and contract inventory

### Aligned identities

- distribution: 0.10.0
- engine: 0.10.0
- static canonical graph input: 1.3.0 only
- temporal source bundle: `temporal_projection_source_bundle` 1.0.0
- canonical temporal graph: `canonical_temporal_activation_graph` 1.0.0
- temporal request: `temporal_projection_request.v1`
- projected temporal graph: `projected_temporal_activation_graph` 1.0.0
- temporal route receipt: 1.0.0
- profile engine contract: 1.0.0 for all three profiles

### Identity defects or ambiguity

1. Distribution version and `ENGINE_VERSION` are separate hard-coded sources
   with no alignment regression test. They can drift.
2. Static projected artifacts identify package type, engine, profile, context,
   and source hash but emit no explicit static output `contract_version`.
3. Static/temporal artifacts and route receipts do not identify distribution
   version, wheel hash, release tag/commit, or semantic resource-set fingerprint.
4. Temporal route receipts omit engine/resource identity even though they are
   intended to support routing provenance.
5. The Orthodox ontology JSON omits `profile_version`; the other two ontologies
   include it. No ontology schema validates this identity.
6. Profile manifests declare supported source graph types, but the engine never
   compares the request graph family to that declaration.
7. Static `ProjectionRequest.context` is only typed as an object in its JSON
   Schema; it does not reference `projection_context_v1`, unlike the temporal
   request contract.

## Profile and context inventory

All three manifests pass `projection_profile_manifest_v1`; all three term
registries pass schema and specialized validation. Registry counts are:

- Orthodox: 68 terms, registry 1.0.0;
- Cognitive: 56 terms, registry 0.2.0;
- Woofmapping: 56 terms, registry 0.1.0.

All 13 context files pass `projection_context_v1` when full JSON Schema
validation is available.

Context declaration is not yet release-stable:

- `woofmapped.doghouse.general.v0`, required by the AstroWoof four-context
  authoring boundary, is absent from the Woofmapping manifest's
  `supported_context_ids`;
- the asymmetric dog-dog context identity is also absent from that declaration;
- Orthodox `orthodox.general.v1`, used for natal examples/tests, is absent from
  its manifest's supported-context list;
- Cognitive has no supported-context ID declaration;
- context lists are metadata only and are not enforced by profile resolution;
- Woofmapping currently accepts non-general Doghouse contexts with a warning;
  and
- the handler/direct/hybrid contexts carry temporal/horoscope intent while
  AstroWoof currently applies them to natal projection.

Slice 3 must distinguish supported static, temporal, and synastry contexts and
define exact-version failure behavior. This is contract formalization, not
permission to invent new context semantics.

## Validation dependency finding

The no-runtime-dependency claim is behaviorally unsafe. `validate_contract()`
uses full Draft 2020-12 validation only when `jsonschema` is importable. Without
it, validation falls back to checking only top-level required fields.

This was demonstrated using two Python 3.12.13 environments:

- without `jsonschema`, a context containing a schema-forbidden extra property
  was accepted;
- with `jsonschema` 4.26.0, the same context was rejected with
  `ProjectionValidationError`.

Thus an identical SPC wheel has different contract enforcement depending on an
undeclared ambient package. Immutable release behavior cannot depend on this.
Slice 2 must either make the full validator a declared runtime dependency and
pin its resolved runtime set in deployment, or replace the fallback with an
equally deterministic internal validator. Quietly retaining the current split
is not acceptable.

## Determinism and provenance finding

Current strengths:

- canonical JSON and stable hashes drive IDs;
- source rows, projected rows, mapping executions, registries, indexes, and
  temporal rows are deterministically sorted;
- static audit records request/source/context hashes;
- forensic materialization records component hashes;
- temporal summaries and route receipts record semantic/route hashes; and
- Hypothesis tests exercise stable ID/hash properties.

Release gap:

These identities establish deterministic semantic inputs but not the exact code
and policy bundle. Two wheels with the same `ENGINE_VERSION` and profile version
could contain changed Python mappings or resources and still emit metadata that
looks equivalent. Slice 4 must add installed runtime/resource identity and
regression tests proving that a semantic resource change changes the fingerprint.

## QA and release-infrastructure finding

### Passed source-tree checks

- 139 tests passed on CPython 3.12.13 / Windows.
- Branch-aware coverage: 89.01%, above the enforced 85% floor.
- All 41 audited package/context JSON files parsed.
- All 19 schemas passed Draft 2020-12 metaschema checking.
- All manifests, registries, and contexts passed their available validators.
- `pip check` passed in the editable dev environment.
- `compileall` passed for `src`.
- Actual editable profile entry-point discovery returned exactly three profiles.

### Non-blocking source quality debt

Ruff reports 82 findings under `src` (primarily unused/unsorted imports). Two
`RUF012` findings identify mutable class-level source-selection dictionaries;
they are not currently mutated, but should be made intentionally immutable or
annotated during bounded release hardening. Broad repository lint cleanup is not
a release slice by itself.

### Missing release infrastructure

- no installed-runtime smoke command;
- no runtime/resource manifest API;
- no wheel-only QA harness;
- no release manifest, compatibility handoff, checksums, or release notes;
- no reproducible-build script/control;
- unbounded build requirements (`setuptools>=68`, `wheel`);
- no GitHub workflow or local publication automation; and
- no demonstrated wheel content, install, or reproducibility.

The build toolchain must be pinned exactly for the reproducibility proof. A
fixed `SOURCE_DATE_EPOCH` alone is insufficient evidence if setuptools/wheel can
change between builds.

## Release blockers and slice assignment

| ID | Blocker | Assigned slice |
|---|---|---|
| B1 | Versioned contexts are checkout resources, not installed package resources | 2 |
| B2 | Validation changes with undeclared ambient `jsonschema` availability | 2 |
| B3 | No real wheel-content, fresh-install, wrapper-CLI, or entry-point proof | 2 |
| B4 | No installed runtime smoke/resource inspection entry point | 2 |
| B5 | Distribution and engine versions are duplicated without an alignment guard | 2/4 |
| B6 | Supported context declarations are incomplete and unenforced | 3 |
| B7 | Manifest source graph types are unenforced | 3 |
| B8 | Public Python/CLI/intermediate temporal boundaries are not intentionally frozen | 3 |
| B9 | AGF relies on a permissive range and SPC profile internals | 3/6 |
| B10 | Orthodox ontology lacks version identity and ontologies lack validation contract | 3/4 |
| B11 | Static output lacks explicit contract version identity | 3/4 |
| B12 | Artifacts/receipts lack exact runtime and semantic resource-set identity | 4 |
| B13 | Packaged deterministic/negative QA does not exist outside the checkout | 5 |
| B14 | AGF-to-SPC-to-SBE wheel-only compatibility is unproved | 6 |
| B15 | Reproducible build, checksums, release assets, and publication verification are absent | 7 |

## Refined later-slice plan

### Slice 2 refinement

- Move/copy supported contexts into an installed resource namespace and expose
  lookup by exact context ID/version; repository paths become compatibility
  inputs, not authority.
- Resolve deterministic full validation before advertising runtime dependencies.
- Establish one authoritative distribution/engine version source or an enforced
  equality check.
- Add an installed runtime inspection/smoke command that reports distribution,
  engine, entry points, profiles, contexts, schemas, and provisional resource
  identity.
- Build and inspect the wheel in temporary storage, install without the checkout,
  clear `PYTHONPATH`, change working directory away from the repository, and
  prove every wrapper executable plus real profile discovery.

### Slice 3 refinement

- Define a small supported top-level Python API and classify each CLI as public,
  compatibility/intermediate, or unsupported.
- Reconcile static graph-family identity with AGF's actual canonical graph shape
  before enforcing manifest declarations.
- Declare contexts by route and exact version; explicitly include the four
  AstroWoof natal contexts only if current intended support is confirmed.
- Add ontology identity validation and explicit static output contract identity.
- Record AGF's current internal imports as a compatibility decision requiring
  AGF-owner review, not an automatic SPC promise.

### Slice 4 refinement

- Fingerprint installed semantic Python policy as well as JSON resources.
- Include the resource-set ID in static/temporal artifacts, forensic outputs,
  and route receipts without using a repository-relative path as provenance.
- Keep wheel SHA-256 and source/tag commit in the external release manifest;
  do not pretend an executing artifact can know its containing wheel hash unless
  the deployment supplies verified release identity.

### Slice 5 refinement

- Use a copied compact fixture/harness outside the checkout; assert the checkout
  is absent from `sys.path`, imported module paths, resource paths, and entry
  point metadata.
- Exercise installed wrapper executables, not only `python -m` or direct `main()`.
- Add all-four-context static equivalence/correspondence checks, registry subset
  checks, repeat serialization checks, and validation behavior without ambient
  optional packages.

### Slice 6 refinement

- Use locally built/installed AGF and SPC artifacts with hashes recorded; no
  editable install may participate.
- Use SBE's released `astrowoof.projected_natal_input.v0.1` acceptance and
  registry merge behavior as the downstream gate.
- Limit Ella proof to deterministic projection and SBE ingestion/basis boundary;
  no LLM prose run is required.

### Slice 7 refinement

- Pin exact Python/build frontend/setuptools/wheel versions in the reproducible
  builder and record them.
- Design tag/build/publication ordering so the annotated tag resolves to the
  exact qualified source commit while publication evidence can be committed
  afterward without moving the tag.
- Treat release-download verification as a separate explicit approval boundary
  using ephemeral least-privilege credentials.

## Slice 1 gate decision

The packaging/resource inventory is complete enough to proceed. The proposed
version/tag scheme is justified. Release blockers and later-slice assignments
are explicit.

**Gate result:** Slice 1 complete; current release candidate blocked. Await
approval before beginning Slice 2.

