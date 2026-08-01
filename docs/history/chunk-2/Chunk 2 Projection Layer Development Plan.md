# Chunk 2 Projection Layer Development Plan

**Project starting point:** Astrology Analysis SDK after Chunk 1.5  
**Plan status:** Proposed implementation roadmap  
**Primary goal:** Build and prove an extraction-ready semantic projection framework, then separate it into its own GitHub project  
**Reference profiles required by completion:** `orthodox_astrology.v1` and `cognitive_architecture_demo.v0`  
**Explicitly deferred:** claim graphs, narrative units, standard report compilation, prose generation, multi-pipeline evidence synthesis, publishing, game-specific mechanics, and mature domain-specific projection libraries

---

## 1. Executive summary

Chunk 1 established a trustworthy pre-projection source boundary:

```text
calculated chart facts
        ↓
canonical_astrology_graph
        ↓
structural_evidence_graph
        ↓
projection boundary
```

The Astrology Analysis SDK can now provide:

- deterministic canonical astrology objects and relationships;
- evidence tiers and derivation lineage;
- root-owner references;
- record-level and evidence-family independence groups;
- source-chart and sensor-instance identity;
- projection-neutral structural strength;
- stable full, analysis, and streaming materialization policies;
- an explicitly namespaced but still provisional `orthodox_astrology.v1` view.

Chunk 2 turns projection from a compatibility convention into a real software layer.

The central operation is:

```text
canonical source graph
+ structural evidence
+ projection profile
+ projection context
+ optional source registries
→ projected semantic graph
+ projection audit
+ diagnostics
```

The new machinery must be usable inside the Astrology Analysis SDK during development but deliberately designed for later extraction into an independent project. The projection engine must not import ephemeris providers, chart pipelines, or astrology-specific calculation code. Orthodox astrology must be implemented as a profile that uses the generic contracts rather than as hard-coded behavior in the engine.

Chunk 2 is successful when:

1. a source package can be projected through a generic API;
2. every projected object and relationship is traceable to canonical sources and mapping rules;
3. `orthodox_astrology.v1` reproduces the current useful orthodox row semantics, including complete Synastry registry resolution;
4. a second profile, `cognitive_architecture_demo.v0`, proves that the engine can produce a genuinely different target ontology;
5. projection context demonstrably changes target-domain output without mutating source evidence;
6. the projection machinery is extracted into its own installable repository/project;
7. the Astrology Analysis SDK consumes that project through a narrow adapter.

Chunk 2 does **not** need to solve every difficult projected-chart problem. It needs to establish a sound, testable, extensible infrastructure and prove it with two representative profiles.

---

## 2. Current repository assessment

The present repository already contains important precursors to a projection layer, but they remain coupled to SDK package finalization.

### 2.1 Existing source contracts

Current stable inputs include:

```text
canonical_astrology_graph
structural_evidence_graph
semantic_boundary
source_chart_id / source_chart_ids
sensor_instance_id
projection_views["orthodox_astrology.v1"]
```

The canonical graph is already appropriate as the primary source contract. It preserves source astrology identity, topology, source operators, evidence lineage, and structural scoring while excluding orthodox theme tags.

The structural evidence graph already performs much of the destination-neutral aggregation originally imagined for early Chunk 2:

- evidence-tier counts;
- record and family independence counts;
- source-chart family grouping;
- repeated operator families;
- temporal activation groups where applicable;
- structural strength.

Chunk 2 should consume these structures rather than redesign them.

### 2.2 Existing provisional orthodox behavior

`common/semantic_layers.py` currently contains:

- `ORTHODOX_PROFILE_ID`;
- `orthodox_projection_view()`;
- `orthodox_row_annotation()`;
- compact view helper accessors;
- package finalization that materializes an orthodox view.

This code is useful migration material, not the final projection architecture.

The current orthodox view mostly packages precomputed metrics, claim candidates, and report materials. The row adapter derives conventional tags from source, target, and aspect. It does not yet implement a complete profile contract, mapping-rule audit, projected graph, context handling, or registry-aware mapping in a generic engine.

The clearest current limitation is Synastry:

```text
theme_key + theme_registry
→ should produce complete projected theme set
```

The provisional adapter currently recovers aspect-level fallback themes but not always the full registry-backed meaning set. This becomes the first concrete acceptance test for the real orthodox profile.

### 2.3 Existing documentation direction

The repository already documents the intended separation:

```text
calculation
→ canonical astrology graph
→ structural evidence
→ projection profile
→ projected reasoning
→ synthesis
→ reports / games / parks / cognitive models
```

The ecosystem architecture anticipates an independent `astro-projection` project. Chunk 2 should now operationalize that boundary.

---

## 3. Architectural principles

### 3.1 Projection is not report writing

Projection produces a structured target-domain model. A report may later consume that model, but prose, section planning, narrative flow, and publishing belong downstream.

Examples of possible projected outputs include:

- conventional astrology semantic models;
- cognitive-process models;
- professional-collaboration models;
- parent-child system models;
- game-mechanics vectors;
- park/trail/ecosystem models;
- visual publication structures.

Chunk 2 should remain agnostic about final presentation.

### 3.2 Canonical source evidence is immutable

The engine must never mutate:

- `canonical_astrology_graph`;
- `structural_evidence_graph`;
- source registries;
- source package identity;
- evidence lineage.

