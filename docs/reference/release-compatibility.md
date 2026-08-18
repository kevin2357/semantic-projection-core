# Release compatibility contract

## Authority and scope

This page freezes the supported consumer boundary for
`semantic-projection-core` 0.11.1. The packaged
`semantic_projection.release/compatibility.json` file is its machine-readable
counterpart. JSON Schemas and implementation remain authoritative for field
validation and execution behavior.

This contract covers installed artifacts and public integration routes. It does
not make every importable module, helper, mapping constant, or repository tool a
stable Python API.

## Runtime identity

| Dimension | Supported value |
|---|---|
| Distribution | `semantic-projection-core` 0.11.1 |
| Python package | `semantic_projection` |
| Python requirement | 3.10 or newer |
| Engine version | 0.11.1 |
| Engine/profile contract | 1.0.0 |
| Required validation dependency | `jsonschema>=4,<5` |

Distribution metadata, `semantic_projection.__version__`, and
`ENGINE_VERSION` derive from one source. A consumer must reject disagreement.
The release tag is `semantic-projection-core-v0.11.1`. Its published
wheel SHA-256 is
`dc345cd3253de333a5428e4fc7e24816447a065215ef288ba76527960a7da612`.
The annotated remote tag and authenticated asset download have been verified.
Production consumers must pin that exact hash. The
immutable 0.10.0 and 0.11.0 releases remain available at their existing tags and
hashes.

Generated artifacts also carry the installed runtime and resource fingerprints
described in [Runtime and release identity](runtime-and-release-identity.md).

## Supported source boundaries

### Static

`ProjectionRequest` accepts canonical static graph version 1.3.0. Other graph
versions fail validation.

Each profile manifest declares the graph types within its qualified mapping
scope:

| Profile | Version | Declared static graph types |
|---|---:|---|
| `orthodox_astrology.v1` | 1.0.0 | natal, synastry, composite, Davison, solar return, lunar return |
| `cognitive_architecture_demo.v0` | 0.2.0 | natal |
| `woofmapped_astrology.v0` | 0.1.0 | natal, synastry |

Important enforcement distinction: SPC rejects unsupported graph *versions*.
The generic static validator does not currently reject solely because a
`graph_type` string falls outside the selected manifest's declarations.
Manifest graph types are therefore the release's qualified support scope, not
permission to assume every other graph type will be rejected before mapping.
Consumers must submit only a declared type and validate coverage and
diagnostics. Treating an undeclared type as supported is outside this contract.

### Temporal

The supported AGF boundary is exactly:

- `temporal_projection_source_bundle` contract 1.0.0;
- embedded `canonical_temporal_activation_graph` contract 1.0.0;
- normalized `temporal_projection_request.v1`;
- a static target graph at canonical graph version 1.3.0.

SPC rejects unsupported bundle, temporal graph, request, and static graph
versions. The supported temporal route is a saved AGF bundle through intake and
directional projection. Raw transit prose, an analysis summary, or a temporal
graph passed to the static command is not supported.

### Bounded natal

The dedicated bounded route was introduced against AGF 0.8.0. SPC 0.11.1 is
qualified against preferred compatible patch AGF 0.8.1 and accepts this bounded
wire boundary:

- `bounded_natal_dataset` package schema 1.0.0;
- `bounded_canonical_astrology_graph` version 1.7.0;
- `agf.bounded_uncertainty_evidence.v1.0.0`;
- calculation profile `agf.bounded_natal.calculation_profile.v1.12.0`; and
- interval-proof profile `agf.interval_proof.v1.0.0`.

It produces `projected_bounded_semantic_graph.v1` through
`woofmapped_bounded_astrology.v0@0.1.0`. The route preserves invariant facts,
capability dispositions, limitations, proof evidence, family identity, and
source lineage. It never selects a representative instant or supplies missing
degrees, houses, scores, probabilities, or confidence.

AGF 0.8.1 repairs bounded-evidence validation while retaining the package,
graph, evidence, calculation-profile, and interval-proof identities above. SPC
0.11.1 directly qualifies that patch without changing bounded contract identity.

### Bounded source-selection correction

SPC 0.11.1 enforces the bounded profile's existing True Node preference. It
excludes Mean Node, all derived objects owned by Mean Node, and relationships
touching that excluded family before projection identity, evidence closure,
registry materialization, or relevance allocation. Missing True Node does not
promote Mean Node. AGF's single bounded calculated point named `Fortune` remains
eligible; it is not the exact graph's duplicate legacy Fortune alias.

Bounded artifacts produced by SPC 0.11.0 can therefore contain both node
variants despite declaring the True Node selection policy. Consumers requiring
the corrected semantic basis should regenerate from the immutable AGF source
with SPC 0.11.1 rather than deduplicate projected rows downstream.

Distribution provenance is external to the projected JSON. The artifact embeds
the upstream wire-contract identities and source-artifact hash, but not the AGF
distribution version or wheel hash. A production orchestrator must retain the
AGF runtime receipt and exact wheel SHA-256; consumers must not infer them from
the projected artifact alone.

## Supported outputs

