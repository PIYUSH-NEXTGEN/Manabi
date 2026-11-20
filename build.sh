#!/usr/bin/env sh
# MANABI deploy build: backend deps + frontend build → frontend/dist/
# Used by Render (render.yaml). Run from the repo root.
set -e
cd "$(dirname "$0")"

echo "--- backend deps ---"
python -m pip install --upgrade "pip==26.3"
python -m pip install --no-cache-dir -r backend/requirements.txt

echo "--- frontend build ---"
cd frontend
if ! command -v npm >/dev/null 2>&1; then
  echo "ERROR: npm is required to build the frontend." >&2
  exit 1
fi
npm ci
npm run build
if [ ! -f dist/index.html ]; then
  echo "ERROR: frontend build produced no dist/index.html." >&2
  exit 1
fi
