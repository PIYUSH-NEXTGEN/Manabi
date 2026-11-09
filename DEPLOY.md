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
- The catalog is populated from the seed scripts (`scripts/seed_*_web_projects.py`)
  and manual curation in the app; production data is curated offline.

## 3b. The 0004_cleanup migration (required before running this deploy)

Revision `0004_cleanup` **drops** every table of the removed ops features
(webhooks, api-contracts, tenant-security, incidents, file-ingestion, analytics,
accessibility, inventory, offline-sync, workflows — 36 tables) plus the crawler
bookkeeping tables (`crawl_runs`, `crawl_items`) and 8 crawler-only columns on
`problems`. Core data (`users`, `problems`, `projects`) is never touched, and the
migration is defensive: it inspects the schema first and skips anything already
absent, so it also succeeds on a database where earlier revisions never ran.

Before deploying:

1. **Take a full database backup** (`pg_dump -Fc -f manabi-pre-0004.dump $DATABASE_URL`).
   `0004.downgrade` recreates the dropped schema *empty* — dropped rows are only
   recoverable from this backup.
2. **If the dropped tables hold rows you care about**, export them from the backup
   before deploying (they will not survive otherwise).
3. Run the deploy, then verify:
   - `alembic current` → `0004_cleanup (head)`
   - the dropped tables are gone and `users` / `problems` / `projects` row counts
     match the pre-deploy counts.

### If `alembic upgrade head` fails with "table ... already exists"

That means the database was created by `create_all` (tables exist physically)
while `alembic_version` lags behind. Re-running the failing revision from scratch
cannot work; instead **stamp the version to the revision matching the physical
state, then upgrade forward**:

```
# If the DB already contains e.g. webhook_endpoints / crawl_runs
# (i.e. the physical schema matches 0003's output), stamp 0003 first:
alembic stamp 0003_advanced_projects
alembic upgrade head          # now only 0004_cleanup runs, and it is defensive
alembic current               # expect: 0004_cleanup (head)
```

