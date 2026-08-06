# Release consumer handoff

## Purpose

This handoff tells AGF, the AstroWoof runtime, and other production consumers
what to install, invoke, validate, preserve, and reject for SPC 0.10.0. It
summarizes the [release compatibility contract](../reference/release-compatibility.md)
without duplicating native schemas.

The final qualified wheel SHA-256 is
`60bd0f18d3b183d2f4c6375447f90881ab6c22c6138b8f9b8ffe69a246015150`.
The private release is published and its assets have been downloaded through
GitHub's authenticated asset API and verified against their qualified hashes:
`https://github.com/kevin2357/semantic-projection-core/releases/tag/semantic-projection-core-v0.10.0`.

## Install and verify

Production builds must obtain the private release wheel through an ephemeral,
least-privilege credential, verify its published SHA-256, and install that exact
file. Do not install `main`, use an editable checkout, or accept a permissive
version range.

A hash-checked requirements entry should use the final published asset, for
example:

```text
semantic-projection-core @ https://github.com/kevin2357/semantic-projection-core/releases/download/semantic-projection-core-v0.10.0/semantic_projection_core-0.10.0-py3-none-any.whl \
    --hash=sha256:60bd0f18d3b183d2f4c6375447f90881ab6c22c6138b8f9b8ffe69a246015150
```

After installation, run:

```powershell
semantic-runtime-smoke --require-installed --json
```

Reject the runtime unless:

- distribution, package, and engine versions are all 0.10.0;
- `editable` is false;
- all three bundled profile entry points resolve at their exact versions;
- the six supported console scripts are present;
- all 13 packaged contexts validate;
- the packaged release compatibility contract is present; and
- the semantic-resource fingerprint matches the final release manifest.

Generate and archive the installed runtime manifest with
`--release-manifest-out`. Verify both its complete runtime-package fingerprint
and its semantic-resource fingerprint against the published release evidence.

## AGF handoff

AGF produces the source; it must not delegate calculation or canonical graph
repair to SPC.

For static execution, supply the complete saved canonical graph 1.3.0,
structural evidence, source identity, and required source registries. Do not
submit an AGF analysis view or compact summary.

For temporal execution, supply
`temporal_projection_source_bundle` 1.0.0 containing
`canonical_temporal_activation_graph` 1.0.0 and a static target graph at 1.3.0.
SPC preserves timing facts but does not calculate them.

AGF currently declares `semantic-projection-core>=0.10.0` and imports some SPC
profile mapping internals. Those are development conveniences, not compliant
production release integration. Before AGF becomes the production orchestrator,
its build must pin the exact wheel hash and its integration must use SPC's public
request/runtime boundary rather than internal mapping modules.

## AstroWoof static natal handoff

For each saved AGF natal artifact, execute the exact
`woofmapped_astrology.v0` 0.1.0 profile once for each supported natal context:

- `woofmapped.doghouse.general.v0` 0.1.0;
- `woofmapped.handler_guidance.v1` 1.0.0;
- `woofmapped.dog_direct.v1` 1.0.0;
- `woofmapped.hybrid_horoscope.v1` 1.0.0.

SPC supports `standard`, `full`, or `forensic` materialization for SBE;
`summary` lacks the graph rows SBE needs. AstroWoof's current project-level
integration policy selects `full` as the conservative initial materialization
so every row and evidence surface remains available. That selection is a
downstream promotion policy, not a restriction of SPC's native compatibility.

Persist the normalized request and untouched native output for every context.
Before constructing the SBE input bundle, require compatible engine, profile,
target ontology, registry, source graph, and materialization identities. Join
parallel context rows through source and mapping evidence, never projected ID
or array position.

Merge used-term registries by stable term key only when registry identity and
version match and duplicate definitions are identical. A conflicting duplicate
is a hard integration error. Preserve all definitions required by retained rows
and derived claims.

The projection contexts are not finished AstroWoof audience modes. SBE and the
product own selection, synthesis, authoring, prose voice, cards, filters, and
delivery.

## What to archive

SPC artifacts now carry `semantic_projection.runtime_identity.v1`, including
installed runtime, semantic-resource, schema, profile-policy, context, route,
and output-contract identity. The orchestrator must verify that receipt against
the qualified runtime release manifest and additionally retain:

- final wheel SHA-256 and release tag;
- engine/distribution version;
- runtime-package and semantic-resource-set SHA-256 values;
- release compatibility contract ID;
- exact profile ID/version;
- exact context ID/version, canonical content hash, and packaged resource hash;
- target ontology and projected-term registry ID/version;
- materialization mode;
- AGF source contract identities and immutable source artifact hash;
- normalized projection request and request/source/context hashes;
- untouched projected artifact hash, coverage, diagnostics, and limitations;
- downstream SBE runtime/input identity.

The final wheel SHA-256 remains external to embedded provenance because an
installed package cannot reconstruct the original wheel bytes.

## Reject rather than guess

Reject:

- version, profile, context, ontology, registry, or resource fingerprint drift;
- an unknown native contract or materialization;
- a summary where row-bearing content is required;
- missing registry definitions or conflicting duplicates;
- missing source/mapping/context references needed for lineage;
- unsupported graph types even though the generic validator may not reject the
  graph-type string by itself;
- an artifact mutated in place while retaining an SPC package identity;
- a projected artifact presented as a finished reading.

Product-specific orchestration remains authoritative in the
[AstroWoof project integration documentation](https://github.com/kevin2357/astrowoof-project/blob/main/docs/architecture/Semantic%20Projection%20Integration.md).
