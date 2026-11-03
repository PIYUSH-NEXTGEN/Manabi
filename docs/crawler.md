# Crawler

The crawler discovers public problem statements, extracts one structured problem per
LLM call, and publishes them with a human review safety net. It **refuses to run**
unless the source has a recent, permissive compliance record.

## Architecture

```
backend/app/crawler/
  config.py          # CRAWLER_* env, kill switch, admin allow-list
  registry.py        # validated sources/*.yaml
  compliance.py      # verdict/age gate + robots.txt cache (fails closed)
  fetcher.py         # SSRF-safe, throttled, conditional HTTP; PDF text
  discovery/         # static_list, sitemap, rss, json_api, listing_html, file_table
  split.py           # deterministic multi-problem splitter
  extract.py         # one-problem LLM prompt, Pydantic validation, evidence check
  dedupe.py          # identity, content hashing, near-duplicate detection
  publish.py         # quality gate, auto-publish vs pending_review, human-edit guard
  report.py          # counters, structured log lines, coverage markdown
  run.py             # orchestration + CLI
  sources/           # one YAML per crawl source
```

Every fetched page is untrusted data. The extractor never follows links or
instructions found inside source text, never lets the LLM choose URLs, and validates
all output against the Pydantic schema before anything is stored.

## Add a new source (in this order)

1. **Compliance check first.** Read the site's terms/privacy/robots.txt, look for an
   official API/feed/dataset, record the licence/ownership and access model.
2. Write `docs/sources/<slug>.md` with short verbatim quotes, robots rules, the
   verdict (`allowed`/`api_only`/`manual_only`/`forbidden`/`unclear`), contact,
   throttle settings and display policy. **Stop and ask the owner** if the verdict is
   `manual_only`, `forbidden` or `unclear`.
3. Add `backend/app/crawler/sources/<slug>.yaml` (key must equal the filename). Pick
   the discovery method and, if needed, a small parser.
4. Add fixtures from real saved pages under `backend/tests/fixtures/crawler/<slug>/`
   and tests for the parser and one end-to-end run.
5. Run `pytest`, then a dry run:

   ```sh
   cd backend
   CRAWLER_ENABLED=true CRAWLER_CONTACT=you@example.com \
     .venv/bin/python -m app.crawler.run --source <slug> --dry-run --limit 5
   ```

Nothing else should be required. Discovery methods live in `discovery/`; a new HTML
layout is one parser function plus fixtures.

## Registry (YAML)

Required fields: `key`, `name`, `base_url`, `compliance.verdict`,
`compliance.checked_on`, `compliance.record`, `discovery.method`.

`compliance.checked_on` older than **180 days** blocks the run. `politeness` defaults
to 3 s between requests, 200 pages/run, one connection per host and a 500 KB cap;
raise `max_bytes` only when the official release genuinely needs it. `display_policy`
is `summary_only` by default; `summary_plus_excerpt` requires a licence that clearly
permits it. `publish.auto_publish` plus `min_confidence` decide whether a clean item
goes live or to the review queue.

## CLI

```sh
cd backend
python -m app.crawler.run --source sih-2026 --dry-run --limit 10
python -m app.crawler.run --source sih-2026 --env prod
```

`CRAWLER_ENABLED=false` is the kill switch and makes every entry point exit before
any request. `CRAWLER_CONTACT` is required. `--env prod` (or
`CRAWLER_REQUIRE_POSTGRES=true`) refuses to crawl against SQLite. The CLI writes a
markdown coverage report to stdout and to `$GITHUB_STEP_SUMMARY` when present.

Exit codes: `0` for a completed run (per-page failures are reported in the summary),
`2` for an environment refusal, non-zero for an infrastructure failure.

## Environment

| Variable | Purpose |
|---|---|
| `CRAWLER_ENABLED` | Kill switch; default `false` |
| `CRAWLER_CONTACT` | Required contact in the User-Agent |
| `CRAWLER_REQUIRE_POSTGRES` | Refuse to crawl a SQLite database |
| `CRAWLER_MAX_REQUESTS_PER_RUN` / `CRAWLER_MAX_LLM_CALLS` | Per-run budgets |
| `SITE_URL` | Site link in the User-Agent |
| `ADMIN_GITHUB_USERNAMES` | Comma-separated GitHub logins allowed into `/api/admin/*` and `/admin/review` |

## Scheduled runs

`.github/workflows/crawl.yml` runs the CLI against Postgres with Alembic, a
concurrency lock and a 30-minute timeout. It is **off by default**: scheduled runs
only execute when the repository variable `CRAWLER_SCHEDULE_ENABLED` is `true`.
Manual `workflow_dispatch` works as soon as the secrets are set.

Secrets: `DATABASE_URL` (Postgres), `GEMINI_API_KEY`, `CRAWLER_CONTACT`.
Optional repository variable: `SITE_URL`.

To enable:

1. Add the three secrets.
2. Set `ADMIN_GITHUB_USERNAMES` on the web service so admins can review.
3. Set `CRAWLER_SCHEDULE_ENABLED=true` to allow the daily schedule.
4. Run the workflow once with `dry_run=true`, inspect the report, then run for real.

SQLite cannot be shared with GitHub Actions, so production crawling needs the
Postgres `DATABASE_URL`.

## Offline demo seed

When an LLM key is unavailable (or the provider is returning 5xx), you can populate
a local database from the saved official fixtures without any network or LLM call:

```sh
cd backend
.venv/Scripts/python scripts/seed_sih_demo.py --limit 40 --reset
```

It uses the real SIH parsers and deterministic metadata and writes clearly generated
summaries — never verbatim source text. It is a demo fallback only; the scheduled
crawler remains the source of truth for production.

## Review and takedown

- `/admin/review` shows pending problems with confidence, notes, source link and
  approve/reject/unpublish/edit controls. Non-admins get a 403 from the API.
- `POST /api/admin/sources/{key}/unpublish-all` removes every problem for a source
  key (takedown). Single problems can be unpublished by id.
- Crawled pages show source, year, organiser, "View original", the generated-summary
  notice and a "Report / request removal" link. Full verbatim crawled text is never
  returned by the API.

## Troubleshooting

| Symptom | Cause |
|---|---|
| `CRAWLER_ENABLED is false` | Kill switch is off |
| `CRAWLER_CONTACT is required` | Set the contact env var |
| `compliance verdict ... refusing` | Source YAML says `manual_only`/`forbidden` |
| `compliance record is N days old` | Re-check the source and update `checked_on` |
| `robots.txt returned HTTP 5xx` | Robots unavailable; the host is skipped (fail closed) |
| `LLM call budget exhausted` | Remaining items are reported as `deferred`; rerun later |
| `Refusing to crawl against SQLite` | Use the Postgres URL for Actions/prod |
