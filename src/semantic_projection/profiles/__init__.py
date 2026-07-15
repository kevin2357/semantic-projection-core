"""Built-in reference projection profiles."""

from semantic_projection.registry import ProjectionProfileRegistry
from .orthodox_astrology import OrthodoxAstrologyProfile
from .cognitive_architecture_demo import CognitiveArchitectureDemoProfile
from .woofmapped_astrology import WoofmappedAstrologyProfile


def builtin_projection_registry() -> ProjectionProfileRegistry:
    registry = ProjectionProfileRegistry()
    registry.register(OrthodoxAstrologyProfile())
    registry.register(CognitiveArchitectureDemoProfile())
    registry.register(WoofmappedAstrologyProfile())
    return registry


__all__ = [
    "OrthodoxAstrologyProfile",
    "CognitiveArchitectureDemoProfile",
    "WoofmappedAstrologyProfile",
    "builtin_projection_registry",
]
