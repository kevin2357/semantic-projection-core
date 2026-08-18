# Runtime and release identity

## Two nested resource identities

SPC 0.11.1 distinguishes two installed identities:

1. **Semantic resource set**: every packaged JSON context, profile manifest,
   ontology, projected-term registry, release contract, and JSON Schema.
2. **Runtime package set**: every installed SPC Python and JSON file plus the
   distribution's `METADATA`, `WHEEL`, and `entry_points.txt` content.

The semantic set answers which declarative policy resources were installed.
The runtime set additionally covers the engine, executable mapping and
source-selection rules, resource loaders, validation behavior, and installed
entry points. Mapping behavior cannot be identified truthfully from profile
JSON alone because current bundled profiles implement part of their policy in
Python.

Each set is sorted by package-relative path. Every record carries its byte size
and SHA-256. The aggregate SHA-256 hashes each path, a NUL separator, its content
SHA-256, and a line-feed separator. Filesystem location, modification time, and
repository-relative paths do not participate.

Inventories are cached for the process lifetime after first inspection. This is
safe for an immutable installed release and avoids re-reading every mapping and
registry for each projection. An editable process that changes package files in
place must restart before its identity can be trusted; editable installations
are never release-qualified.

Changing a covered file changes the relevant record and aggregate fingerprint.
Formatting changes to a packaged policy file therefore change exact release
identity even when parsed semantics happen to remain equal.

## Full runtime release manifest

`runtime_release_manifest()` returns
`semantic_projection.runtime_release_manifest.v1`. It contains:

- installed distribution and package versions;
- release compatibility contract identity and content hash;
- complete runtime-package and semantic-resource inventories;
- the schema-only resource set;
- each bundled profile's executable policy resource set; and
- every bundled context's exact identity and hashes.

Generate an installed manifest with:

```powershell
semantic-runtime-smoke `
  --require-installed `
  --json `
  --release-manifest-out release-manifest.json
```

The manifest validates against
`runtime_release_manifest_v1.schema.json`. Each release pairs the installed
manifest with the external wheel SHA-256 recorded in its release manifest and
checksums. Published 0.10.0 and 0.11.0 identities remain immutable; the 0.11.1
release corrects bounded source selection without changing bounded wire or
profile identity.
See [ADR-0001](../decisions/ADR-0001%20-%20Include%20Executable%20Semantic%20Policy%20in%20Release%20Identity.md)
for the identity boundary.

The published external manifest is the qualification-time snapshot. Remote
release IDs and authenticated download verification live in separate
publication evidence so the uploaded manifest never changes after hashing; see
[ADR-0003](../decisions/ADR-0003%20-%20Separate%20Qualification%20Evidence%20from%20Publication%20Receipts.md).

An installed Python package cannot recover the byte hash of the original wheel
after extraction. The wheel SHA-256 therefore remains an external release and
orchestration identity. It must accompany, not be confused with, the installed
runtime-package fingerprint.

## Artifact runtime identity

Every generated static graph, bounded graph, temporal foundations artifact,
temporal graph, and temporal route receipt carries a compact
`semantic_projection.runtime_identity.v1`. It identifies:

- distribution, package, and engine-aligned release basis;
- release compatibility contract and its packaged hash;
- runtime-package, semantic-resource, and schema-set fingerprints;
- exact profile ID/version and its executable policy fingerprint;
- exact context ID/version, canonical content hash, and packaged resource hash
  when bundled;
- execution route; and
- output contract.

Static artifacts place the receipt in `metadata.runtime_identity`. Temporal
graphs place the same receipt in metadata and provenance; route receipts repeat
it. Temporal foundations place it in metadata. All static and temporal
materialization modes preserve it, as does the separate static forensic audit.

For an unbundled context, the canonical context content hash remains available
but packaged resource path/hash are null. For a third-party profile, SPC records
the exact profile ID/version but marks the bundled policy set false and cannot
claim a hash for another distribution's code. A release using a third-party
profile must pin and manifest that plugin separately.

## What downstream systems must still record

The embedded identity does not replace:

- final wheel SHA-256 and release tag;
- source and output artifact SHA-256 values;
- exact projection request and options;
- AGF runtime, calculation, source contract, and source artifact identity;
- downstream SBE/API/runtime identity; or
- consumer promotion policy and diagnostics decisions.

It does remove ambiguity about which installed SPC code and bundled semantic
policy produced the projected artifact.
