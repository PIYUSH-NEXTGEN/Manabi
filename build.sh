#!/usr/bin/env sh
# MANABI deploy build: backend deps + frontend build → frontend/dist/
# Used by Render (render.yaml). Run from the repo root.
set -e
cd "$(dirname "$0")"

echo "--- backend deps ---"
pip install --no-cache-dir -r backend/requirements.txt

echo "--- frontend build ---"
cd frontend
if command -v npm >/dev/null 2>&1; then
  npm ci
  npm run build
else
  echo "npm not found — skipping frontend build (API-only mode)."
fi
