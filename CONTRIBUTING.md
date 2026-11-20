# Contributing

Thanks for taking a look. MANABI is a small project and contributions are welcome, especially the boring ones: clearer error text, better test coverage, docs that match the app as it is now, and fixes that do not ask for a redesign.

## How the project is organized

The app is one service. The backend is FastAPI and also serves the built frontend. The frontend is Vite plus React plus TypeScript.

Top-level layout:

- `backend/` - the API, models, services, seed scripts, and config
- `frontend/` - the React app, build output, and tests
- `docs/` - machine-readable API contract
- `DEPLOY.md` - the production runbook
- `README.md` - the project overview

If you are touching both sides, read the relevant section of `DEPLOY.md` first so your change fits the production shape.

## Getting started

Backend on Windows PowerShell:

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
Copy-Item .env.example .env
# Edit .env for OAuth or a real LLM; mock mode works without keys.
.\.venv\Scripts\python.exe -m alembic upgrade head
.\.venv\Scripts\python.exe -m uvicorn app.main:app --port 8000
```

Backend on macOS/Linux:

```sh
cd backend
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
cp .env.example .env
# Edit .env for OAuth or a real LLM; mock mode works without keys.
.venv/bin/python -m alembic upgrade head
.venv/bin/python -m uvicorn app.main:app --port 8000
```

Frontend, in a second terminal:

```sh
cd frontend
npm ci
npm run dev
```

The frontend proxy sends `/api` calls to the backend on `localhost:8000`, so you usually do not need to wire anything else for local work. Python 3.12 and Node 22.13.0 are the verified versions; see `README.md` for the supported matrix.

## What counts as a good change

A good change usually does one of these:

- Fixes a verified problem or a clear gap in the docs
- Makes an existing flow easier to follow without changing its behavior
- Adds or improves a test for behavior that is already there
- Cleans up something that has drifted out of date, like this README

A change is less useful when it:

- Rewrites a flow just because a different pattern exists somewhere else
- Adds a feature nobody asked for
- Touches the project model or the submission rules without a reason that is easy to explain in the PR

If you are unsure whether a change is in scope, ask first. A short question saves a lot of rework.

## Working with auth and GitHub

The app uses GitHub OAuth for login. Local development can run with a real OAuth app or with mocks, depending on what you are testing.

If you are touching login, sessions, or any route behind auth, make sure the test coverage still makes sense. Mocked GitHub responses are already in place for the relevant test paths, and new auth behavior should not rely on a live GitHub call in tests.

## Working with AI features

The app supports `gemini`, `anthropic`, and `mock` providers. The mock provider is the default for offline dev and tests. If you add or change anything that touches the LLM path, make sure the tests still run without real provider keys.

`POST /api/chat` returns `503` with a plain message when AI is not configured.
That is intentional; do not hide it. Submission verification is different: with
no LLM it falls back to an offline keyword check that can only reach
`needs_review`.

## Tests

Run the backend tests with:

```sh
cd backend
.venv/bin/python -m pytest -q
```

On Windows, use `.venv\Scripts\python.exe` instead. Backend tests default to
`LLM_PROVIDER=mock`; they never call a real provider or GitHub. A few tests
override the provider to exercise failure paths and still stub the network.

Run the frontend checks with:

```sh
cd frontend
npm run typecheck
npm test
npm run build
```

There is also a Playwright smoke path if you want browser coverage:

```sh
cd frontend
npx playwright install chromium   # first run only
npm run e2e
```

Before you open a PR, run at least the checks for the side you changed. If you
changed both sides, run both. There is no separate backend linter/formatter
configuration; match the surrounding style. `npm run typecheck` is the
frontend's static check.

### If you change the API or database

- API route or schema changes: from `backend/`, run
  `.venv/bin/python scripts/export_openapi.py`, then from `frontend/`, run
  `npm run gen:api`. Commit both `docs/openapi.json` and
  `frontend/src/api/schema.d.ts`.
- Model changes: create an Alembic migration (`alembic revision -m "..."`),
  hand-edit it, and run `alembic upgrade head`. Do not edit migrations that
  have already shipped.
- CI runs the backend suite, SQLite and Postgres migration checks, the frontend
  build/typecheck, Vitest, and the Playwright smoke test on every push and pull
  request. Watch the CI result before asking for review.

No branch naming or commit-message convention is enforced. Keep commits focused
and explain any deploy, migration, or configuration impact in the PR.

## Submitting a change

Please keep PRs small enough to review in one sitting. If a change grows, split it.

A useful PR usually has:
- A short description of what changed and why
- The tests that cover the changed behavior, if any
- A note about anything that needs a deploy step, config change, or migration

If your change affects production setup, say so clearly. The maintainer should not have to read a diff to discover that a secret, migration, or env var is now required.

## Documentation

Docs lag behind code more often than they should. If you touch a feature and notice that `README.md` or `DEPLOY.md` is now wrong, fix the doc in the same PR if you can. A doc update is not glamorous, but it is one of the easiest ways to make the project better.

## Reporting a bug

Please include:
- What you did
- What you expected
- What actually happened
- Whether it happened on local, preview, or deployed instance
- Any relevant error text or request details

If the bug involves submissions, auth, or admin actions, include enough context to reproduce it without reaching into someone else's data.

## Code style

Do less where you can. The project already has enough moving parts.

For the backend, keep routers thin when possible and put business rules where they can be tested without faking too much HTTP. For the frontend, keep components honest about their own state and do not silently swallow errors that users should see.

If you are tempted to add a new dependency, check whether the project already has something that can do the job. New dependencies should pull their weight.
