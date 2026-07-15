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
