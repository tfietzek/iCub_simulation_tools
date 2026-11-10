"""
Beispiel 2: Objekte bewegen, rotieren, verschieben und loeschen (modulare Version).
"""

import time

from gazebohelper import GazeboWorld, Quaternion, Vector3

world = GazeboWorld("default")

box = world.spawn_box("moving_box", position=Vector3(0, 0, 1))
time.sleep(1)

box.move(Vector3(3, 0, 1))
time.sleep(1)

box.translate(Vector3(0, 2, 0))
time.sleep(1)

box.rotate(Quaternion.from_euler(0, 0, 1.5708))
time.sleep(1)

box.delete()
