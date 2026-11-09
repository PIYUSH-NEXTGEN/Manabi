# MANABI — Phase 2 Security Audit

Date: 2026-11-09 · Scope: entire repository (backend FastAPI, frontend React/TS, migrations, seeders,
deployment docs) · Method: manual evidence-based review + dependency audits + secret scan + targeted
regression tests, per the authorized audit-and-remediate phase.

## A. Executive summary

- Security posture: solid for the application's threat model. All SQL access is parameterized (no dynamic
  SQL construction anywhere), no command/code execution or unsafe deserialization vectors exist, OAuth and
  session handling use vetted libraries with server-side-only credential storage, and Rubin visibility rules
  (owner/admin vs public, "non-existent to others" 404 masking) are enforced at every project read path.
- **3 findings remediated** (all low severity, each with regression tests): repo-URL path smuggling via
  percent-encodings, spreadsheet formula injection in the XLSX export, and a missing rate limit on problem
  publishing. Plus 1 vulnerable direct dependency (vite dev-server advisory) patched 6.4.4 → 6.4.5.
- Remaining: dev-tooling dependency upgrades (vitest/tinypool criticals — dev-only exposure), a documented
  design decision needed on instant publication of user-created problems, and production-transport
  assumptions (HSTS/CSP) owned by the hosting platform. No unresolved critical/high-severity issues in
  the verified scope.

## B. Audit scope

Trust boundaries: browser ↔ API (session cookie auth), API ↔ GitHub (OAuth + user tokens), API ↔ LLM
providers (Gemini/Anthropic), app ↔ SQLite/Postgres.

Areas assessed with evidence:
- **Injection**: every SQLAlchemy call site (static sweep for `text()/execute()/from_statement` with dynamic
  content — none; LIKE needles are bound params); no `subprocess/eval/exec/pickle/yaml.load` in backend or
  scripts (grep).
- **Web app**: SPA path traversal (already hardened, probes in `test_wiring.py`), React output escaping
  (no `dangerouslySetInnerHTML` anywhere), markdown rendering via react-markdown v10 (URL scheme
  sanitization built-in: `javascript:` → inert), CORS (`localhost:5173` only in dev, no cross-origin in
  prod), CSRF (cookies `SameSite=lax` + all state-changing routes are JSON-token bodies or POSTs that don't
  accept form encodings; OAuth uses state parameter), open redirects (callback redirects to a fixed "/",
  GitHub-configured URLs only).
- **AuthN/AuthZ**: session signed-cookie middleware (HttpOnly/Secure/SameSite), `AdminUser` dependency on
  every `/api/admin/*` route, ownership checks server-side in every project mutation; IDOR-class probes in
  `test_visibility.py`/`test_projects_github.py` all enforced server-side; GitHub token stored server-side
  and asserted never in API responses (`test_profile_shape` asserts `"secret-token" not in str(data)`).
- **File/exports**: single export endpoint (xlsx, generated server-side from DB, filename sanitized
  `[^A-Za-z0-9_-]`), uploads: none exist.
- **Deserialization**: JSON only (pydantic-validated); no YAML/XML/pickle.
- **Secrets**: pattern scan across the working tree (ghp_/sk-/AIza/AKIA/PEM/key-file patterns): 0 hits;
  `.env` files and `*.db` gitignored throughout; git history file inventory contains no secret files;
  ephemeral local `.env` verified present-but-ignored with a real SESSION_SECRET; placeholder
  SESSION_SECRET is blocked on non-local boot (`guard_deploy_secrets`).
- **Dependencies**: `npm audit` (vite/GHSA-8g5g-mxqh-grgj — fixed; vitest/tinypool/@vitest/mocker
  critical+moderate; react-router moderate), `pip-audit` on `requirements.txt`: **no known vulnerabilities**.
- **Rate limits/abuse**: chat (anon 10/h per IP, user 30/h), submissions (5/24h + 10 active), reports
  (30/h), re-verify (24h interval); found the one unprotected expensive public action (problem creation) and
  closed it.
- **Headers/transport**: app sets `X-Content-Type-Options: nosniff`, `Referrer-Policy:
  strict-origin-when-cross-origin`; cookie `Secure` flag tied to BASE_URL https; HSTS/TLS delegated to the
  platform (Render/Railway docs) — not directly verifiable from the repo (see F).

Excluded/blocked: production environment inspection (no access), live GitHub/LLM quota behavior, container
config (none exists in-repo), CI (no workflows directory).

## C. Vulnerability findings

| ID | Title | Severity | Status |
|---|---|---|---|
| S-1 | Repo-URL path smuggling via percent-encoded segments | Low | **Fixed** (confirmed) |
| S-2 | Spreadsheet formula injection in `/api/problems/{id}/export.xlsx` | Low | **Fixed** (confirmed) |
| S-3 | Unthrottled problem publishing by any authenticated user | Low | **Fixed** (rate limit added; publication model = design decision, see F) |
| S-4 | Vite dev-server advisory GHSA-8g5g-mxqh-grgj | Low (dev-only) | **Fixed** (upgraded 6.4.4→6.4.5) |
| S-5 | vitest/tinypool criticals (RCE-class) via `npm audit` | Medium (dev-only) | Documented — needs major upgrade, see F |
| S-6 | react-router advisory (open redirect in `<Link>`, CVE-2025-68470 bypass + SSR-hydration) | Medium-low (dev/runtime pkg) | Documented — major upgrade 6→7, see F |
| S-7 | User-created problems publish instantly with no moderation step | Medium (design) | Documented — owner decision, see F |
| S-8 | No Content-Security-Policy header | Low (hardening) | Documented — see F |

