"""
GazeboEntity: leichtgewichtiges Handle auf eine gespawnte Entität.

Wird von GazeboWorld.spawn_*() zurückgegeben und delegiert alle
Operationen an die zugehörige GazeboWorld-Instanz.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from .geometry import Quaternion, Vector3

if TYPE_CHECKING:
    from .world import GazeboWorld


class GazeboEntity:
    def __init__(self, world: "GazeboWorld", name: str):
        self._world = world
        self.name = name

    def move(self, position: Vector3, orientation: Optional[Quaternion] = None) -> bool:
        return self._world.move(self.name, position, orientation)

    def rotate(self, orientation: Quaternion) -> bool:
        return self._world.rotate(self.name, orientation)

    def translate(self, delta: Vector3) -> bool:
        return self._world.translate(self.name, delta)

    def delete(self) -> bool:
        return self._world.delete(self.name)

    def exists(self) -> bool:
        return self._world.exists(self.name)

    def get_pose(self):
        return self._world.get_pose(self.name)

    def __repr__(self) -> str:
        return f"GazeboEntity(name={self.name!r})"
