#!/usr/bin/env sh
# MANABI single-service start (Linux/macOS/Render/Railway/Fly box).
# Assumes: frontend/dist already built (see DEPLOY.md) and env vars set.
set -e
cd "$(dirname "$0")"

pip install --no-cache-dir -r requirements.txt

exec uvicorn app.main:app --host 0.0.0.0 --port "${PORT:-8000}"
