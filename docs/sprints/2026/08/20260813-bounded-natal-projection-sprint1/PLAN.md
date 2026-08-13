# Bounded Natal Projection Sprint 1

```yaml
status: active
owner: semantic-projection-core
scope: bounded-birth-time canonical graph intake and Woofmapping projection
created: 2026-08-13
implementation_authorized: false
current_gate: slice_1_review
candidate_distribution_version: 0.11.0
candidate_engine_version: 0.11.0
candidate_output_contract: projected_bounded_semantic_graph.v1
qualified_source_release: astrology-graph-foundry 0.8.0
```

## 1. Sprint outcome

Add an explicit bounded-natal projection route that consumes AGF's released
bounded-birth-time wire artifact and produces a new bounded projected artifact.
The route must preserve what AGF proved, including uncertainty evidence,
capability limits, lineage, and derived-object family identity, while applying
target-domain semantics without inventing exact values, confidence, salience,
or reader-facing interpretation.

The existing `projected_semantic_graph.v1` contract and its exact-chart
behavior remain unchanged. The first qualified target implementation is the
Woofmapping canine projection in its `handler`, `direct-to-dog`, `hybrid`, and
`general` contexts.

This document proposes the implementation sequence. No implementation, release,
tag, push, or publication work is authorized until the applicable gate is
approved.

## 2. Candidate identities and assumptions

### Qualified source baseline

- distribution: `astrology-graph-foundry` 0.8.0
- annotated tag: `astrology-graph-foundry-v0.8.0`
- source commit: `2e5feef35e6d7144c3e639ece0aba9ff587ea4e9`
- wheel SHA-256:
  `f236de0bb7c254c4421f571e816f2314251636ebbed9aa3cb9cb2a09925c04ae`
- runtime-manifest SHA-256:
  `413c84728bc279bdfa67f892481ebe9837c0306093c2d28444caf239043ed5e2`
- package type: `bounded_natal_dataset`
- package schema: 1.0.0
- graph type: `bounded_canonical_astrology_graph`
- graph version: 1.7.0
- evidence contract: `agf.bounded_uncertainty_evidence.v1.0.0`
- calculation profile: 1.12.0
- interval-proof profile: `agf.interval_proof.v1.0.0`

These identities are audit inputs, not substitutes for inspecting the actual
released schemas and representative artifacts in Slice 1.

### Candidate SPC release identity

Because this sprint adds a public route, packaged semantic policy, and an output
contract without changing the existing exact contract, the initial release
candidate is:

- distribution/engine: `semantic-projection-core` 0.11.0
- output contract: `projected_bounded_semantic_graph.v1`
- request contract: `bounded_natal_projection_request.v1`
- installed command: `semantic-bounded-project`
- tag, if separately qualified and approved later:
  `semantic-projection-core-v0.11.0`

Names and version numbers remain proposals until the Slice 1 contract audit.
The existing 0.10.0 release and tag are immutable.

### Profile identity decision to resolve

The leading option is a sibling bounded source-policy profile, tentatively
`woofmapped_bounded_astrology.v0`, rather than silently changing the semantics
of released `woofmapped_astrology.v0`. It may reuse shared target ontology and
projected-term resources where their identity and meaning are genuinely the
same. Slice 1 must compare this option with a new version of the existing
profile and record the selected ownership/versioning model before mappings are
implemented.

### Fixed semantic decisions

The following are approved sprint constraints, not open design questions:

1. Bounded projection has its own output schema.
2. `projected_semantic_graph.v1` is not extended or weakened for bounded input.
3. Projection contexts do not vary epistemic certainty. Across all four
   contexts, the source-supported status, evidence, limitations, and capability
   facts are identical. Context may vary target-domain relevance and framing.
4. Derived-object multiplicity receives both treatments:
   - preserve AGF root-owner and evidence-family correspondence; and
   - prevent sibling multiplicity from inflating coverage, relevance, salience,
     confidence, or apparent independent support.
5. Missing exact values are not filled with representative, midpoint, default,
   or context-selected values.

## 3. Explicit slice sequence

### Slice 1 — Released contract and semantic audit

Inspect the exact AGF 0.8.0 release schemas, manifests, bounded evaluator
results, fixtures, compatibility evidence, and wire artifacts alongside SPC's
current validators, profiles, mappings, schemas, provenance, CLI, package
resources, and QA. Produce:

- a field-level input inventory and compatibility matrix;
- the authoritative released status and availability vocabulary;
- an inventory of bounded object and relationship kinds;
- evidence-reference, namespace-normalization, and closure rules;
- capability and partial-evaluation semantics;
- size/topology characteristics and performance risks;
- selected request, route, output-contract, profile, and release identities;
- a decision on whether SPC packages consumer-side validation resources,
  validates an SPC-owned semantic boundary after external schema validation, or
  uses another dependency-neutral mechanism; and
- fixtures and acceptance cases for later slices.

No broad implementation changes occur before this gate.

