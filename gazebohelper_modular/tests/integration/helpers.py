"""
Kleine Hilfsfunktionen für die Live-Gazebo-Integrationstests.

Bewusst als eigenständiges Modul (nicht in conftest.py), damit es per
einfachem `from helpers import wait_until` importiert werden kann, ohne
sich auf pytests Import-Mechanik für conftest.py zu verlassen.
"""

from __future__ import annotations

import time
from typing import Callable


def wait_until(predicate: Callable[[], bool], timeout: float = 3.0, interval: float = 0.1) -> bool:
    """Pollt `predicate`, bis sie True zurückgibt oder das Timeout erreicht ist.

    Nötig, weil Pose-Updates über das gz-transport Topic mit leichter
    Verzögerung ankommen können - ein einzelner sofortiger Check wäre
    manchmal ein falsches Negativ."""
    deadline = time.time() + timeout
    while time.time() < deadline:
        if predicate():
            return True
        time.sleep(interval)
    return predicate()
