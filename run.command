#!/usr/bin/env bash
# Lanzador para macOS — doble clic en Finder para abrir la app.
# La primera vez crea un entorno e instala las dependencias automáticamente.
set -e
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$DIR"

if ! command -v python3 >/dev/null 2>&1; then
  osascript -e 'display alert "Falta Python 3" message "Instala Python 3 desde https://www.python.org/downloads/ y vuelve a hacer doble clic en este archivo."' >/dev/null 2>&1 || true
  echo "No se encontró python3. Instálalo desde https://www.python.org/downloads/"
  read -n 1 -s -r -p "Pulsa una tecla para cerrar…"
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
