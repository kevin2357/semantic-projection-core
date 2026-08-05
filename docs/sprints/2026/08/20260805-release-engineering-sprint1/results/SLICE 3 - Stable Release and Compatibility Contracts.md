# Slice 3 - Stable Release and Compatibility Contracts

```yaml
status: complete
gate: passed_pending_review
qualification_date: 2026-08-05
candidate_distribution: semantic-projection-core
candidate_version: 0.10.0
```

## Outcome

SPC 0.10.0 now has a documented and machine-readable supported release
boundary. A downstream implementing agent can determine what to install,
invoke, validate, preserve, and reject without treating internal modules or
historical documentation as public API.

Changes remain uncommitted pending review. Slice 4 has not begun.

## Contracts added

The packaged `semantic_projection.release_compatibility.v1` resource freezes:

- distribution, package, engine, Python, and engine-contract versions;
- canonical static graph 1.3.0 compatibility;
- AGF temporal bundle and temporal graph 1.0.0 compatibility;
- normalized temporal request identity;
- static, temporal, foundations, and route-receipt output contracts;
- four materialization modes;
- all three bundled profile IDs, versions, and declared static source types;
- all six installed commands;
- profile entry-point group and exact-version failure policy; and
- the four exact Woofmapping natal context ID/version pairs.

The runtime smoke report now exposes the compatibility contract ID and version
alignment. The compatibility JSON is included in the installed semantic-resource
fingerprint.

## Public boundary clarified

Supported Python routes are high-level top-package APIs for static projection,
the complete temporal pipeline, participant-aware synastry, exact bundled
context resolution, runtime resource identity, and public contract dataclasses.

SPC profile mapping modules, private helpers, mapping tables, and repository
`tools/` or `scripts/` are explicitly not stable release APIs. Consumer-owned
profiles may use the named Python entry-point group and an explicitly constructed
registry; bundled commands do not promise arbitrary third-party discovery on
every route.

Installed commands have stable required options, output-mode choices, exit code
0 on success, and exit code 2 for validation/command failures in this release.
Diagnostic error text and debug tracebacks are not a machine-readable contract.

## Enforcement distinction recorded

The generic validators reject unsupported canonical and temporal *versions*.
Static profile manifests declare the graph types within qualified release scope,
but the generic engine does not currently reject solely because a `graph_type`
string is outside that list. Consumers must submit only a declared graph type
and inspect coverage/diagnostics. This is an implemented limitation, not a
future guarantee disguised as present behavior.

## Four-context decision

SPC now formally qualifies these exact contexts for static Woofmapped natal
projection:

- `woofmapped.doghouse.general.v0` 0.1.0;
- `woofmapped.handler_guidance.v1` 1.0.0;
- `woofmapped.dog_direct.v1` 1.0.0;
- `woofmapped.hybrid_horoscope.v1` 1.0.0.

The Woofmapping manifest records the same set. This closes SPC's acceptance and
qualification question while preserving the product boundary: the names do not
define AstroWoof prose, audience behavior, recommendations, or card structure,
and no context receives canonical priority.

## AGF and AstroWoof handoff findings

Read-only inspection confirmed:

- AGF HEAD `259058d` declares `semantic-projection-core>=0.10.0`. That remains
  convenient for development but is not an immutable production pin.
- AGF imports top-level SPC APIs as well as internal engine, registry,
  validation, profile, and Orthodox mapping modules. The handoff explicitly
  marks mapping-module imports unsupported for released integration.
- AstroWoof API HEAD `e0d171d` already proposes SPC 0.10.0, Woofmapping 0.1.0,
  exact context identities/hashes, and full materialization. Its open question
  about the four natal context identities is now answered by SPC's release
  contract.
- Whether AstroWoof accepts `standard` instead of conservative `full`
  materialization remains a downstream SBE/API acceptance decision. SPC only
  guarantees that standard is row-bearing and summary is not.
- The API repository had a pre-existing untracked `src/astrowoof_api/storage/`
  path. It was not inspected as user work beyond Git status and was not changed.

No AGF, API, SBE, or astrowoof-project files were modified.

## Unsupported routes made explicit

- temporal synastry without a future AGF source contract;
- raw transit prose or summaries as projection input;
- static graphs reconstructed from AGF analysis summaries;
- summary materialization where rows/evidence are required;
- internal module imports as stable public API;
- mutable branch or permissive-range production installation;
- product claims, advice, authorship, cards, UI, or publication;
- filenames, labels, or list positions as cross-context identity.

## Verification

- New release-contract consistency tests: 4 passed.
- Focused contract/resource tests: 10 passed.
- Full source suite: 150 passed in 92.04 seconds.
- Focused Ruff: passed.
- Relative links in all eight created or materially updated entry-point
  documents: passed.
- Packaged compatibility and evidence JSON parsing: passed.
- Machine-readable evidence:
  `results/compatibility-contract-verification.json`.

## Gate assessment

Slice 3 gate is satisfied. A naive consumer can identify the exact supported
versions and profiles, use supported CLIs or top-level APIs, preserve native
artifacts and registries, and fail closed on incompatibility. Final wheel URL,
tag, and SHA-256 remain deliberately absent until Slice 7 produces and publishes
the final reproducible artifact.