Projection creates new target-domain objects and relationships with explicit references back to source material.

### 3.3 The engine is generic; profiles are domain-specific

The projection engine knows how to:

- load and validate profiles;
- resolve mapping rules;
- traverse source objects and relationships;
- apply context conditions;
- create deterministic projected IDs;
- merge compatible mapping outputs;
- preserve provenance;
- emit diagnostics and audits.

The engine must not know that Venus means harmony, Mars means action, or a square means tension. Those belong to `orthodox_astrology.v1` or another profile.

### 3.4 Orthodox astrology is a projection, not a privileged internal mode

`orthodox_astrology.v1` should be the first reference profile because the repository already contains orthodox themes, mappings, and consumer expectations.

It should not receive special treatment from the generic engine. A future external profile should use the same contracts and registry.

### 3.5 Context is first-class but initially conservative

A projection request must permit context such as:

- relationship type;
- subject scope;
- age/life stage;
- application target;
- audience;
- domain constraints;
- output intent.

Chunk 2 should establish the contract and prove that context affects projection. It should not attempt a universal context ontology.

### 3.6 Profiles may be semi-declarative

A purely declarative mapping language would be premature and could become a project of its own.

The initial model should combine:

```text
versioned manifest/configuration
+
Python profile implementation
```

Declarative fields should cover identity, compatibility, ontology declarations, mapping-rule metadata, required context, and output contract. Python may implement nontrivial matching and transformation logic.

### 3.7 Every projected result must be auditable

A projected row should support this trace:

```text
projected row
→ mapping rule execution
→ canonical source row(s)
→ root-owner lineage
→ source chart / sensor identity
→ computed chart facts
```

Fallbacks, skipped mappings, ambiguous mappings, and unmapped sources should be visible in diagnostics.

### 3.8 Determinism is mandatory

The same:

```text
source package
+ profile version
+ context
+ engine version
```

must produce stable projected IDs and deterministic ordering.

---

## 4. Target architecture at the end of Chunk 2

### 4.1 Independent project layout

The final extracted repository should resemble:

```text
semantic-projection/
├── pyproject.toml
├── README.md
├── docs/
│   ├── Architecture.md
│   ├── Profile Authoring Guide.md
│   ├── Projection Context.md
│   ├── Projection Audit.md
│   └── Reference Profiles.md
├── src/
│   └── semantic_projection/
│       ├── __init__.py
│       ├── contracts.py
│       ├── engine.py
│       ├── registry.py
│       ├── ids.py
│       ├── audit.py
│       ├── diagnostics.py
│       ├── io.py
│       ├── validation.py
│       ├── schemas/
│       │   ├── projection_profile_manifest_v1.schema.json
│       │   ├── projection_context_v1.schema.json
│       │   ├── projection_request_v1.schema.json
│       │   ├── projected_semantic_graph_v1.schema.json
│       │   ├── projected_object_v1.schema.json
│       │   ├── projected_relationship_v1.schema.json
│       │   ├── mapping_execution_v1.schema.json
│       │   ├── projection_audit_v1.schema.json
│       │   └── projection_diagnostics_v1.schema.json
│       └── profiles/
│           ├── orthodox_astrology/
│           │   ├── manifest.json
│           │   ├── profile.py
│           │   ├── mappings.py
│           │   └── ontology.json
│           └── cognitive_architecture_demo/
│               ├── manifest.json
│               ├── profile.py
│               ├── mappings.py
│               └── ontology.json
├── tests/
│   ├── fixtures/
│   ├── test_contracts.py
│   ├── test_engine.py
│   ├── test_registry.py
│   ├── test_audit.py
│   ├── test_orthodox_profile.py
│   ├── test_cognitive_demo_profile.py
│   └── test_determinism.py
└── examples/
    ├── project_orthodox.py
    ├── project_cognitive_demo.py
    └── contexts/
```

The exact package/repository name may be selected during extraction. For planning purposes, this document uses `semantic_projection`.

### 4.2 Astrology SDK integration layout

After extraction, the Astrology Analysis SDK should retain only an adapter such as:

```text
src/astro_analysis_sdk/projection_adapter.py
```

Responsibilities:

1. read an SDK package;
2. extract canonical and structural source contracts;
3. provide SDK-specific registries where available;
4. construct a generic `ProjectionRequest`;
5. call `semantic_projection.project()`;
6. optionally embed or write the result.

The adapter should not contain profile rules.

---

## 5. Core contracts

The exact field names may evolve during implementation, but Chunk 2 should preserve these conceptual contracts.

### 5.1 Projection profile manifest

```json
{
  "profile_id": "orthodox_astrology.v1",
  "profile_version": "1.0.0",
  "engine_contract_version": "1.0.0",
  "source_ontology": "canonical_astrology_graph.v1",
  "target_ontology": "orthodox_astrology.v1",
  "implementation": {
    "type": "python",
    "entrypoint": "semantic_projection.profiles.orthodox_astrology.profile:OrthodoxAstrologyProfile"
  },
  "supported_source_graph_types": [
    "natal",
    "synastry",
    "composite",
    "davison",
    "transit",
    "solar_return",
    "lunar_return",
    "eclipse_lunation",
    "annual_profection"
  ],
  "required_context_fields": [],
  "optional_context_fields": [
    "relationship_type",
    "age_band",
    "application_context",
    "audience",
    "constraints"
  ],
  "mapping_rule_namespace": "orthodox_astrology.v1",
  "output_contract": "projected_semantic_graph.v1",
  "deterministic": true
}
```