Details (root cause / evidence):
- **S-1**: `github.parse_repo_url` accepted segments like `a%2Fb`; the GitHub API fetch path
  `/repos/{owner}/{name}` then resolves (after GitHub's decode) to `/repos/a/b/...` — a *different repo
  than the URL shown to the visitor* (e.g. `https://github.com/a%2Fb/c` fetches `a/b/c`). No persistent
  integrity breach was demonstrated (stored rows record the *decoded* repo canonically, and ownership checks
  judge the fetched repo's facts), so impact is confusion + a path-smuggling primitive, not auto-verify
  bypass. Fix: segments must survive full decoding unchanged and match GitHub's legal charset.- **S-2**: `export_problem` wrote raw DB strings (summary/organisation can be user-created via
  `POST /api/problems`) as cells; Excel/LibreOffice execute `=`, `+`, `-`, `@` leading cells as formulae
  (DDE/HYPERLINK). Fix: single escape point `_safe_cell()` applied to every string cell.
- **S-3**: `POST /api/problems` authenticated-but-unthrottled → unbounded spam/content flooding (also the
  upload vector into S-2). Fix: `PROBLEM_CREATE_PER_HOUR` (default 5/h per user; admins exempt), reusing
  the existing `RateLimiter`.
- **S-5/S-6**: vulnerabilities exist but in codepaths that do not execute for end users: vitest/tinypool
  are dev/test tooling (exploitation requires running the test runner on hostile local input);
  react-router's advisories concern its SSR-hydration data path and a `<Link>`-backslash redirect this app
  does not construct (no user input flows into `to`, links are literals). Fix is a semver-major package
  upgrade — deferred to a dedicated maintenance change rather than bundled silently into the security
  phase; tracked in F.

## D. Remediation summary

1. **S-1** — `backend/app/services/github.py`: `_segment_is_literally_github_name()` (idempotent-decoding +
   charset check) applied to both URL segments; crafted encodings rejected at parse time, before any API
   call. Regression tests: `test_parse_repo_url_rejects_encoded_separators`,
   `test_parse_repo_url_still_accepts_plain_names`.
2. **S-2** — `backend/app/routers/problems.py`: `_KINDS_FORMULA_PREFIX` + `_safe_cell()`; every string cell
   in the export sheet passes through it. Regression: `test_export_neutralises_formula_injection`
   (asserts no cell renders with a formula-leading char; literal text preserved as `'=...`).
3. **S-3** — `backend/app/config.py` (`PROBLEM_CREATE_PER_HOUR=5`), `routers/problems.py` (limiter in
   `create_problem`, admin-exempt), `.env.example` + `DEPLOY.md` documented. Regression:
   `test_problem_create_rate_limited_for_regular_users`, `test_problem_create_admins_are_exempt`.
4. **S-4** — `frontend/package.json` / lockfile: `vite@6.4.5` within the existing semver range; full rebuild
   + suites re-run clean.

## E. Verification results

- Backend suite: **231 passed** (226 pre-audit + 5 new security tests) — includes all prior
  authorization/visibility tests untouched.
- Frontend suite: **125 passed**; `tsc -b` clean; production build succeeds on vite 6.4.5.
- Dependency audits: `pip-audit` → clean; `npm audit` → all remaining advisories are the documented
  dev-tooling majors (S-5/S-6), none with an in-range safe fix.
- Secret scan (patterns above, whole tree): 0 hits. Git history filename inventory: no secret objects.
- Static sweeps: no dynamic SQL, no exec/python-eval/pickle/yaml vectors, no `dangerouslySetInnerHTML`.
- Targeted exploit probes: `parse_repo_url` smuggling cases all rejected; formula cells neutralized in a
  generated workbook; rate limit trips at the configured threshold and admits admins.
- Not performed: live production header/TLS inspection (no production access), GitHub/LLM quota abuse
  testing (would hit third-party services), browser-based CSRF/red-team round.

## F. Remaining risks and actions

1. **S-7 (needs owner decision)** — any logged-in user can publish a problem instantly
   (`create_problem` never sets `status`, model default `published`). With S-3 closed the flood vector is
   throttled, but content moderation remains absent. Options: (a) default `pending_review` + admin queue,
   (b) admin-only problem creation. Not chosen unilaterally — requires product policy.
2. **S-5/S-6 (planned maintenance)** — upgrade vitest 3→5 and react-router-dom 6→7 in a dedicated change;
   both are semver-major. Dev-only exposure meanwhile; do not run untrusted test code locally.
3. **S-8 (hardening)** — add a CSP (`style-src 'unsafe-inline'` likely required by the Vite CSS injection
   story) and consider HSTS when the proxy contract is confirmed. Needs a build-pipeline check first.
4. **Deployment-owned controls (unverified)** — TLS/HSTS, HTTP/2, header injection by the reverse proxy;
   session cookie lifetime is Starlette's default 14 days (no absolute-expiry reauth); both depend on
   config outside the repository.
5. **Accepted risks** — RateLimiter memory growth retained (documented in Phase 1, audit E); anonymous
   GitHub API quota burn via stale-cache progress refreshes is bounded by the 10-minute cache and GitHub's
   own per-IP limits.

## G. Final security status

**No known unresolved critical or high-severity vulnerabilities within the verified scope.**
The three confirmed exploits (S-1, S-2, S-3) were fixed with regression tests and the dependency fix (S-4)
verified by full rebuilds; findings S-5–S-8 are documented with remediation plans but are either
dev-only-exposed or require owner decisions/future upgrades rather than being active exploitable paths.
This reflects the audited scope only — it is not a claim of OWASP compliance or absence of all defects.
