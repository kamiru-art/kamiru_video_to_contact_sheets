"""Carga y guardado de la configuración del usuario (para recordar ajustes)."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path


def _config_dir() -> Path:
    if sys.platform == "darwin":
        base = Path.home() / "Library" / "Application Support"
    elif sys.platform.startswith("win"):
        base = Path(os.environ.get("APPDATA", Path.home()))
    else:
        base = Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config"))
    d = base / "Kamiru"
    try:
        d.mkdir(parents=True, exist_ok=True)
    except OSError:
        d = Path.home()
    return d


CONFIG_PATH = _config_dir() / "settings.json"


def load() -> dict:
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, ValueError, OSError):
        return {}


def save(data: dict) -> None:
    try:
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except OSError:
        pass