### 5.2 Projection context

```json
{
  "context_id": "orthodox.general.v1",
  "context_version": "1.0.0",
  "subject_scope": "individual",
  "relationship_type": null,
  "age_band": null,
  "target_domain": "orthodox_astrology",
  "application_context": "general_interpretation",
  "audience": "adult_general",
  "output_intent": "structured_semantic_model",
  "constraints": {},
  "parameters": {},
  "extensions": {}
}
```

Context must be serializable and hashable for deterministic output identity.

### 5.3 Projection request

```json
{
  "request_id": "projection_request:<stable-hash>",
  "profile_id": "orthodox_astrology.v1",
  "profile_version": "1.0.0",
  "source_graph": {},
  "structural_evidence": {},
  "source_identity": {
    "source_chart_id": "natal:kevin",
    "source_chart_ids": ["natal:kevin"],
    "sensor_instance_id": "natal:kevin"
  },
  "context": {},
  "source_registries": {},
  "options": {
    "retain_unmapped_sources": true,
    "include_audit": true,
    "include_diagnostics": true
  }
}
```

The generic project should not require the entire Astrology SDK package.

### 5.4 Projected object

```json
{
  "id": "projected:orthodox_astrology.v1:<stable-token>",
  "object_type": "orthodox_semantic_primitive",
  "name": "relationship_value",
  "target_ontology": "orthodox_astrology.v1",
  "operators": ["value", "attract", "harmonize"],
  "attributes": {},
  "source_refs": ["canonical:natal:Venus"],
  "mapping_rule_refs": [
    "orthodox_astrology.v1.object.venus.relationship_value"
  ],
  "context_refs": ["orthodox.general.v1"],
  "structural_strength_score": 0.82,
  "projection_relevance_score": 0.91,
  "provenance": {}
}
```

### 5.5 Projected relationship

```json
{
  "id": "projected_relation:orthodox_astrology.v1:<stable-token>",
  "relationship_type": "destabilizes_or_updates",
  "source_id": "projected:...change_pressure",
  "target_id": "projected:...relationship_value",
  "operators": ["polarize", "stress", "update"],
  "theme_tags": ["growth_edge", "change_pressure"],
  "source_relationship_refs": [
    "canonical:aspect:Uranus:square:Venus"
  ],
  "mapping_rule_refs": [
    "orthodox_astrology.v1.aspect.square.change_policy"
  ],
  "context_refs": ["orthodox.general.v1"],
  "projection_relevance_score": 0.88,
  "provenance": {}
}
```

### 5.6 Mapping execution record

```json
{
  "execution_id": "mapping_execution:<stable-token>",
  "mapping_rule_id": "orthodox_astrology.v1.aspect.square.change_policy",
  "mapping_rule_version": "1.0.0",
  "source_refs": ["canonical:aspect:Uranus:square:Venus"],
  "context_refs": ["orthodox.general.v1"],
  "conditions_evaluated": [],
  "result_refs": ["projected_relation:..."],
  "status": "applied",
  "warnings": []
}
```

### 5.7 Projection audit

```json
{
  "profile_id": "orthodox_astrology.v1",
  "profile_version": "1.0.0",
  "engine_version": "1.0.0",
  "request_hash": "...",
  "source_graph_hash": "...",
  "context_hash": "...",
  "mapping_executions": [],
  "coverage": {
    "source_object_count": 189,
    "mapped_source_object_count": 189,
    "unmapped_source_object_count": 0,
    "source_relationship_count": 4239,
    "mapped_source_relationship_count": 3890,
    "unmapped_source_relationship_count": 349
  },
  "unmapped_source_refs": [],
  "fallbacks": [],
  "diagnostics_ref": "projection_diagnostics"
}
```

### 5.8 Projected semantic graph package

```json
{
  "metadata": {
    "package_type": "projected_semantic_graph",
    "projection_id": "projection:<stable-token>",
    "created_at": "...",
    "engine_version": "1.0.0",
    "profile_id": "orthodox_astrology.v1",
    "profile_version": "1.0.0",
    "context_id": "orthodox.general.v1",
    "context_version": "1.0.0"
  },
  "source_identity": {},
  "source_graph_ref": {},
  "target_ontology": "orthodox_astrology.v1",
  "objects": [],
  "relationships": [],
  "indexes": {},
  "summary": {},
  "audit": {},
  "diagnostics": {}
}
```

---

## 6. Reference profile 1: `orthodox_astrology.v1`

### 6.1 Purpose

This profile formalizes the existing conventional astrology interpretation layer.

It should preserve familiar astrology-domain vocabulary while making all interpretive additions explicit and auditable.

### 6.2 Required behavior

The profile should map:

- canonical planets and points to conventional semantic primitives;
- signs and houses to orthodox domains and modes;
- aspects to orthodox interaction operators;
- timing relationships to orthodox activation vocabulary;
- Synastry contacts and overlays to relationship-domain themes;
- Composite/Davison objects to relationship-entity semantics;
- evidence lineage and structural strength into projected relevance without erasing source metadata.

