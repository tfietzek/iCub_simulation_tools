"""
Zentrale Logging-Konfiguration für gazebohelper.

Alle anderen Module holen sich ihren Logger über
``logging.getLogger("gazebohelper.<modulname>")`` – dieses Modul richtet
nur den Root-Logger ``"gazebohelper"`` mit einem sinnvollen Standard-Handler
ein, falls noch keiner registriert ist.
"""

from __future__ import annotations

import logging

logger = logging.getLogger("gazebohelper")

if not logger.handlers:
    _handler = logging.StreamHandler()
    _handler.setFormatter(
        logging.Formatter(
            "[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s",
            datefmt="%H:%M:%S",
        )
    )
    logger.addHandler(_handler)

logger.setLevel(logging.INFO)


def get_logger(submodule: str) -> logging.Logger:
    """Return a child logger, e.g. get_logger('world') -> 'gazebohelper.world'."""
    return logging.getLogger(f"gazebohelper.{submodule}")
