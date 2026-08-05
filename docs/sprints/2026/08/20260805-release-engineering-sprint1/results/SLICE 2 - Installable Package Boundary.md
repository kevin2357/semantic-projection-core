# Slice 2 - Installable Package Boundary

```yaml
status: complete
gate: passed_pending_review
qualification_date: 2026-08-05
candidate_distribution: semantic-projection-core
candidate_version: 0.10.0
```

## Status

Gate passed on 2026-08-05. The changes remain uncommitted pending review.

This is qualification evidence for Slice 2, not the final release artifact.
Later slices may change the wheel and therefore its SHA-256.

## Defects corrected

1. The 13 versioned contexts are now package resources under
   `semantic_projection.contexts`; the `examples/contexts` copies are explicitly
   non-authoritative compatibility and inspection copies.
2. `jsonschema>=4,<5` is a required runtime dependency. Contract validation no
   longer becomes shallow when an optional dependency is absent.
3. Distribution and engine versions now derive from one authoritative
   `semantic_projection._version.__version__` value. Setuptools reads that same
   value for distribution metadata.
4. The installed runtime exposes deterministic semantic-resource inventory and
   exact context resolution APIs.
5. A new `semantic-runtime-smoke` command verifies installed distribution,
   version alignment, contexts, profile entry points, console entry points, and
   the semantic-resource fingerprint. `--require-installed` rejects editable
   installations.

## Candidate built and inspected

| Property | Result |
|---|---|
| Wheel | `semantic_projection_core-0.10.0-py3-none-any.whl` |
| Slice 2 SHA-256 | `264dd80c29cc9b3ceacf42dd7c472979d18b0ceec6185893693066f5c2340d98` |
| Size | 123,402 bytes |
| Archive members | 98 |
| Packaged contexts | 13 JSON files |
| Packaged schemas | 19 JSON files |
| Packaged profile resources | 9 JSON files |
| Runtime dependency installed | `jsonschema` 4.26.0 |

The wheel was built with PEP 517 build isolation and installed into a new
CPython 3.12.13 virtual environment outside the repository. `PYTHONPATH` was
cleared for the installed command proof. Import inspection resolved
`semantic_projection` from the fresh environment's `site-packages`, not the
checkout.

## Installed semantic resources

The installed runtime reported 41 semantic-policy resources:

- 13 contexts;
- 9 profile manifests, ontologies, and projected-term registries;
- 19 JSON Schemas.

Their deterministic aggregate fingerprint was:

`4ddcbc98bda8af59563a37ab73608b08d4991d4b0d81d00a4b732f2260187912`

The hash is derived from sorted installed resource paths and their content
hashes, not filesystem timestamps or repository locations. Unit coverage proves
that repeated inventory is stable and a changed resource record changes the
aggregate fingerprint. Slice 4 will connect this identity to output provenance
and add the release-level manifest contract.

## Installed entry points and meaningful routes

Fresh distribution metadata discovered all three profile entry points:

- `orthodox_astrology`;
- `cognitive_architecture_demo`;
- `woofmapped_astrology`.

Every previously supported console command was executed through a meaningful
safe route from outside the checkout:

| Command | Installed route exercised | Result |
|---|---|---|
| `semantic-project` | static orthodox request to summary artifact | Passed |
| `semantic-temporal-intake` | AGF bundle to cognitive temporal request | Passed |
| `semantic-temporal-foundations` | temporal request to foundations | Passed |
| `semantic-temporal-project` | temporal request to summary artifact | Passed |
| `semantic-temporal-run` | AGF bundle through full route plus receipt | Passed |
| `semantic-runtime-smoke` | non-editable runtime/resource inspection | Passed |

The generated route receipt identified
`temporal_projection_route_receipt`; foundations identified
`projected_temporal_foundations`; static and temporal artifacts both reported
summary materialization.

## Verification

- Full source suite: 146 passed.
- Focused Ruff check of all changed Python and test files: passed.
- All packaged contexts validated against `projection_context_v1.schema.json`.
- Packaged contexts and repository examples were compared as parsed JSON.
- Exact nonexistent context-version resolution failed closed in unit coverage.
- Editable-install rejection passed in unit coverage.
- Wheel archive inspection confirmed contexts, schemas, profile resources,
  runtime smoke module, and distribution entry-point metadata.
- Compact machine-readable evidence is in `installed-smoke.json`.

## Gate assessment and remaining work

Slice 2 gate is satisfied: an isolated installed environment can use the
intended runtime without checkout access, resources are installed and
fingerprintable, and repository examples are clearly non-authoritative.

The following are intentionally deferred:

- supported-contract/public-boundary freeze and consumer handoff (Slice 3);
- artifact provenance carrying runtime resource identity (Slice 4);
- exhaustive profile/context determinism and negative-path QA (Slice 5);
- real AGF to SPC to SBE candidate compatibility (Slice 6);
- reproducible double build, final checksums, tag, and publication (Slice 7).
