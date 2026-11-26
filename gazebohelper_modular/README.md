# gazebohelper (modulare Version)

Python-Bibliothek zum Einfügen, Bewegen, Rotieren und Löschen von Objekten
zur Laufzeit im modernen Gazebo Sim (Fortress, Garden, Harmonic, Ionic).

Dies ist die modularisierte Variante derselben Bibliothek: statt einer
einzigen `gazebohelper.py`-Datei ist der Code jetzt als echtes
Python-Package aufgeteilt. Funktional identisch zur monolithischen
Version, aber leichter zu warten, zu testen und zu erweitern.

## Paketstruktur

```
gazebohelper/
├── __init__.py          Öffentliche API (re-exportiert alles Wichtige)
├── geometry.py           Vector3, Quaternion, Pose, Color
├── sdf.py                 SDF-Erzeugung (build_model_sdf)
├── bindings.py            Automatische Erkennung von gz.transport/gz.msgs
├── entity.py               GazeboEntity
├── world.py                GazeboWorld (Haupt-Einstiegspunkt)
└── logging_config.py       Zentrales Logging-Setup
examples/
├── example_01_spawn_basic.py
├── example_02_move_rotate_delete.py
├── example_03_sdf_and_mesh.py
├── example_04_world_control.py
└── example_05_offline_geometry_test.py   Läuft OHNE Gazebo!
tests/
├── conftest.py       Fake-Bindings (FakeNode, FakeEntityFactory, ...) + Fixtures
├── test_geometry.py
├── test_sdf.py
├── test_bindings.py
├── test_world.py
└── integration/       Tests gegen ECHTES, laufendes Gazebo (siehe README dort)
    ├── conftest.py
    ├── helpers.py
    ├── test_spawn_live.py
    ├── test_world_control_live.py
    └── README.md
pyproject.toml
LICENSE
```

## Warum modular?

- **Testbarkeit ohne Simulator**: `gazebohelper.geometry` und
  `gazebohelper.sdf` haben keine Abhängigkeit zu `gz.transport`/`gz.msgs`.
  Die Gazebo-Bindings werden erst geladen, wenn tatsächlich eine
  `GazeboWorld`-Instanz erzeugt wird (`gazebohelper/bindings.py`,
  lazy via `get_bindings()`). Dadurch lassen sich Vektor-/Quaternion-Mathe
  und SDF-Generierung mit `pytest` o.ä. testen, ganz ohne installiertes
  Gazebo. Siehe `examples/example_05_offline_geometry_test.py`.
- **Kleinere, fokussierte Dateien** statt einer 700-Zeilen-Datei -
  einfacher zu lesen, zu reviewen und zu erweitern.
- **Sauber erweiterbar**: neue Features wie `set_velocity()` oder
  `apply_force()` kommen in `world.py`, neue Geometrie-Helfer in
  `geometry.py`, ohne dass man sich durch eine riesige Datei scrollen muss.
- **pip-installierbar** über die beiliegende `pyproject.toml`.

## Installation

Optional als Package installieren (empfohlen, dann funktioniert
`import gazebohelper` aus jedem Verzeichnis):

```bash
cd gazebohelper_modular
pip install -e .
```

Alternativ genügt es, den Ordner `gazebohelper/` neben dein Skript zu legen.

Voraussetzung für die eigentliche Simulator-Anbindung sind die
Python-Bindings von Gazebo, z.B. für Harmonic:

```bash
sudo apt install python3-gz-transport13 python3-gz-msgs10
```

(Paketnamen variieren je nach Distribution und Gazebo-Version.)

## Schnellstart

```python
from gazebohelper import GazeboWorld, Vector3, Color

world = GazeboWorld("default")

box = world.spawn_box(
    name="my_box",
    position=Vector3(0, 0, 1),
    size=Vector3(1, 1, 1),
    color=Color.RED,
)

box.move(Vector3(2, 0, 1))
box.delete()
```

Vorher eine leere Welt starten:

```bash
gz sim -v 4 empty.sdf
```

## Beispiele

