# Integrationstests (mit echtem Gazebo)

Im Unterschied zu `tests/` (Unit-Tests mit Fake-Bindings, laufen überall
in <0.2s) brauchen die Tests in diesem Ordner eine **tatsächlich laufende
Gazebo-Sim-Welt**. Sie spawnen echte Entitäten, bewegen sie, prüfen
Posen über den echten `pose/info`-Topic und verifizieren `pause()`/
`resume()`/`step()` anhand einer real fallenden Box.

## Voraussetzungen

1. Gazebo-Python-Bindings installiert (siehe Haupt-README), z.B. für Harmonic:
   ```bash
   sudo apt install python3-gz-transport13 python3-gz-msgs10
   ```
2. Eine laufende Welt mit Physik und Gravitation, z.B.:
   ```bash
   gz sim -v4 empty.sdf
   ```
   Headless (ohne GUI) geht auch, z.B.:
   ```bash
   gz sim -s -r -v4 empty.sdf
   ```
3. Die Bibliothek installiert bzw. im Python-Pfad:
   ```bash
   pip install -e ".[test]"
   ```

## Ausführen

Integrationstests sind mit dem Marker `integration` versehen und werden
von einem normalen `pytest`-Aufruf standardmäßig **übersprungen**
(siehe `pyproject.toml`, `addopts = -m "not integration"`). Explizit
anfordern:

```bash
pytest -m integration -v
```

Nur die Integrationstests, alle anderen Marker ignorieren:

```bash
pytest tests/integration -v
```

## Verhalten ohne laufendes Gazebo

Die Tests sind so gebaut, dass sie bei fehlenden Bindings oder fehlender
laufender Welt sauber **übersprungen** (`SKIPPED`), nicht fehlschlagen
(`FAILED`). Das übernimmt die `live_world`-Fixture in `conftest.py`:
sie versucht einen echten `pause()`-Service-Aufruf und ruft `pytest.skip()`
mit einer erklärenden Meldung auf, falls das nicht klappt.

## Konfiguration

Über Umgebungsvariablen anpassbar, falls z.B. eine andere Welt als
`default` verwendet wird oder Service-Aufrufe mehr Zeit brauchen:

```bash
GAZEBOHELPER_TEST_WORLD=my_world GAZEBOHELPER_TEST_TIMEOUT_MS=3000 pytest -m integration -v
```

## Was hier getestet wird

| Datei | Testet |
|---|---|
| `test_spawn_live.py` | Spawnen (Box/Kugel/Zylinder/SDF-Datei), Existenzprüfung über echte Pose-Abfrage, move/translate/rotate mit Toleranzvergleich, delete |
| `test_world_control_live.py` | `pause()` friert eine fallende Box tatsächlich ein, `resume()` lässt sie weiterfallen, `step()` bewegt sie im pausierten Zustand einen definierten Schritt weiter, `reset()` |

## Warum getrennt von den Unit-Tests?

- Unit-Tests (`tests/*.py`) sollen in jeder CI-Pipeline laufen, auch ohne
  Gazebo-Installation - deshalb arbeiten sie mit Fake-Bindings.
- Diese Integrationstests sind langsamer (echte Netzwerk-/Topic-Latenz,
  `time.sleep()` für physikalische Verifikation) und brauchen eine
  Simulatorumgebung - deshalb als expliziter Opt-in per Marker, z.B. für
  einen separaten CI-Job mit installiertem Gazebo oder für manuelle
  Tests auf dem Entwicklungsrechner.
