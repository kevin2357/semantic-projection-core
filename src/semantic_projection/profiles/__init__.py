"""Built-in reference projection profiles."""

from semantic_projection.registry import ProjectionProfileRegistry

from .cognitive_architecture_demo import CognitiveArchitectureDemoProfile
from .orthodox_astrology import OrthodoxAstrologyProfile
from .woofmapped_astrology import WoofmappedAstrologyProfile
from .woofmapped_bounded_astrology import WoofmappedBoundedAstrologyProfile


def builtin_projection_registry() -> ProjectionProfileRegistry:
    registry = ProjectionProfileRegistry()
    registry.register(OrthodoxAstrologyProfile())
    registry.register(CognitiveArchitectureDemoProfile())
    registry.register(WoofmappedAstrologyProfile())
    registry.register(WoofmappedBoundedAstrologyProfile())
    return registry


__all__ = [
    "CognitiveArchitectureDemoProfile",
    "OrthodoxAstrologyProfile",
    "WoofmappedAstrologyProfile",
    "WoofmappedBoundedAstrologyProfile",
    "builtin_projection_registry",
]
