# Semantic Projection Core 0.10.0

SPC 0.10.0 is the first qualified immutable runtime release of the current
projection engine and bundled semantic policy set.

## Included

- deterministic static projection and four materialization modes;
- AGF temporal intake, projection, foundations, and route receipts;
- participant-aware synastry projection;
- exact-version bundled profile and context discovery;
- Orthodox 1.0.0, cognitive demonstration 0.2.0, and Woofmapping 0.1.0;
- all four AstroWoof Woofmapping natal contexts;
- artifact-scoped projected-term registries;
- embedded runtime, schema, profile-policy, context, route, and contract
  provenance; and
- installed runtime smoke and release-manifest generation.

## Qualification

The wheel builds byte-identically from independent clean archives under a fixed
epoch and pinned build toolchain. The exact release candidate passed 157 source
tests, six installed static cases, all four Woofmapping contexts, a temporal
route, six negative cases, every installed command and profile entry point, and
the AGF-to-SPC-to-SBE boundary.

The final wheel is 130,243 bytes at SHA-256
`60bd0f18d3b183d2f4c6375447f90881ab6c22c6138b8f9b8ffe69a246015150`.

## Consumer action

Production consumers must replace mutable branches or permissive version ranges
with the exact-hash requirement in `requirements-production.txt`, run the
installed smoke, and preserve the release and artifact provenance described in
`CONSUMER INTEGRATION.md`.

Published from annotated tag `semantic-projection-core-v0.10.0`, targeting
release commit `68f11c56ff1ad26873958cf955b7f3699895e870`. All release assets were
downloaded through GitHub's authenticated asset API and matched against their
qualified local hashes.
