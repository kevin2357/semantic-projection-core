# Release consumer handoff

## Purpose

This handoff tells AGF, the AstroWoof runtime, and other production consumers
what to install, invoke, validate, preserve, and reject for SPC 0.11.1. It
summarizes the [release compatibility contract](../reference/release-compatibility.md)
without duplicating native schemas.

The release is published at
`https://github.com/kevin2357/semantic-projection-core/releases/tag/semantic-projection-core-v0.11.1`.
The authenticated wheel download matches the qualified SHA-256, and the remote
annotated tag dereferences to the qualified release commit.

## Install and verify

Production builds must obtain the private release wheel through an ephemeral,
least-privilege credential, verify its published SHA-256, and install that exact
file. Do not install `main`, use an editable checkout, or accept a permissive
version range.

A hash-checked requirements entry should use the final published asset, for
example:

```text
semantic-projection-core @ https://github.com/kevin2357/semantic-projection-core/releases/download/semantic-projection-core-v0.11.1/semantic_projection_core-0.11.1-py3-none-any.whl \
    --hash=sha256:dc345cd3253de333a5428e4fc7e24816447a065215ef288ba76527960a7da612
```

After installation, run:

```powershell
semantic-runtime-smoke --require-installed --json
```

Reject the runtime unless:

- distribution, package, and engine versions are all 0.11.1;
- `editable` is false;
- all four bundled profile entry points resolve at their exact versions;
- the seven supported console scripts are present;
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

For bounded natal execution, supply the complete AGF
`bounded_natal_dataset` package. Select
`woofmapped_bounded_astrology.v0@0.1.0` and invoke
`semantic-bounded-project` once per exact context ID/version. Do not route the
bounded graph through `semantic-project`, choose a representative instant, or
replace unavailable facts with exact-chart defaults.

SPC 0.11.1 qualifies against AGF 0.8.1. Its bounded wire identities remain
dataset 1.0.0, graph 1.7.0, evidence 1.0.0, calculation profile 1.12.0, and
interval-proof profile 1.0.0. The exact AGF 0.8.1 wheel SHA-256 is
`860c48793318c82c986b32664cd0f3fe97c4b1e02fb1e489561bc395c8b5a3ed`.
SPC's installed-candidate qualification replays that boundary through all four
bounded contexts.

AGF is runtime-decoupled from SPC: it declares no SPC package dependency and
imports no SPC runtime modules. The production orchestrator must install and pin
both immutable wheels independently, retain both runtime receipts, and pass the
complete AGF artifact across SPC's public request/runtime boundary.

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

## AstroWoof bounded natal handoff

The bounded four-context family is structurally parallel and epistemically
invariant. Verify it with `validate_parallel_bounded_contexts()`, join rows by
`correspondence_id`, and preserve `source_artifact_ref`, source identity,
capabilities, feature dispositions, limitations, evidence closure,
evidence-family identity, registry definitions, and runtime provenance.

Current SBE releases implement a dedicated bounded admission, compilation,
authoring, authority-hydration, QA, and lifecycle route. This downstream support
does not relax SPC's boundary: do not invent relevance scores, alias
`source_artifact_ref` into an exact-only field, or flatten bounded evidence into
the exact contract.

SPC 0.11.1 removes Mean Node and its dependent family before delivery. A 0.11.0
bounded family may contain both Mean and True Node mapped to the same target
primitive even though its profile receipt declares a True Node preference.
Regenerate those projections with 0.11.1; do not ask SBE to guess which projected
claim SPC intended to retain.

## What to archive

SPC artifacts now carry `semantic_projection.runtime_identity.v1`, including
installed runtime, semantic-resource, schema, profile-policy, context, route,
and output-contract identity. The orchestrator must verify that receipt against
the qualified runtime release manifest and additionally retain:

- final wheel SHA-256 and release tag;
- the exact AGF distribution version, wheel SHA-256, and runtime receipt used
  to generate the source artifact;
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
The same boundary applies upstream: projected JSON proves its source artifact
and declared wire contracts, not which AGF wheel produced those bytes.

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
