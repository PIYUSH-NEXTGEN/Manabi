# MANABI backend

FastAPI backend for MANABI: a catalog of curated real-world problems,
GitHub-linked student projects, a catalog chatbot, and personalized recommendations.

## Quick start

macOS/Linux:

```sh
cd backend
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
cp .env.example .env                  # edit only for OAuth or a real LLM; mock works without keys
.venv/bin/python -m alembic upgrade head
# Optional: populate briefs from curated seed packs (no network/LLM):
.venv/bin/python -m app.seed.seed_webdev_projects
.venv/bin/python -m app.seed.seed_webdev_hackathon_projects
.venv/bin/python -m app.seed.seed_webdev_learning_projects
.venv/bin/python -m app.seed.seed_aiml_projects
.venv/bin/python -m app.seed.seed_aiml_hackathon_projects
.venv/bin/python -m app.seed.seed_aiml_learning_projects
.venv/bin/python -m uvicorn app.main:app --port 8000
```

On Windows PowerShell, use `python -m venv .venv`,
`.\.venv\Scripts\python.exe`, and `Copy-Item` instead of `.venv/bin/python`
and `cp`.

The backend is API-only: all routes live under `/api`, and the frontend is
built and served separately (Cloudflare Pages, or `frontend/dist` on any static
host). On Postgres, startup runs `alembic upgrade head` first.

## Tests

```sh
.venv/bin/python -m pytest -q
```

Tests default to `LLM_PROVIDER=mock` and never call a real provider or GitHub.
A few failure-path tests override the provider and still stub the network.
External services are mocked with `respx`; SQLite in-memory via dependency overrides.

## Migrations (Alembic)

Schema changes ship as Alembic migrations (`alembic/versions/`); they work on both SQLite
(dev) and Postgres (prod). On startup, the app runs `create_all` **only** for SQLite;
against Postgres it runs `alembic upgrade head` itself, so prod never silently diverges.

```sh
.venv/bin/python -m alembic upgrade head          # migrate to latest
.venv/bin/python -m alembic history              # list revisions
.venv/bin/python -m alembic revision -m "..."    # create a new revision (hand-edit it)
```

On Windows, use `.\.venv\Scripts\python.exe` instead.

- `DATABASE_URL` is read from `backend/.env` / env. Plain `postgres://` and
  `postgresql://` URLs are normalized to the installed `postgresql+psycopg2`
  driver automatically.
- Run `upgrade head` before starting the app against a fresh Postgres (Neon/Supabase) —
  see `../DEPLOY.md`.

## Configuration (backend/.env, never committed)

| Variable | Purpose |
|---|---|
| `APP_ENV` | `development` (default), `test`, or `production`; production enforces HTTPS, public `BASE_URL`, and non-SQLite `DATABASE_URL` |
| `DATABASE_URL` | SQLite (`sqlite:///./app.db`) or Postgres |
| `SESSION_SECRET` | Session cookie signing key — set a long random string |
| `BASE_URL` | Used for OAuth callback routing (localhost or deployed domain) |
| `GITHUB_CLIENT_ID` / `GITHUB_CLIENT_SECRET` | GitHub OAuth app for login |
| `LLM_PROVIDER` | `gemini`, `anthropic`, or `mock` |
| `GEMINI_API_KEY`, `GEMINI_MODEL` | Gemini (default model in code: `gemini-3.8-flash`) |
| `GEMINI_API_KEYS_EVAL`, `GEMINI_API_KEYS_CHAT` | Optional ordered, comma-separated key pools; exhausted keys rotate out until quota resets |
| `GEMINI_API_KEY_CHAT`, `GEMINI_MODEL_CHAT` | Optional second Gemini project for the chat (default model: `gemini-3.5-flash-lite`); empty falls back to the shared key |
| `ANTHROPIC_API_KEY`, `LLM_MODEL_FAST` | Optional Anthropic provider |
| `CHAT_RATE_LIMIT_PER_DAY` | Chat messages per account per rolling 24 h (login-only; anonymous users are rejected) |
| `ADMIN_GITHUB_USERNAMES` | Comma separated GitHub logins allowed into the `/admin/review` page |
| `LOG_LEVEL`, `LOG_FORMAT`, `SLOW_REQUEST_MS`, `APP_VERSION` | Structured logging controls; see `../DEPLOY.md` |

The full list with defaults and comments is `backend/.env.example`; the
production table is in `../DEPLOY.md`.

The remaining rate limits (submit attempts 10/h, stars 60/h, login 20/h per IP,
progress refresh 10/h, problem create 5/h, reports 5/h, client errors 60/h per
IP, admin sanity cap 100/h) default in `app/config.py` and are documented with
comments in `.env.example`. Every 429 carries a `Retry-After` header, and its message
names the wait ("Try again in about 37 minutes"). Limits live in the
`rate_limit_hits` DB table, so they survive restarts and multi-worker deploys.

Without an LLM key, `POST /api/chat` returns `503 {"detail": "AI is not
configured yet"}`. Submission verification falls back to an offline keyword
check that can only reach `needs_review`; it never auto-verifies or rejects on
an LLM outage.

## API surface

- `GET /api/health/live` — process liveness only
- `GET /api/health` / `GET /api/health/ready` — readiness + DB check
- **Problems:** `GET /api/problems` (filters `q/field/domain/difficulty/goal/tech/source/sort/seed/distinct/limit/offset`), `GET /api/problems/facets`, `GET /api/problems/{id}`, `POST /api/problems` (auth), `POST`/`DELETE /api/problems/{id}/star` (auth)
- **GitHub OAuth:** `GET /api/auth/github/login`, `GET /api/auth/github/callback`, `GET /api/auth/me`, `POST /api/auth/logout`
- **Projects:** `POST /api/problems/{id}/projects` (auth), `GET /api/projects/{id}`, `GET /api/projects/{id}/progress?refresh=`, `PATCH`/`DELETE /api/projects/{id}` (owner/admin), `GET /api/me/projects` (auth), `POST /api/projects/{id}/report` (auth), `POST`/`DELETE /api/projects/{id}/star` (auth)
- **Chat:** `POST /api/chat` (login-only; `[P<id>]` references resolved against the DB, unknown ids stripped)
- **Recommendations:** `GET /api/recommendations` (auth; GitHub signals cached 10 min)
- **Profiles:** `GET /api/u/{username}` (public), `GET /api/me/github-heatmap` (auth)
- **Stats:** `GET /api/stats`
- **Admin:** `GET /api/admin/submissions`, `POST /api/admin/submissions/{id}/approve|reject`, `POST /api/admin/problems/{id}/goal` (admin)
- **Observability:** `POST /api/client-errors` (public, rate limited; logs only)

Full machine-readable contract: `docs/openapi.json` (regenerate from `backend/`
with `.venv/bin/python scripts/export_openapi.py`).

## Security notes

- GitHub tokens, `SESSION_SECRET`, and API keys live server-side only; nothing
  auth-related is ever returned by an API.
- Problem text, repo README excerpts, and user summaries are wrapped as data in
  LLM prompts with instructions to ignore embedded instructions. That reduces
  prompt-injection risk but does not eliminate it.
- Rate limiting is DB-backed (`rate_limit_hits`), so limits survive restarts
  and multi-worker deploys. See `../SECURITY.md` for accepted risks.
