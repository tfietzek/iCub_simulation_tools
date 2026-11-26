"""
SDF-Erzeugung für einfache Ein-Link-Modelle (Box, Kugel, Zylinder, Mesh).

Nutzt ausschließlich die Standardbibliothek (xml.etree.ElementTree), keine
Abhängigkeit zu Gazebo selbst - dieses Modul lässt sich also isoliert
testen, auch ohne installiertes gz.transport.
"""

from __future__ import annotations

from typing import Optional
from xml.dom import minidom
from xml.etree import ElementTree as ET

from .geometry import Color


def _pretty_xml(elem: ET.Element) -> str:
    rough = ET.tostring(elem, encoding="unicode")
    return minidom.parseString(rough).toprettyxml(indent="  ")


def _add_geometry(parent: ET.Element, shape: str, **kwargs) -> None:
    geometry = ET.SubElement(parent, "geometry")
    shape_el = ET.SubElement(geometry, shape)
    if shape == "box":
        size = kwargs["size"]
        ET.SubElement(shape_el, "size").text = str(size)
    elif shape == "sphere":
        ET.SubElement(shape_el, "radius").text = str(kwargs["radius"])
    elif shape == "cylinder":
        ET.SubElement(shape_el, "radius").text = str(kwargs["radius"])
        ET.SubElement(shape_el, "length").text = str(kwargs["length"])
    elif shape == "mesh":
        ET.SubElement(shape_el, "uri").text = kwargs["uri"]
        if kwargs.get("scale") is not None:
            ET.SubElement(shape_el, "scale").text = str(kwargs["scale"])
    else:
        raise ValueError(f"Unbekannte Shape: {shape!r}")


def _add_material(parent: ET.Element, color: Optional[Color]) -> None:
    if color is None:
        return
    material = ET.SubElement(parent, "material")
    for tag in ("ambient", "diffuse", "specular"):
        ET.SubElement(material, tag).text = f"{color.r} {color.g} {color.b} {color.a}"


def build_model_sdf(
    name: str,
    shape: str,
    static: bool = False,
    gravity: bool = True,
    color: Optional[Color] = None,
    mass: float = 1.0,
    **shape_kwargs,
) -> str:
    """Baut einen kompletten <sdf><model> String für eine primitive Form
    oder ein Mesh.

    shape: "box" | "sphere" | "cylinder" | "mesh"
    shape_kwargs je nach shape:
      box:      size=Vector3(...)
      sphere:   radius=float
      cylinder: radius=float, length=float
      mesh:     uri=str, scale=Vector3 | None
    """
    sdf = ET.Element("sdf", version="1.9")
    model = ET.SubElement(sdf, "model", name=name)
    ET.SubElement(model, "static").text = "true" if static else "false"

    link = ET.SubElement(model, "link", name="link")
    ET.SubElement(link, "gravity").text = "true" if gravity else "false"

    if not static:
        inertial = ET.SubElement(link, "inertial")
        ET.SubElement(inertial, "mass").text = str(mass)

    collision = ET.SubElement(link, "collision", name="collision")
    _add_geometry(collision, shape, **shape_kwargs)

    visual = ET.SubElement(link, "visual", name="visual")
    _add_geometry(visual, shape, **shape_kwargs)
    _add_material(visual, color)

    return _pretty_xml(sdf)
