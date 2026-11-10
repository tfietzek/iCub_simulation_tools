"""
gazebohelper - Python-Bibliothek für den modernen Gazebo Sim Simulator.

Modularer Aufbau:
    gazebohelper.geometry        Vector3, Quaternion, Pose, Color
    gazebohelper.sdf             SDF-Erzeugung (build_model_sdf)
    gazebohelper.bindings        Automatische Erkennung von gz.transport/gz.msgs
    gazebohelper.entity          GazeboEntity
    gazebohelper.world           GazeboWorld
    gazebohelper.logging_config  Zentrales Logging-Setup

Öffentliche API (das, was die meisten Nutzer brauchen):

    from gazebohelper import GazeboWorld, Vector3, Quaternion, Pose, Color

    world = GazeboWorld("default")
    box = world.spawn_box("my_box", position=Vector3(0, 0, 1), color=Color.RED)
    box.move(Vector3(2, 0, 1))
    box.delete()
"""

from .bindings import GazeboBindingsError, GzBindings, get_bindings
from .entity import GazeboEntity
from .geometry import Color, Pose, Quaternion, Vector3
from .logging_config import logger
from .sdf import build_model_sdf
from .world import GazeboWorld

__all__ = [
    "GazeboWorld",
    "GazeboEntity",
    "Vector3",
    "Quaternion",
    "Pose",
    "Color",
    "build_model_sdf",
    "get_bindings",
    "GzBindings",
    "GazeboBindingsError",
    "logger",
]

__version__ = "0.2.0"
