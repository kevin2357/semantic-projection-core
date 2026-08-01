from __future__ import annotations

from hypothesis import given
from hypothesis import strategies as st

from semantic_projection.ids import canonical_json, projected_object_id, stable_hash

json_scalars = st.none() | st.booleans() | st.integers() | st.text(max_size=20)
json_values = st.recursive(
    json_scalars,
    lambda children: st.lists(children, max_size=5) | st.dictionaries(st.text(min_size=1, max_size=10), children, max_size=5),
    max_leaves=20,
)


@given(json_values)
def test_canonical_hash_is_stable_for_json_round_trip(value):
    assert stable_hash(value) == stable_hash(value)
    assert canonical_json(value) == canonical_json(value)


@given(st.lists(st.text(min_size=1, max_size=10), min_size=1, max_size=8, unique=True))
def test_projected_object_identity_is_source_order_independent(source_refs):
    assert projected_object_id(
        profile_id="profile.v1",
        target_key="operator",
        source_refs=source_refs,
        context_id="context.v1",
    ) == projected_object_id(
        profile_id="profile.v1",
        target_key="operator",
        source_refs=list(reversed(source_refs)),
        context_id="context.v1",
    )
