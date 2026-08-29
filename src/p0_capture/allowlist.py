"""Experiment-surface allow-list and pause control."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class SurfaceAllowList:
    surfaces: set[str] = field(default_factory=set)
    active: bool = True

    def add(self, surface: str) -> None:
        self.surfaces.add(surface)

    def is_allowed(self, surface: str) -> bool:
        return self.active and surface in self.surfaces

    def pause(self) -> None:
        self.active = False

    def resume(self) -> None:
        self.active = True
