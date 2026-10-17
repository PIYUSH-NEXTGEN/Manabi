# MANABI 

MANABI helps students and developers find **real-world problems to build** (from
governments, companies, and hackathons), claim them, link a GitHub repo for
auto-tracked progress, talk to a catalog chatbot, and practice production-style
ML questions.

**One service:** FastAPI serves the built React app from `frontend/dist` at `/`
(with SPA fallback) and keeps every API route under `/api`. No nginx needed —
put your platform's TLS / load balancer in front of uvicorn.

## Repo layout

```
MANABI/
├── backend/            # FastAPI API (serves the built frontend too)
│   ├── app/            # routers, services, models, config
│   ├── scripts/        # export_openapi.py
│   ├── requirements.txt
│   ├── start.sh        # prod entrypoint (pip install + uvicorn)
│   └── Procfile        # Render / Railway / Heroku-style
├── frontend/           # Vite + React + TS (calls relative /api/...)
│   └── dist/           # build output — NEVER committed, built on deploy
├── docs/
│   └── openapi.json    # machine-readable API contract
├── DEPLOY.md           # full production runbook (read this to deploy)
└── render.yaml         # one-click Render blueprint
```

Internal working notes (`TASKS.md`, `docs/REQUESTS.md`, `frontend/agent.md`) and
the private dataset (`frontend/projects.txt`) are intentionally **not committed**
— see `.gitignore` and `DEPLOY.md §3`.

## Quick start (local dev)

```sh
# Terminal 1 — backend
cd backend
python -m venv .venv
.venv/Scripts/pip install -r requirements.txt     # macOS/Linux: .venv/bin/pip
copy .env.example .env                            # then edit secrets (never commit .env)
.venv/Scripts/python -m app.seed.import_projects --file ../frontend/projects.txt
.venv/Scripts/python -m app.seed.seed             # ML practice questions (idempotent)
.venv/Scripts/python -m uvicorn app.main:app --port 8000

# Terminal 2 — frontend
cd frontend
npm ci
npm run dev                                       # http://localhost:5173 (proxies /api → :8000)
```

## Tests

```sh
cd backend && ../backend/.venv/Scripts/python -m pytest -q   # LLM_provider forced to mock
cd frontend && npm run test        # Vitest + RTL + MSW
```

## Deploy (summary — full steps in DEPLOY.md)

```sh
cd frontend && npm ci && npm run build     # → frontend/dist/
# set env vars on the host (DATABASE_URL, SESSION_SECRET, BASE_URL,
# GITHUB_CLIENT_ID/SECRET, GEMINI_API_KEY) — never in git
cd ../backend && sh start.sh               # uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

Health check: `GET /api/health` → `{"status":"ok"}`.

## Configuration

| Variable | Purpose |
|---|---|
| `DATABASE_URL` | SQLite (`sqlite:///./app.db`) locally, Postgres (Neon/Supabase) in prod |
| `SESSION_SECRET` | Long random string — app refuses to boot non-local with the placeholder |
| `BASE_URL` | Public origin; drives OAuth callback + cookie Secure/HttpOnly flags |
| `GITHUB_CLIENT_ID` / `GITHUB_CLIENT_SECRET` | GitHub OAuth app for login |
| `LLM_PROVIDER` | `gemini` \| `mock` (mock = offline dev/tests) |
| `GEMINI_API_KEY` / `GEMINI_MODEL` | Gemini key + optional model override |
| `AI_RATE_LIMIT_PER_HOUR` | Ingest + graded ML attempts (default 15) |
| `CHAT_RATE_LIMIT_ANON_PER_HOUR` / `CHAT_RATE_LIMIT_USER_PER_HOUR` | Chat limits (10 / 30) |

Without an LLM key, AI endpoints return `503 {"detail": "AI is not configured yet"}` —
everything else works.
