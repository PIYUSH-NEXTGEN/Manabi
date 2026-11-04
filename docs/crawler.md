# Crawler (historical archive)

This page preserves the architecture notes for the crawler and admin review modules
that were removed. They are **not** part of the current codebase: `app/crawler/` and
`app/routers/admin.py` were deleted, the scheduled `crawl` GitHub Actions workflow was
repointed to the offline demo seed, and the `.env` config rows for the crawler are
legacy now.

## What was removed

```text
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

The admin review queue and the `/api/admin/*` routes were removed alongside it, so
`ADMIN_GITHUB_USERNAMES`, the `/admin/review` page, and the takedown endpoint
(`POST /api/admin/sources/{key}/unpublish-all`) no longer exist. Problems that came in
through the crawler carried `origin="crawler"`; any such rows are transient demo rows
written by `scripts/seed_sih_demo.py`.

## Why

The crawler was a compliance-first system: it refused to run unless the source had a
recent permissive compliance record, enforced robots.txt and throttling, and published
only through a quality gate or human review. That complexity was more than the project
needs right now. The current offline path is a small in-repo parser over the saved SIH
HTML/XLSX archives (see `scripts/seed_sih_demo.py`), which writes generated summaries
and never full verbatim source text. Live-source ingestion and human review are
deferred to a later phase.

## Compliance records (historical)

The `docs/sources/` folder still holds the compliance write-ups that were prepared
before removal:

- `docs/sources/sih.md` — Smart India Hackathon (`allowed`; SIH 2026 pages + official 2024 XLSX).
- `docs/sources/kaggle.md` — Kaggle (`forbidden`; terms prohibit storage/display).
- `docs/sources/drivendata.md` — DrivenData (`forbidden`; terms prohibit automated copying).

Those records were written for the crawler path and are kept here for provenance. They
do **not** imply any active ingestion.

## Current demo fallback

To populate a local database without any network or LLM call:

```sh
cd backend
.venv/Scripts/python scripts/seed_sih_demo.py --limit 40 --reset
```

The script parses the stored SIH archives with a small in-file parser and writes
deterministic metadata plus generated summaries. It is a demo fallback only; it does not
contact the live site, does not use the LLM, and does not enforce the old compliance
gate.
