# Running MANABI in production

MANABI deploys as **two services plus a database**:

- the React app as a static build on **Cloudflare Pages**;
- the FastAPI API on **Render**, with every route under `/api`;
- **Supabase** Postgres for durable data.

The API is API-only: it does not serve `frontend/dist`. The default deployment
keeps one browser origin: a Cloudflare Pages Function proxies `/api/*` to
Render, so the session cookie is first-party and login works. The backend's
`BASE_URL` and `FRONTEND_URL` then point at the Pages origin.

A direct cross-origin setup also works (`VITE_API_BASE_URL` set to the Render
origin), but the cookie becomes third-party; login is only dependable when both
hosts share a registrable domain. The same code still works as a single-service
deploy when frontend and API share an origin.

The application itself has no background workers, queues, or scheduled jobs.
GitHub and the LLM providers are called synchronously from
request/verification code. A separate, optional Cloudflare Worker
(`keepalive-worker/`) pings the health endpoints on a schedule so the free
Render instance does not spin down; see section 1.3.

```text
Browser
  -> Cloudflare Pages (TLS + static React build, SPA fallback via _redirects)
  -> /api/... cross-origin fetch (credentials: include)
       -> Render edge TLS / load balancer
       -> one uvicorn process (FastAPI, API only)
            -> Supabase Postgres (pooled connection, TLS required)
            -> GitHub API / Gemini or Anthropic (optional features)
```

## 0. Requirements

- Python 3.12.7 (what `render.yaml` pins; CI targets the 3.12 line). Python
  3.11 is not covered by CI.
- Node 22.13.0 and npm 10+ to build the frontend (Cloudflare Pages reads
  `package.json` engines; `.node-version` pins the same version locally).
- A Cloudflare Pages project whose build root is `frontend/`.
- A Supabase project with its **Supavisor session-pooler** connection string
  (IPv4). The direct `db.<ref>.supabase.co` host is IPv6-only and Render's
  egress is generally IPv4, so use the pooler URL.
- A durable Postgres database. SQLite is for local development and tests only.
- A generated session secret:
  `python -c "import secrets; print(secrets.token_urlsafe(32))"`.
- A GitHub OAuth app whose callback is
  `https://<your-domain>/api/auth/github/callback` if login is enabled.
- Optionally a Gemini or Anthropic key. Without one, `POST /api/chat` returns
  `503 {"detail": "AI is not configured yet"}`. Submission verification falls
  back to an offline keyword check that can only reach `needs_review`; it never
  auto-verifies or rejects on an LLM outage. The rest of the app works.

## 1. Build

### 1.1 Frontend on Cloudflare Pages

Create a Pages project connected to this repository and set:

| Setting | Value |
|---|---|
| Build command | `npm ci && npm run build` |
| Build output directory | `dist` |
| Root directory | `frontend` |
| `VITE_API_BASE_URL` | Empty. API calls stay relative and go through the proxy below. |
| `VITE_USE_MOCKS` | `false` |
| `API_ORIGIN` | `https://<your-service>.onrender.com` (no trailing slash) |

`frontend/functions/api/[[path]].ts` is a Pages Function that forwards every
`/api/*` request to `API_ORIGIN`. The site and the API therefore share the
`*.pages.dev` origin, so the session cookie is first-party and login works.
Point the API's `BASE_URL` at this Pages origin to match (see section 2).

If you prefer the direct cross-origin setup (no Function, `VITE_API_BASE_URL`
set to the Render origin), expect the session cookie to be treated as a
third-party cookie: browsing works, but login usually fails unless both hosts
share a registrable domain (for example `app.example.com` and `api.example.com`).

The build outputs `frontend/dist`. `frontend/public/_redirects` is copied into
the output and gives client-side routes (`/problems/12`, `/admin/review`) an
`index.html` fallback, which Pages does not guarantee on its own. Functions
run before that fallback, so `/api/*` is never captured by it.

The frontend has no secrets. `VITE_*` values are compiled into the public
bundle, so never put a key in one.

