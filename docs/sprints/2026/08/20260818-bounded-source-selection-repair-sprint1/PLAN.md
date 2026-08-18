# Bounded Source-Selection Repair Sprint 1

```yaml
status: active
owner: semantic-projection-core
scope: enforce declared bounded node and fortune source-selection policy
created: 2026-08-18
implementation_authorized: true
current_gate: slice_2_review
candidate_distribution_version: 0.11.1
current_released_version: 0.11.0
affected_profile: woofmapped_bounded_astrology.v0@0.1.0
affected_output_contract: projected_bounded_semantic_graph.v1
```

## 1. Sprint outcome

Repair the bounded Woofmapping profile so its executable source selection agrees
with its already-declared policy:

- prefer True Node and exclude Mean Node aliases;
- preserve AGF's canonical bounded calculated `Fortune` point as the bounded
  representation of Part of Fortune;
- exclude derived objects owned by an excluded source object;
- exclude relationships whose endpoints were excluded by source-selection
  policy; and
- report those exclusions truthfully as policy decisions rather than unsupported
  mappings or generic outside-scope rows.

The repair occurs before SBE selection or authorship. SBE should not need to
deduplicate two projected rows that SPC intentionally maps to one semantic
primitive.

The bounded request and output schemas remain unchanged. Exact static and
temporal behavior remain unchanged except for regression verification. The
released 0.11.0 wheel and tag remain immutable.

## 2. Established facts and candidate release identity

### Existing exact behavior

`woofmapped_astrology.v0` and `cognitive_architecture_demo.v0` already declare
True Node and Part of Fortune preferences and enforce them during exact static source
classification. Dependent relationships inherit
`excluded_by_source_selection_policy`. Temporal projection mirrors the same
profile policy.

### Bounded defect

`woofmapped_bounded_astrology.v0@0.1.0` declares:

```json
{
  "node_variant": "true",
  "fortune_variant": "part_of_fortune"
}
```

Its bounded `classify_source_object()` currently tests mapping availability but
does not enforce those choices. Because both True Node and Mean Node resolve to
the North Node target primitive, both can be emitted with distinct source and
projected identities. Derived rows owned by Mean Node and relationships touching
either row can also survive. Existing bounded tests do not exercise this policy.

The output audit therefore records a policy that execution does not fully obey.

Slice 1 established an important type-aware distinction: AGF 0.8.1 emits its
bounded lot as one `bounded_calculated_point` named `Fortune`; it does not emit
the exact graph's legacy `lot` alias plus a separate `Part of Fortune` row.
Bounded calculated Fortune is therefore the preferred bounded representation,
not an alias to delete. The exact name-only selection helper cannot be reused
unchanged on bounded rows.

### Version recommendation

The leading release identity is `semantic-projection-core` 0.11.1:

- this is a backward-compatible bug fix to executable semantic policy;
- no request, output, profile, ontology, context, or registry contract version
  is expected to change;
- corrected outputs intentionally differ from 0.11.0 when excluded aliases are
  present; and
- SPC release identity and semantic-resource fingerprints must change because
  executable semantic policy changed.

The final version decision remains gated on Slice 1 confirming the complete
impact. A new profile version would be warranted only if the audit shows the
declared policy itself must change, which is not the current evidence.

## 3. Explicit slice sequence

### Slice 1 - Reproduction and policy-closure audit

Construct minimal bounded fixtures containing:

- True Node and Mean Node;
- accepted spelling/identifier variants;
- bounded calculated Fortune plus a synthetic Part of Fortune control to prove
  the type-aware distinction;
- derived antiscia, contra-antiscia, and harmonic rows owned by preferred and
  excluded variants;
- direct and derived relationships touching every variant; and
- unrelated eligible rows as controls.

Compare exact, temporal, and bounded policy behavior. Trace AGF 0.8.1 emitted
names and object types, canonical-name normalization, mapping aliases,
root-owner/evidence-family identity, relationship classification, coverage,
audit output, registries, and four-context correspondence.

Decide and record:

- the exact bounded spelling/identity predicates;
- whether existing exact selection logic can be safely shared or whether the
  bounded shape requires a dedicated helper;
- how excluded owner rows propagate to derived descendants;
- how all dependent relationships are classified;
- whether policy-excluded rows remain visible in diagnostics/coverage with
  sufficient source identity; and
- the final package/profile version disposition.

Do not implement the repair before this audit gate.

**Gate:** the defect is reproduced; every affected row family and classification
path is enumerated; expected counts and semantics are explicit; the release
identity is justified.

### Slice 2 - Bounded policy enforcement

Implement source-selection enforcement at the bounded profile boundary.

Required behavior:

1. A directly excluded Mean Node receives
   `excluded_by_source_selection_policy`.
2. A derived object whose semantic owner is policy-excluded receives the same
   classification rather than becoming eligible through its mapping.
3. A relationship touching any policy-excluded endpoint receives
   `excluded_by_source_selection_policy`.
4. True Node and AGF's bounded calculated Fortune remain eligible when otherwise
   supported.
5. Missing True Node does not cause Mean Node to be silently promoted. The node
   preference is a source-selection contract, not a “whichever exists” heuristic.
6. Projection emits no row, term use, relevance allocation, correspondence, or
   evidence-family vote for excluded variants.
7. Coverage and audit counts retain the exclusions as deliberate policy choices.

Prefer one canonical classification path so policy metadata and execution cannot
drift independently again. Do not alter AGF artifacts or mutate source evidence.

