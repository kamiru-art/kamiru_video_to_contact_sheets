#!/usr/bin/env bash
# Lanzador para Linux (y macOS desde terminal).
# La primera vez crea un entorno e instala las dependencias automáticamente.
set -e
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$DIR"

if ! command -v python3 >/dev/null 2>&1; then
  echo "No se encontró python3. Instálalo con el gestor de paquetes de tu sistema."
  echo "  Debian/Ubuntu:  sudo apt install python3 python3-venv python3-tk"
  echo "  Fedora:         sudo dnf install python3 python3-tkinter"
  exit 1
fi

if [ ! -d ".venv" ]; then
  echo "Creando entorno (solo la primera vez)…"
  python3 -m venv .venv
fi
# shellcheck disable=SC1091
source .venv/bin/activate

if [ ! -f ".venv/.deps_ok" ]; then
  echo "Instalando dependencias (solo la primera vez)…"
  python -m pip install --upgrade pip
  python -m pip install -r requirements.txt
  touch .venv/.deps_ok
fi

echo "Abriendo Kamiru…"
python -m kamiru
