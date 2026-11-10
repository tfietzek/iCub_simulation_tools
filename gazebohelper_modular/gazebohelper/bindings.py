"""
Automatische Erkennung der installierten gz-transport / gz-msgs
Python-Bindings.

Gazebo benennt seine Python-Pakete versionsabhängig, z.B. ``gz.transport13``
zusammen mit ``gz.msgs10`` für Harmonic. Damit dieselbe Bibliothek über
Fortress, Garden, Harmonic und Ionic hinweg funktioniert, wird hier beim
ersten Zugriff automatisch die passende Kombination gesucht.
"""

from __future__ import annotations

import importlib
from dataclasses import dataclass
from typing import Optional

from .logging_config import get_logger

logger = get_logger("bindings")


class GazeboBindingsError(RuntimeError):
    """Wird ausgelöst, wenn keine passenden gz.transport/gz.msgs Bindings gefunden werden."""


# Suchreihenfolge: neueste zuerst.
_CANDIDATE_TRANSPORT_VERSIONS = (14, 13, 12, 11)
_CANDIDATE_MSGS_VERSIONS = (11, 10, 9, 8)

_RELEASE_HINTS = {
    14: "Harmonic / Ionic",
    13: "Harmonic",
    12: "Garden",
    11: "Fortress",
}


@dataclass
class GzBindings:
    transport_version: int
    msgs_version: int
    Node: type
    EntityFactory: type
    Boolean: type
    Entity: type
    Pose: type
    WorldControl: type
    Vector3d: type


_bindings: Optional[GzBindings] = None


def _detect() -> GzBindings:
    last_error: Optional[Exception] = None

    for t_ver in _CANDIDATE_TRANSPORT_VERSIONS:
        try:
            transport_mod = importlib.import_module(f"gz.transport{t_ver}")
        except ImportError as exc:
            last_error = exc
            continue

        for m_ver in _CANDIDATE_MSGS_VERSIONS:
            try:
                entity_factory_mod = importlib.import_module(f"gz.msgs{m_ver}.entity_factory_pb2")
                boolean_mod = importlib.import_module(f"gz.msgs{m_ver}.boolean_pb2")
                entity_mod = importlib.import_module(f"gz.msgs{m_ver}.entity_pb2")
                pose_mod = importlib.import_module(f"gz.msgs{m_ver}.pose_pb2")
                world_control_mod = importlib.import_module(f"gz.msgs{m_ver}.world_control_pb2")
                vector3d_mod = importlib.import_module(f"gz.msgs{m_ver}.vector3d_pb2")
            except ImportError as exc:
                last_error = exc
                continue

            logger.info(
                "Verwende gz.transport%d / gz.msgs%d (Gazebo %s Bindings).",
                t_ver, m_ver, _RELEASE_HINTS.get(t_ver, "unbekanntes Release"),
            )
            return GzBindings(
                transport_version=t_ver,
                msgs_version=m_ver,
                Node=transport_mod.Node,
                EntityFactory=entity_factory_mod.EntityFactory,
                Boolean=boolean_mod.Boolean,
                Entity=entity_mod.Entity,
                Pose=pose_mod.Pose,
                WorldControl=world_control_mod.WorldControl,
                Vector3d=vector3d_mod.Vector3d,
            )

    raise GazeboBindingsError(
        "Konnte keine funktionierenden gz.transport / gz.msgs Python-Bindings finden.\n"
        f"Versucht wurden Transport-Versionen {_CANDIDATE_TRANSPORT_VERSIONS} "
        f"und Msgs-Versionen {_CANDIDATE_MSGS_VERSIONS}.\n"
        "Stelle sicher, dass die Gazebo-Python-Bindings installiert sind, z.B.:\n"
        "  sudo apt install python3-gz-transport13 python3-gz-msgs10\n"
        "(Paketnamen variieren je nach Gazebo-Version - siehe https://gazebosim.org)\n"
        f"Letzter Import-Fehler: {last_error}"
    )


def get_bindings() -> GzBindings:
    """Bindings werden lazy und nur einmal aufgelöst (Modul-weiter Cache)."""
    global _bindings
    if _bindings is None:
        _bindings = _detect()
    return _bindings


def reset_bindings_cache() -> None:
    """Nützlich für Tests: erzwingt eine erneute Erkennung beim nächsten get_bindings()."""
    global _bindings
    _bindings = None