**Gate:** the source boundary, semantic invariants, unsupported cases, contract
names, profile ownership, and exact implementation scope are explicit.

### Slice 2 — Bounded wire intake and validation

Implement the new request/intake boundary without adding AGF as an implicit
runtime executor or restoring the removed AGF-to-SPC coupling. Validate the
supported package/graph/evidence/profile versions, reference closure,
capabilities, source namespaces, identities, and semantic preconditions.
Normalize qualified source references only according to AGF's documented wire
rules. Reject unsupported, malformed, ambiguous, or incomplete inputs with
deterministic diagnostics.

The existing exact and temporal intake routes continue to reject bounded graphs
rather than guessing a route.

**Gate:** the exact AGF 0.8.0 wire artifact enters SPC through a dedicated,
dependency-conscious boundary; invalid variants fail explicitly; all existing
intake behavior passes regression tests.

### Slice 3 — Projected bounded contract and provenance

Define and implement the new projected bounded schema. It must distinguish
projected semantic content from source epistemic evidence and retain enough
identity to trace every projected fact to its source object or relationship,
evidence family, proof scope, capability state, route, context, profile,
contracts, runtime resource set, and source artifact.

Define deterministic identity and ordering rules, evidence-registry embedding
or referencing, projected-term registry requirements, materialization limits,
and failure behavior. Make absence, unavailability, variability,
inconclusiveness, and unsupported capability distinguishable wherever the
released AGF contract distinguishes them.

**Gate:** the schema validates representative artifacts and cannot express a
bounded result as if it were an exact chart or a confidence-weighted guess.
The existing projected schema is byte-for-byte unchanged.

### Slice 4 — Woofmapping bounded object projection

Implement source-selection and target mapping for supported invariant bounded
objects. Cover the released object families deliberately, including bodies,
angles, cusps, sect state, calculated points, antiscia and contra-antiscia
points, and harmonic points where the audit confirms target semantics.

Mappings may reinterpret source semantics in the canine domain, but they may
not manufacture scalar positions, exact degrees, representative houses,
strength, or prose conclusions. Unsupported object kinds must be explicit, not
silently dropped.

**Gate:** supported objects project deterministically with complete lineage,
projected-term definitions, and evidence references; unsupported semantics have
auditable failure or omission policy.

### Slice 5 — Relationships, operators, and evidence families

Implement bounded relationship and operator projection for the supported
ordinary, derived, declination, angle, calculated-point, and ownership
relationships established in Slice 1. Preserve topology and source roles while
omitting prohibited exact-chart measurements such as orb, distance,
applying/separating delta, and structural strength.

Make root-owner/evidence-family membership first-class enough for downstream
consumers to recognize related derived facts. Define family-aware coverage and
relevance accounting so one source construction cannot become many independent
votes merely because AGF represents its components faithfully. In particular,
the current fallback from a missing structural score to `1.0` must not govern
bounded artifacts.

**Gate:** every emitted relationship is source-supported and traceable;
family-aware metrics pass duplication/adversarial tests; no bounded artifact
acquires invented strength or independent-support semantics.

### Slice 6 — Four-context materialization and certainty invariance

Project representative bounded inputs through `handler`, `direct-to-dog`,
`hybrid`, and `general`. Define structurally parallel identity/correspondence
across contexts. Permit target relevance, role framing, or vocabulary variants
only where profile configuration owns them.

Add cross-context assertions that source epistemic status, evidence membership,
capability state, limitations, and family identity do not vary. No context is
the canonical epistemic interpretation, and similarly named product audiences
are not inferred from projection context names.

**Gate:** all four outputs are structurally comparable, certainty-invariant,
deterministic, and correctly registry-scoped.

### Slice 7 — Deterministic, negative, scale, and regression QA

Exercise narrow, whole-day, and maximum-supported intervals; stable and partly
stable charts; unavailable or inconclusive terrestrial frames; large derived
families; circular/disjoint ranges; transition witnesses; counterexamples; and
capability-limited inputs. Include negative cases for unsupported versions,
broken references, evidence conflicts, duplicate IDs, missing resources,
unknown object/relationship kinds, and route confusion.

Repeat projections to prove byte- or contract-defined semantic determinism.
Measure representative large artifacts without checking expanded artifacts,
caches, or environments into the sprint directory. Run the complete current
static and temporal regression suites to prove no legacy route changed.

**Gate:** positive, negative, determinism, scale, and existing-route regression
evidence passes with compact machine-readable summaries under `results/`.

### Slice 8 — Installed runtime and cross-repository acceptance

Build and install the candidate SPC wheel outside the checkout. Exercise the
new installed command and runtime resource discovery against an artifact from
the exact AGF 0.8.0 wheel. Verify all four contexts, fingerprints, provenance,
registries, and deterministic output without editable imports.

Test the bounded output against an explicitly agreed SBE acceptance boundary.
If SBE does not yet support the new schema, produce a precise handoff and
machine-verifiable fixture rather than weakening SPC's contract or claiming
end-to-end acceptance.

