"""
Beispiel 1: Grundlegendes Spawnen von primitiven Formen (modulare Version).

Voraussetzung: eine laufende Gazebo-Sim-Welt, z.B.
    gz sim -v 4 empty.sdf
"""

from gazebohelper import Color, GazeboWorld, Vector3

world = GazeboWorld("default")

box = world.spawn_box(
    name="box1", position=Vector3(0, 0, 1), size=Vector3(1, 1, 1), color=Color.RED,
)
sphere = world.spawn_sphere(
    name="sphere1", position=Vector3(2, 0, 1), radius=0.5, color=Color.BLUE,
)
cylinder = world.spawn_cylinder(
    name="cylinder1", position=Vector3(-2, 0, 1), radius=0.4, length=1.2, color=Color.YELLOW,
)

print("Gespawnte Entitaeten:", world.list_entities())
