"""
Beispiel 3: Vorhandene SDF-Datei laden und ein Mesh (STL/DAE/OBJ) spawnen (modulare Version).
"""

from gazebohelper import GazeboWorld, Vector3

world = GazeboWorld("default")

chair = world.spawn_sdf_file(
    "/home/user/models/chair/model.sdf", name="chair1", pose=None,
)

mesh = world.spawn_mesh(
    uri="/home/user/models/lamp/lamp.stl", name="lamp1",
    position=Vector3(1, 1, 0), static=True,
)

print("Chair existiert:", chair.exists())
print("Lamp existiert:", mesh.exists())