**Gate:** the installed wheel independently consumes the pinned AGF artifact;
the bounded contract has a verified downstream disposition; current installed
SPC routes still pass.

### Slice 9 — Documentation, release candidate, and handoff

Document the supported boundary, semantic interpretation, compatibility matrix,
consumer invocation, provenance requirements, projected registry preservation,
family-aware handling, context invariants, limitations, and unsupported routes.
Create release notes and compact qualification evidence. Reconcile SPC and
AstroWoof project-level documentation only where separately authorized.

Prepare—but do not publish—the 0.11.0 release candidate and exact-hash consumer
instructions. Any reproducible-build, tag, push, GitHub release, or downstream
pin update requires a separate approval boundary.

**Gate:** a downstream implementer can install, select the bounded route,
validate and preserve its output, reject incompatibility, and avoid treating it
as either an exact chart or a finished reading.

## 4. Controls and safety constraints

- Inspect the worktree before every slice and preserve user changes.
- Keep slice work bounded and uncommitted until review; commit only after
  explicit approval.
- Do not modify AGF, SBE, AstroWoof API, frontend, or project repositories unless
  separately requested. Cross-repository checks are read-only by default.
- Pin the AGF qualification artifact by exact SHA-256. Do not use a moving branch
  as compatibility evidence.
- Do not add AGF projection execution back into AGF or make source-checkout paths
  part of SPC's runtime contract.
- Do not change `projected_semantic_graph.v1`, its schemas, or its accepted
  semantics to accommodate bounded input.
- Do not infer exact values, midpoints, representative states, default houses,
  strengths, probabilities, confidence, salience, or prose interpretations.
- Do not let projection context change source certainty or evidence.
- Do not count derived siblings as independent support or use raw graph density
  as importance.
- Preserve source identity, proof scope, evidence references, root-owner family,
  capabilities, limitations, profile/context identity, and resource provenance.
- Resolve profile IDs and versions exactly. No permissive fallback selects a
  semantically adjacent profile.
- Prefer deterministic local tests before installed or cross-repository tests.
- Keep large artifacts, wheels, environments, caches, and expanded fixtures out
  of `docs/sprints`; retain compact hashes, counts, summaries, and minimal
  fixtures only.
- Run relevant tests and `git diff --check` before every proposed commit.
- Do not tag, push, publish, or change downstream pins without explicit approval.

## 5. Exit criteria

The sprint exits only when:

1. the dedicated bounded request/intake route accepts the exact supported AGF
   0.8.0 wire contract and rejects incompatible versions deterministically;
2. `projected_bounded_semantic_graph.v1` exists as a separate validated
   contract and `projected_semantic_graph.v1` remains unchanged;
3. every supported emitted fact is traceable through source identity and
   evidence to the bounded input;
4. no exact scalar, structural strength, probability, confidence, salience, or
   representative state is invented;
5. supported object, relationship, operator, evidence, and capability semantics
   have explicit coverage or explicit unsupported behavior;
6. root-owner and evidence-family identity is preserved;
7. family multiplicity cannot inflate coverage, relevance, or apparent support;
8. all four Woofmapping contexts pass and are epistemically invariant;
9. projected-term registries are valid, complete for emitted terms, scoped as
   specified, deterministic, and preserved through materialization;
10. representative repeats prove contract-defined deterministic equivalence;
11. narrow, broad, partial, inconclusive/unavailable, large, and invalid cases
    have passing QA evidence;
12. all existing static and temporal contracts and tests pass unchanged;
13. a clean installed candidate wheel works outside both source checkouts;
14. installed compatibility uses the pinned AGF wheel/artifact identity;
15. SBE acceptance is either proved against an agreed boundary or documented as
    an explicit downstream blocker with a complete handoff fixture;
16. runtime/profile/contract/context/resource-set provenance is sufficient to
    reproduce the projection basis;
17. consumer and compatibility documentation clearly distinguishes bounded
    projection from exact projection and from reader-facing authorship; and
18. temporary large artifacts are cleaned and compact result evidence is
    retained.

## 6. Deferred work and non-goals

- Existing exact projection schema redesign is out of scope.
- Temporal bounded-birth-time combinations are out of scope unless a later
  explicitly approved sprint defines their semantics.
- Synastry involving a bounded natal graph is out of scope.
- Probability distributions, rectification, interpolation, representative
  chart selection, and most-likely-state inference are out of scope.
- Reader-facing prose, card selection, Semantic Closure, product audience,
  filter assignment, API persistence, and frontend presentation remain
  downstream responsibilities.
- AGF calculation behavior and canonical graph generation remain AGF-owned.
- A complete bounded implementation for Orthodox or Cognitive profiles is not
  required for this sprint. The engine boundary should not preclude future
  profiles, but Woofmapping is the first qualified target.
- Publishing 0.11.0, moving consumer pins, or declaring production readiness is
  not implied by implementation completion and requires separate release
  qualification and approval.