### 6.3 Registry-aware Synastry acceptance requirement

The first major regression test should use an existing Synastry contact with:

```text
theme_key
theme_registry
```

The projected relationship must include the complete registry-resolved set.

Example:

```text
theme_key:
communication | ease_support | home_family
```

Expected projected themes:

```json
[
  "communication",
  "ease_support",
  "home_family"
]
```

The engine/profile must not reduce this to only:

```json
["ease_support"]
```

derived from the trine aspect.

### 6.4 Context proof within orthodox astrology

At least two contexts should be implemented:

```text
orthodox.relationship.general.v1
orthodox.relationship.professional.v1
```

These contexts should share the same canonical sources but adjust target-domain vocabulary, allowable themes, or salience.

A Venus–Mercury contact might produce:

```text
general:
affectionate communication, rapport, shared taste

professional:
diplomacy, values alignment, collaborative exchange
```

The projected output remains structured; prose examples are explanatory only.

### 6.5 Compatibility target

The orthodox profile should make current report consumers possible without using legacy hidden theme logic.

It does not need to produce final claims or prose. It should produce the projected semantic rows and theme structures from which later reasoning can operate.

---

## 7. Reference profile 2: `cognitive_architecture_demo.v0`

### 7.1 Why this profile

The original projected-chart work began with cognitive-domain mapping. A small cognitive architecture profile is therefore historically appropriate and proves that the engine can produce a genuinely different ontology rather than merely reorganizing orthodox astrology.

It is also simple enough to constrain carefully.

### 7.2 Explicit demo status

This profile should be labeled:

```text
experimental
demo
not a validated psychological model
```

Its purpose is architectural proof, not scientific diagnosis.

### 7.3 Limited source scope

To prevent scope explosion, version `v0` should initially support only:

- core planets/luminaries;
- major aspects;
- optionally angles;
- Natal source graphs;
- one simple context.

Unsupported expanded objects should be retained as unmapped diagnostics rather than force-fit.

### 7.4 Example target ontology

A modest target ontology might include:

```text
identity_organization
attention_orientation
emotional_regulation
valuation_preference
action_selection
constraint_management
meaning_abstraction
change_adaptation
imagination_permeability
communication_processing
```

Illustrative primitive mappings:

| Canonical source | Cognitive target primitive |
|---|---|
| Sun | identity organization / central coherence |
| Moon | emotional regulation / safety-state memory |
| Mercury | information processing / symbolic exchange |
| Venus | valuation / preference weighting / harmonization |
| Mars | action selection / mobilization / assertion |
| Jupiter | expansion / abstraction / possibility generation |
| Saturn | constraint / structure / inhibition / durability |
| Uranus | novelty / discontinuity / change adaptation |
| Neptune | permeability / imagination / ambiguity processing |
| Pluto | deep transformation / control / intensity processing |

Major aspects can map to interaction operators:

| Aspect | Example cognitive interaction |
|---|---|
| conjunction | fuse / co-activate |
| opposition | polarize / alternate / mirror |
| square | interfere / pressure / force adaptation |
| trine | facilitate / automate / support |
| sextile | enable / offer coordination |

### 7.5 Projection-first reasoning proof

The profile should demonstrate that a source relationship is reasoned between mapped target primitives.

Example:

```text
Mars square Venus
```

must not be projected by translating finished romance prose.

Instead:

```text
Mars
→ action_selection

Venus
→ valuation_preference

square
→ interfere / force adaptation
```

Projected result:

```text
action selection and value evaluation create friction or require active coordination
```

This should be stored as structured operators and relationships, not final prose.

### 7.6 Demo acceptance criteria

- at least ten core objects project successfully;
- major aspects project into cognitive interaction relationships;
- source refs and mapping-rule refs are complete;
- unmapped expanded objects are reported cleanly;
- canonical graph remains unchanged;
- results are deterministic;
- output ontology is visibly different from orthodox astrology.

---

## 8. Development sequence

The following version numbers describe implementation rounds. If a round requires cleanup passes, use patch-like extensions such as `2.2.1`, `2.2.2`, and so forth.

---

# Chunk 2.1 — Contracts, schemas, and extraction-ready package skeleton

## Objective

Create the generic projection package skeleton and its plain-data contracts without implementing substantive profile semantics.

## Work

### Code

Add an internal package:

```text
src/astro_analysis_sdk/projection/
```

Initial modules:

```text
contracts.py
ids.py
diagnostics.py
audit.py
validation.py
io.py
```

The code should have no imports from:

```text
astro_analysis_sdk.pipelines
astro_analysis_sdk.ephemeris
pyswisseph
```

Temporary imports from SDK schema utilities may be tolerated but should be identified for later extraction.

### Contracts

Implement typed dataclasses or similarly explicit Python models for:

- `ProjectionProfileManifest`;
- `ProjectionContext`;
- `ProjectionRequest`;
- `ProjectedObject`;
- `ProjectedRelationship`;
- `MappingExecution`;
- `ProjectionAudit`;
- `ProjectionDiagnostics`;
- `ProjectedSemanticGraph`.

Models must serialize to plain dictionaries/JSON.

### Schemas

Add the schemas listed in Section 4.1.

### IDs

Define deterministic ID functions for:

