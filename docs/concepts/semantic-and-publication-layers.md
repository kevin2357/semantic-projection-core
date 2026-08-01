# Projection, reasoning, and publication layers

A projected semantic graph is reusable precisely because it is not a finished report.

```text
canonical facts
  -> projected semantic graph
  -> claims and application reasoning
  -> narrative or rule planning
  -> publication / runtime materialization
```

SPC owns the first transformation into target-domain semantics. It may expose deterministic local rendering helpers for inspection, but it does not decide the final message, recommendation, game effect, report section, or visual layout.

## Projection context is not style

Context answers what the projection is for: an individual, a professional relationship, handler guidance, direct address to a dog, or a game system. Style answers how a consumer presents the result: technical, playful, compact, literary, visual, or interactive.

Audience can affect semantic emphasis without authorizing SPC to manufacture audience-facing prose. For example, the Woofmapped handler context marks practical guidance intent; a downstream reasoning layer decides which routine adjustment is warranted, and a publisher decides how to phrase it.

## Downstream responsibilities

Downstream systems may:

- synthesize several projected relationships into a claim;
- combine static baselines with temporal activations;
- resolve or preserve tensions according to an application policy;
- calculate game magnitudes or behavioral recommendations;
- organize report sections and narrative arcs;
- render Markdown, web, cards, dashboards, or runtime records.

They should preserve projection IDs, source references, mapping-rule references, registry identity, and limitations so the final output remains auditable.
