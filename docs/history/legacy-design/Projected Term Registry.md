# Projected Term Registry

## Purpose

A projected semantic graph uses stable machine-oriented terms such as:

```text
pack_role_identity
social_harmony_maintenance_mode
doghouse_8_deep_trust_vulnerability
```

Those identifiers are useful for deterministic mappings, IDs, rules, tests, and graph traversal, but they should not require every consumer to infer their meaning from underscore-separated words.

Each real projection profile therefore owns a versioned **projected term registry**.

## Profile-level and instance-level materialization

The complete registry is stored with the profile:

```text
profiles/<profile>/projected_term_registry.json
```

Projection terms are authored when the profile is authored. A projection run does not invent new terms.

Each projected graph embeds a portable `used_terms_subset` containing only terms referenced by that graph.

```text
complete profile vocabulary
→ projection selects used vocabulary
→ used-term subset embedded once
→ graph rows carry stable term refs
```

The full registry is not duplicated in every projected row.

## Typed single-registry contract

A registry contains one typed vocabulary rather than separate operator, mode, domain, interface, and relation files.

Required entry fields:

```text
term_type
canonical_label
short_description
```

Supported term types:

```text
operator
mode
domain
interface
relation
theme
orientation
```

Strongly encouraged fields:

```text
friendly_labels
long_description
core_operators
semantic_facets
output_guidance
```

Optional fields:

```text
related_terms
extensions
```

## Composition guidance

Composition is a first-class purpose of the registry.

Operator/interface entries provide noun and subject phrases. Modes provide adverbial or operating-style phrases. Domains provide context/location phrases. Relations provide verb phrases and sentence templates.

A deterministic renderer can therefore turn:

```text
pack_role_identity
+ social_harmony_maintenance_mode
+ doghouse_8_deep_trust_vulnerability
```

into a serviceable sentence before an LLM performs any stylistic refinement.

The registry guides interpretation; it does not pre-author one mandatory narrative claim.

## Graph references

Projected rows retain stable refs such as:

```text
term_ref
mode_ref
domain_ref
relation_ref
interaction_mode_ref
```

Registry identity and version also appear in projection metadata.

## Validation

The SDK validates:

- required registry fields;
- known term types;
- required labels and descriptions;
- related-term references;
- every emitted term selected into the used-term subset;
- deterministic registry materialization.

## Architectural ownership

The profile creates the vocabulary, so the profile owns its definitions. Claim generation, report planning, and publishing may use this registry, but they should not redefine profile terms downstream.

## Deterministic rendering experiment

The initial deterministic renderer treats the projected term registry as executable semantic guidance rather than merely documentation. It deliberately remains narrower than a publishing engine.

Its first responsibilities are:

```text
projected operator + projected mode + projected domain
→ canonical composition sentence

projected endpoint + projected relation + projected endpoint
→ canonical relationship sentence

preselected object + bounded relationship neighborhood
→ local narrative paragraph
```

The renderer does not yet discover centers of gravity, rank claims, infer functional sequences, plan whole reports, or choose an audience-specific narrative focus. Those are separate reasoning and publishing concerns.

The renderer emits traceable JSON containing the source term references and template IDs used for every sentence. A companion Markdown showcase makes the output easy to compare with LLM-authored projected chart reads.

### Consumer prose versus composition scaffolding

The registry's explicit operator/mode/domain decomposition is essential for machines and audits, but ordinary projected chart reads should not expose that machinery mechanically.

Technical rendering may say:

```text
Pack-Role Identity operates through Social-Harmony Maintenance Mode in Doghouse 8.
```

Natural rendering should preserve the same semantics while hiding the scaffolding:

```text
Nivek organizes his place in the pack around preserving social cohesion, especially where deep trust and vulnerability are involved.
```

The projected term registry supplies meaning and grammatical affordances. A renderer decides how visibly the composition should appear.