The equivalent local build is:

```sh
cd frontend
npm ci
npm run build
```

### 1.2 Backend on Render

`render.yaml` installs only the pinned backend runtime dependencies:

```sh
python -m pip install --upgrade "pip==26.3"
python -m pip install --no-cache-dir -r backend/requirements.txt
```

The repository-root `build.sh` still installs the backend deps and builds
`frontend/dist`; it is for single-service deploys and local verification, not
for the split Render service.

### 1.3 Keepalive Worker (optional)

Render spins a free web service down after 15 minutes without inbound traffic
and takes about a minute to wake. `keepalive-worker/` is a small Cloudflare
Worker that resets that timer:

| Cron | Request | Purpose |
|---|---|---|
| `*/10 * * * *` | `GET /api/health/live` | Keeps the Render instance awake |
| `17 6 * * *` | `GET /api/health/ready` | Runs a query so free Supabase does not pause |

The Worker targets `TARGET_URL` (default `https://manabi-bsh.pages.dev`, which
the Pages Function proxies to Render). Change the `vars` block in
`keepalive-worker/wrangler.jsonc` if your public origin differs.

```sh
cd keepalive-worker
npm install
npx wrangler deploy
```

**Render free-tier budget:** 750 instance hours per workspace per calendar
month, shared by every free web service. Keeping one service awake 24/7 uses
about 744 hours in a 31-day month, leaving roughly 6 hours. Exceeding the cap
suspends all free web services until the next month, so keep this as the only
free web service. The interval must stay below 15 minutes; 10 minutes leaves
headroom for scheduler jitter.

## 2. Environment variables

Set these in the platform dashboard, never in Git. `backend/.env` is only for
local development and is ignored.