**Gate:** focused object, derived-family, relationship, coverage, audit, and
registry tests pass; the minimal reproduction emits one semantic node and one
Fortune concept without source-policy descendants.

### Slice 3 - Four-context, determinism, and regression QA

Project representative bounded fixtures through general, handler,
direct-to-dog, and hybrid contexts. Verify:

- the exact context set and versions;
- identical policy exclusions and source epistemic material across contexts;
- stable correspondence for retained rows;
- absence of excluded source refs and dependent relationship refs;
- valid artifact-scoped projected-term registries;
- family-aware coverage/relevance conservation;
- byte-level or contract-defined deterministic repeat behavior; and
- schema plus specialized validator acceptance.

Run the complete bounded suite and full SPC suite. Re-run exact static and
temporal node/Fortune regression tests to prove no released route regressed.
Exercise an AGF 0.8.1-shaped fixture or installed boundary representative.

**Gate:** all four bounded contexts agree, deterministic QA passes, exact and
temporal behavior remains unchanged, and no excluded alias enters an output.

### Slice 4 - Installed candidate, compatibility, and release handoff

If the earlier gates retain the patch-release recommendation:

- advance distribution/package/engine identity to 0.11.1;
- update packaged release compatibility without changing bounded wire or output
  contract versions;
- build the wheel reproducibly;
- install it outside the checkout on the qualified runtime boundary;
- exercise the bounded CLI against AGF 0.8.1-shaped input in all four contexts;
- prove semantic resource and runtime fingerprints changed appropriately;
- prepare release notes, checksums, manifest, exact-hash consumer instructions,
  and an SBE/API correction handoff; and
- document that 0.11.0 bounded artifacts may contain aliases contrary to the
  declared preference and should be regenerated rather than deduplicated
  downstream when exact provenance matters.

Tagging, pushing a tag, publishing a GitHub release, and updating production
pins remain separately approved actions.

**Gate:** a naive downstream implementer can identify affected 0.11.0 artifacts,
install the immutable corrected candidate, validate the retained rows, and avoid
papering over the defect in SBE.

## 4. Controls and safety constraints

- Preserve the current clean worktree and inspect it before every slice.
- Keep each slice uncommitted until explicit review and approval.
- Do not modify AGF, SBE, API, frontend, or project repositories without separate
  authorization; cross-repository inspection is read-only.
- Do not move or overwrite the existing 0.11.0 tag or release assets.
- Do not change `projected_bounded_semantic_graph.v1` merely to repair selection.
- Do not change the meaning of True Node, Mean Node, Part of Fortune, or bounded
  calculated Fortune.
- Do not select a disfavored alias merely because its preferred sibling is absent.
- Apply policy before projection IDs, correspondence IDs, term materialization,
  family accounting, or downstream relevance can be created.
- Preserve evidence and source rows in the immutable input; exclusion affects the
  projected view, not AGF's canonical artifact.
- Treat base objects, derived descendants, and dependent relationships as one
  policy-closure problem.
- Keep policy exclusions distinct from unsupported scope, invalid source data,
  mapping failure, and epistemic uncertainty.
- Run focused tests before full regression and installed-wheel tests.
- Keep large fixtures, wheels, environments, caches, and outputs outside the
  sprint directory; retain compact evidence and hashes only.
- Run JSON/Markdown validation and `git diff --check` before every proposed
  commit.
- Do not commit, push, tag, publish, or change downstream pins without the
  corresponding explicit approval.

## 5. Exit criteria

The sprint exits only when:

1. Mean Node aliases are policy-excluded for the bounded Woofmapping profile;
2. the preferred True Node remains eligible and maps exactly once;
3. AGF's canonical bounded calculated Fortune remains eligible and maps once;
4. derived descendants of excluded owners are also policy-excluded;
5. every relationship touching an excluded row is policy-excluded;
6. no excluded source ref enters projected rows, registry usage, family counts,
   relevance allocation, or correspondence indexes;
7. coverage, audit, and diagnostics report exclusions truthfully;
8. all four contexts contain the same retained semantic topology and exclusion
   disposition;
9. deterministic and schema/specialized validation passes;
10. exact static and temporal source-selection behavior remains unchanged;
11. the complete bounded and SPC test suites pass;
12. installed-wheel execution works outside the checkout against the supported
    AGF boundary;
13. release/runtime fingerprints reflect the executable-policy repair;
14. compatibility and downstream handoff documentation identifies affected
    0.11.0 outputs and the regeneration policy;
15. release artifacts are reproducible and exact-hash instructions exist if a
    patch release is approved; and
16. temporary large artifacts are cleaned and the worktree is clean after final
    approved publication work.

## 6. Deferred work and non-goals

- Changing AGF's decision to emit both canonical node variants is out of scope.
- SBE-side semantic deduplication is not the primary repair and is not authorized
  by this sprint.
- General synonym, semantic-equivalence, or claim-deduplication architecture is
  out of scope.
- Changing the target ontology or projected-term definitions is not expected.
- Redesigning exact static, temporal, or bounded schemas is out of scope.
- Selecting Mean Node as a fallback when True Node is absent is out of scope and
  contrary to the current declared policy.
- Historical 0.11.0 artifacts and release assets remain immutable; consumers may
  quarantine or regenerate them under downstream policy.
- A broader audit of every possible canonical alias may be proposed separately
  if Slice 1 finds evidence beyond node and Fortune policy closure.