Only stamp when you have verified `alembic current` lags behind but the tables
of that revision really exist. If `alembic current` is already `0003_advanced_projects`
or the DB is genuinely empty, a plain `alembic upgrade head` just works.
If the version lags for a **partially** created schema (some of a revision's
tables exist, some don't), reconcile manually from a copy first — do not stamp.

The local dev SQLite DB has this exact shape (version `0002_crawler`, tables
created by `create_all`): take a copy, `alembic stamp 0003_advanced_projects`,
then `alembic upgrade head` on the copy. Only after the copy checks out, repeat
on the real `app.db`.

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
5. `curl https://<domain>/api/problems/<known id>` → 200; the response must not
   contain crawler fields (`content_hash`, `crawl_source_key`, `source_status`, …)
6. `alembic current` → `0006_problem_goal (head)`; log in with GitHub in the browser → redirected home, username in the nav
7. Chat dock → ask → reply links point at real catalog problems

## Rate limits (env-tunable)

`CHAT_RATE_LIMIT_ANON_PER_HOUR=10`, `CHAT_RATE_LIMIT_USER_PER_HOUR=30`, and
`PROBLEM_CREATE_PER_HOUR=5` (problem creation per user per hour; admins are
exempt). The UI shows the backend's raw limit messages honestly when they trip.

## 6. The submission-verification system (0005) — production checklist

Revision `0005_project_verification` adds columns on `projects`
(`verification_status` default `needs_review`), a partial unique index
`uq_project_repo_github_id_user_id` and the `project_reports` table. It is
additive and safe: `0005.downgrade` only removes what it added.

1. **Backup**: `pg_dump -Fc -f manabi-pre-0005.dump $DATABASE_URL`.
2. **Check the stamp on a copy first**: the production DB must be at
   `0004_cleanup` before `upgrade head` (the app auto-runs `upgrade head` on
   Postgres at startup, so a lagging stamp usually never happens here — verify
   with `alembic current` on a restored copy).
3. **Deploy** and confirm `alembic current` → `0005_project_verification (head)`.
4. **Run the one-time re-verification dry run** (backfilled rows get
   `relevance_checked_at = NULL`; this populates real relevance evidence):

   ```
   cd backend
   python scripts/reverify_projects.py            # dry run — no writes, CSV report
   # review backend/scripts/reverify_report.csv, then:
   python scripts/reverify_projects.py --apply    # or --limit 20 to go in batches
   ```

   The script needs working `LLM_PROVIDER` config (it re-runs the relevance
   check) and uses each owner's stored GitHub token when present. It is
   **fail safe**: LLM or GitHub failure downgrades to `needs_review`, never to
   `verified`, and it never inflates counts by force — statuses only move to
   `verified` when the model itself confirms relevance (§6.4). Tokens are
   never printed or written to the CSV.
5. **Smoke test** the money path: submit a repo you own against any problem
   (expect 201 + `needs_review` from the mock LLM or a real score with
   Gemini), then approve it at `/admin/review`, then confirm the problem page
   shows the verified-only counts.

### Verification rules at a glance (details in backend/app/services/verification.py)

- **Ownership (hard gate)**: the repo owner by GitHub numeric id (the only
  accepted basis for a personal repo — a collaborator invite is not
  ownership), push/admin permission from the authenticated repo payload for
  organization-owned repos, or ≥ `CONTRIBUTOR_MIN_COMMITS` (3) entries under
  your own id in `/contributors`. Username string matches are never trusted.
- **Anti-abuse**: `MAX_SUBMISSIONS_PER_DAY` (5 rolling 24h),
  `MAX_ACTIVE_PROJECTS_PER_USER` (10 non-rejected rows), one repo per user per
  problem, one GitHub repo id per problem across everyone (legacy rows with a
  NULL `repo_github_id` are exempt until re-verified), forks rejected unless
  `ALLOW_FORK_SUBMISSIONS=true`, archived/disabled repos rejected.
- **Relevance**: Gemini judges a `<problem>` block against a `<repository>`
  block (README excerpt ≤ 4000 chars) and the submitter's summary — all
  untrusted data is delimited and the prompt tells the model to ignore
  instructions inside it. Score ≥ `RELEVANCE_VERIFY_MIN` (0.70) → `verified`;
  ≥ `RELEVANCE_REJECT_BELOW` (0.35) → `needs_review`; below → hard 422. LLM
  outages fall back to a keyword heuristic that can only reach
  `needs_review`, never `verified`. Repos older than
  `PREEXISTING_REPO_DAYS` (180) also need ≥ 0.85 to auto-verify.
- **Re-verification paths**: progress refresh / project detail can flip a row
  to `needs_review` (repo gone, renamed — tracked by the immutable GitHub id —
  or ownership lost); a `needs_review` row auto-re-checks once per
  `AUTO_REVERIFY_MIN_INTERVAL_HOURS` (24) when the repo gains a README + 3
  commits; editing the solution summary re-runs the check at most once per
  that interval (429 `verification_rate_limited` otherwise).
- **Human review**: admins run the submissions queue at `/admin/review`
  (approve → `verified`, reject → `rejected`). Reports: any viewer may report
  a verified project once; ≥ `REPORTS_BEFORE_REVIEW` (3) reports flips the row
  back to `needs_review` for an admin.
- **Limitation (known)**: contributor detection matches by GitHub **account
  id**; if your commit emails are not linked to that account, your commits do
  not appear in `/contributors` and contributor-based ownership fails even
  though you contributed. Fix upstream (add the email to your GitHub account)
  or submit with push access. This is a GitHub limitation, not a MANABI bug;
  it is documented in the final report.

### Token storage note (report-only, deliberately not implemented)

`users.github_token` (OAuth access token) is stored **in plaintext**,
`String(255)`, inside the database. Pre-existing behaviour — this change set
did not touch it — but the risk is documented: a database dump or SQLi leaks
every user's GitHub token. Recommended hardening (not in this PR): encrypt at
rest with an env-held key (`SESSION_SECRET` or a dedicated `GITHUB_TOKEN_KEY`)
using Fernet/AES, decrypt only in the GitHub service layer, and rotate the
defunct fallback collection. Ask before implementing.