| Variable | Required | Sensitive | Purpose / default |
|---|---|---|---|
| `APP_ENV` | Production | No | `development`, `test`, or `production`. Render sets `production`; startup then rejects localhost, HTTP, and SQLite. |
| `DATABASE_URL` | Production | **Yes** | Managed Postgres connection string. Local default is `sqlite:///./app.db`. |
| `SESSION_SECRET` | Production | **Yes** | Session-cookie signing key, at least 32 random characters. The placeholder is rejected outside localhost. |
| `BASE_URL` | Production | No | Public HTTPS origin the browser uses to reach the API. With the Pages proxy this is the Pages origin (`https://manabi.pages.dev`), so the OAuth callback goes back through the proxy; with a direct cross-origin setup it is the API origin (`https://manabi.onrender.com`). Drives the GitHub OAuth callback and cookie flags, and must match the OAuth app's callback URL. No trailing slash. |
| `FRONTEND_URL` | Split deploy | No | Public HTTPS origin of the browser app, e.g. `https://manabi.pages.dev`. Used for the post-login redirect and always allowed by CORS. Empty keeps same-origin behavior. Production rejects a non-HTTPS value. |
| `CORS_ALLOW_ORIGINS` | Optional | No | Comma-separated extra origins allowed to call the API with cookies. `FRONTEND_URL` is added automatically; the default is `http://localhost:5173`. |
| `GITHUB_CLIENT_ID` | Optional | No | GitHub OAuth app client id. Login is disabled when empty. |
| `GITHUB_CLIENT_SECRET` | Optional | **Yes** | GitHub OAuth app secret. |
| `LLM_PROVIDER` | Optional | No | `gemini`, `anthropic`, or `mock`; default `mock`. |
| `GEMINI_API_KEY` | Optional | **Yes** | Shared Gemini key. |
| `GEMINI_MODEL` | Optional | No | Gemini model override. |
| `GEMINI_API_KEYS_EVAL` | Optional | **Yes** | Ordered evaluation key pool, comma-separated. |
| `GEMINI_API_KEYS_CHAT` | Optional | **Yes** | Ordered chat key pool, comma-separated. |
| `GEMINI_API_KEY_CHAT` | Optional | **Yes** | Separate Gemini project key for chat. |
| `GEMINI_MODEL_CHAT` | Optional | No | Chat model override. |
| `ANTHROPIC_API_KEY` | Optional | **Yes** | Anthropic key when `LLM_PROVIDER=anthropic`. |
| `LLM_MODEL_FAST` | Optional | No | Fast-model override. |
| `CHAT_RATE_LIMIT_PER_DAY` | Optional | No | Chat messages per account per rolling 24h; default `20`. |
| `SUBMIT_RATE_LIMIT_PER_HOUR` | Optional | No | Submit attempts per account per hour; default `10`. |
| `AUTH_LOGIN_RATE_LIMIT_PER_HOUR` | Optional | No | Login attempts per client IP per hour; default `20`. |
| `STAR_RATE_LIMIT_PER_HOUR` | Optional | No | Star toggles per account per hour; default `60`. |
| `ADMIN_RATE_LIMIT_PER_HOUR` | Optional | No | Shared admin sanity cap; default `100`. |
| `PROGRESS_REFRESH_RATE_LIMIT_PER_HOUR` | Optional | No | Forced progress refreshes; default `10`. |
| `PROBLEM_CREATE_PER_HOUR` | Optional | No | Problem publishing per user per hour; default `5`. |
| `REPORT_RATE_LIMIT_PER_HOUR` | Optional | No | Project reports per user per hour; default `5`. |
| `CLIENT_ERROR_RATE_LIMIT_PER_HOUR` | Optional | No | Browser error reports per client IP per hour; default `60`. |
| `LOG_LEVEL` | Optional | No | `DEBUG`, `INFO`, `WARNING`, `ERROR`, or `CRITICAL`; default `INFO`. |
| `LOG_FORMAT` | Optional | No | `json` or `text`; defaults to JSON in production and text in development/test. |
| `SLOW_REQUEST_MS` | Optional | No | Requests at or above this duration log a `slow_request` warning; default `2000`. |
| `APP_VERSION` | Optional | No | Release stamp attached to every log line. Falls back to `RENDER_GIT_COMMIT`, then `dev`. |
| `ADMIN_GITHUB_USERNAMES` | Optional | No | Comma-separated GitHub logins allowed into `/admin/review`. |
| `RELEVANCE_VERIFY_MIN` | Optional | No | Auto-verify score threshold; default `0.70`. |
| `RELEVANCE_REJECT_BELOW` | Optional | No | Hard-reject score threshold; default `0.35`. |
| `CONTRIBUTOR_MIN_COMMITS` | Optional | No | Contributor ownership minimum; default `3`. |
| `MAX_ACTIVE_PROJECTS_PER_USER` | Optional | No | Active-project cap; default `10`. |
| `MAX_SUBMISSIONS_PER_DAY` | Optional | No | Rolling submission cap; default `5`. |
| `PREEXISTING_REPO_DAYS` | Optional | No | Older-repo scrutiny threshold; default `180`. |
| `ALLOW_FORK_SUBMISSIONS` | Optional | No | Allow fork submissions; default `false`. |
| `AUTO_REVERIFY_MIN_INTERVAL_HOURS` | Optional | No | Automatic re-check interval; default `24`. |
| `REPORTS_BEFORE_REVIEW` | Optional | No | Reports needed to trigger review; default `3`. |

Platform/build variables:

