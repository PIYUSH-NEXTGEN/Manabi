# MANABI

MANABI is a catalog of real problems worth building. Students pick a brief,
link their GitHub repo, and the site tracks their progress from public repo
activity. A chat assistant helps you choose, and everything runs on a single
FastAPI service that also serves the built frontend.

Problem briefs are curated manually, via seed scripts and the app itself — the
app needs no network sources. Automated crawling was evaluated early on and
intentionally removed: several public sources prohibit scraping. The seed files
fill in web, mobile, ML, data science, cloud, cybersecurity, systems, and web3
briefs.

## What the app does

- Problem board with search plus field, difficulty, and domain filters
- Problem detail pages with tech stack, build guide, and future ideas
- Submit a project by repo URL, then auto-tracked progress badges
- Dashboard that follows your claimed problems and activity
- Catalog chat with rate limits and an honest mock mode for offline work
- Admin review page at `/admin/review`, gated by `ADMIN_GITHUB_USERNAMES`
- Night mode with a persisted toggle

**One service:** FastAPI serves the built React app from `frontend/dist` at `/`
(with SPA fallback) and keeps every API route under `/api`. No nginx needed.
Put your platform's TLS or load balancer in front of uvicorn.

## Repo layout

```
MANABI/
├── backend/            # FastAPI API (serves the built frontend too)
│   ├── app/            # routers, services, models, seed files, config
│   ├── scripts/        # seed_*_web_projects.py, export_openapi.py
│   ├── requirements.txt
│   ├── start.sh        # prod entrypoint (pip install + uvicorn)
│   └── Procfile        # Render / Railway / Heroku-style
├── frontend/           # Vite + React + TS (calls relative /api/...)
│   └── dist/           # build output, never committed, built on deploy
├── docs/
│   └── openapi.json    # machine-readable API contract
├── DEPLOY.md           # full production runbook (read this to deploy)
└── render.yaml         # one-click Render blueprint
```

## Quick start (local dev)

```sh
# Terminal 1, backend
cd backend
python -m venv .venv
.venv/Scripts/pip install -r requirements.txt     # macOS/Linux: .venv/bin/pip
copy .env.example .env                            # then edit secrets (never commit .env)
.venv/Scripts/python -m alembic upgrade head
.venv/Scripts/python scripts/seed_beginner_web_projects.py
.venv/Scripts/python -m uvicorn app.main:app --port 8000

# Terminal 2, frontend
cd frontend
npm ci
npm run dev                                       # http://localhost:5173 (proxies /api -> :8000)
```

## Demo and seed data

The app starts empty. Load briefs without any network or LLM call:

```sh
cd backend
.venv/Scripts/python scripts/seed_beginner_web_projects.py
.venv/Scripts/python scripts/seed_intermediate_web_projects.py
```

Summaries are clearly generated, never verbatim source text. Seed scripts are
for local setups and demos; the production database is fully curated offline.

## Tests

```sh
cd backend && .venv/Scripts/python -m pytest -q    # LLM provider forced to mock
cd frontend && npm run test                        # Vitest + Testing Library + MSW
```

Playwright e2e is also wired up in `frontend` (`npm run e2e`) if you want
browser coverage.

## Deploy (summary, full steps in DEPLOY.md)

```sh
cd frontend && npm ci && npm run build     # -> frontend/dist/
# set env vars on the host (DATABASE_URL, SESSION_SECRET, BASE_URL,
# GITHUB_CLIENT_ID/SECRET, LLM keys); never in git
cd ../backend && sh start.sh               # uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

Health check: `GET /api/health` returns `{"status":"ok"}`.

## Configuration

| Variable | Purpose |
|---|---|
| `DATABASE_URL` | SQLite (`sqlite:///./app.db`) locally, Postgres (Neon/Supabase) in prod |
| `SESSION_SECRET` | Long random string. The app refuses to boot non-local with the placeholder |
| `BASE_URL` | Public origin, drives OAuth callback and cookie Secure/HttpOnly flags |
| `GITHUB_CLIENT_ID` / `GITHUB_CLIENT_SECRET` | GitHub OAuth app for login |
| `LLM_PROVIDER` | `gemini`, `anthropic`, or `mock` (mock for offline dev and tests) |
| `GEMINI_API_KEY` / `GEMINI_MODEL` / `ANTHROPIC_API_KEY` | Provider keys and optional model override |
| `CHAT_RATE_LIMIT_ANON_PER_HOUR` / `CHAT_RATE_LIMIT_USER_PER_HOUR` | Chat rate limits (10 / 30) |
| `ADMIN_GITHUB_USERNAMES` | Comma separated GitHub logins allowed into the `/admin/review` page |

Without LLM keys, AI endpoints return `503 {"detail": "AI is not configured yet"}`.
Everything else works fine without them.
