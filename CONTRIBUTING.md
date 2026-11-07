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

To work on the backend:

```sh
cd backend
python -m venv .venv
.venv/Scripts/pip install -r requirements.txt
copy .env.example .env
# edit .env with real values if you want the full stack; mock mode is fine for a lot of work
.venv/Scripts/python -m alembic upgrade head
.venv/Scripts/python -m uvicorn app.main:app --port 8000
```

To work on the frontend:

```sh
cd frontend
npm ci
npm run dev
```

The frontend proxy sends `/api` calls to the backend on `localhost:8000`, so you usually do not need to wire anything else for local work.

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

The API returns `503` with a plain message when AI is not configured. That is intentional. Do not treat that as something to hide away.

## Tests

Run the backend tests with:

```sh
cd backend && .venv/Scripts/python -m pytest -q
```

The backend tests force the LLM provider to mock, so they do not need real keys.

Run the frontend tests with:

```sh
cd frontend && npm run test
```

There is also a Playwright smoke path if you want browser coverage:

```sh
cd frontend && npm run e2e
```

Before you open a PR, run at least the test suite for the side you changed. If you changed both sides, run both.

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
