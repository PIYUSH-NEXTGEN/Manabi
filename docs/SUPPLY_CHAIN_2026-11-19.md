# Phase 6 — Dependency and Software Supply-Chain Audit

Date: 2026-11-19

## A. Dependency Inventory

**Package managers and runtimes**

- Backend: Python 3.12.7 in production (`runtime.txt`, `render.yaml`, CI); local verification used Python 3.14.
- Frontend/build: Node 20.18.1 (`.node-version`, `render.yaml`, CI), npm with `package-lock.json` v3.
- Deployment: Render build via `build.sh`, then FastAPI serving the Vite build. No Dockerfile or container image exists.
- CI: GitHub Actions; Playwright Chromium is downloaded at CI runtime.

**Direct dependencies**

| Ecosystem | Production | Development/test | Total |
|---|---:|---:|---:|
| Python | 11 | 4 | 15 |
| npm | 16 | 16 | 32 |

Python has 95 installed distributions including transitive packages. npm has 461 locked packages and 385 installed package entries.

**Manifests and build files inspected**

- `backend/requirements.txt`, `backend/requirements-dev.txt`
- `frontend/package.json`, `frontend/package-lock.json`
- `runtime.txt`, `.node-version`, `render.yaml`, `build.sh`, `Procfile`, `backend/Procfile`
- `.github/workflows/ci.yml`, `.dockerignore`
- Both `.env.example` files

All npm packages resolve from `https://registry.npmjs.org/`; there are no Git, file, or private-registry dependencies. Python packages resolve from PyPI.

## B. Vulnerability Findings

`pip-audit` initially reported 28 advisory matches (duplicate aliases) across six packages. Deduplicated, these are 12 unique advisories. `npm audit` reported zero vulnerabilities.

| Package | Installed Version | Vulnerability | Severity | Project Impact | Status |
|---|---|---|---|---|---|
| certifi | 2026.7.22 | PYSEC-2026-4320 / GHSA-6q48-6c7w-9gw2 | Critical | Bundled CA store is used for outbound HTTPS to GitHub and Gemini; compromised CA trust is a real TLS risk. | Fixed at 2026.10.23 |
| starlette | 0.52.1 | PYSEC-2026-161 (6.5), PYSEC-2026-2281 (7.5), PYSEC-2026-249 (7.5), PYSEC-2026-2280 (5.3), PYSEC-2026-248 (3.7) | High | Reachable through FastAPI. Host/request-URL handling and form limits are relevant; the StaticFiles issue is Windows-specific and production is Linux. | Fixed at 1.10.0 via FastAPI 0.165.0 |
| pyasn1 | 0.6.4 | CVE-2026-119194, -119195, -119196, -119197 | High | Transitive through google-auth; the app does not directly decode attacker-controlled ASN.1, but the library is patched defensively. | Fixed at 0.6.5 |
| joserfc | 1.7.5 | CVE-2026-119284 / GHSA-9pg5-8c7x-5hfx | Medium | Transitive through Authlib. GitHub OAuth uses opaque tokens, not application-parsed JWS, so observed exposure is low. | Fixed at 1.8.0 |
| opentelemetry-api | 1.45.1 | CVE-2026-126360 / GHSA-mf5v-w3w3-f6cg | Medium | FastAPI dependency; no tracing/propagator setup is configured in this app, so the ReDoS path is not presently exercised. | Fixed at 1.45.2 |
| pip | 25.3 | PYSEC-2026-1796, -2875, -2876, -196, -3721 | Low–Medium (build tool) | Used to install packages during Render/CI builds, not at application runtime. | Fixed with pip 26.3 in the build and CI configuration; local environment upgraded |

After remediation, `pip-audit` reports **no known vulnerabilities** in the installed Python environment and `npm audit` reports **0 vulnerabilities**.

## C. Maintenance and Dependency Risks