| Route | Native output |
|---|---|
| Static | `projected_semantic_graph.v1` |
| Temporal projection | `projected_temporal_activation_graph` 1.0.0 |
| Temporal foundations | `projected_temporal_foundations` 0.1.0 |
| Temporal route receipt | `temporal_projection_route_receipt` 1.0.0 |
| Bounded natal | `projected_bounded_semantic_graph.v1` |

Supported materializations are `full`, `standard`, `summary`, and `forensic`.
Summary artifacts intentionally omit row-bearing graph content. They are not
valid inputs for consumers that require projected objects, relationships,
activations, evidence links, or complete used-term definitions.

Static v1 is identified by the schema/package name and required metadata; it
does not carry an independent numeric `contract_version` field. Consumers must
not invent one. Temporal outputs carry explicit 1.0.0 contract versions.

## Four supported Woofmapping natal contexts

SPC 0.11.1 formally supports the following contexts for both exact static and
bounded Woofmapped natal projection:

| Context ID | Version | Project shorthand |
|---|---:|---|
| `woofmapped.doghouse.general.v0` | 0.1.0 | general |
| `woofmapped.handler_guidance.v1` | 1.0.0 | handler |
| `woofmapped.dog_direct.v1` | 1.0.0 | direct-to-dog |
| `woofmapped.hybrid_horoscope.v1` | 1.0.0 | hybrid |

This freezes current projection acceptance and structural qualification. It
does not redefine the temporal-sounding context labels as product audience
behavior, prose voices, card sections, or advice. All four retain their declared
projection-layer parameters and constraints. No context has canonical priority.

Consumers must resolve the exact ID/version and preserve the installed context
content hash from the semantic-resource manifest. Friendly filenames and
project shorthand are not release identities.

The four bounded outputs share source epistemic, capability, limitation,
evidence-family, and structural-semantic identity. Context may vary only its
declared target framing and relevance. Rows correspond by `correspondence_id`,
not output ID or array position; no context is canonical.

## Supported installed commands

- `semantic-project`
- `semantic-temporal-intake`
- `semantic-temporal-foundations`
- `semantic-temporal-project`
- `semantic-temporal-run`
- `semantic-runtime-smoke`
- `semantic-bounded-project`

Their documented option names, required inputs, output modes, successful exit
code 0, and validation/error exit code 2 are supported for 0.11.1. `--debug`
may expose implementation tracebacks and is not a machine-readable error
contract. Standard error text is diagnostic and should not be parsed as a
stable schema.

Files under repository `tools/` and `scripts/` are source-checkout conveniences,
not installed release commands. Their module layout and helper imports are not
public compatibility promises.

## Supported Python integration boundary

The preferred high-level imports are:

- `ProjectionRequest` plus `project_with_builtin_profiles()` for static
  projection;
- `project_foundry_temporal_bundle()` for the complete temporal route;
- `project_synastry()` for participant-aware static synastry;
- `project_bounded_natal()` and `validate_parallel_bounded_contexts()` for the
  bounded route and its four-context family;
- `load_bundled_context()` for exact context resolution;
- `semantic_resource_manifest()` and `release_compatibility()` for runtime
  identity and compatibility inspection;
- public contract dataclasses exported from `semantic_projection` when callers
  must construct a native request.

Third-party profiles use the `semantic_projection.profiles` entry-point group
and exact `(profile_id, profile_version)` resolution. The bundled installed
commands execute bundled profiles; they are not a promise that every command
will discover arbitrary third-party profiles. Custom-profile consumers should
construct a registry explicitly through the Python API.

Imports from profile mapping modules, private helpers, or repository tools are
unsupported. In particular, downstream code must not import SPC's object or
relationship mapping tables as an integration shortcut.

## Failure and compatibility behavior

Consumers must expect a hard failure for:

- unknown or mismatched profile versions;
- exact bundled-context resolution at an unknown version;
- a context target ontology that differs from the profile target ontology;
- an unsupported canonical graph, temporal bundle, temporal graph, or temporal
  request version;
- an unsupported bounded package, graph, evidence, calculation-profile, or
  interval-proof version;
- schema-invalid inputs or outputs;
- missing projected-term definitions and conflicting registry entries when a
  downstream merger validates them.

Coverage exclusions and unmapped eligible rows are represented in artifacts;
they are not automatically fatal unless the request's coverage policy or the
consumer's promotion policy makes them so.

## Explicitly unsupported in 0.11.1

- temporal synastry without a future AGF temporal-synastry source contract;
- raw transit reports or prose as projection input;
- reconstructed canonical graphs made from AGF summaries;
- reader-facing claims, advice, prose, card organization, or product delivery;
- treating summary materialization as a row-bearing artifact;
- mutable branch installation or a permissive production requirement;
- internal Python module paths as a stable public API;
- filenames, array positions, or labels as cross-context identity.
- bounded temporal combinations or synastry involving a bounded natal graph;
- midpoint, most-likely, rectified, or representative-chart inference;
- treating bounded `null` relevance or unavailable capability as permission to
  apply an exact-chart default; and
- treating projected source aliases as a downstream deduplication responsibility.

See the [release consumer handoff](../integration/release-consumer-handoff.md)
for installation, validation, and preservation requirements.
