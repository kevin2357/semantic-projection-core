# Semantic Graph Philosophy

**Status:** Pass 2 philosophy document.  
**Scope:** Why the SDK centers semantic graphs, evidence objects, provenance, registries, and domain-neutral concepts.

## 1. Why semantic graphs?

A raw chart fact is necessary but not sufficient.

```text
Mercury in Scorpio in the 8th house
```

A semantic graph preserves the fact and makes it reusable:

```text
Mercury -> language / interpretation / cognition
Scorpio -> depth / hidden structure / investigation
8th -> intimacy / transformation / shared resources / psychological underworld
Composite meaning -> investigative interpretation engine
```

## 2. Why not just prose?

Prose is final-form. Graphs are reusable. A semantic graph can support reports, games, dashboards, projections, visualizations, research, evidence integration, and future model comparison.

## 3. Evidence-first principle

The repeated design instinct across SDK, CFANFF, archaeology, OMTA, and projection work is:

> Do not throw evidence away. Make evidence first-class.

Evidence should be traceable:

```text
final claim
↓
evidence bundle
↓
semantic relationship
↓
graph object
↓
computed chart fact
```

## 4. Domain neutrality

Upstream concepts should remain portable. Venus should not simply equal romantic love. A more reusable concept is value / attraction / harmony / pleasure / social cohesion / aesthetic preference.

## 5. Registries and stable IDs

Registries began as an optimization for large transit/synastry files, but they also support evidence integration. If three pipelines all point to "communication," a future synthesis layer should connect those evidence items to a shared concept rather than treating them as unrelated strings.

## 6. Graph levels

A pipeline semantic graph answers what this package says. A Meta Semantic Graph answers what multiple packages collectively say.

## 7. Context-aware interpretation

The graph should not decide whether a person is a child, a grandparent, a coworker, a lover, a game character, or a park ecosystem. Those are projection contexts.

## 8. Relationship semantics

Relationship packages should expose interaction and entity structures in domain-neutral ways: activation, friction, support, communication, values alignment, emotional permeability, responsibility, repair, novelty, pacing, and shared purpose.

## 9. Timing semantics

Timing packages should expose time-scale roles: profection foregrounds a subsystem, solar return describes the year chart, lunar return describes the month container, transit gives active weather, and lunation/eclipse supplies punctuation/window.

## 10. Design principles

1. Preserve chart facts.
2. Preserve provenance.
3. Build semantic relationships.
4. Keep upstream meaning domain-neutral.
5. Provide compact references for consumer views.
6. Expose evidence claims.
7. Preserve contradictions.
8. Delay projection until context is known.
9. Delay publication until report structure is known.
10. Treat documentation as part of the architecture.

## Canonical source semantics versus projected meaning

The phrase “semantic graph” previously covered both source-domain operators and orthodox interpretive themes. These are now separated.

`canonical_astrology_graph` preserves the astrology source ontology and its operators. `structural_evidence_graph` records conservative source-level aggregation. `projection_views.orthodox_astrology.v1` contains familiar astrology themes and report-oriented claim candidates.

This distinction matters because reasoning over mapped primitives can produce different relations than translating a completed ordinary astrology interpretation. Mars square Venus mapped to execution and valuation mechanisms must be reasoned about between those projected functions, not translated from romance prose afterward.

See `Pre-Projection Semantic Boundary.md`.