- **Outdated but secure:** pydantic 2.14.1 (latest 2.14.3), pydantic-settings 2.16.0 (2.16.3), SQLAlchemy 2.1.5 (2.1.9), and alembic 1.16.5 (1.20.1) have newer patch/minor releases but no reported vulnerabilities. They were left unchanged to avoid unnecessary churn.
- **Major-version gap:** google-genai 2.31.0 vs 3.6.1. No advisory was found, and the major upgrade was not forced; it needs a separate compatibility review.
- **Pinning:** production Python dependencies are now exact-pinned, including the previously ranged `psycopg2-binary` and the advisory-affected transitive packages. Dev/test tools are also pinned. npm uses caret ranges plus a committed lockfile and `npm ci` in CI/Render.
- **Unused dependencies:** no unused direct package was found. All npm direct packages are referenced, and Python direct packages are used by the application/build. Removal was not attempted.
- **Duplicates/large trees:** npm contains 461 locked packages, including five intentional font packages. No material duplicate functionality was identified; no large unused dependency was found.
- **Package sources:** public PyPI/npm only; no private package namespace or alternate registry configuration exists. No dependency-confusion evidence was found.
- **Integrity:** npm lock entries include integrity hashes, except six nested optional WASM packages under `@tailwindcss/oxide-wasm32-wasi`. Python requirements are version-pinned but not hash-pinned.
- **Install scripts:** the only relevant scripts are esbuild's binary postinstall, msw's local postinstall, and optional fsevents hooks. Static inspection showed normal package-local behavior; no suspicious downloads, credential access, or project-file mutation was found.

## D. Supply-Chain and CI/CD Findings

- **Secrets:** no tracked `.env`, private key, or credential file was found. Working-tree scans for GitHub tokens, Google API keys, AWS keys, and PEM private keys returned no values. History search found only documentation text mentioning the scan patterns, not a secret. This was a pattern-based scan, not exhaustive secret-scanning tooling.
- **CI permissions:** CI had default workflow token permissions. Added top-level `permissions: contents: read`, and both checkouts now use `persist-credentials: false`.
- **Action integrity:** official actions were referenced by mutable major tags. They are now pinned to immutable commit SHAs:
  - `actions/checkout` v4.2.1
  - `actions/setup-python` v5.6.0
  - `actions/setup-node` v4.4.0
- **Update automation:** added `.github/dependabot.yml` for weekly grouped pip, npm, and GitHub Actions updates. This keeps SHA pins and dependency versions from silently aging.
- **Build-time downloads:** Playwright downloads Chromium via `npx playwright install`; the version comes from the lockfile. This is an external build dependency, but it is the official Playwright mechanism.
- **No containers:** there is no Dockerfile or base image to scan.
- **Residual CI gap:** vulnerability audits are run manually; CI does not yet gate on `pip-audit`/`npm audit`. Dependabot alerts/updates are enabled by configuration, but repository security settings must also be active on GitHub.

## E. License Audit

- Project license: MIT (`LICENSE`).
- **npm:** 404 MIT, 18 ISC, 12 MPL-2.0, 10 Apache-2.0, 5 OFL-1.1, plus BSD/0BSD/CC-BY packages. OFL font packages carry attribution/notice obligations; MPL-2.0 is file-level copyleft. No GPL/AGPL package was identified.
- **Python:** predominantly MIT, BSD, and Apache-2.0, plus MPL-2.0 (`certifi`) and LGPL with exceptions (`psycopg2-binary`). `tld` declares `MPL-1.1 OR GPL-2.0-only OR LGPL-2.1-or-later`; the disjunctive choice requires a deliberate review if redistributed. Six distributions expose missing/ambiguous license metadata (`colorama`, `itsdangerous`, `markdown-it-py`, `mdurl`, `pip_audit`, `tomli_w`), although their upstream projects are commonly permissive.
- No definitive legal conclusion is made. The OFL notices, MPL/LGPL obligations, and `tld` choice should be reviewed before distributing binaries or bundled assets.

## F. Changes Made

