"""
Beispiel 4: Simulation pausieren, fortsetzen, zuruecksetzen, Einzelschritte (modulare Version).
"""

import time

from gazebohelper import GazeboWorld

world = GazeboWorld("default")

world.pause()
time.sleep(1)

world.step(steps=10)
time.sleep(1)

world.resume()
time.sleep(2)

world.reset()
