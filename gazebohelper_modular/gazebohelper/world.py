"""
GazeboWorld: Haupt-Einstiegspunkt der Bibliothek.

Eine Instanz pro Gazebo-Welt, die gesteuert werden soll. Kapselt alle
gz-transport Service-Aufrufe (create, remove, set_pose, control) sowie
das kurzzeitige Abonnieren des pose/info-Topics für get_pose().
"""

from __future__ import annotations

import os
import time
import uuid
from importlib import import_module
from typing import Dict, List, Optional

from .bindings import get_bindings
from .entity import GazeboEntity
from .geometry import Color, Pose, Quaternion, Vector3
from .logging_config import get_logger
from .sdf import build_model_sdf

logger = get_logger("world")


class GazeboWorld:
    """
    Beispiel:
        world = GazeboWorld("default")
        box = world.spawn_box("box1", position=Vector3(0, 0, 1))
        box.move(Vector3(1, 1, 1))
        box.delete()
    """

    def __init__(self, world_name: str = "default", timeout_ms: int = 2000):
        self.world_name = world_name
        self.timeout_ms = timeout_ms
        self._bindings = get_bindings()
        self._node = self._bindings.Node()
        self._known_entities: Dict[str, GazeboEntity] = {}
        logger.info("GazeboWorld-Wrapper mit Welt '%s' verbunden.", world_name)

    # -- interne Helfer ------------------------------------------------------

    def _service(self, suffix: str) -> str:
        return f"/world/{self.world_name}/{suffix}"

    def _call(self, service: str, request, response_type):
        result, response = self._node.request(
            service, request, response_type, timeout=self.timeout_ms
        )
        if not result:
            logger.warning("Service-Aufruf an '%s' fehlgeschlagen oder Timeout.", service)
        return result, response

    def _unique_name(self, prefix: str) -> str:
        return f"{prefix}_{uuid.uuid4().hex[:8]}"

    def _apply_pose_to_request(self, req, pose: Optional[Pose]) -> None:
        if pose is None:
            return
        req.pose.position.x = pose.position.x
        req.pose.position.y = pose.position.y
        req.pose.position.z = pose.position.z
        req.pose.orientation.x = pose.orientation.x
        req.pose.orientation.y = pose.orientation.y
        req.pose.orientation.z = pose.orientation.z
        req.pose.orientation.w = pose.orientation.w

    # -- Spawnen ---------------------------------------------------------------

    def spawn_sdf_string(self, sdf: str, name: Optional[str] = None,
                          pose: Optional[Pose] = None) -> GazeboEntity:
        b = self._bindings
        req = b.EntityFactory()
        req.sdf = sdf
        if name:
            req.name = name
        self._apply_pose_to_request(req, pose)

        ok, _ = self._call(self._service("create"), req, b.Boolean)
        entity_name = name or self._unique_name("entity")
        if ok:
            logger.info("Entität '%s' gespawnt.", entity_name)
        else:
            logger.error("Spawnen der Entität '%s' fehlgeschlagen.", entity_name)
        entity = GazeboEntity(self, entity_name)
        self._known_entities[entity_name] = entity
        return entity

    def spawn_sdf_file(self, path: str, name: Optional[str] = None,
                        pose: Optional[Pose] = None) -> GazeboEntity:
        if not os.path.isfile(path):
            raise FileNotFoundError(f"SDF-Datei nicht gefunden: {path}")
        b = self._bindings
        req = b.EntityFactory()
        req.sdf_filename = path
        if name:
            req.name = name
        self._apply_pose_to_request(req, pose)

        ok, _ = self._call(self._service("create"), req, b.Boolean)
        entity_name = name or self._unique_name("entity")
        if ok:
            logger.info("Entität '%s' aus Datei '%s' gespawnt.", entity_name, path)
        else:
            logger.error("Spawnen aus Datei '%s' fehlgeschlagen.", path)
        entity = GazeboEntity(self, entity_name)
        self._known_entities[entity_name] = entity
        return entity

    def spawn_box(self, name: Optional[str] = None, position: Optional[Vector3] = None,
                  size: Optional[Vector3] = None, static: bool = False, gravity: bool = True,
                  color: Optional[Color] = None, mass: float = 1.0) -> GazeboEntity:
        position = position or Vector3(0, 0, 1)
        size = size or Vector3(1, 1, 1)
        model_name = name or self._unique_name("box")
        sdf = build_model_sdf(model_name, "box", static=static, gravity=gravity,
                               color=color, mass=mass, size=size)
        return self.spawn_sdf_string(sdf, name=model_name, pose=Pose(position=position))

    def spawn_sphere(self, name: Optional[str] = None, position: Optional[Vector3] = None,
                      radius: float = 0.5, static: bool = False, gravity: bool = True,
                      color: Optional[Color] = None, mass: float = 1.0) -> GazeboEntity:
        position = position or Vector3(0, 0, 1)
        model_name = name or self._unique_name("sphere")
        sdf = build_model_sdf(model_name, "sphere", static=static, gravity=gravity,
                               color=color, mass=mass, radius=radius)
        return self.spawn_sdf_string(sdf, name=model_name, pose=Pose(position=position))

    def spawn_cylinder(self, name: Optional[str] = None, position: Optional[Vector3] = None,
                        radius: float = 0.5, length: float = 1.0, static: bool = False,
                        gravity: bool = True, color: Optional[Color] = None,
                        mass: float = 1.0) -> GazeboEntity:
        position = position or Vector3(0, 0, 1)
        model_name = name or self._unique_name("cylinder")
        sdf = build_model_sdf(model_name, "cylinder", static=static, gravity=gravity,
                               color=color, mass=mass, radius=radius, length=length)
        return self.spawn_sdf_string(sdf, name=model_name, pose=Pose(position=position))

    def spawn_mesh(self, uri: str, name: Optional[str] = None, position: Optional[Vector3] = None,
                   scale: Optional[Vector3] = None, static: bool = True,
                   gravity: bool = True, color: Optional[Color] = None,
                   mass: float = 1.0) -> GazeboEntity:
        """uri akzeptiert einen lokalen Pfad (file://...), einen absoluten
        Dateisystempfad oder eine model://-URI (über GZ_SIM_RESOURCE_PATH
        auflösbar). Unterstützt STL, DAE, OBJ."""
        position = position or Vector3(0, 0, 0)
        model_name = name or self._unique_name("mesh")
        if os.path.isabs(uri) and os.path.isfile(uri) and not uri.startswith("file://"):
            uri = f"file://{uri}"
        sdf = build_model_sdf(model_name, "mesh", static=static, gravity=gravity,
                               color=color, mass=mass, uri=uri, scale=scale)
        return self.spawn_sdf_string(sdf, name=model_name, pose=Pose(position=position))

    # -- Manipulation ------------------------------------------------------------

    def move(self, name: str, position: Vector3,
             orientation: Optional[Quaternion] = None) -> bool:
        b = self._bindings
        req = b.Pose()
        req.name = name
        req.position.x = position.x
        req.position.y = position.y
        req.position.z = position.z
        q = orientation or Quaternion.identity()
        req.orientation.x = q.x
        req.orientation.y = q.y
        req.orientation.z = q.z
        req.orientation.w = q.w

        ok, _ = self._call(self._service("set_pose"), req, b.Boolean)
        if ok:
            logger.info("'%s' nach (%s, %s, %s) bewegt.", name, position.x, position.y, position.z)
        else:
            logger.error("Bewegen von '%s' fehlgeschlagen.", name)
        return ok

    def rotate(self, name: str, orientation: Quaternion) -> bool:
        """Rotiert am aktuellen Ort - dafür wird zunächst die aktuelle
        Position per get_pose() abgefragt."""
        current = self.get_pose(name)
        position = current.position if current else Vector3(0, 0, 0)
        return self.move(name, position, orientation)

    def translate(self, name: str, delta: Vector3) -> bool:
        current = self.get_pose(name)
        if current is None:
            logger.error("Kann '%s' nicht verschieben: aktuelle Pose unbekannt.", name)
            return False
        return self.move(name, current.position + delta, current.orientation)

    def delete(self, name: str) -> bool:
        b = self._bindings
        req = b.Entity()
        req.name = name
        req.type = b.Entity.MODEL

        ok, _ = self._call(self._service("remove"), req, b.Boolean)
        if ok:
            logger.info("Entität '%s' gelöscht.", name)
            self._known_entities.pop(name, None)
        else:
            logger.error("Löschen von '%s' fehlgeschlagen.", name)
        return ok

    def exists(self, name: str) -> bool:
        return self.get_pose(name) is not None

    def get_pose(self, name: str) -> Optional[Pose]:
        """Fragt die aktuelle Pose einer Entität ab, indem kurz das
        pose/info-Topic der Welt abonniert und nach Namen gefiltert wird.
        Gibt None zurück, wenn die Entität innerhalb des Timeouts nicht
        gefunden wurde."""
        result_holder: dict = {}

        def _callback(msg):
            for p in msg.pose:
                if p.name == name:
                    result_holder["pose"] = Pose(
                        position=Vector3(p.position.x, p.position.y, p.position.z),
                        orientation=Quaternion(p.orientation.x, p.orientation.y,
                                                p.orientation.z, p.orientation.w),
                    )

        topic = f"/world/{self.world_name}/pose/info"
        try:
            b = self._bindings
            pose_v_mod = import_module(f"gz.msgs{b.msgs_version}.pose_v_pb2")
            self._node.subscribe(pose_v_mod.Pose_V, topic, _callback)
            waited = 0.0
            step = 0.05
            while "pose" not in result_holder and waited < (self.timeout_ms / 1000.0):
                time.sleep(step)
                waited += step
            self._node.unsubscribe(topic)
        except Exception as exc:  # pragma: no cover - hängt von laufender Sim ab
            logger.error("get_pose('%s') fehlgeschlagen: %s", name, exc)
            return None

        return result_holder.get("pose")

    def list_entities(self) -> List[str]:
        """Namen aller über diesen Wrapper gespawnten (und noch nicht
        gelöschten) Entitäten. Erfasst keine Entitäten, die bereits vor
        dem Start dieser GazeboWorld-Instanz in der Welt vorhanden waren."""
        return list(self._known_entities.keys())

    def clone(self, name: str, new_name: Optional[str] = None,
              offset: Optional[Vector3] = None) -> Optional[GazeboEntity]:
        """Platzhalter: echtes Klonen erfordert das Zwischenspeichern der
        beim Spawn verwendeten SDF, das ist in dieser Version noch nicht
        implementiert."""
        logger.warning(
            "clone() ist noch nicht vollständig implementiert - "
            "spawne die Entität stattdessen manuell erneut."
        )
        return None

    # -- Weltsteuerung -------------------------------------------------------------

    def _control(self, **fields) -> bool:
        b = self._bindings
        req = b.WorldControl()
        for k, v in fields.items():
            setattr(req, k, v)
        ok, _ = self._call(self._service("control"), req, b.Boolean)
        return ok

    def pause(self) -> bool:
        ok = self._control(pause=True)
        logger.info("Simulation pausiert." if ok else "Pausieren fehlgeschlagen.")
        return ok

    def resume(self) -> bool:
        ok = self._control(pause=False)
        logger.info("Simulation fortgesetzt." if ok else "Fortsetzen fehlgeschlagen.")
        return ok

    def reset(self) -> bool:
        b = self._bindings
        req = b.WorldControl()
        req.reset.all = True
        ok, _ = self._call(self._service("control"), req, b.Boolean)
        logger.info("Welt zurückgesetzt." if ok else "Zurücksetzen fehlgeschlagen.")
        return ok

    def step(self, steps: int = 1) -> bool:
        ok = self._control(multi_step=steps)
        logger.info(
            "Simulation um %d Schritte fortgeschritten." % steps
            if ok else "Schrittweises Fortschreiten fehlgeschlagen."
        )
        return ok
