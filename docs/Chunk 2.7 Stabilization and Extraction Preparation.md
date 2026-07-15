# Chunk 2.7 — Stabilization, Materialization, and Extraction Preparation

## Purpose

Chunk 2.7 stabilizes the internal projection layer before repository separation. It does not add a new ontology or a publishing engine. It makes existing projections easier to profile, materialize, validate, and extract.

## Materialization policy

Projection now has four explicit materializations:

```text
full      complete graph, full audit, full diagnostics
standard  graph + used-term registry + compact audit/diagnostics
summary   no graph rows; identity, coverage, and diagnostic counts
forensic  complete graph plus deterministic integrity hashes
```

`standard` is the recommended ordinary interchange artifact. `full` remains useful during development. `forensic` is intended for audits and regression analysis. `summary` is appropriate for catalogs and quick inspection.

A full audit can also be separated as a `projection_forensic_audit` artifact without changing the projected graph's semantic content.

## Truthful coverage and thresholds

Profiles distinguish:

```text
eligible and mapped
eligible but unmapped
outside declared scope
excluded by source-selection policy
```

CLI unmapped thresholds now default to the **eligible** denominator. This avoids treating intentionally unsupported canonical rows as profile failures. A `canonical` denominator remains available for forensic comparison.

## Artifact profiling

`scripts/profile_projection_artifacts.py` reports:

- file and compact JSON size;
- graph-row, audit, diagnostics, and registry byte contributions;
- object and relationship counts;
- mapping-execution counts;
- eligible-scope coverage;
- deterministic object/relationship hashes;
- read time.

This provides the data needed to decide whether audits should be embedded, compacted, or written separately for each consumer.

## Extraction readiness

`scripts/inspect_projection_extraction_readiness.py` checks the generic package for imports from non-projection SDK modules and records contract ownership.

The standalone project should own:

- projection contracts and schemas;
- generic engine and profile protocol;
- IDs, validation, registry, audit, diagnostics;
- projected term registries;
- materialization and deterministic rendering;
- reference profiles and generic examples.

The Astrology Analysis SDK should retain:

- canonical astrology and structural-evidence contracts;
- saved-package adapters;
- astrology-specific source registries;
- the SDK CLI bridge;
- cross-project integration tests.

## Deterministic renderer findings

The small deterministic renderer proved that projected term registries have value outside an LLM context. The same generic code rendered cognitive and Woofmapped objects without profile-specific rules.

The strongest deterministic inputs were:

```text
core operators
mode phrases
domain phrases
relationship phrases
```

Generic short descriptions were less useful than structured semantics. The next lexical-realization improvements, when appropriate, include:

- article and pluralization policies;
- term-specific active clauses;
- collocation and inflection hints;
- pronoun and reference management;
- relationship grouping;
- lexical collision avoidance;
- canonical versus stylistic realization packs.

These are future publication concerns, not requirements for extraction.

## Semantic and publication layers

The mature direction is:

```text
canonical source graph
→ projection profile
→ projected semantic graph
→ projected term registry / semantic lexicon
→ deterministic canonical realization
→ intermediate semantic reasoning and claims
→ report specification and context selection
→ style, voice, audience, and publication
```

Context and style are orthogonal. Manager–employee versus parent–child context can change relevance and semantic emphasis; formal versus playful voice changes presentation. Neither should mutate canonical evidence or profile vocabulary.

Consumer reports should normally hide composition scaffolding. Instead of:

> Pack-Role Identity operates through Social-Harmony Maintenance Mode in Doghouse 8.

ordinary prose should say:

> Nivek defines his place in the pack by preserving social cohesion, especially where trust and vulnerability are involved.

Explicit registry, graph, and evidence language belongs in audit-oriented outputs.

## Findings from registry-grounded reports

Comparisons of cognitive and Woofmapped reports before and after projected term registries showed:

- less reasoning effort spent decoding labels;
- stronger functional reasoning from preserved verbs;
- more stable vocabulary across long reports;
- better treatment of low-salience subsystems;
- clearer multi-node circuits and architectural complexes;
- more specific practical deductions;
- easier cross-domain querying through operators and semantic facets;
- humor becoming mnemonic rather than load-bearing;
- centralized term definitions making disagreement and revision maintainable.

The profiles are therefore evolving from lists of renamed concepts into domain-specific semantic languages with definitions, operators, facets, composition rules, and discourse support.

Useful Woofmapped examples include:

- the Doghouse 8 Trust Core;
- trust as platform rather than prize;
- “train the meaning, not only the behavior”;
- safe location versus regulated body;
- successful role performance not implying low internal cost.

## Chunk 2.8 handoff

After rich-fixture review, repository separation should be mechanical rather than architectural:

1. create standalone package metadata;
2. move generic code, schemas, docs, tests, examples, and profiles;
3. rename the package namespace;
4. keep SDK package adapters in the astrology repository;
5. add editable-path integration and cross-repository tests.

## Timing-package correctness guard

Rich-fixture QA showed that a Transit package could project only its top-level target chart and therefore produce a valid-looking result identical to a static Natal projection. Chunk 2.7 now rejects `transit_dataset`, `transit_range_dataset`, and `transit_period_dataset` explicitly.

The intended future contract is `projected_temporal_activation_graph.v1`. See `Projected Timing and Temporal Activation Design.md`. This is the first recommended substantive feature after repository extraction.
