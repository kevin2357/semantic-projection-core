# Slice 4 - Installed Candidate and Release Handoff

## Outcome

Semantic Projection Core 0.11.1 is a qualified, reproducible release candidate.
Its distribution and engine identity distinguish the corrected executable
semantic policy while bounded wire, profile, ontology, registry, and context
identities remain unchanged.

## Immutable candidate artifact

| Field | Value |
|---|---|
| Wheel | `semantic_projection_core-0.11.1-py3-none-any.whl` |
| Bytes | 161706 |
| SHA-256 | `dc345cd3253de333a5428e4fc7e24816447a065215ef288ba76527960a7da612` |
| Fixed epoch | 1787090400 |
| Builds | 2 |
| Byte-identical | yes |
| Candidate tag | `semantic-projection-core-v0.11.1` |

The candidate installed non-editably under Linux/Python 3.11.15. Runtime smoke
found all four profile entry points, seven installed commands, and 13 bundled
contexts with aligned distribution, package, engine, and compatibility identity.

## Installed runtime fingerprints

| Resource set | Count | SHA-256 |
|---|---:|---|
| Runtime package | 116 | `38de395c5089289fb025dc93888d26f64e1c315daaed98bafd069e950d95aa44` |
| Semantic resources | 52 | `464b91889b5146abc92a74ac477ea9b7ac469d0b7c7783700264195e01615b0a` |
| Schemas | 26 | `cf0466af1d04f4115c007edffb1a583058a829a56048ff24023620906c3839eb` |
| Compatibility resource | 1 | `eb1272394ded9a8cb769498cdd1328b639dc7711ef24c83103d71cf3bc5a2551` |

The semantic-resource fingerprint differs from 0.11.0 because executable
profile policy and release compatibility identity participate in the installed
resource set. Schema identity remains stable as intended.

## Installed bounded execution

The installed `semantic-bounded-project` command successfully projected the
checked-in AGF 0.8.1-shaped bounded fixture through:

- `woofmapped.doghouse.general.v0@0.1.0`;
- `woofmapped.handler_guidance.v1@1.0.0`;
- `woofmapped.dog_direct.v1@1.0.0`; and
- `woofmapped.hybrid_horoscope.v1@1.0.0`.

Slice 3 already proved policy closure, correspondence, parallel validation, and
repeat determinism on an AGF-shaped fixture containing True Node, Mean Node,
derived descendants, and dependent relationships. This installed check proves
the packaged boundary and commands rather than repeating source-only logic.

## Downstream handoff

SPC 0.11.0 bounded output is affected only when the source contains excluded
Mean Node aliases or descendants. The safe correction is regeneration from the
immutable AGF bounded source with 0.11.1. Downstream semantic deduplication would
occur after projected identity, evidence closure, registry materialization, and
relevance allocation and therefore cannot recreate the authoritative SPC result.

Current SBE has a dedicated bounded authoring route. That downstream capability
does not transfer source-selection authority to SBE. AGF remains authoritative
for canonical bounded source facts; SPC remains authoritative for projection
policy; SBE remains authoritative for downstream selection and authorship.
AGF and SPC are runtime-decoupled distributions, so the production orchestrator
must pin, install, invoke, and receipt them independently.

## Qualification summary

- final complete source suite: **232 passed** in 57.31 seconds;
- release identity/resource/provenance set: **17 passed**;
- installed runtime smoke: passed;
- non-editable installed execution: passed;
- four installed bounded commands: passed;
- reproducible build: passed.

Machine evidence is recorded in
[`installed-release-candidate.json`](installed-release-candidate.json). Release
assets and instructions are under [`releases/0.11.1`](../../../../../../releases/0.11.1/RELEASE%20NOTES.md).

## Gate disposition

Slice 4 is ready for review. Publication remains a separate approval boundary:
no release commit, tag, tag push, GitHub release, asset upload/download
verification, or downstream production pin has occurred.