| Variable | Required | Sensitive | Purpose |
|---|---|---|---|
| `PORT` | Platform | No | Uvicorn bind port. Render supplies it. |
| `PYTHON_VERSION` | Render | No | `3.12.7`. |
| `NODE_VERSION` | Cloudflare Pages | No | `22.13.0`; keep in sync with `.node-version`. Render never builds the frontend, so it needs no Node pin. |
| `FORWARDED_ALLOW_IPS` | Proxied hosts | No | Uvicorn trusted proxy CIDRs. Defaults to loopback only; see section 6. Behind Cloudflare, requests reach Render from Cloudflare egress IPs (or the Pages proxy), so per-IP limits may bucket together until this is set to the real proxy range. |
| `VITE_USE_MOCKS` | Build | No | Must be `false` in production. |
| `VITE_API_BASE_URL` | Build | No | Backend origin for a split deploy, e.g. `https://manabi.onrender.com`. Empty keeps relative `/api/...` calls. |
| `VITE_CONTACT_EMAIL` | Build | No | Public contact address. |
| `VITE_GITHUB_ISSUES_URL` | Build | No | Public issue-tracker URL. |
| `VITE_MASCOT_RIVE_SRC` | Build | No | Public Rive asset path; empty uses the PNG fallback. |
| `VITE_APP_VERSION` | Build | No | Release stamp attached to browser error reports. |

`VITE_*` values are compiled into the public bundle. Never put a secret in one.

## 3. Production configuration guard

When `APP_ENV=production`, the app refuses to start if:

- `BASE_URL` is not a public `https://` origin;
- `BASE_URL` points at localhost/loopback;
- `FRONTEND_URL` is set but is not an `https://` origin;
- `DATABASE_URL` is SQLite;
- `SESSION_SECRET` is the placeholder or shorter than 32 characters.

These checks run before uvicorn accepts traffic. A failed deploy is preferable
to a production service with insecure cookies or an ephemeral database. The
defaults remain convenient for local development when `APP_ENV` is unset.

`BASE_URL` must be the final public origin. OAuth callbacks are built from it,
and `https://` enables Secure session cookies and HSTS (`max-age=31536000`).

## 4. Database migrations

Alembic is the source of truth for Postgres. Current head is
`0017_integrity_constraints`. CI runs a migration smoke check on both SQLite
and a disposable Postgres service; that is a schema check, not a restore or
production migration.

- SQLite local development keeps `create_all` convenience.
- On Postgres startup the app runs `alembic upgrade head` before serving.
- The startup path has no cross-instance migration lock. Run a single web
  instance during a schema-changing deploy, or run migrations as a separate
  release step before scaling out. Do not start multiple migrating instances
  concurrently.
- Run migrations against a restored copy first whenever rows may be affected.

Manual command:

```sh
cd backend
python -m alembic current
python -m alembic upgrade head
```

### Seed the catalog

A fresh Supabase database has the schema but no problems, and nothing seeds it
at startup. Run each curated pack once against the deployed database:

```sh
cd backend
DATABASE_URL='postgresql://...supabase.com:5432/postgres?sslmode=require' \
  python -m app.seed.seed_webdev_projects
# repeat for seed_webdev_hackathon_projects, seed_webdev_learning_projects,
# seed_aiml_projects, seed_aiml_hackathon_projects, seed_aiml_learning_projects
```

The seed runner skips rows whose `source_id` already exists, so re-running is
safe. Skip this step and the site serves an empty catalog.

### Hosted database access control

`0018_public_schema_lockdown` revokes every privilege on `public` from the
provider's `anon` and `authenticated` roles, removes the default privileges
that would hand the same rights to future tables, and enables row level
security (with no policies) on every public table. The API connects as the
owning role, so it is unaffected, and the provider dashboard keeps working
through `service_role`.

The effect is that the project's public anon key can read nothing, including
`users.github_token`. If supabase-js is ever added to the frontend, write
explicit policies for the tables it needs; do not re-grant `anon`.

### Free-plan limits

- Render sleeps a service after ~15 minutes without traffic; the next request
  waits 30-60 s. If the wait exceeds the proxy timeout the browser sees a
  Cloudflare 524, and a reload works.
- A Supabase free project pauses after about a week without database activity.
  While paused the API returns 5xx until it is restored from the dashboard.
