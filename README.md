# MANABI 

MANABI helps students and developers find **real-world problems to build** (from
governments, companies, and hackathons), claim them, link a GitHub repo for
auto-tracked progress, and talk to a catalog chatbot. Public problem statements are
discovered by a compliance-first crawler and reviewed before they go live.

**One service:** FastAPI serves the built React app from `frontend/dist` at `/`
(with SPA fallback) and keeps every API route under `/api`. No nginx needed —
put your platform's TLS / load balancer in front of uvicorn.

## Repo layout

```
MANABI/
├── backend/            # FastAPI API (serves the built frontend too)
│   ├── app/            # routers, services, crawler, models, config
│   ├── scripts/        # export_openapi.py
│   ├── requirements.txt
│   ├── start.sh        # prod entrypoint (pip install + uvicorn)
│   └── Procfile        # Render / Railway / Heroku-style
├── frontend/           # Vite + React + TS (calls relative /api/...)
│   └── dist/           # build output — NEVER committed, built on deploy
├── docs/
│   ├── crawler.md      # crawler architecture, add-a-source checklist, ops
│   ├── sources/        # per-source compliance records
│   └── openapi.json    # machine-readable API contract
├── DEPLOY.md           # full production runbook (read this to deploy)
└── render.yaml         # one-click Render blueprint
```



## Quick start (local dev)

```sh
# Terminal 1 — backend
cd backend
python -m venv .venv
.venv/Scripts/pip install -r requirements.txt     # macOS/Linux: .venv/bin/pip
copy .env.example .env                            # then edit secrets (never commit .env)
.venv/Scripts/python -m alembic upgrade head
# optional demo data from the saved official SIH fixtures (no network/LLM):
.venv/Scripts/python scripts/seed_sih_demo.py --limit 40
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
| `CHAT_RATE_LIMIT_ANON_PER_HOUR` / `CHAT_RATE_LIMIT_USER_PER_HOUR` | Chat limits (10 / 30) |
| `CRAWLER_ENABLED` | Kill switch — crawler exits while `false` (default) |
| `CRAWLER_CONTACT` | Required contact in the crawler User-Agent |
| `CRAWLER_REQUIRE_POSTGRES` | Refuse to crawl a SQLite database |
| `CRAWLER_MAX_REQUESTS_PER_RUN` / `CRAWLER_MAX_LLM_CALLS` | Per-run caps (400 / 200) |
| `SITE_URL` | Site URL shown in the crawler User-Agent |
| `ADMIN_GITHUB_USERNAMES` | Comma-separated logins allowed into `/admin/review` |

Without an LLM key, AI endpoints return `503 {"detail": "AI is not configured yet"}` —
everything else works.

## Crawler

```sh
cd backend
CRAWLER_ENABLED=true CRAWLER_CONTACT=you@example.com \
  .venv/Scripts/python -m app.crawler.run --source sih-2026 --dry-run --limit 5
```

Every source needs a compliance record in `docs/sources/` and a registry entry in
`backend/app/crawler/sources/`. The crawler enforces robots.txt, throttling, a
contact User-Agent, SSRF protections and a kill switch. Low-confidence or duplicate
items go to the admin review queue at `/admin/review`. Full guide:
[`docs/crawler.md`](docs/crawler.md).
