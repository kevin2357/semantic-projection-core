# Ideas and Future Work

- Projected temporal activation graphs and timing materializations.
- Profile plugin discovery and external profile packages.
- Richer lexical realization metadata: articles, pluralization, collocations, term-specific active clauses, collision avoidance, pronouns, and multilingual lexicons.
- Deterministic relationship grouping and local narrative planning.
- Semantic-facet queries across target ontologies.
- Claim/narrative-unit interfaces without collapsing projection into reasoning.
- Canonical versus stylistic realization packs.
- Context-aware relevance distinct from style, voice, and audience presentation.
- Explicit claim-versus-illustration provenance.
- Compact external forensic audits and large-graph indexing.


## Stage C continuation after Chunk 3.beta.1

The Foundry temporal bundle intake and generic temporal request contract are implemented. The next focused pass is C2:

- finalize `projected_temporal_activation_graph.v1`;
- define activator, activation, sequence, and state contracts;
- separate preserved `temporal_facts` from Core-owned projected fields;
- define referential-integrity and deterministic-ID invariants;
- validate the hand-authored contract against the real Kevin temporal bundle before implementing mapping execution.

## Temporal projection after C2

Stage C3 should reuse the existing static object, sign, house, aspect, term-registry, audit, and coverage abstractions. Avoid parallel temporal-only mapping tables unless a target ontology genuinely requires distinct temporary-activation semantics.

Future temporal materializations may include event-only, daily, monthly-index, and streaming views, but these remain deferred until the full/standard/summary/forensic projected temporal contract is implemented and validated.

## Temporal artifact identity and tooling

Extend the new artifact-identity utility as additional request, projected, materialized, QA, and rejection artifact types appear. Keep CLI, profiler, and QA classification centralized rather than relying on filenames.

## Post-C4 temporal work

- Finalize temporal full/standard/summary/forensic materializations.
- Replace the provisional full-registry carry-through with a compact used-term
  subset policy where appropriate.
- Expand target-resolution diagnostics to distinguish explicit static policy
  exclusions from unsupported source-object families.
- Add cross-profile and Composite/Davison rich-fixture QA in Stage C6/C7.
- Keep temporal rendering and claim synthesis downstream of Stage C.

## Post-C5 temporal follow-ups

- Consider externalizing full temporal forensic audit payloads as a separable artifact, paralleling static projection.
- Evaluate whether future event/daily/streaming materializations should be views over the same arc graph rather than new execution contracts.

## Post-C6 temporal work

- Extend cross-profile QA to Composite and Davison target bundles during C7.
- Add richer context matrices as profile contexts mature.
- Keep temporal-fact invariance as a permanent regression property.
- Revisit intentional profile-scope exclusions such as Cognitive `Spirit` only through explicit profile-version evolution.

## Post-Stage-C work

- Exercise the C7 production route against Composite and Davison temporal bundles as soon as Foundry fixtures are available; the QA runner already accepts multiple fixture families.
- Treat cross-profile temporal-fact invariance as a permanent hero regression test.
- Grow the C6 comparison artifact into a general semantic-diff utility while keeping it downstream of projection execution.
- Keep the C6 architectural conclusion in high-level architecture documentation: temporal projection is the same compiler over a time-indexed canonical graph, with semantic variability orthogonal to canonical temporal facts.


## Queued documentation: architectural retrospective

Create **Evolution of Semantic Projection Core: Lessons from Static and Temporal Projection** as a narrative onboarding document. Cover the emergence of registries, deterministic IDs, materialization modes, increasingly explicit coverage classifications, the Foundry-facts/Core-semantics boundary, and the central lesson that projection is structural compilation rather than interpretation.

## Synastry projection expansion

Add a dedicated future pass for synastry projection:

- audit current synastry object and relationship coverage;
- add or refine relationship-specific mappings where useful;
- preserve person-A/person-B ownership and directional semantics;
- establish cross-profile synastry QA;
- add temporal synastry routing when Foundry provides canonical fixtures;
- compare synastry with Composite and Davison projection contracts without conflating their source identities.


## Post-C8 Orthodox and temporal follow-ups

- Audit the 1,020 canonical relationship rows currently outside the Orthodox profile's declared relationship scope; classify which families deserve identity projection and which are aliases, administrative edges, or intentionally excluded.
- Consider explicit Orthodox temporal state composition so target-chart transit houses project to Orthodox house references rather than generic domain-unavailable status.
- Consider a slimmer Orthodox temporal interchange/materialization for consumers that need current activations without embedding thousands of static relationships.
- Preserve the retrospective documentation task **Evolution of Semantic Projection Core: Lessons from Static and Temporal Projection**.

## Woofmapped horoscope contexts and downstream rendering

Maintain two context modes over the same Woofmapped primitive profile:

- handler-facing guidance about baseline-relative changes and practical adjustments to routines, training, enrichment, expectations, rest, social exposure, and handling;
- dog-facing direct address in a playful horoscope voice, explaining what may feel different and offering advice for navigating or contextualizing those changes.

These remain separate projection/rendering contexts, not separate primitive mappings. Projection owns audience and relevance framing; downstream reasoning and rendering own recommendations and prose.