- `.github/workflows/keepalive.yml` pings `/api/health/ready` once a day, which
  runs `SELECT 1` and so counts as activity for both. GitHub [disables scheduled
  workflows](https://docs.github.com/actions/managing-workflow-runs/disabling-and-enabling-a-workflow)
  after 60 days without repository activity, so a dormant repo stops pinging.
- Supabase free has no point-in-time recovery. Take an off-host logical dump
  before anything that changes or deletes data:

  ```sh
  pg_dump "$DATABASE_URL" -Fc -f manabi-$(date +%F).dump
  ```

  The Supavisor session pooler (port 5432) supports `pg_dump`; the transaction
  pooler (6543) does not.

### Destructive history and backups

- `0004_cleanup` drops removed ops/crawler tables and columns.
- `0015_remove_data_science_field` and `0016_remove_upcoming_fields`
  permanently delete retired problem fields and their related projects,
  stars, and reports. Downgrade is intentionally a no-op.
- `0017_integrity_constraints` validates existing rows before adding checks;
  it raises and changes nothing when data is incompatible.

Before any deploy that may cross these revisions:

1. Take and verify a full backup off the database host.
2. Record the affected row counts.
3. Restore the backup into a disposable database and run `alembic upgrade head`
   there first.
4. Only then deploy, and verify the kept-field counts and integrity checks.

A database rollback is **restore from backup**, not `alembic downgrade`.
Application rollback does not reverse data deletions.

### Legacy "table already exists" state

If a database was created by `create_all` while `alembic_version` lags, do not
blindly stamp it. Inspect the physical schema and stamp only the revision that
matches it, on a copy first:

```sh
alembic stamp 0003_advanced_projects
alembic upgrade head
alembic current
```

If only part of a revision's schema exists, reconcile manually from a copy.

### Restore verification

```sh
createdb manabi_restore_check
pg_restore --clean --if-exists -d manabi_restore_check manabi-latest.dump
DATABASE_URL=postgresql://.../manabi_restore_check alembic upgrade head
psql manabi_restore_check -c "SELECT COUNT(*) FROM users;"
psql manabi_restore_check -c "SELECT COUNT(*) FROM problems;"
psql manabi_restore_check -c "SELECT COUNT(*) FROM projects;"
psql manabi_restore_check -c "SELECT COUNT(*) FROM project_reports;"
```

Then check `/api/health/ready` and `/api/stats` against the restored copy. The
repository does not define an RPO/RTO; confirm the provider's backup schedule,
retention, encryption, and restore time in the provider dashboard.

## 5. Start the service

Render uses the start command in `render.yaml`:

```sh
cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT --timeout-graceful-shutdown 25 --no-access-log
```

`--no-access-log` disables uvicorn's plain access line because the app emits
its own structured, request-id-aware line per API request.

On a VM or a Procfile-based host:

```sh
sh backend/start.sh
```

`backend/start.sh` installs the pinned runtime dependencies and then `exec`s
uvicorn, so shutdown signals reach the server. The repository's root
`Procfile` uses this script. The ignored `backend/Procfile` is a leftover
duplicate; do not use it.

The app must run from `backend/` (or have that directory on `PYTHONPATH`)
because Alembic and `.env` resolution use the backend working directory.

## 6. HTTPS, proxies, CORS, and cookies

- Render terminates TLS at its edge. `BASE_URL` must still be the public HTTPS
  origin; the app does not infer it from proxy headers.
- `SESSION_SECRET` signs an HttpOnly session cookie. In production it is
  `SameSite=None; Secure`, which is required for a Cloudflare Pages frontend to
  send it to Render; outside production it stays `SameSite=Lax`.
- HSTS is sent on HTTPS responses. It deliberately omits `includeSubDomains`.
- CORS allows exactly the origins in `CORS_ALLOW_ORIGINS` plus `FRONTEND_URL`,
  with credentials enabled. Nothing else can call the API with cookies. Local
  development defaults to `http://localhost:5173` for the Vite server.
- **Third-party cookie caveat:** `*.pages.dev` and `*.onrender.com` are
  different sites, so browsers with third-party cookie blocking (Safari/ITP,
  Chrome incognito) can drop the session cookie. For reliable login, put both
  services on one registrable domain, e.g. `app.example.com` (Pages) and
  `api.example.com` (Render), and set `FRONTEND_URL`/`BASE_URL` accordingly.
  The custom domains are cross-origin but same-site, so the cookie is
  first-party.
- No `TrustedHostMiddleware` is configured. The app does not build absolute
  links from the Host header, but host-header validation is an open hardening
  item.
- There is no full Content-Security-Policy beyond `frame-ancestors 'none'`.
  Adding one requires auditing the Rive, font, image, and inline-style surface.

**Proxy IP requirement:** Uvicorn only trusts `X-Forwarded-For` from
`FORWARDED_ALLOW_IPS`, which defaults to loopback. Behind a platform proxy,
set it to the platform's private proxy CIDR (Render's blueprint uses
`10.0.0.0/8,127.0.0.1,::1`). Never use `*`: a client can spoof the leftmost
address. The exact Render proxy range could not be verified from this
repository; confirm it against the live platform before relying on per-IP login
limits. If proxy trust is wrong, login attempts can share one bucket.

