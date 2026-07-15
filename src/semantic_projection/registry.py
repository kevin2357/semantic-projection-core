from __future__ import annotations

from importlib import metadata
from typing import Iterable

from .profile import ProjectionProfile


class ProjectionProfileRegistryError(LookupError):
    pass


class ProjectionProfileRegistry:
    """Exact-version profile registry with optional entry-point discovery."""

    def __init__(self) -> None:
        self._profiles: dict[tuple[str, str], ProjectionProfile] = {}

    def register(self, profile: ProjectionProfile, *, replace: bool = False) -> None:
        manifest = profile.manifest
        key = (manifest.profile_id, manifest.profile_version)
        if key in self._profiles and not replace:
            raise ProjectionProfileRegistryError(
                f"Profile {manifest.profile_id!r} version {manifest.profile_version!r} "
                "is already registered"
            )
        self._profiles[key] = profile

    def resolve(self, profile_id: str, profile_version: str) -> ProjectionProfile:
        key = (profile_id, profile_version)
        try:
            return self._profiles[key]
        except KeyError as exc:
            versions = sorted(
                version for candidate, version in self._profiles if candidate == profile_id
            )
            if versions:
                raise ProjectionProfileRegistryError(
                    f"Profile {profile_id!r} does not have version {profile_version!r}; "
                    f"available versions: {versions}"
                ) from exc
            raise ProjectionProfileRegistryError(
                f"Unknown projection profile {profile_id!r}"
            ) from exc

    def manifests(self) -> list[dict]:
        return [
            profile.manifest.to_dict()
            for _, profile in sorted(self._profiles.items())
        ]

    def discover_entry_points(
        self,
        *,
        group: str = "semantic_projection.profiles",
        replace: bool = False,
    ) -> int:
        """Load profiles exposed by Python entry points.

        Discovery is optional in the embedded SDK phase but establishes the
        plugin boundary needed after repository extraction.
        """
        count = 0
        selected: Iterable = metadata.entry_points().select(group=group)
        for entry_point in selected:
            loaded = entry_point.load()
            profile = loaded() if isinstance(loaded, type) else loaded
            self.register(profile, replace=replace)
            count += 1
        return count