- projection request;
- projected package;
- projected object;
- projected relationship;
- mapping execution.

Hashes should depend on normalized stable inputs, never generation timestamp or dictionary insertion accidents.

### Validation

Add:

- schema validation;
- profile/context compatibility validation;
- source graph version checks;
- duplicate projected-ID checks.

## Tests

Keep tests focused:

- round-trip serialization;
- schema validation;
- deterministic IDs;
- invalid manifest/profile/context errors;
- no SDK pipeline imports from projection core.

## Documentation

Add:

```text
docs/Chunk 2 Projection Contracts.md
```

Update architecture docs with the extraction-ready package boundary.

## Acceptance criteria

- a projection request can be serialized and validated;
- an empty projected graph can be created deterministically;
- contracts contain no astrology calculation dependencies;
- schemas are self-consistent;
- no actual mapping semantics are required yet.

## Expected review artifacts

- contract examples;
- schema examples;
- import-dependency report;
- tiny projected graph fixture.

---

# Chunk 2.2 — Generic engine, profile interface, and registry

## Objective

Implement a minimal engine capable of loading a profile and projecting source rows through profile-supplied rules.

## Work

### Profile protocol

Define a profile interface approximately like:

```python
class ProjectionProfile(Protocol):
    manifest: ProjectionProfileManifest

    def validate_context(self, context: ProjectionContext) -> list[Diagnostic]:
        ...

    def project_object(
        self,
        source_object: dict,
        request: ProjectionRequest,
    ) -> list[ProjectedObjectDraft]:
        ...

    def project_relationship(
        self,
        source_relationship: dict,
        projected_object_index: dict,
        request: ProjectionRequest,
    ) -> list[ProjectedRelationshipDraft]:
        ...

    def finalize(
        self,
        graph: ProjectedSemanticGraph,
        request: ProjectionRequest,
    ) -> None:
        ...
```

The profile should return drafts/results while the engine owns:

- deterministic IDs;
- provenance envelope;
- audit records;
- merge policy;
- ordering;
- diagnostics;
- output materialization.

### Registry

Implement a registry that:

- registers built-in profiles;
- loads manifests;
- resolves exact profile/version;
- rejects ambiguous or unsupported versions;
- permits future entry-point/plugin discovery.

### Engine flow

```text
validate request
load profile
validate context
index canonical source graph
project objects
project relationships
resolve references
merge compatible outputs
record mapping executions
record unmapped sources
finalize graph
sort deterministically
validate output
```

### Unmapped policy

Support options:

```text
retain as diagnostic
retain as passthrough placeholder
ignore with warning
fail
```

Default should be diagnostic retention.

### Merge policy

Profiles may map multiple source rows to one projected primitive. The engine must merge without losing source refs or mapping-rule refs.

## Tests

- mock profile projects one object and one relationship;
- multi-source merge preserves all source refs;
- unmapped rows appear in diagnostics;
- deterministic output ordering;
- profile registry exact-version resolution;
- canonical input remains byte-equivalent after projection.

## Acceptance criteria

- engine works with a toy mock profile;
- audit covers every applied mapping;
- unmapped coverage is measurable;
- no orthodox or cognitive semantics are hard-coded in the engine.

---

# Chunk 2.3 — Orthodox profile foundation

## Objective

Implement the first real profile for core objects and major aspects.

## Work

### Profile package

Add:

```text
projection/profiles/orthodox_astrology/
```

with:

```text
manifest.json
profile.py
ontology.json
object_mappings.py
relationship_mappings.py
context.py
```

### Core object mappings

Initially cover:

- Sun;
- Moon;
- Mercury;
- Venus;
- Mars;
- Jupiter;
- Saturn;
- Uranus;
- Neptune;
- Pluto;
- Ascendant;
- Midheaven;
- other angles where straightforward.

### Major aspects

Cover:

- conjunction;
- opposition;
- square;
- trine;
- sextile.

Preserve source operators from canonical rows while adding orthodox target operators and themes.

### Projection relevance

Define a profile-specific relevance score distinct from structural strength.

The initial formula may combine:

```text
structural strength
× profile object salience
× profile relationship salience
× context salience
```

Every component must be reported in audit metadata. Do not call the result calibrated confidence.

### Current compatibility

Use existing theme helpers and orthodox mapping knowledge where useful, but place them inside the profile package rather than generic SDK code.

## Tests

Use small Natal fixtures:

- Venus object maps to orthodox value/attraction/harmonization primitives;
- Mars square Venus maps to expected orthodox themes/operators;
- canonical row has no theme tags after projection;
- projected row contains complete provenance;
- deterministic IDs and ordering.

## Acceptance criteria

- core Natal chart projects into a nonempty orthodox graph;
- major aspects project correctly;
- current orthodox row adapter can be implemented by reading the projected output rather than recomputing themes separately.

---

# Chunk 2.4 — Registry-aware Synastry and relationship projection

## Objective

Prove the profile on the most demanding current row-level use case and retire the provisional Synastry limitation.

## Work

### Source-registry adapter

The Astrology SDK adapter should supply:

- Synastry `theme_registry`;
- operator registry;
- object registries;
- natal-context registry;
- relationship metrics where relevant as profile inputs, not canonical facts.

### Complete theme resolution

Implement:

```text
contact.theme_key
→ source theme_registry
→ orthodox projected relationship themes
```

