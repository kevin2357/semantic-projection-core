# Slice 8 — Installed Runtime and Cross-Repository Acceptance

## Outcome

The SPC 0.11.0 candidate is a real installable bounded-projection runtime. A
non-editable wheel installed outside the checkout discovers the bounded profile,
resolves packaged policy resources, exposes a dedicated command, consumes the
qualified AGF boundary fixture, and emits a valid structurally parallel
four-context set.

The AGF → SPC boundary passes. SBE's current four-file loader and registry merge
also pass, but SBE's candidate-building semantics remain exact-chart-specific.
This slice therefore records a precise downstream handoff instead of weakening
the bounded contract or inventing an end-to-end success.

## Candidate identity

| Item | Identity |
| --- | --- |
| Distribution / engine | `semantic-projection-core` 0.11.0 |
| Wheel | `semantic_projection_core-0.11.0-py3-none-any.whl` |
| Wheel SHA-256 | `b28786325e3a37ea511f2e1f265d14f98ec0ecc963ff725fadf7a1e9f52cc44a` |
| Wheel bytes | 161,185 |
| Profile | `woofmapped_bounded_astrology.v0@0.1.0` |
| Output | `projected_bounded_semantic_graph.v1` |
| Command | `semantic-bounded-project` |
| Runtime-package SHA-256 | `961b83ee6fda0ca9a275ae0bac7caea82a1ace2b276eaa67666ef5a284e4d72c` |
| Semantic-resource SHA-256 | `b901049d4c1bcf322ede511497af06bb4b0874a8c4bc64105c4e384895fa1e02` |

This is a qualification candidate, not a published release asset. Slice 9 owns
the final reproducible build and release handoff.

## Installed proof

The candidate wheel was installed into a fresh Python 3.12.13 virtual
environment under temporary storage. `semantic_projection.__file__` resolved
under that environment's `Lib/site-packages`; the installation was non-editable.

Installed smoke verified:

- distribution, package, engine, and compatibility version alignment at 0.11.0;
- four profile entry points, including the bounded profile;
- seven console commands, including `semantic-bounded-project`;
- 52 packaged semantic JSON resources;
- all bounded execution modules, source/output schemas, manifest, ontology, and
  projected-term registry present in the wheel;
- bounded profile policy resources fingerprinted as a five-resource bundled set;
- exact bundled context identity recorded in every output.

All seven commands passed `--help`. The bounded command projected all four
contexts meaningfully, and runtime smoke wrote a full release manifest.

## AGF boundary

The private AGF 0.8.0 release wheel was downloaded and matched the previously
qualified SHA-256 exactly:
`f236de0bb7c254c4421f571e816f2314251636ebbed9aa3cb9cb2a09925c04ae`.

AGF's installed saved-package doctor passed. Swiss Ephemeris was unavailable in
this Windows environment, so the test replayed SPC's checked-in bounded fixture,
whose source contract identities match the AGF 0.8.0 qualification boundary.
No claim of a fresh live calculation is made.

The four installed outputs passed `validate_parallel_bounded_contexts` with:

- 2 object correspondences;
- 1 relationship correspondence;
- epistemic SHA-256
  `50f10a88a660e76ec73f7ba09327ceb35cdffccb1453905927bb128dac40b9c1`;
- structural-semantic SHA-256
  `c8b78a607d9fe0131ef6ceb031aaaf6e1d624419c5a8a648de09d0b06ee85713`;
- no canonical context priority.

## SBE disposition

Installed `astrowoof-natal-authoring` 0.3.0 first accepted the four context files
through `load_and_validate_contexts` and merged their six used projected terms.
Candidate construction then failed deterministically because it performs
arithmetic on an object `projection_relevance_score` that is `null` in the
bounded contract.

That `null` is intentional: bounded object relevance was not established and
must not become zero, one, or an exact-chart fallback. SBE also currently looks
for `source_graph_ref`; bounded artifacts use `source_artifact_ref` because the
source is a versioned bounded package with evidence and capabilities beyond the
canonical subgraph.

The complete handoff is in
[`SBE Bounded Projection Acceptance Handoff.md`](SBE%20Bounded%20Projection%20Acceptance%20Handoff.md).

## Verification

- complete SPC suite: 228 passed in 69.89 seconds;
- focused bounded CLI/release contract: 6 passed;
- runtime/release/provenance tests: 17 passed;
- Ruff: passed;
- wheel contents and installed provenance: passed;
- installed AGF saved-package mode: passed;
- installed four-context bounded projection and cross-context validation: passed;
- SBE loader/registry boundary: passed;
- SBE candidate construction: explicit downstream blocker;
- compact evidence: [`installed-cross-repository-acceptance.json`](installed-cross-repository-acceptance.json).

## Gate disposition

Slice 8 is ready for review. Slice 9 documentation and release-candidate handoff
has not begun. No tag, release, downstream pin, or publication was performed.