| Package | Previous | New | Reason |
|---|---|---|---|
| fastapi | 0.143.3 | 0.165.0 | Pulls a Starlette release with all listed advisories fixed |
| starlette | 0.52.1 | 1.10.0 | Explicit security pin; fixed Host/URL, form-limit, and static-file advisories |
| Authlib | 1.9.1 | 1.9.9 | Patch update; supplies patched joserfc dependency |
| joserfc | 1.7.5 | 1.8.0 | CVE-2026-119284 |
| pyasn1 | 0.6.4 | 0.6.5 | Four high-severity denial-of-service advisories |
| opentelemetry-api | 1.45.1 | 1.45.2 | ReDoS advisory |
| certifi | 2026.7.22 | 2026.10.23 | Critical compromised-CA advisory |
| psycopg2-binary | `>=2.9,<3` | 2.9.13 | Exact pin for reproducible installs; already the resolved version |
| pip (build/CI) | 25.3 | 26.3 | Build-tool advisories; patched before package installation |

**Development pins:** pytest 9.1.1, pytest-asyncio 1.4.0, pytest-cov 7.1.0, respx 0.23.1.

**Configuration changes:**

- `build.sh`: upgrades pip to 26.3 before installing backend dependencies.
- `.github/workflows/ci.yml`: upgrades pip, pins actions to SHAs, limits token permissions, disables persisted credentials.
- `.github/dependabot.yml`: weekly grouped updates.
- `frontend/src/components/chat/ChatWidget.test.tsx`: fixed a timing race where Send was clicked while still disabled, and allowed the four-turn interaction a 15-second timeout. This was test reliability work, not an application behavior change.

No dependencies were removed.

## G. Verification Results

| Verification | Result | Details |
|---|---|---|
| Vulnerability scan | Passed | `pip-audit`: no known vulnerabilities; `npm audit`: 0 vulnerabilities |
| Dependency resolution | Passed | `pip check` clean; clean venv installed `requirements-dev.txt`; `npm ci` completed |
| Lockfile consistency | Passed | `npm ci` resolved exactly 384 packages from the lockfile; Python requirements are exact-pinned (no Python lockfile) |
| Clean installation | Passed | Fresh Python 3.14 venv + full 334-test run; clean npm install |
| Unit tests | Passed | Backend 334 passed; frontend 187 passed on three consecutive full runs after the test stabilization |
| Integration tests | Passed | Included in the backend 334-test suite |
| Production build | Passed | `npm run build` completed in 9.05s; existing >500 kB chunk warning remains |
| E2E smoke | Passed | Playwright smoke test passed after the clean npm install |
| Type checking | Passed | `npx tsc --noEmit` |
| Migration smoke | Passed | `alembic upgrade head` on fresh SQLite |
| CI/CD review | Completed with noted residual | YAML parses; build shell syntax passes; workflow has not been executed on GitHub from this environment |

**Important limitation:** the fresh-install verification ran on local Python 3.14. CI targets Python 3.12; the pinned packages declare 3.12 compatibility, but a Python 3.12 clean install was not available locally.

## H. Remaining Risks

- Python wheels are not hash-verified/attested. A compromised PyPI package at the pinned version would not be detected by version pins alone. Hash-locking would require platform-specific lockfiles and a deliberate tooling decision.
- Six nested optional npm WASM entries lack integrity fields; they are part of the Tailwind optional toolchain. This is a minor provenance gap, not an advisory.
- CI does not yet run vulnerability scans as a blocking gate. Dependabot is configured, but GitHub security settings and alert delivery still need confirmation in the repository.
- google-genai remains a major version behind. No advisory was found, but upgrading it would require a separate compatibility review.
- `tld` has a multi-license expression requiring a deliberate MPL/LGPL/GPL choice if the dependency is redistributed; six Python packages have incomplete license metadata.
- CI actions are pinned to SHA but at older major versions; Dependabot should propose updates that need review.
- No live production rebuild/container/provenance verification was possible; there is no container image, and real OAuth/Gemini credentials were not exercised.

## I. Final Assessment

**Dependency audit completed.**

All known critical/high-severity findings in the installed production dependency tree were remediated with targeted, compatible updates, and the confirmed patches were verified through clean installs, the full backend and frontend suites, type checking, and production builds. A clean vulnerability scan was obtained for both ecosystems. Residual risks are documented and are primarily provenance hardening, CI gating, and a major-version upgrade that was intentionally not forced.