## 7. Health checks

| Endpoint | Purpose | DB required |
|---|---|---|
| `GET /api/health/live` | Process liveness; used by Render's HTTP health check | No |
| `GET /api/health` | Backward-compatible readiness check | Yes |
| `GET /api/health/ready` | Explicit readiness check | Yes |

A database outage makes readiness fail but liveness stay green, avoiding a
restart loop that cannot repair the database. Monitor readiness separately;
Render's health check alone is not proof that the API can serve data.

## 8. Post-deploy checks

`<api>` is the Render origin, `<app>` is the Cloudflare Pages origin.

1. `curl https://<api>/api/health/live` → `{"status":"ok"}`.
2. `curl https://<api>/api/health/ready` → `{"status":"ok"}`.
3. `curl https://<api>/api/stats` → real counts (after seeding).
4. `curl -H 'Accept: text/html' https://<app>/problems` → SPA HTML with
   `<title>MANABI</title>`.
5. `curl -I https://<app>/assets/<asset from dist>` → `200` and the correct
   `content-type`.
6. `curl -I https://<api>/api/health/live` → confirm
   `Strict-Transport-Security`.
7. `curl -i https://<api>/api/stats -H 'Origin: https://<app>'` → response
   carries `access-control-allow-origin: https://<app>`.
8. `alembic current` → `0017_integrity_constraints (head)`.
9. Open the app, log in with GitHub, submit a test project, and exercise the
   admin review path if those features are enabled. Check DevTools → Network
   that `/api/auth/me` returns 200 after login (a 401 there means the session
   cookie was not sent).

## 9. Logging, diagnostics, and monitoring

The API writes one structured line per event to stdout; the platform captures
it. Production defaults to JSON (`LOG_FORMAT=json`), development/test to compact
text. Every line carries `timestamp`, `level`, `service`, `environment`,
`version`, `logger`, `message`, and `request_id`.

- One `request_completed` line per `/api/*` request (method, route template,
  status, duration). Client errors such as 4xx stay `INFO`; 5xx emit
  `request_failed` at `ERROR`, and requests over `SLOW_REQUEST_MS` add a
  `slow_request` warning.
- Successful health probes are not access-logged: Render polls them
  continuously and their lines would bury real incidents. A failing or slow
  probe is still logged.
- Exceptions log a stack trace and `error_type` server-side, but responses keep
  a generic message and a request id. Credentials (Bearer tokens, API keys,
  GitHub tokens, database URLs) are redacted centrally before formatting.
- The request id comes from `X-Request-ID` when it is short and well-formed,
  otherwise a UUID is minted. The same value is returned in the response header
  and included in every log line emitted while that request is being handled.
- The frontend reports uncaught errors and React error-boundary crashes from
  production builds to `POST /api/client-errors`. Reports are bounded, logged,
  and rate limited per IP; nothing is persisted.
