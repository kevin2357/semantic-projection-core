# Slice 7 - Reproducibility and Publication Candidate

## Result

Status: **local release gate passed; publication awaiting approval**

The final SPC 0.10.0 wheel is byte-reproducible, installable outside the
checkout, fully smoke-tested, and prepared with checksums, release manifest,
compatibility guidance, consumer instructions, and release notes. No tag,
push, GitHub release, upload, or private-release download has occurred.

Evidence:

- [reproducible-build-verification.json](reproducible-build-verification.json)
- [final-installed-smoke.json](final-installed-smoke.json)
- [release package](../../../../../../releases/0.10.0/RELEASE%20NOTES.md)

## Reproducible build

Two separate clean Git archives of qualified commit
`caa4e3c5243b226d914b8c36ca5dcbeaeb885232` were built with:

- `SOURCE_DATE_EPOCH=1785958444`;
- CPython 3.12.13;
- `build==1.5.0`;
- `setuptools==80.9.0`;
- `wheel==0.45.1`; and
- PEP 517 build isolation disabled so the pinned backend was authoritative.

Both wheels were 130,243 bytes and byte-identical at SHA-256
`60bd0f18d3b183d2f4c6375447f90881ab6c22c6138b8f9b8ffe69a246015150`.
A third same-control build written to the ignored `dist/` asset location and a
fourth build used for protected-environment installation produced the same
hash.

## Archive normalization finding

The clean Git archive applies the repository's line-ending normalization to
packaged JSON resources. Parsed JSON semantics, profile/context versions, and
canonical content hashes are unchanged, but exact packaged resource hashes
differ from the earlier working-checkout candidate wheels.

This is not semantic drift. It is nevertheless provenance drift, so the final
archive-built wheel received a complete installed QA rerun and a fresh
AGF-to-SPC-to-SBE recheck. Release evidence and consumer pins use only the
final archive-built identities:

- runtime package set:
  `209be10ee879312293d7955f76dc7d9c0ade2dcb4e3a2fead11d424483f80611`;
- semantic resource set:
  `74ba2450c20e4b8c636ba2ffcb0a8b6db8ae3e0964f552cfdfbf78bde1145afd`;
- schema set:
  `559ca31adc4e718b247defc90044ecb0cb5ca113d76ddc5581fe3955449e6963`.

## Final installed verification

The exact reproducible wheel installed into a fresh environment with no source
checkout on `PYTHONPATH`. `semantic-runtime-smoke --require-installed` passed
with version alignment, six commands, three profile entry points, 13 contexts,
101 runtime records, 44 semantic resources, and 21 schemas.

The complete installed QA harness then passed six deterministic static cases,
all four Woofmapping natal contexts, registry closure and strict conflict
handling, a deterministic temporal route, and all six negative cases.

Because the archive normalization changed exact provenance hashes, the final
wheel was also installed alongside AGF 0.5.0 and SBE 0.1.0. The current AGF
natal boundary projected through four contexts and SBE accepted the resulting
50-claim basis with status `pass`. Thus the exact publication candidate—not
only the earlier semantic understudy—has downstream evidence.

## Release handoff files

`releases/0.10.0/` now contains:

- `SHA256SUMS.txt`;
- `release-manifest.json`;
- `requirements-production.txt`;
- `COMPATIBILITY.md`;
- `CONSUMER INTEGRATION.md`; and
- `RELEASE NOTES.md`.

The exact final wheel remains locally in ignored
`dist/semantic_projection_core-0.10.0-py3-none-any.whl` for the approved upload
step. It is not committed as a repository blob.

## Remaining publication gate

After explicit approval, the remaining state-changing operations are:

1. commit this release handoff;
2. create annotated tag `semantic-projection-core-v0.10.0` at that release
   commit and verify its local dereference;
3. push the release commit and immutable tag;
4. create the private GitHub release and upload the wheel, `SHA256SUMS.txt`, and
   `release-manifest.json`;
5. download all assets through the real private-release path using ephemeral
   least-privilege authentication;
6. verify downloaded hashes and remote tag dereference;
7. write `publication-verification.json`, update publication status and
   project-level released-baseline documentation, then commit those records;
8. clean retained publication artifacts and confirm every changed working tree
   is clean.

The GitHub CLI was absent during the Slice 1 audit. Publication may use a
least-privilege GitHub API flow or an available authenticated browser session,
but credentials must never enter command output, repository files, or evidence.