Merge with object/aspect-derived themes without duplicates and preserve origin metadata:

```json
{
  "theme": "home_family",
  "origin": "source_registry",
  "source_ref": "theme_registry:<key>"
}
```

### House overlays

Project house overlays into explicit orthodox relationship-domain structures while preserving target-house nodes and person direction.

### Context modes

Add:

```text
orthodox.relationship.general.v1
orthodox.relationship.professional.v1
```

Professional context should:

- avoid romance-only vocabulary;
- preserve source structures;
- alter target labels and salience;
- expose context-driven mapping decisions in audit records.

### SDK analysis views

Replace or wrap the provisional `orthodox_row_annotation()` behavior so compact Natal, Transit, and Synastry views can use the real profile result or a small compatibility facade over it.

Avoid running a full expensive projection repeatedly per row. Use batch projection and indexes.

## Tests

- known Synastry `theme_key` resolves to all registry themes;
- aspect fallback themes remain represented with distinct origin;
- professional context changes target vocabulary/salience;
- canonical Synastry graph stays clean;
- directional person/house references remain correct;
- compact analysis rows can be reconstructed from projected graph indexes.

## Acceptance criteria

- the known Chunk 1.5 Synastry limitation is eliminated;
- report-facing relationship rows derive from the real profile;
- same source/context/profile produces deterministic output;
- different context produces a controlled, auditable difference.

---

# Chunk 2.5 — Standalone projection pipeline and CLI/API

## Objective

Make projection independently callable rather than only an internal package-finalization side effect.

## Python API

Provide:

```python
from astro_analysis_sdk.projection import project_dataset

result = project_dataset(
    source_package,
    profile_id="orthodox_astrology.v1",
    context=projection_context,
)
```

Internally, the API must construct a generic request and call the generic engine.

## CLI

Add something like:

```bat
python -m astro_analysis_sdk.cli project ^
  --source-dataset kevin_natal_dataset.json ^
  --projection-profile orthodox_astrology.v1 ^
  --projection-context orthodox_general_context.json ^
  --out kevin_natal_orthodox_projection.json
```

Support:

- context file;
- minimal inline context options where safe;
- profile/version selection;
- output path;
- audit inclusion;
- diagnostics inclusion;
- fail-on-unmapped threshold;
- summary-only output if useful.

## Output modes

At minimum:

```text
full projected package
projection summary
```

Do not add streaming/game-specific output in Chunk 2 unless trivially derived.

## SDK package integration

Full SDK packages may continue to include:

```text
projection_views["orthodox_astrology.v1"]
```

but the preferred implementation should derive that view from the same engine/profile, not separate hard-coded logic.

Standalone projected output remains the primary proof of decoupling.

## Tests

- CLI can project a small Natal fixture;
- output validates against schema;
- embedded and standalone orthodox projections agree on shared content;
- unknown profile errors clearly;
- invalid context errors clearly.

## Acceptance criteria

- projection is a standalone operation;
- SDK calculation pipelines need not rerun;
- consumers can project an existing package later with a different context/profile.

---

# Chunk 2.6 — Cognitive architecture demo profile

## Objective

Prove that the engine supports a genuinely different ontology.

## Work

Implement:

```text
cognitive_architecture_demo.v0
```

Scope:

- Natal only;
- core planets/luminaries;
- major aspects;
- one context:
  `cognitive_architecture.general.v0`;
- unsupported expanded objects remain visible in diagnostics.

### Mapping model

Map source objects into cognitive primitives and aspects into interaction operators as described in Section 7.

### Guardrails

The profile manifest and output must state:

- experimental demonstration;
- not clinical;
- not empirically validated;
- not a diagnostic instrument;
- intentionally incomplete source coverage.

### Comparison fixture

Project the same Natal fixture through:

```text
orthodox_astrology.v1
cognitive_architecture_demo.v0
```

Demonstrate:

- identical source graph identity;
- different target ontology;
- different projected objects and relationships;
- common provenance model;
- no source mutation.

## Tests

- core objects map to cognitive primitives;
- Mars–Venus square is reasoned between mapped target primitives;
- profile output contains no orthodox romance tags unless explicitly part of a mapping;
- unsupported source types appear in diagnostics;
- deterministic output.

## Acceptance criteria

- second profile uses the same engine and contracts;
- no engine changes are needed solely because the ontology differs;
- output visibly proves projection-first reasoning.

---

# Chunk 2.7 — Stabilization, profiling, and extraction preparation

## Objective

Use real Kevin/Bre/Brandi packages and generated fixture sets to identify defects before repository separation.

## Fixture review

Generate standalone projections for representative packages:

- Kevin Natal, orthodox;
- Kevin Natal, cognitive demo;
- Kevin/Bre Synastry, orthodox general;
- Kevin/Bre Synastry, orthodox professional;
- Kevin/Bre Composite, orthodox;
- Kevin/Bre Davison, orthodox;
- selected Transit package, orthodox;
- selected Solar Return or Lunar Return package, orthodox.

### Review dimensions

- projected object/relationship counts;
- mapping coverage;
- unmapped source distribution;
- deterministic ordering;
- file size;
- audit size;
- duplicate source refs;
- theme completeness;
- context sensitivity;
- canonical immutability;
- profile execution time;
- registry resolution;
- nested graph behavior.

