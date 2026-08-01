from __future__ import annotations

import pytest

from semantic_projection.rendering import (
    ProjectedTermResolutionError,
    render_local_narrative,
    render_object_sentence,
    render_relationship_sentence,
)
from semantic_projection.rendering.resolver import ProjectedTermResolver, object_index


def graph_fixture() -> dict:
    registry = {
        "registry_id": "test.projected_terms",
        "registry_version": "0.1.0",
        "target_ontology": "test.v0",
        "terms": {
            "pack_role_identity": {
                "term_type": "operator",
                "canonical_label": "Pack-Role Identity",
                "friendly_labels": ["pack role identity"],
                "short_description": "Coordinates identity and role within the pack.",
                "core_operators": ["coordinate", "belong", "organize"],
                "output_guidance": {"noun_phrase": "identity and role within the pack"},
            },
            "social_harmony_maintenance_mode": {
                "term_type": "mode",
                "canonical_label": "Social-Harmony Maintenance Mode",
                "friendly_labels": ["social harmony maintenance mode"],
                "short_description": "Preserves social balance and cohesion.",
                "output_guidance": {"adverbial_phrase": "in a socially balancing, cohesion-maintaining way"},
            },
            "doghouse_8_deep_trust_vulnerability": {
                "term_type": "domain",
                "canonical_label": "Doghouse 8: Deep Trust and Vulnerability",
                "friendly_labels": ["Doghouse 8 deep trust vulnerability"],
                "short_description": "Deep attachment, vulnerability, surrender, and shared risk.",
                "output_guidance": {"context_phrase": "where deep trust and vulnerability are involved"},
            },
            "training_rule_structure": {
                "term_type": "operator",
                "canonical_label": "Training-Rule Structure",
                "friendly_labels": ["training rule structure"],
                "short_description": "Creates predictable rules and routines.",
                "core_operators": ["train", "sequence", "stabilize"],
                "output_guidance": {"noun_phrase": "training and rule structure"},
            },
            "trainable_usable_channel": {
                "term_type": "relation",
                "canonical_label": "Trainable Usable Channel",
                "friendly_labels": ["trainable usable channel"],
                "short_description": "A relationship that supports deliberate coordination.",
                "output_guidance": {"verb_phrase": "trainable usable channel"},
            },
        },
    }
    objects = [
        {
            "id": "o:identity",
            "name": "pack_role_identity",
            "operators": ["coordinate"],
            "attributes": {
                "projected_mode": "social_harmony_maintenance_mode",
                "projected_domain": "doghouse_8_deep_trust_vulnerability",
            },
        },
        {
            "id": "o:training",
            "name": "training_rule_structure",
            "operators": ["train"],
            "attributes": {},
        },
    ]
    relationships = [
        {
            "id": "r:1",
            "source_id": "o:identity",
            "target_id": "o:training",
            "relationship_type": "trainable_usable_channel",
            "projection_relevance_score": 0.9,
            "attributes": {},
        }
    ]
    return {"projected_term_registry": registry, "objects": objects, "relationships": relationships}


def test_natural_object_composition_is_deterministic_and_hides_raw_keys():
    graph = graph_fixture()
    row = graph["objects"][0]
    first = render_object_sentence(row, graph["projected_term_registry"], subject="Nivek")
    second = render_object_sentence(row, graph["projected_term_registry"], subject="Nivek")
    assert first == second
    assert "pack_role_identity" not in first.text
    assert "social_harmony_maintenance_mode" not in first.text
    assert "doghouse_8_deep_trust_vulnerability" not in first.text
    assert "Nivek's identity and role within the pack" in first.text
    assert first.semantic_components == {
        "operator": "pack_role_identity",
        "mode": "social_harmony_maintenance_mode",
        "domain": "doghouse_8_deep_trust_vulnerability",
        "verbs": ["coordinate", "belong", "organize"],
    }


def test_relationship_rendering_preserves_source_relation_and_target():
    graph = graph_fixture()
    rendered = render_relationship_sentence(
        graph["relationships"][0], object_index(graph), graph["projected_term_registry"], subject="Nivek"
    )
    assert "identity and role within the pack" in rendered.text
    assert "deliberately coordinated" in rendered.text
    assert "training and rule structure" in rendered.text
    assert rendered.semantic_components["relation"] == "trainable_usable_channel"


def test_local_narrative_is_bounded_and_traceable():
    graph = graph_fixture()
    result = render_local_narrative(graph, "o:identity", subject="Nivek", relationship_limit=1)
    assert len(result.relationship_sentences) == 1
    assert len(result.source_term_refs) == 5
    assert result.paragraph.startswith("Nivek's identity")
    assert result.template_ids == [
        "object.natural.subject_mode_domain.v1",
        "relationship.natural.active.v1",
    ]


def test_unresolved_term_fails_clearly():
    graph = graph_fixture()
    graph["objects"][0]["name"] = "not_registered"
    try:
        render_object_sentence(graph["objects"][0], graph["projected_term_registry"], subject="Nivek")
    except ProjectedTermResolutionError as exc:
        assert "unresolved projected term" in str(exc)
    else:
        raise AssertionError("unresolved term should fail")


def test_technical_and_domain_emphasis_variants_are_traceable():
    graph = graph_fixture()
    technical = render_object_sentence(graph["objects"][0], graph["projected_term_registry"], subject="James", style="technical")
    emphasized = render_object_sentence(graph["objects"][0], graph["projected_term_registry"], subject="James", variant=1)
    assert technical.text.startswith("James' identity")
    assert technical.template_id == "object.technical.explicit_composition.v1"
    assert "most active in Doghouse 8" in emphasized.text
    assert emphasized.template_id == "object.natural.domain_emphasis.v1"


def test_relationship_technical_style_and_reverse_focus():
    graph = graph_fixture()
    rendered = render_relationship_sentence(
        graph["relationships"][0],
        object_index(graph),
        graph["projected_term_registry"],
        subject="Nivek",
        style="technical",
        focus_id="o:training",
    )
    assert rendered.text.startswith("Training And Rule Structure")
    assert rendered.template_id == "relationship.technical.explicit.v1"
    assert rendered.semantic_components["source"] == "training_rule_structure"


def test_resolver_accessors_and_empty_registry_errors():
    registry = graph_fixture()["projected_term_registry"]
    resolver = ProjectedTermResolver(registry)
    assert resolver.label("pack_role_identity") == "Pack-Role Identity"
    assert resolver.friendly_label("pack_role_identity") == "pack role identity"
    assert resolver.output_guidance("pack_role_identity")["noun_phrase"] == "identity and role within the pack"
    assert resolver.resolve_key(None) is None
    assert resolver.term_ref(None) is None
    with pytest.raises(ProjectedTermResolutionError, match="no terms"):
        ProjectedTermResolver({})


def test_local_narrative_deduplicates_and_ranks_relationships():
    graph = graph_fixture()
    duplicate = dict(graph["relationships"][0], id="r:weaker", projection_relevance_score=0.1)
    graph["relationships"].append(duplicate)
    result = render_local_narrative(graph, "o:identity", subject="Nivek", relationship_limit=4)
    assert len(result.relationship_sentences) == 1
    with pytest.raises(KeyError, match="projected object not found"):
        render_local_narrative(graph, "missing", subject="Nivek")