- `/api/health*` exposes only a status string.
- There are no metrics, tracing, or bundled APM. Use the platform (or an
  external monitor) for availability, latency, 5xx-rate, and database alerts on
  `/api/health/ready`. Log retention and alerting are platform responsibilities.
- The API docs (`/docs`, `/openapi.json`) are public schema documentation, not
  an operator console.

## 10. Rollback and release procedure

Releases are identified by the Git commit Render deploys. Render retains the
previous deploy and its logs; the repository has no separate artifact registry.

Application rollback:

1. In Render, redeploy the previous known-good commit.
2. Restore the matching environment variables and `BASE_URL`.
3. Rebuild the frontend from that commit in Cloudflare Pages. The API and
   frontend are versioned together; re-deploy the matching Pages commit so a
   new bundle does not call an older API contract.
4. Run the readiness and post-deploy checks again.

Database rollback:

- Alembic downgrade is not a data-recovery plan. `0015` and `0016` deleted rows
  and their downgrade is a no-op.
- For data loss or a bad destructive migration, stop writes, restore the last
  verified backup into a new database, point `DATABASE_URL` at it, and verify
  with `alembic current`, `/api/health/ready`, and row counts.
- The application schema must match the code version. If rolling back across a
  schema-changing release, restore a backup from before that release or keep a
  backward-compatible schema.

Configuration rollback:

- Revert dashboard environment variables and redeploy; do not rely on an old
  process retaining them.
- Rotating `SESSION_SECRET` invalidates existing sessions. That is expected on
  a suspected compromise, not a routine rollback.

Failed deploy handling:

- A failed build cannot deploy because the Render install step or the
  Cloudflare Pages build exits non-zero.
- A failed startup fails the guard or uvicorn; Render keeps the previous live
  instance.
- A passing liveness check does not prove Postgres readiness; check
  `/api/health/ready` before declaring success.

## 11. Submission verification rules

- **Ownership:** verified by GitHub numeric id (personal owner), push/admin
  permission from the repo payload (organization), or
  `CONTRIBUTOR_MIN_COMMITS` entries in `/contributors`. Username matches are
  never trusted.
- **Anti-abuse:** rolling daily submission cap, active-project cap, one repo per
  user per problem, one GitHub repo id per problem, fork rejection unless
  enabled, and archived/disabled repo rejection.
- **Relevance:** delimited problem/repo text goes to the LLM. Score at or above
  `RELEVANCE_VERIFY_MIN` verifies; at or above `RELEVANCE_REJECT_BELOW` goes to
  human review; below it is rejected. LLM outages fall back to a keyword check
  that can only reach `needs_review`. Repos older than `PREEXISTING_REPO_DAYS`
  need a higher score to auto-verify.
- **Human review:** admins use `/admin/review`; three reports flip a verified
  project back to review.
- **Known limitation:** contributor detection matches GitHub account ids. Commit
  emails not linked to the account do not count as contributions.

## 12. Known limitations

- `users.github_token` is stored in plaintext in the database. A database dump
  or SQL injection could expose GitHub tokens. Encryption is a separate,
  deliberately unimplemented hardening project.
- LLM prompts contain untrusted brief/README text. Delimiting and instructions
  reduce prompt-injection risk but do not eliminate it.
- The app auto-migrates at Postgres startup and has no cross-instance migration
  lock. Use one instance during schema-changing deploys.
- Proxy IP ranges and the resulting per-IP login limit require verification on
  the live platform. With a Pages → Render split, Cloudflare (or the Pages
  proxy) is the immediate client of Render, so `FORWARDED_ALLOW_IPS` must match
  the actual proxy range or per-IP login limits share one bucket.
- Cross-site sessions depend on third-party cookies when the frontend and API
  are on different registrable domains (`*.pages.dev` + `*.onrender.com`). Use
  custom subdomains of one domain for reliable login.
- No formal RPO/RTO, metrics, tracing, or alerting are defined in the
  repository; structured logs exist, but retention and paging stay with the
  hosting platform.
- Browser support is not formally pinned; Playwright covers Chromium only.
