# Release compatibility contract

## Authority and scope

This page freezes the supported consumer boundary for
`semantic-projection-core` 0.10.0. The packaged
`semantic_projection.release/compatibility.json` file is its machine-readable
counterpart. JSON Schemas and implementation remain authoritative for field
validation and execution behavior.

This contract covers installed artifacts and public integration routes. It does
not make every importable module, helper, mapping constant, or repository tool a
stable Python API.

## Runtime identity

| Dimension | Supported value |
|---|---|
| Distribution | `semantic-projection-core` 0.10.0 |
| Python package | `semantic_projection` |
| Python requirement | 3.10 or newer |
| Engine version | 0.10.0 |
| Engine/profile contract | 1.0.0 |
| Required validation dependency | `jsonschema>=4,<5` |

Distribution metadata, `semantic_projection.__version__`, and
`ENGINE_VERSION` derive from one source. A consumer must reject disagreement.
The final release wheel must be pinned by its exact SHA-256; a version number
alone is not an immutable runtime identity.

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

## Supported outputs

| Route | Native output |
|---|---|
| Static | `projected_semantic_graph.v1` |
| Temporal projection | `projected_temporal_activation_graph` 1.0.0 |
| Temporal foundations | `projected_temporal_foundations` 0.1.0 |
| Temporal route receipt | `temporal_projection_route_receipt` 1.0.0 |

Supported materializations are `full`, `standard`, `summary`, and `forensic`.
Summary artifacts intentionally omit row-bearing graph content. They are not
valid inputs for consumers that require projected objects, relationships,
activations, evidence links, or complete used-term definitions.

Static v1 is identified by the schema/package name and required metadata; it
does not carry an independent numeric `contract_version` field. Consumers must
not invent one. Temporal outputs carry explicit 1.0.0 contract versions.

## Four supported Woofmapping natal contexts

SPC 0.10.0 formally supports the following contexts for static Woofmapped natal
projection:

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

## Supported installed commands

- `semantic-project`
- `semantic-temporal-intake`
- `semantic-temporal-foundations`
- `semantic-temporal-project`
- `semantic-temporal-run`
- `semantic-runtime-smoke`

Their documented option names, required inputs, output modes, successful exit
code 0, and validation/error exit code 2 are supported for 0.10.0. `--debug`
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
- schema-invalid inputs or outputs;
- missing projected-term definitions and conflicting registry entries when a
  downstream merger validates them.

Coverage exclusions and unmapped eligible rows are represented in artifacts;
they are not automatically fatal unless the request's coverage policy or the
consumer's promotion policy makes them so.

## Explicitly unsupported in 0.10.0

- temporal synastry without a future AGF temporal-synastry source contract;
- raw transit reports or prose as projection input;
- reconstructed canonical graphs made from AGF summaries;
- reader-facing claims, advice, prose, card organization, or product delivery;
- treating summary materialization as a row-bearing artifact;
- mutable branch installation or a permissive production requirement;
- internal Python module paths as a stable public API;
- filenames, array positions, or labels as cross-context identity.

See the [release consumer handoff](../integration/release-consumer-handoff.md)
for installation, validation, and preservation requirements.
