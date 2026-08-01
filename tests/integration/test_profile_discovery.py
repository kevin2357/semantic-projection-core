from __future__ import annotations

import semantic_projection.registry as registry_module
from semantic_projection import ProjectionProfileRegistry
from semantic_projection.profiles.demo import DemonstrationProjectionProfile


class FakeEntryPoint:
    def load(self):
        return DemonstrationProjectionProfile


class FakeEntryPoints:
    def select(self, *, group):
        assert group == "semantic_projection.profiles"
        return [FakeEntryPoint()]


def test_installed_profile_entry_point_discovery(monkeypatch):
    monkeypatch.setattr(registry_module.metadata, "entry_points", lambda: FakeEntryPoints())
    registry = ProjectionProfileRegistry()
    assert registry.discover_entry_points() == 1
    profile = registry.resolve("demonstration_projection.v0", "0.1.0")
    assert profile.manifest.status == "reference_test_profile"


def test_entry_point_discovery_can_replace_an_existing_profile(monkeypatch):
    monkeypatch.setattr(registry_module.metadata, "entry_points", lambda: FakeEntryPoints())
    registry = ProjectionProfileRegistry()
    registry.register(DemonstrationProjectionProfile())
    assert registry.discover_entry_points(replace=True) == 1
