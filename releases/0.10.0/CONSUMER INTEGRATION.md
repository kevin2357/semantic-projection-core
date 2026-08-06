# Semantic Projection Core 0.10.0 Consumer Integration

The private GitHub release asset is intended to be installed by exact URL and
hash. The release is published and the URL below is active for authenticated
consumers with access to the private repository:

```text
semantic-projection-core @ https://github.com/kevin2357/semantic-projection-core/releases/download/semantic-projection-core-v0.10.0/semantic_projection_core-0.10.0-py3-none-any.whl \
    --hash=sha256:60bd0f18d3b183d2f4c6375447f90881ab6c22c6138b8f9b8ffe69a246015150
```

After installation, run:

```powershell
semantic-runtime-smoke --require-installed --json --release-manifest-out installed-release-manifest.json
```

Require distribution, package, and engine version 0.10.0; a non-editable
install; all six commands; three exact profile entry points; 13 contexts; and
the runtime/resource hashes in `release-manifest.json`.

AGF must supply complete canonical graph 1.3.0 packages or supported temporal
bundles. AstroWoof must execute `woofmapped_astrology.v0@0.1.0` separately for
the four exact natal contexts, retain all native artifacts, merge artifact-term
registries only under strict identical-definition rules, and pass row-bearing
outputs to SBE. See the full
[release consumer handoff](../../docs/integration/release-consumer-handoff.md).
