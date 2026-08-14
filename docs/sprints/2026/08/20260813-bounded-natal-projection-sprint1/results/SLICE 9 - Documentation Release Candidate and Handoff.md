# Slice 9 - Documentation, release candidate, and handoff

## Outcome

Prepared the SPC 0.11.0 release candidate and a consumer-facing bounded natal
contract without tagging or publishing it. Existing exact static and temporal
routes remain supported and unchanged.

## Consumer boundary made durable

- AGF 0.8.0 source contract identities and the dedicated bounded route.
- `projected_bounded_semantic_graph.v1` and
  `woofmapped_bounded_astrology.v0@0.1.0`.
- Four exact context IDs/versions, correspondence behavior, and certainty
  invariance.
- Evidence, capability, limitation, family, registry, source-artifact, and
  runtime-provenance preservation requirements.
- Unsupported representative-chart, bounded temporal, and bounded synastry
  behavior.
- The honest SBE 0.3.0 disposition: shallow load/registry acceptance passes;
  candidate construction remains blocked on exact-chart authoring assumptions.

## Reproducible candidate

With `SOURCE_DATE_EPOCH=1786681793`, two builds using Python 3.12.13, pip
26.2.1, setuptools 83.0.0, and wheel 0.47.0 produced byte-identical wheels:

- file: `semantic_projection_core-0.11.0-py3-none-any.whl`
- bytes: 161334
- SHA-256:
  `82290df44fe5697e87df2e27eb0aa4bab3b7954c66ce988efda0962964e1366d`

The exact wheel installed non-editably outside the checkout. Installed smoke
confirmed four profile entry points, seven commands, 13 contexts, and aligned
distribution/package/engine 0.11.0. All seven commands passed `--help`.
The final source suite passed all 228 tests; changed/new JSON, relative
Markdown links, and whitespace validation also passed. Repository-wide Ruff
continues to expose 139 pre-existing findings outside this documentation-only
slice and is recorded as baseline debt rather than silently claimed as green.

Installed fingerprints:

- runtime package: 116 resources,
  `6088b1775a786071f9c55d77616a5cc4dbe1539b1987dbf19a4f885e02a94883`;
- semantic resources: 52 resources,
  `b901049d4c1bcf322ede511497af06bb4b0874a8c4bc64105c4e384895fa1e02`;
- schemas: 26 resources,
  `cf0466af1d04f4115c007edffb1a583058a829a56048ff24023620906c3839eb`.

## Gate disposition

Ready for review. The candidate remains untagged and unpublished. After this
slice is approved and committed, tag creation and GitHub publication remain a
separate explicit approval boundary.
