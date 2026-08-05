# Slice 4 - Provenance and Release Identity

```yaml
status: complete
gate: passed_pending_review
qualification_date: 2026-08-05
candidate_distribution: semantic-projection-core
candidate_version: 0.10.0
```

## Outcome

Generated artifacts can now be traced to the installed SPC code and semantic
policy bundle that produced them. The release manifest identifies the complete
installed boundary; each artifact embeds a compact route/profile/context-specific
receipt.

Changes remain uncommitted pending review. Slice 5 has not begun.

## Identity model

### Semantic resource set

The existing JSON resource inventory now includes contexts, profile manifests,
ontologies, projected-term registries, release contracts, and all schemas. This
set answers which declarative semantic resources were installed.

### Runtime package set

The new runtime inventory covers every installed SPC Python and JSON file plus
distribution `METADATA`, `WHEEL`, and `entry_points.txt`. It therefore includes:

- engine and materialization behavior;
- source-selection policy;
- object and relationship mappings implemented in Python;
- profile JSON resources and registries;
- contexts, schemas, and release compatibility;
- installed dependency and command metadata.

This distinction corrects the inadequate assumption that profile JSON alone
could fingerprint executable semantic policy.

### Profile and context identity

Each bundled profile receives a policy-set fingerprint covering its Python and
JSON package subtree. Each context records:

- exact ID and version;
- SHA-256 of canonical parsed content;
- whether the submitted content exactly equals a bundled resource;
- packaged resource path and byte hash when bundled.

A modified context reusing a bundled ID/version is correctly marked unbundled
rather than inheriting the packaged resource identity. A third-party profile is
similarly marked unbundled because SPC cannot fingerprint another distribution's
code; that plugin requires its own release manifest.

## Full release manifest

`runtime_release_manifest()` and
`semantic-runtime-smoke --release-manifest-out` produce
`semantic_projection.runtime_release_manifest.v1`, validated by the packaged
`runtime_release_manifest_v1.schema.json`.

The full manifest records distribution identity, release compatibility,
complete runtime and semantic inventories, schemas, all bundled profile policy
sets, and all bundled contexts.

The source-checkout preview fingerprint is retained only as Slice 4 evidence.
It is explicitly not the final release identity. Slice 7 must generate the final
manifest from the reproducibly built and installed release wheel.

An installed distribution cannot reconstruct the byte hash of its original
wheel. Wheel SHA-256 remains a separate external release identity paired with
the installed manifest.

## Embedded artifact provenance

`semantic_projection.runtime_identity.v1` is now present in:

- static graph metadata;
- every static materialization, including summary;
- the separate static forensic audit;
- temporal foundations metadata;
- temporal graph metadata and provenance;
- every temporal materialization; and
- temporal route receipts.

The receipt includes distribution/package version, release compatibility hash,
runtime/semantic/schema fingerprints, exact profile identity and policy hash,
exact context identity/hashes, route, and output contract.

The compact receipt validates through `runtime_identity_v1.schema.json` wherever
it is required by a native artifact schema.

## Defect corrected during qualification

Slice 3's compatibility resource and documentation incorrectly described
`projected_temporal_foundations` as contract 1.0.0. Implementation and schema
both use 0.1.0. Slice 4 corrected the release contract and documentation to
0.1.0 and added a consistency assertion so the mistake cannot silently return.

## Change-sensitivity proof

Regression coverage proves:

- repeated inventories are stable;
- changing a semantic resource record changes the semantic aggregate;
- changing executable Woofmapping object-mapping code changes the complete
  runtime fingerprint;
- that same mapping change changes the Woofmapping profile-policy fingerprint;
- altered context content cannot claim the bundled resource path/hash; and
- route-specific receipts share one runtime basis while retaining distinct
  route/output identities.

## Verification

- Final full source suite: 157 passed in 91.63 seconds.
- Focused temporal/provenance suite after fixture correction: 19 passed.
- Focused Ruff: passed.
- Runtime release manifest schema validation: passed.
- All 21 packaged schemas parsed; generated artifacts validate through their
  native schemas in the full suite.
- Compact evidence:
  `results/provenance-identity-verification.json`.

The first full run produced six failures because the standalone temporal
contract-skeleton test fixture lacked the newly required identity. Actual static
and temporal execution tests passed. The fixture was updated to carry a valid
real runtime identity; the corrected full run passed all 157 tests. That run
took 132.53 seconds because each projection re-read the entire installed
resource set. Process-lifetime caching appropriate to an immutable installation
reduced the final run to 91.63 seconds, consistent with the pre-provenance suite.

## Gate assessment

Slice 4 gate is satisfied. A projected artifact identifies its exact installed
runtime/resource/profile/context basis, and changing executable or declarative
semantic policy changes the corresponding fingerprint. Final installed-wheel
values remain deferred to later packaged QA and release construction.
