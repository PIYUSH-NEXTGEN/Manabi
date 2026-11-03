# Compliance record — DrivenData (drivendata.org)

| Field | Value |
|---|---|
| Source name | DrivenData |
| Base URL | `https://www.drivendata.org` |
| Target page | `https://www.drivendata.org/competitions/` |
| Date checked | 2026-11-03 |
| Checked by | agent (Phase 0) |
| Compliance record | `docs/sources/drivendata.md` (this file) |
| Verdict | **forbidden** |
| Adapter status | **not written** — awaiting owner decision |

## 1. What DrivenData is

DrivenData, LLC (Denver, US) hosts data-science competitions "for social good" on behalf of
sponsors (NASA, NIH, World Bank, US Bureau of Reclamation, etc.). The `/competitions/`
listing is public and server-rendered: each card shows a title, short tagline, theme tags,
participant count, prize, status and deadline. Individual competition pages add a problem
description, data-download instructions, an evaluation metric and the competition rules.

## 2. Terms of Use check

Official Terms of Use: `https://www.drivendata.org/termsofuse/` (read 2026-11-03; last
modified 2014-08-07). It is the binding agreement for the whole site, "whether as a guest
or a registered user".

Relevant verbatim quotes (each <= 25 words):

- "These Terms of Use permit you to use the Website for your personal, non-commercial use only."
- "You must not reproduce, distribute, modify, create derivative works of, publicly display,
  publicly perform, republish, download, store or transmit any of the material on our Website"
- "Use any robot, spider or other automatic device, process or means to access the Website
  for any purpose, including monitoring or copying any of the material on the Website."
- "Use any manual process to monitor or copy any of the material on the Website or for any
  other unauthorized purpose without our prior written consent."
- "Link to any part of the Website other than the homepage."
- "You must not access or use for any commercial purposes any part of the Website or any
  services or materials available through the Website."

The exceptions listed are narrow and all personal: temporary RAM copies, browser cache,
and printing/downloading "one copy of a reasonable number of pages ... for your own
personal, non-commercial use and not for further reproduction, publication or
distribution."

There is no API carve-out, no open-content licence and no permission to build a third-party
catalog from the material.

Privacy Policy: `https://www.drivendata.org/privacypolicy/` (effective 2026-09-08). It covers
account, competition and participation data. MANABI would not collect participant data in
any case; noted for completeness only.

Note on the copyright policy (`/copyrightpolicy/`) — it is a DMCA notice procedure, not a
reuse licence.

## 3. robots.txt

`https://www.drivendata.org/robots.txt` (verified 2026-11-03 with curl):

```
User-agent: *
Disallow: /accounts/
Disallow: /competitions/search/
Disallow: /*/leaderboard_partial
Disallow: /*/leaderboard_partial/
```

- `/competitions/` and individual `/competitions/<id>/<slug>/` pages are **not** disallowed,
  and no `Crawl-delay` or `Sitemap` is declared.
- robots.txt therefore permits crawling the competition pages.
- robots.txt is not the only rule: the Terms of Use independently prohibit automated access
  for copying and any republication/display. **The stricter document governs.**

## 4. Official API / feed / export

- `https://www.drivendata.org/api/` → **HTTP 404**; `https://www.drivendata.org/docs/` →
  **HTTP 404**. No documented public API, and no API link anywhere in the site footer.
- No JSON/XHR competition feed: the listing and detail pages are server-rendered HTML.
- No RSS/Atom feed and no sitemap.xml declared or linked.
- Registered-user endpoints exist for submissions and leaderboards, but they require an
  account and are covered by the same Terms; we would not use them, and would never touch
  leaderboards or participant data.

So this source can only be read as HTML pages — which is precisely the access the Terms
address most directly.

## 5. Content licence / ownership

- "The Website and its entire contents, features and functionality ... are owned by the
  Company, its licensors or other providers ... and are protected by United States and
  international copyright ... laws."
- No open licence (CC-BY, ODbL, etc.) is attached to competition statements. The
  competition rules govern *participant submissions and data*, not reuse of the problem
  text by third parties.
- Datasets are separately licensed and are **out of scope**; we would never download them.

## 6. Access model

- Public listing and competition pages: visible without login.
- Joining a competition, downloading data and submitting require an account.
- No login bypass, no captcha bypass, no rate-limit circumvention would be attempted.
- We would not store anything from `/accounts/`, `/competitions/search/` or any leaderboard.

## 7. Verdict and reasoning

**Verdict: `forbidden`.**

robots.txt is permissive for the competition pages, and the pages are plain server-rendered
HTML, so the technical path exists. The binding Terms nonetheless prohibit the intended use:

1. MANABI is a public catalog, not "personal, non-commercial use" by the reader.
2. Storing title + generated summary + organisation + deadline and displaying them to third
   parties is storing and publicly displaying material from the Website.
3. "Use any robot, spider or other automatic device ... for any purpose, including ...
   copying" covers automated collection used to populate the catalog, whether or not the
   collection is polite.
4. The site's own linking clause restricts links to the homepage, which conflicts with a
   "View original" deep link to each competition.
5. Creating MANABI summaries is explicitly "create derivative works of ... publicly display".

This is not `api_only` (no API exists), and not `unclear` (the prohibitions are explicit and
not limited to commercial use alone — the automated-access clause is unconditional).

## 8. Fit assessment (even if permission existed)

DrivenData is a **poor fit** for MANABI even setting licensing aside:

- Every competition is a supervised-ML task on a specific dataset. To be buildable, a
  participant must join the competition and download that data, which MANABI explicitly
  will not do and cannot redistribute.
- Pages are mostly metric + submission-format + rules text, not a software brief with users,
  constraints and an expected product. The natural "project" is "train a model", not "ship an
  app for the affected organisation".
- Many entries are past competitions whose data access and support have closed.
- Titles/taglines are one sentence; a useful summary would be almost entirely MANABI's
  invention rather than sourced from the page.

Verdict on fit: **do not include.**

## 9. Decision needed

Do **not** ingest DrivenData without written permission from DrivenData, LLC that covers
storage of competition metadata and public display of derived summaries with attribution and
a deep link.

Owner options:

1. **Exclude DrivenData** (recommended) and move to dev.to challenges.
2. Obtain written permission / a data licence from DrivenData; then re-check this record and
   the "View original" link policy (deep links are currently restricted by their Terms).
3. Keep it as a private, non-published research input (not compatible with the public board).

## 10. Re-check

If DrivenData's Terms of Use are revised, an official API/feed is published, or written
permission is obtained, re-check this record and update the verdict before any adapter is
written.
