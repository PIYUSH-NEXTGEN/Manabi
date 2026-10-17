# MANABI backend

FastAPI backend for MANABI: a catalog of real-world problems (from hackathon sources),
GitHub-linked student projects, AI-assisted problem ingestion, rubric-graded ML
practice questions, a catalog chatbot, and personalized recommendations.

## Quick start

```
cd backend
python -m venv .venv                    # Windows:  .venv\Scripts\python
.venv\Scripts\pip install -r requirements.txt
copy .env.example .env                  # then edit (session secret, GitHub OAuth, LLM key)
.venv\Scripts\python -m app.seed.import_projects --file ../frontend/projects.txt
.venv\Scripts\python -m app.seed.seed   # ML practice questions (idempotent)
.venv\Scripts\python -m uvicorn app.main:app --port 8000
```

On start the app serves `frontend/dist` incl. SPA fallback if the frontend is built;
otherwise it is API-only. All API routes live under `/api`.

## Tests

```
.venv\Scripts\python -m pytest -q
```

Tests always run with `LLM_PROVIDER=mock` — they never call a real LLM or real GitHub.
External services are mocked with `respx`; SQLite in-memory via dependency overrides.

## Configuration (backend/.env, never committed)

| Variable | Purpose |
|---|---|
| `DATABASE_URL` | SQLite (`sqlite:///./app.db`) or Postgres |
| `SESSION_SECRET` | Session cookie signing key — set a long random string |
| `BASE_URL` | Used for OAuth callback routing (localhost or deployed domain) |
| `GITHUB_CLIENT_ID` / `GITHUB_CLIENT_SECRET` | GitHub OAuth app for login |
| `LLM_PROVIDER` | `gemini` \| `anthropic` \| `mock` |
| `GEMINI_API_KEY`, `GEMINI_MODEL` | Gemini (default model in code: `gemini-3.8-flash`) |
| `ANTHROPIC_API_KEY`, `LLM_MODEL_FAST` | Optional Anthropic provider |
| `AI_RATE_LIMIT_PER_HOUR` | Rate limit for ingest + graded ML attempts |
| `CHAT_RATE_LIMIT_ANON_PER_HOUR` / `CHAT_RATE_LIMIT_USER_PER_HOUR` | Chat limits |

Without an LLM key the AI endpoints return `503 {"detail": "AI is not configured yet"}`.

## API surface

- `GET /api/health` — liveness + DB check
- **Problems:** `GET /api/problems` (filters `q/field/domain/difficulty/tech/source/sort/limit/offset`), `GET /api/problems/facets`, `GET /api/problems/{id}`, `POST /api/problems` (auth)
- **GitHub OAuth:** `GET /api/auth/github/login`, `GET /api/auth/github/callback`, `GET /api/me`, `POST /api/auth/logout` (logout is POST)
- **Projects:** `POST /api/problems/{id}/projects` (auth), `GET /api/projects/{id}`, `GET /api/projects/{id}/progress?refresh=`, `GET /api/me/projects` (auth)
- **Ingestion:** `POST /api/ingest` (auth, rate limited; SSRF-guarded fetch → AI draft, not saved)
- **ML practice:** `GET /api/ml/questions`, `GET /api/ml/questions/{id}`, `POST /api/ml/questions/{id}/attempts` (auth, rate limited), `GET /api/ml/questions/{id}/attempts/me` — rubrics are never sent to clients; explanations unlock after an attempt
- **Chat:** `POST /api/chat` (public; [P<id>] references resolved against the DB, fake ids stripped)
- **Recommendations:** `GET /api/recommendations` (auth; GitHub signals cached 10 min)
- **Stats:** `GET /api/stats`
- **Stretch:** `GET /api/u/{username}` — public profile

Full machine-readable contract: `docs/openapi.json` (regenerate with
`python scripts/export_openapi.py`).

## Security notes

- GitHub tokens, `SESSION_SECRET`, and API keys live server-side only; nothing auth
  -related is ever returned by an API.
- Outbound fetches (ingest) are SSRF-guarded: http/https only, ports 80/443,
  private/loopback/link-local/reserved IP resolution rejected (including after each
  redirect), 3-redirect cap, 8s timeout, 500 KB size cap, HTML/text only.
- The DB is open to pattern-injection style data (user answers, fetched pages) — all
  such text is wrapped as data in LLM prompts with explicit instructions to ignore
  embedded instructions.
- Known post-hackathon hardening TODOs: DNS-TOCTOU (resolve-time pinning), durable
  (Redis/DB) rate limiting instead of in-memory counters.