### Materialization policy

Decide whether audit records are:

```text
embedded full
compact embedded + external audit
optional
```

Avoid allowing projection audit to recreate Chunk 1’s file-size explosion.

### Extraction readiness audit

Check for imports from:

```text
astro_analysis_sdk.*
```

inside generic projection modules. Move SDK-specific adapters out of the core.

## Acceptance criteria

- rich fixture corpus produces stable results;
- no unresolved canonical contamination;
- audit size and projected output size are practical;
- generic core has a clean dependency graph;
- remaining issues are profile-specific rather than architectural.

---

# Chunk 2.8 — Separate projection layer into its own GitHub project

## Objective

Create the independent projection repository and make the Astrology Analysis SDK consume it as an external dependency or local editable/submodule dependency.

## Repository extraction

Move:

```text
projection core
contracts
schemas
engine
registry
audit
diagnostics
orthodox profile
cognitive demo profile
generic tests/docs/examples
```

into the new project.

Keep in Astrology Analysis SDK:

```text
SDK source-package adapter
optional CLI bridge
package embedding integration
SDK-specific fixture generation
```

## Dependency approach

During local development, support one or more:

```text
pip install -e ..\semantic-projection
Git submodule
path dependency in development tooling
published package later
```

Do not require publishing to PyPI to complete Chunk 2.

## Contract ownership

The independent project should own:

- projection request/context/profile schemas;
- projected graph schemas;
- engine/profile protocols;
- audit/diagnostics contracts.

The Astrology SDK should own:

- canonical astrology graph;
- structural evidence graph;
- astrology package schemas;
- adapters from package-specific registries.

## Cross-repository integration tests

In the SDK:

- project a Natal package through external orthodox profile;
- project Synastry with registry adapters;
- verify source identity and provenance;
- verify embedded and standalone results.

In the projection repo:

- use generic canonical fixtures independent of the Astrology SDK;
- test both reference profiles;
- test plugin/profile registry behavior.

## Documentation handoff

New project documentation must include:

- architecture;
- installation;
- API;
- CLI if retained there;
- profile authoring;
- context authoring;
- audit interpretation;
- reference profiles;
- known limitations;
- extraction history.

Update Astrology SDK docs to point downstream:

```text
Astrology Analysis SDK
→ canonical source packages

Semantic Projection
→ target-domain projected models
```

## Completion criteria

Chunk 2 is complete when:

1. the new projection repository installs independently;
2. it has no dependency on astrology calculation pipelines;
3. it contains both reference profiles;
4. the SDK calls it through a narrow adapter;
5. orthodox Synastry registry themes resolve completely;
6. the cognitive demo proves a distinct ontology;
7. standalone projection works from saved SDK packages;
8. projected results retain complete provenance and audit paths;
9. context affects output predictably;
10. current canonical packages require no schema-breaking redesign.

---

## 9. Recommended implementation discipline

### 9.1 Keep each development round narrow

Chunk 1 demonstrated that subtle boundary work benefits from iterative fixture review. Each Chunk 2 round should end with:

- updated repo archive;
- brief change summary;
- focused tests;
- one or two generated projection fixtures where applicable.

Do not attempt full Kevin/Bre/Brandi generation inside the build response when it risks timeouts. Generate large fixtures locally afterward and analyze them in chat.

### 9.2 Prefer fixture analysis over speculative abstraction

The engine should grow in response to actual profile needs. Avoid designing a universal projection DSL before two profiles have proved which abstractions are truly shared.

### 9.3 Preserve old behavior only when it remains useful

No downstream consumer currently requires strict backward compatibility for provisional `projection_views`. Prefer a clean migration to the real engine, with temporary adapters only where they help compare outputs.

### 9.4 Keep audits useful but bounded

A mapping execution per source row can become large. Consider:

- audit registries;
- mapping-rule registries;
- source-ref arrays;
- compact audit summaries;
- optional full audit output.

Auditability must remain, but repeated payload should not multiply unnecessarily.

### 9.5 Treat profile configuration as versioned code

A profile version changes when mapping behavior changes materially. Context versions should also be explicit. Generated projections must record both.

---

## 10. Testing strategy

### 10.1 Unit tests

Use small hand-built canonical graphs for:

- deterministic IDs;
- mapping application;
- merge behavior;
- context conditions;
- diagnostics;
- audit paths;
- schema validation.

### 10.2 Golden fixtures

Maintain tiny stable fixtures for:

- orthodox Natal;
- orthodox Synastry;
- professional Synastry context;
- cognitive Natal demo.

Golden fixtures should be small enough for repository tests and code review.

### 10.3 Rich external fixtures

Use the 58-file Kevin/Bre/Brandi corpus outside the normal unit suite for post-round analysis:

- coverage;
- file size;
- runtime;
- mapping completeness;
- unexpected unmapped families;
- profile consistency.

### 10.4 Determinism tests

Run identical projection twice and compare:

- projected IDs;
- ordering;
- graph hash;
- audit hash excluding timestamps;
- diagnostics ordering.

### 10.5 Immutability tests

Hash canonical and structural inputs before and after projection. They must remain identical.

### 10.6 Cross-profile tests

The same source graph projected through two profiles should:

- share source identity;
- differ in target ontology;
- preserve independent audits;
- never leak target concepts into the other result.

