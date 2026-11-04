# Running MANABI in production

MANABI is **one service**: FastAPI serves the built React app from `frontend/dist` at `/` (with SPA fallback) and keeps every API route under `/api`. No nginx needed; put your platform's TLS/LB in front of uvicorn.

## 0. What you need

- Python 3.11+ and Node 20+ (Node is only needed to build the frontend)
- A generated session secret: `python -c "import secrets; print(secrets.token_urlsafe(32))"`
- A GitHub OAuth app with callback `https://<your-domain>/api/auth/github/callback` (a separate OAuth app from the local one)
- Optionally a Gemini API key (`LLM_PROVIDER=gemini`) — without it, AI endpoints return a calm `503 {"detail": "AI is not configured yet"}` and everything else works

## 1. Build the frontend

```
cd frontend
npm ci
npm run build          # output: frontend/dist/
```

The frontend has zero secrets: all calls are relative `/api/...`. `VITE_USE_MOCKS` must stay `false` for production (it is by default); MSW only activates when it is `true` (that mode exists for the Playwright smoke test).

## 2. Environment variables (set on the server — never in git)

`backend/.env` or platform env vars:

```
DATABASE_URL=<sqlite:///./app.db  — or your Neon/Supabase string>
SESSION_SECRET=<generated above>
BASE_URL=https://<your-domain>
GITHUB_CLIENT_ID=<deployed OAuth app id>
GITHUB_CLIENT_SECRET=<secret>
LLM_PROVIDER=gemini            # or mock to start
GEMINI_API_KEY=<key>
SITE_URL=https://<your-domain>  # site URL
```

Notes:

- `BASE_URL` also controls the OAuth callback and the session-cookie flags (`Secure` + `HttpOnly` when it starts with `https`).
- Postgres URLs from Neon/Supabase (`postgres://...`) are accepted — the engine rewrites the scheme to `postgresql://` and enables `pool_pre_ping` (serverless Postgres kills idle connections; without pre-ping the first request after idle 500s).
- The app refuses to boot with the placeholder `SESSION_SECRET` when `BASE_URL` is not localhost — fail fast beats an impersonatable session cookie.
- Health endpoint for uptime checks: `GET /api/health` (touches the DB, returns `{"status":"ok"}`).

## 3. Migrations + seed data

Run these ONCE locally (or from a GitHub Action), pointed at the production database (`DATABASE_URL`):

```
cd backend
python -m venv .venv
.venv/bin/pip install -r requirements.txt          # + requirements-dev.txt for tests only
.venv/bin/python -m alembic upgrade head           # schema; idempotent
```

- **Migrations are the source of truth for Postgres.** Run `alembic upgrade head` before
  every deploy (on Render: prepend it to the start command, e.g.
  `.venv/bin/python -m alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port $PORT`).
  As a safety net the app itself also runs `upgrade head` on startup when `DATABASE_URL` is Postgres.
- SQLite (local dev) keeps `create_all` on startup; do not rely on that in production.
- The catalog is populated from the saved official SIH fixtures when you run
  `.venv/bin/python scripts/seed_sih_demo.py --limit 40 --reset` pointed at the
  production database. Live-source ingestion (the old crawler and admin review queue)
  was removed; re-adding it is a separate planned effort.

## 4. Start the service

```
cd backend
sh start.sh                   # installs runtime deps, then: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

On Render/Railway a `Procfile` is included (`web: uvicorn app.main:app --host 0.0.0.0 --port $PORT`). If your platform builds from git: extend the start command to run step 1 first, or commit `frontend/dist` from CI.

## 5. Post-deploy checks

1. `curl https://<domain>/api/health` → `{"status":"ok"}`
2. `curl https://<domain>/api/stats` → real counts (non-zero problems/sources)
3. `curl https://<domain>/problems` → the SPA HTML with `<title>MANABI</title>`
4. `curl -I https://<domain>/assets/<asset from dist>` → `200` + correct `content-type`
5. Log in with GitHub in the browser → redirected home, username in the nav
6. Chat dock → ask → reply links point at real catalog problems

## Rate limits (env-tunable)

`CHAT_RATE_LIMIT_ANON_PER_HOUR=10`, `CHAT_RATE_LIMIT_USER_PER_HOUR=30`. The UI shows the backend's raw limit messages honestly when they trip.
