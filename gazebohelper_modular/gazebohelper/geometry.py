"""
Geometrie- und Farb-Hilfsklassen: Vector3, Quaternion, Pose, Color.

Diese Klassen haben keine Abhängigkeit zu gz.transport/gz.msgs und lassen
sich daher auch ohne installiertes Gazebo importieren und testen.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Tuple


@dataclass
class Vector3:
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0

    def __iter__(self):
        yield self.x
        yield self.y
        yield self.z

    def __add__(self, other: "Vector3") -> "Vector3":
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: "Vector3") -> "Vector3":
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, scalar: float) -> "Vector3":
        return Vector3(self.x * scalar, self.y * scalar, self.z * scalar)

    def length(self) -> float:
        return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

    def as_tuple(self) -> Tuple[float, float, float]:
        return (self.x, self.y, self.z)

    def __str__(self) -> str:
        return f"{self.x} {self.y} {self.z}"


@dataclass
class Quaternion:
    """x, y, z, w - passend zu gz.msgs.Quaternion (w zuletzt)."""
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0
    w: float = 1.0

    @staticmethod
    def identity() -> "Quaternion":
        return Quaternion(0.0, 0.0, 0.0, 1.0)

    @staticmethod
    def from_euler(roll: float, pitch: float, yaw: float) -> "Quaternion":
        """Quaternion aus Roll/Pitch/Yaw (Radiant, Z-Y-X-Konvention)."""
        cr, sr = math.cos(roll * 0.5), math.sin(roll * 0.5)
        cp, sp = math.cos(pitch * 0.5), math.sin(pitch * 0.5)
        cy, sy = math.cos(yaw * 0.5), math.sin(yaw * 0.5)

        w = cr * cp * cy + sr * sp * sy
        x = sr * cp * cy - cr * sp * sy
        y = cr * sp * cy + sr * cp * sy
        z = cr * cp * sy - sr * sp * cy
        return Quaternion(x, y, z, w)

    def to_euler(self) -> Tuple[float, float, float]:
        """Gibt (roll, pitch, yaw) in Radiant zurück."""
        sinr_cosp = 2 * (self.w * self.x + self.y * self.z)
        cosr_cosp = 1 - 2 * (self.x ** 2 + self.y ** 2)
        roll = math.atan2(sinr_cosp, cosr_cosp)

        sinp = 2 * (self.w * self.y - self.z * self.x)
        pitch = math.copysign(math.pi / 2, sinp) if abs(sinp) >= 1 else math.asin(sinp)

        siny_cosp = 2 * (self.w * self.z + self.x * self.y)
        cosy_cosp = 1 - 2 * (self.y ** 2 + self.z ** 2)
        yaw = math.atan2(siny_cosp, cosy_cosp)
        return roll, pitch, yaw


@dataclass
class Pose:
    position: Vector3 = field(default_factory=Vector3)
    orientation: Quaternion = field(default_factory=Quaternion.identity)

    @staticmethod
    def from_xyz_rpy(x: float, y: float, z: float,
                      roll: float = 0.0, pitch: float = 0.0, yaw: float = 0.0) -> "Pose":
        return Pose(Vector3(x, y, z), Quaternion.from_euler(roll, pitch, yaw))


@dataclass
class Color:
    r: float = 1.0
    g: float = 1.0
    b: float = 1.0
    a: float = 1.0


Color.RED = Color(1, 0, 0, 1)
Color.GREEN = Color(0, 1, 0, 1)
Color.BLUE = Color(0, 0, 1, 1)
Color.WHITE = Color(1, 1, 1, 1)
Color.BLACK = Color(0, 0, 0, 1)
Color.YELLOW = Color(1, 1, 0, 1)
