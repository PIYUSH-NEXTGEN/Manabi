#!/usr/bin/env sh
# MANABI single-service start (Linux/macOS/Render/Railway/Fly box).
# Assumes: frontend/dist already built (see DEPLOY.md) and env vars set.
set -e
cd "$(dirname "$0")"

pip install --no-cache-dir -r requirements.txt

# Give in-flight requests a bounded window to finish; without this an
# abandoned dependency call can block a deploy forever. Access logging lives in
# the app middleware (structured, request-id aware), so uvicorn's plain access
# log is disabled to avoid a second, less useful line per request.
exec uvicorn app.main:app --host 0.0.0.0 --port "${PORT:-8000}" --timeout-graceful-shutdown 25 --no-access-log