| Datei | Inhalt |
|---|---|
| `example_01_spawn_basic.py` | Box, Kugel, Zylinder spawnen |
| `example_02_move_rotate_delete.py` | Bewegen, rotieren, verschieben, löschen |
| `example_03_sdf_and_mesh.py` | Vorhandene SDF-Datei und Mesh laden |
| `example_04_world_control.py` | Pause, Resume, Reset, Einzelschritte |
| `example_05_offline_geometry_test.py` | **Läuft ohne Gazebo** - Geometrie & SDF isoliert testen |

## Tests ausführen

Die Bibliothek hat eine pytest-Suite mit 66 Tests, die **komplett ohne
installiertes Gazebo** laufen (0.1s Laufzeit). Das funktioniert, weil:

- `tests/test_geometry.py` und `tests/test_sdf.py` die reine Mathe- bzw.
  XML-Erzeugung testen, die keine gz-Abhängigkeit hat.
- `tests/test_bindings.py` den Fehlerfall prüft (keine gz-Bindings
  gefunden) sowie den Caching-Mechanismus.
- `tests/test_world.py` `GazeboWorld` gegen ein **Fake-Binding**
  (`tests/conftest.py`) testet: ein `FakeNode` protokolliert jeden
  Service-Aufruf (`create`, `remove`, `set_pose`, `control`), sodass
  geprüft werden kann, welcher Service mit welchen Feldern aufgerufen
  wurde – ganz ohne laufenden Simulator.

Installation und Ausführung:

```bash
pip install -e .[test]
pytest
```

oder ohne Editable-Install direkt aus dem entpackten Ordner:

```bash
pip install pytest
pytest
```

Test-Übersicht:

| Datei | Testet |
|---|---|
| `tests/test_geometry.py` | Vector3, Quaternion (inkl. Euler-Rücktransformation), Pose, Color |
| `tests/test_sdf.py` | SDF-Generierung für Box/Kugel/Zylinder/Mesh, Fehlerfälle |
| `tests/test_bindings.py` | Fehlermeldung ohne Gazebo, Caching der erkannten Bindings |
| `tests/test_world.py` | Spawn/Move/Rotate/Delete/Pause/Resume/Reset/Step über Fake-Bindings, Entity-Delegation |

### Integrationstests gegen echtes Gazebo

Zusätzlich gibt es `tests/integration/` mit Tests, die eine **tatsächlich
laufende Gazebo-Welt** brauchen (echtes Spawnen, echte Posen-Abfragen,
`pause()`/`resume()`/`step()` verifiziert an einer real fallenden Box).
Diese sind mit dem Marker `integration` versehen und werden bei einem
normalen `pytest`-Aufruf standardmäßig übersprungen. Explizit ausführen:

```bash
pytest -m integration -v
```

Details, Voraussetzungen und Konfiguration siehe
`tests/integration/README.md`. Ohne laufendes Gazebo werden diese Tests
sauber übersprungen (`SKIPPED`), nicht als Fehler gemeldet.

## API im Detail

Alles, was in der monolithischen Version verfügbar war, ist unverändert
vorhanden und über `from gazebohelper import ...` erreichbar:

`GazeboWorld`, `GazeboEntity`, `Vector3`, `Quaternion`, `Pose`, `Color`,
`build_model_sdf`, `get_bindings`, `GzBindings`, `GazeboBindingsError`.

Methoden auf `GazeboWorld`: `spawn_box`, `spawn_sphere`, `spawn_cylinder`,
`spawn_mesh`, `spawn_sdf_string`, `spawn_sdf_file`, `move`, `rotate`,
`translate`, `delete`, `exists`, `get_pose`, `list_entities`, `clone`
(Platzhalter), `pause`, `resume`, `reset`, `step`.

## Bekannte Grenzen

Wie bei der monolithischen Version: `clone()` ist nur ein Platzhalter,
`set_velocity()`/`apply_force()` fehlen noch, Materialeigenschaften
beschränken sich auf Farbe (keine PBR-Texturen), und die Versionserkennung
deckt Fortress bis Ionic ab - ungewöhnliche Installationen können
abweichende Modulnamen haben.

## Lizenz

MIT, siehe `LICENSE`.
