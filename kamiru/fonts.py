"""Descubrimiento de fuentes del sistema, multiplataforma.

Pillow necesita la RUTA a un archivo de fuente (.ttf/.otf/.ttc), no solo el
nombre de la familia. Aquí escaneamos las carpetas de fuentes típicas de cada
sistema operativo y construimos un diccionario {nombre visible: ruta}.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

# Extensiones de fuente que Pillow puede abrir con ImageFont.truetype.
_FONT_EXTS = {".ttf", ".otf", ".ttc"}


def _candidate_dirs():
    dirs = []
    home = Path.home()
    if sys.platform == "darwin":  # macOS
        dirs += [
            Path("/System/Library/Fonts"),
            Path("/System/Library/Fonts/Supplemental"),
            Path("/Library/Fonts"),
            home / "Library" / "Fonts",
        ]
    elif sys.platform.startswith("win"):  # Windows
        windir = os.environ.get("WINDIR", r"C:\Windows")
        dirs += [
            Path(windir) / "Fonts",
            home / "AppData" / "Local" / "Microsoft" / "Windows" / "Fonts",
        ]
    else:  # Linux y otros Unix
        dirs += [
            Path("/usr/share/fonts"),
            Path("/usr/local/share/fonts"),
            home / ".fonts",
            home / ".local" / "share" / "fonts",
        ]
    return [d for d in dirs if d.exists()]


def _nice_name(path: Path) -> str:
    """Nombre legible a partir del archivo, p. ej. 'DejaVuSans-Bold' -> 'DejaVu Sans Bold'."""
    stem = path.stem
    # Separa CamelCase y guiones/underscores en palabras.
    out = []
    prev_lower = False
    for ch in stem.replace("_", "-").replace("-", " "):
        if ch.isupper() and prev_lower:
            out.append(" ")
        out.append(ch)
        prev_lower = ch.islower()
    name = "".join(out)
    return " ".join(name.split())


def discover_fonts():
    """Devuelve un dict ordenado {nombre visible: ruta_str} de fuentes disponibles."""
    found = {}
    for d in _candidate_dirs():
        try:
            for path in d.rglob("*"):
                if path.suffix.lower() in _FONT_EXTS and path.is_file():
                    name = _nice_name(path)
                    # Evita duplicados de nombre, prefiere la primera ruta encontrada.
                    if name not in found:
                        found[name] = str(path)
        except (PermissionError, OSError):
            continue
    return dict(sorted(found.items(), key=lambda kv: kv[0].lower()))


# Familias preferidas como valor por defecto (la primera que exista, gana).
_PREFERRED = [
    "Helvetica", "Arial", "Helvetica Neue", "DejaVu Sans", "Verdana",
    "Segoe UI", "Roboto", "Liberation Sans", "Noto Sans", "Tahoma",
]


def default_font(fonts: dict):
    """Elige una fuente por defecto razonable de entre las descubiertas.

    Devuelve (nombre_visible, ruta) o (None, None) si no se encontró ninguna.
    """
    if not fonts:
        return None, None
    lowered = {k.lower(): (k, v) for k, v in fonts.items()}
    for pref in _PREFERRED:
        # Coincidencia exacta primero.
        if pref.lower() in lowered:
            return lowered[pref.lower()]
    for pref in _PREFERRED:
        # Coincidencia parcial (p. ej. 'Arial' dentro de 'Arial Unicode').
        for low, (name, path) in lowered.items():
            if pref.lower() in low:
                return name, path
    # Último recurso: la primera alfabéticamente.
    first = next(iter(fonts.items()))
    return first[0], first[1]