---

## 11. Main risks and mitigations

### Risk: building an overambitious universal mapping language

**Mitigation:** semi-declarative manifests plus Python profile implementations; generalize only after two profiles expose common patterns.

### Risk: profile logic leaks back into the SDK

**Mitigation:** enforce dependency direction and import tests. The SDK adapter may import projection core; projection core may not import SDK pipelines.

### Risk: projection audit causes huge files

**Mitigation:** registries, compact mapping execution records, optional external full audit, and fixture-based size profiling.

### Risk: orthodox profile becomes privileged engine logic

**Mitigation:** tests using the cognitive demo profile and a mock profile; engine code contains no astrology mapping constants.

### Risk: context becomes an unbounded bag of arbitrary values

**Mitigation:** versioned core context fields plus profile-owned validation and `extensions`.

### Risk: current orthodox output cannot be reproduced exactly

**Mitigation:** define compatibility acceptance cases, especially Synastry registry themes; document intentional changes where the new profile is more explicit or correct.

### Risk: projected graph becomes a disguised claim graph

**Mitigation:** restrict projected output to target-domain objects, relationships, operators, tags, salience, and provenance. Defer assertions, support/contradiction, and narrative claims to Chunk 3.

### Risk: cognitive demo expands into a full psychological system

**Mitigation:** narrow scope, explicit demo label, core planets and major aspects only, one context, and unmapped diagnostics.

### Risk: extracting the project too early causes churn

**Mitigation:** develop internally through 2.7 with extraction-ready boundaries, then separate after contracts and two profiles stabilize.

---

## 12. Explicit non-goals for Chunk 2

Chunk 2 will not implement:

- calibrated epistemic claim confidence;
- claim graphs;
- evidence support/contradiction resolution;
- multi-sensor narrative synthesis;
- narrative units;
- standard report definitions;
- report blueprints;
- compiled `report_view`;
- prose generation;
- PDF/web/book publishing;
- Mythos game mechanics;
- full NCS/MPAS projection;
- generalized parent-child or age-aware interpretation libraries;
- group composite or multi-person projection;
- arbitrary user-authored profile DSL;
- model training or empirical validation;
- automatic selection of the “best” projection profile.

These are later projects or chunks.

---

## 13. Decisions that can remain flexible during implementation

The following need not be fixed before Chunk 2.1:

- final standalone repository name;
- dataclasses versus another lightweight typed model library;
- whether full audits embed or write separately;
- exact CLI command location after extraction;
- whether profile discovery initially uses manual registry or Python entry points;
- exact cognitive primitive labels;
- whether context IDs are files, inline objects, or both;
- whether embedded SDK projection views retain their current exact field name.

The plan should preserve the architectural contracts while allowing these implementation details to be settled through experience.

---

## 14. Suggested version/round summary

```text
2.1  Contracts, schemas, IDs, extraction-ready skeleton
2.2  Generic engine, profile protocol, registry, audit
2.3  Orthodox core objects and major aspects
2.4  Registry-aware Synastry + context-aware relationship projection
2.5  Standalone projection API/CLI and SDK integration
2.6  Cognitive architecture demo profile
2.7  Rich-fixture stabilization and extraction preparation
2.8  Separate independent projection GitHub project and integrate SDK
```

If cleanup is needed within a goal:

```text
2.4.1
2.4.2
```

rather than inventing new architectural milestones.

---

## 15. Definition of Chunk 2 success

Chunk 2 should not be judged by how many domains it can project into.

It should be judged by whether it creates a trustworthy transformation boundary.

A successful final demonstration is:

```text
one canonical Kevin Natal package
        ├── orthodox_astrology.v1
        │       → orthodox projected graph
        │
        └── cognitive_architecture_demo.v0
                → cognitive projected graph
```

and:

```text
one Kevin/Bre Synastry package
        ├── orthodox relationship general context
        │       → complete registry-aware relationship projection
        │
        └── orthodox professional context
                → audibly different professional-domain projection
```

All four outputs should:

- share stable source identities;
- leave canonical packages unchanged;
- use the same generic projection engine;
- preserve mapping-rule and source provenance;
- validate against common projected-graph contracts;
- remain independent of report prose and narrative synthesis.

At that point, the independent projection layer will be real—not merely a folder of mapping notes—and Chunk 3 can begin from projected semantic graphs rather than provisional theme tags.

---

## 16. Immediate next action

Before implementing Chunk 2.1:

1. approve or revise this roadmap;
2. choose a temporary internal package name, recommended:
   `astro_analysis_sdk.projection`;
3. choose a working standalone project/package name, recommended:
   repository `Semantic Projection Layer`,
   Python package `semantic_projection`;
4. confirm `cognitive_architecture_demo.v0` as the second reference profile;
5. begin Chunk 2.1 with contracts and schemas only.

No additional conversation-history archaeology should be necessary once this document is retained with the project.

---

## Chunk 2.7 implementation note

Chunk 2.7 was completed after the expanded cognitive, Woofmapped, projected-term-registry, and deterministic-renderer work. It added explicit projection materializations, scope-aware threshold semantics, artifact profiling, extraction-readiness inspection, and consolidated the semantic/publication-layer findings that emerged during Chunk 2.6. Chunk 2.8 should begin from these implemented foundations.
