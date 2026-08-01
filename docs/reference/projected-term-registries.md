# Projected term registries

Every real bundled profile owns a versioned projected term registry. It defines the stable vocabulary used by projected objects and relationships, including operator, facet, mode, domain, interface, and relation terms where the ontology uses them.

## Why registries exist

Machine-oriented keys are necessary for deterministic mappings, graph traversal, tests, and downstream rules, but a key such as `pressures_and_forces_adaptation` should not require every consumer to reverse-engineer its semantics from underscores.

Registry entries can provide:

- stable term identity and category;
- label and definition;
- semantic facets;
- composition and output guidance;
- grammatical affordances used by deterministic rendering.

## Artifact behavior

Full projection execution starts from the profile's complete registry. The output embeds only the terms referenced by that graph and replaces term-like keys with stable registry references where required. This produces a self-describing artifact without copying an entire ontology into every result.

`projected_term_registry.v1` is validated independently. Consumers combining several artifacts from the same profile/version may merge their used-term subsets by key, but duplicate definitions must be identical. A conflicting definition under the same registry identity is a contract error.

## Ownership rule

The profile creates the vocabulary, so the profile owns the definition. Downstream claim generators, applications, and publishers may use the registry but should not silently redefine its terms. Application-specific derived concepts belong in a consumer-owned contract.

## Rendering boundary

SPC includes deterministic helpers for local object sentences, relationship sentences, and bounded local narratives. They resolve terms through the embedded registry and preserve traceability. These helpers demonstrate semantic composition; they are not a claim synthesizer or report writer.
