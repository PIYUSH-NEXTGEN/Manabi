# Compliance record — Kaggle (kaggle.com)

| Field | Value |
|---|---|
| Source name | Kaggle |
| Base URL | `https://www.kaggle.com` |
| Target page | `https://www.kaggle.com/competitions` |
| Date checked | 2026-11-03 |
| Checked by | agent (Phase 0) |
| Compliance record | `docs/sources/kaggle.md` (this file) |
| Verdict | **forbidden** |
| Adapter status | **not written** — awaiting owner decision |

## 1. What Kaggle is

Kaggle is a competition and dataset platform owned by Kaggle Inc. (Google). Hosts publish
competitions with data, rules and a metric; participants submit models. Competition pages
are public, but programmatic access to the platform is through the official Kaggle API/CLI
with an account token.

## 2. Terms of Service check

Official Terms of Use: `https://www.kaggle.com/terms` (read 2026-11-03; the page is
client-rendered, so it was rendered once with the existing Playwright Chromium install).
It is the binding agreement for the "Services", which include the website, API, products
and applications.

Relevant verbatim quotes (each <= 25 words):

- "You will only use the Services for your own internal, personal, non-commercial use"
- "“Crawls,” “scrapes,” or “spiders” any page, data, or portion ... (through use of manual or automated means)"
- "Copies or stores any significant portion of the Content"
- "you won’t ... display ... any Content not owned by you ... without the prior consent of the owner"
- "The materials displayed ... on or through the Services ... are protected by copyright and other intellectual property laws."

The Terms also state that violation is grounds for termination. There is **no API carve-out**
that permits third-party republication or storage of competition content. Using the official
API changes the transport, not the licence.

Privacy Policy: `https://www.kaggle.com/privacy` (read 2026-11-03). It confirms that
competition submissions and account data are personal/account data. We would not collect
participant data in any case.

## 3. robots.txt

- `https://www.kaggle.com/robots.txt` → **HTTP 404** (verified 2026-11-03 with curl and
  read_url).
- No robots file is served, so there are no crawl directives to honour. This does **not**
  grant permission: the Terms of Use independently prohibit automated copying and
  third-party display.

## 4. Official API / feed / export

- Official documented channel: Kaggle API and CLI
  (`https://www.kaggle.com/docs/api`, `https://github.com/Kaggle/kaggle-api`).
- `kaggle competitions list` exposes `ref`, `deadline`, `category`, `reward` and similar
  metadata.
- Authentication is required: a Kaggle account plus an API token (`KAGGLE_API_TOKEN` /
  `~/.kaggle/access_token` / legacy `kaggle.json`), per the official CLI docs
  (`docs/README.md` § Authentication).
- There is no official public feed or open-data export of competition statements, and the
  API docs grant no right to store, summarise or display competition content on another
  site.

## 5. Content licence / ownership

- Competition pages, rules and descriptions are Kaggle / Host User content, protected by
  copyright. No open licence (CC-BY etc.) is attached to competition statements.
- Each competition's own rules may add further restrictions on data and content.
- Competition datasets have their own licences and are **out of scope** for this project;
  we would never download them.

## 6. Access model

- Public competition pages: visible without login.
- Official API: requires an authenticated Kaggle account/token.
- No captcha bypass, login bypass or scraping would be attempted.

## 7. Verdict and reasoning

**Verdict: `forbidden`.**

The official API is the right transport, and robots.txt is absent, but the binding Terms
of Use prohibit exactly what MANABI would do:

1. MANABI is a public catalog, not the user's "own internal, personal, non-commercial use".
2. Storing title + generated summary + organisation + deadline and displaying them to third
   parties is copying/displaying Content not owned by MANABI without the owner's consent.
3. The "crawls/scrapes/spiders ... through manual or automated means" prohibition covers
   automated API collection used to populate a public catalog.
4. "Copies or stores any significant portion of the Content" rules out building a catalog
   from the competition list.

This is not `api_only`: an official API does not override the Terms' reuse and display
restrictions. It is not `unclear`: the prohibitions are explicit.

## 8. Fit assessment (even if permission existed)

Kaggle is a **poor fit** for "buildable problem statements". Most competition pages are
dataset + evaluation-metric specifications rather than a problem brief with users,
constraints and an expected software outcome. Titles and descriptions are often short or
rules-heavy. MANABI would have to generate most of the meaning, and the display would
still be a derivative of all-rights-reserved content.

## 9. Decision needed

Do **not** ingest Kaggle without written permission from Kaggle that covers storage of
competition metadata and public display of derived summaries with attribution and a link.

Owner options:

1. **Exclude Kaggle** (recommended) and move to DrivenData.
2. Provide written permission / a licence from Kaggle; then re-check this record.
3. Use Kaggle only as a private, non-published research input (not compatible with the
   public problem board).

## 10. Re-check

If Kaggle's Terms or competition-ownership rules change, or written permission is obtained,
re-check this record and update the verdict before any adapter is written.
