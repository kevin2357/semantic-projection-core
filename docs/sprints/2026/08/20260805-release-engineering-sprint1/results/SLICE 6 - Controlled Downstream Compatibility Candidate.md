# Slice 6 - Controlled Downstream Compatibility Candidate

## Result

Status: **gate passed**

An exact locally hashed SPC 0.10.0 wheel passed the installed
AGF-to-SPC-to-SBE boundary. All three distributions resolved from one isolated
Python 3.12 environment's `site-packages`; no editable checkout was imported.

Compact machine-readable evidence is in
[cross-repository-compatibility.json](cross-repository-compatibility.json).

## Installed candidate set

| Distribution | Version | Wheel SHA-256 |
|---|---:|---|
| Astrology Graph Foundry | 0.5.0 | `d1dad0b36a4529ff2c161f0a7de9696525fcf30a313b12bdcc4713e1d71c00f5` |
| Semantic Projection Core | 0.10.0 | `127a4ccbc589d738d526f6e0be848a0e304845d297131ff482062e8bbafd6a62` |
| AstroWoof natal authoring | 0.1.0 | `58f8d93066cce040ebfc07bc89ffb11254895f0768965aa305296a722aa39dfe` |

The AGF wheel was built from a clean archive of commit
`259058db9861d867a6c747c31eb1297c6be2a023`. The SPC wheel was built from
approved Slice 5 commit `06a605b066fcb57eae7b205f563e994f851575e5`.
The SBE wheel is its published local release artifact and matches its recorded
release requirement hash.

The SPC hash is a Slice 6 candidate hash, not yet the final release hash.
Uncontrolled wheel ZIP timestamps make it differ from the functionally
identical Slice 5 build. Slice 7 owns the fixed-epoch byte-reproducibility proof
and final checksum.

## AGF boundary

The run replayed AGF's current checked-in full natal QA artifact:
`tests/fixtures/qa_inputs/natal.full.json`. It is a live-Swiss-Ephemeris-origin
canonical package for `natal:kevin`, graph version 1.3.0, with 189 canonical
objects and 4,239 relationships. Its SHA-256 is
`b95a3534b1bf39252c9ccbb57ce1f2ab7ac596a5af0452c873e4ac051e03a968`.

Replay is explicitly allowed by the Slice 6 gate. The artifact was copied
outside AGF before execution, and the installed AGF distribution remained in
the environment to prove dependency compatibility.

## SPC projection result

The standalone `scripts/qualify_downstream_candidate.py` harness projected the
canonical package twice through each supported AstroWoof natal context:

- general `woofmapped.doghouse.general.v0@0.1.0`;
- direct-to-dog `woofmapped.dog_direct.v1@1.0.0`;
- handler `woofmapped.handler_guidance.v1@1.0.0`; and
- hybrid `woofmapped.hybrid_horoscope.v1@1.0.0`.

Each repeated projection was canonically byte-identical and passed the native
static output schema. Every artifact contained 17 objects, 75 relationships,
and an artifact-scoped registry of 47 projected terms with complete reference
closure. All four shared the same source identity, source graph reference, and
source topology while retaining context-specific artifact identities.

Embedded identity reconciled across all four artifacts:

- installed runtime package set:
  `a3408e8032d6a65d74716ba5e1e2fd7baa7c47aebfdbe7b196e9c3b17cd4ae48`;
- semantic resource set:
  `2262689d70b38e3319a7f19a6431462a863acbb68bc8f1da31550c0a9fc72773`;
- schema set:
  `051c3e2814c7ac4bb75e15bfd7361049b6d267374059b393c51d8c3e7ab72c84`;
- Woofmapping policy set:
  `f0afe9a704bb434393008cb316a25ce9d0f8340c9c357cdcd33675badcef288a`.

## SBE acceptance

The harness wrote the four projections plus params under the preferred
`astrowoof.projected_natal_input.v0.1` manifest. It then invoked the installed
`astrowoof-build-natal-basis` command with no source-tree imports.

SBE exited 0 with batch and subject status `pass`. It merged all 47 projected
terms, considered 108 candidates, selected 50 claims including 13 syntheses,
and emitted a 1,545,069-byte selected authoring packet at SHA-256
`495ae4894e1275e661f7e653de55bf51af1efba48627af2356b554874214e28c`.
An independent second extraction produced the identical packet SHA-256.
This establishes downstream structural and semantic-basis acceptability; it
does not claim SPC authored the selected syntheses or any reader-facing prose.

## Accepted-baseline comparison

Compared with SBE's checked-in Kevin reference packet, the new packet retained
identical selection statistics and the same 47 projected-term keys. Forty of
50 canonical selected claim wordings were identical. Ten changed alongside
the current AGF fixture's different canonical relationship identities.

This is an understood compatibility difference, not a gate failure: SBE's
contract accepts semantic inputs and produces a deterministic bounded basis; it
does not require exact identity with a historical golden packet generated from
different upstream source identities.

## Ella and live-generation limitation

Ella was considered first, as requested. Her params and prior projected
artifacts are available, but her original canonical AGF package is not. It
would be invalid to reverse-engineer a canonical source graph from downstream
SPC artifacts, so this slice makes no Ella compatibility claim.

A fresh live AGF run was also attempted. PyPI supplied `pyswisseph` as source
for CPython 3.12, no compatible binary wheel was available, and the host lacks
the required MSVC toolchain. Rather than expand the sprint into compiler
installation, the run used the permitted current AGF fixture replay. A future
AGF release qualification may separately provide a prebuilt live dependency
or a retained Ella canonical fixture.

## Verification

- installed AGF/SPC/SBE boundary: pass;
- repeated four-context projection: pass;
- schema, lineage, topology, runtime identity, and registry closure: pass;
- installed SBE deterministic extraction boundary: pass;
- SPC full suite: 157 passed in 95.11 seconds;
- focused Ruff: pass;
- AGF and SBE working trees: unchanged and clean.

Reader-facing prose generation, API delivery, tag creation, pushing, and
publication were not performed.
