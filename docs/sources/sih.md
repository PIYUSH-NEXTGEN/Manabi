# Compliance record — Smart India Hackathon (sih.gov.in)

| Field | Value |
|---|---|
| Source name | Smart India Hackathon (SIH) |
| Base URL | `https://sih.gov.in` |
| Date checked | 2026-11-03 |
| Checked by | agent (Phase 0, MANABI crawler task) |
| Compliance record | `docs/sources/sih.md` (this file) |
| Verdict | **allowed** (owner approved 2026-11-03) |
| Owner decisions (2026-11-03) | Scope for now: **SIH 2026 pages + official 2024 XLSX only**; owner emails sih@aicte-india.org about historical exports (2022/2023/2025); Internet Archive snapshots **NOT approved**; third-party mirrors remain **excluded** as data origin; `CRAWLER_CONTACT` site URL = `https://github.com/PIYUSH-NEXTGEN/Manabi` |

## 1. What SIH is

sih.gov.in is the official portal of the Smart India Hackathon, run under the Ministry of
Education's Innovation Cell (MIC) / AICTE, Government of India. Problem statements are
submitted by central/state ministries, departments, PSUs, industries and NGOs, and are
published publicly on the portal for participants. MANABI only *displays* problem
statements found here with attribution and a link back; it does not host competitions and
does not claim ownership of the content.

## 2. Terms of Service / Privacy Policy check

**Recorded explicitly: sih.gov.in publishes NO Terms of Service, Terms & Conditions,
Acceptable Use or Privacy Policy document.** This was verified by direct probing
(all returned HTTP 404):

- `/terms-and-conditions`, `/termsconditions`, `/terms`, `/privacy-policy`
- The page footers contain no such links; the only footer notices are:
  - `"© 2025-26 Smart India Hackathon. All rights reserved"`
  - Contact: `sih@aicte-india.org`, phone numbers +91-11-29581222..29581319.
- `Site:pdf/SIH%20policy%20and%20process.pdf` ("Policy and process" download linked from
  the homepage) is about **product IP between organisers and student teams** (e.g.
  "50% of the product IP lies with your organization and the remaining 50% lies with the
  student team"). It says nothing about automated access to, or reuse of, published
  problem-statement content.
- No clause prohibiting automated access, scraping or republication of content was found,
  simply because no such site-level terms document exists.

## 3. robots.txt

Fetched `https://sih.gov.in/robots.txt` (2026-11-03):

```
User-agent: *
Disallow:
```

- Applies to every user-agent including `ManabiBot`: **all paths allowed**, no
  `Crawl-delay`, no `Sitemap` entries declared.

## 4. Official machine-readable channels

| Channel | Status |
|---|---|
| Official XLSX release | **Available**: `https://sih.gov.in/letters/SIH_PS_2024.xlsx` (~194 KB, sheet `sih_ps`, 246 data rows, columns: `Statement_id, Title, Category, Technology_Bucket, Datasetfile, Description, Department, Organisation`). Linked from `/sih2024PS` ("Download Problem Statements"). **Preferred source for SIH 2024.** |
| Public JSON/XHR API | None found. `/sih2026PS` (3.1 MB) is fully server-rendered HTML; no `fetch()`/XHR/AJAX calls in the page source. |
| RSS/Atom feeds | None found. |
| sitemap.xml | Not present (`/sitemap.xml` → 404). robots.txt declares no sitemap. |
| Guidelines PDFs | Official but about the process for participating institutions (e.g. `/letters/2026/SIH 2026 Guidelines.pdf`), not machine-readable PS data. |

## 5. Content licence / ownership

- Footer states "All rights reserved" for the portal (owned by MIC/AICTE / participating
  organisations). No open licence (CC etc.) is attached to the problem statements.
- Individual problem statements are authored by the submitting organisation (ministry,
  PSU, company, NGO). The portal publishes them openly and without login to enable
  participation — their purpose is public dissemination.
- Because the texts are all-rights-reserved, MANABI's display policy for this source is
  **`summary_only`** (decided by the owner): we show our own LLM-generated structured
  summary + deterministic fields (ID, title, organisation, theme, year) with attribution
  and a "View original" link (`source_url` always points to the official sih.gov.in page
  or the official XLSX), and do **not** republish the verbatim source text for crawled
  problems.

## 6b. Takedown / contact path (required by the owner)

- Problems from this source carry a visible **"Report / request removal"** link and the
  generated-summary attribution notice on MANABI's problem pages.
- Takedown: admin `POST /api/admin/sources/<key>/unpublish-all` unpublishes everything
  from this source at once; individual problems can also be unpublished/deleted by id.
- Escalation channel to the source owner: `sih@aicte-india.org` (published on the portal
  footer) — used if the organiser/owner of an individual problem statement contacts us
  and MANABI must remove or correct content.

## 6. Access model

- `/sih2026PS`, `/sih2024PS`, `/sih2025PS`, all overview pages, guidelines, FAQs and
  contact pages: **public, no login**.
- `/signin` and the registration/participation flows: behind login + OTP — **out of
  scope**; the crawler must never touch them.

## 7. Data availability per year (verified 2026-11-03)

| Year | On sih.gov.in today | Source usable by the crawler |
|---|---|---|
| 2026 | `/sih2026PS` live, server-rendered, 264 PSs (68 Hardware, 196 Software), full descriptions visible in HTML modal blocks | ✅ `listing_html` adapter |
| 2025 | `/sih2025PS` exists (HTTP 200) but the DataTable `<tbody>` is **empty**; rows appear to be removed after the edition closed. XLSX with 2025 names probe-tested — 404 | ❌ not available currently (see §9-Q1) |
| 2024 | `/sih2024PS` tbody empty, but official `/letters/SIH_PS_2024.xlsx` exists with Description column | ✅ `file_table` adapter (preferred) |
| 2023 | `/sih2023PS` → 404 (also `SIH2023PS`). `/sih2023s` is only an overview page (234 PSs, no listings). No 2023 XLSX found (`SIH_PS_2023.xlsx` → 404) | ❌ not available on the current portal (see §9-Q1) |
| 2022 | `/sih2022PS` → 404. `/sih2022s` is only an overview page. No 2022 XLSX found | ❌ same as 2023 (see §9-Q1) |

- The §14 link list supplied (`/sih2022PS`, `/sih2023PS`) does not match the live site;
  those URLs return 404. Corrected on-site equivalents are listed in the table above.
- Snapshots of `/sih2023PS` (Dec 2023) and `/sih2022PS` (Dec 2022) — and presumably
  `/sih2025PS` from earlier in 2025 — exist in the Internet Archive (`web.archive.org`),
  but **web.archive.org is not a domain cleared in §14**, so this is deferred to the
  owner's decision (§9-Q1). No Wayback pages have been crawled beyond a read-only
  availability probe of the snapshot redirects.

## 8. Runtime enforcement declarations

- **User-Agent**: `ManabiBot/1.0 (+<SITE_URL>/about; contact: <CRAWLER_CONTACT>)`
- **Contact email**: from env `CRAWLER_CONTACT` (**required before any run**; owner must
  supply — see §9-Q3).
- **Discovery method / throttle config** (to be encoded in `backend/app/crawler/sources/sih.yaml`):
  - `2026`: `listing_html`, URL `https://sih.gov.in/sih2026PS`, `min_delay_seconds: 3`,
    `max_pages_per_run: 200` (single page in practice), `max_concurrency: 1`.
  - `2024`: `file_table`, URL `https://sih.gov.in/letters/SIH_PS_2024.xlsx`
    (XLSX via explicit adapter, size/page caps), same throttle.
- **Display policy**: `summary_only` (§5 above).
- **Conditional requests**: honour `ETag`/`Last-Modified` when returned; hash content so
  unchanged pages cost nothing.
- **Never** touch `/signin`, registration or any authenticated area; never fetch anything
  robots.txt disallows (currently nothing).

## 9. Verdict, reasoning and open items

**Verdict: `allowed`** — public pages, robots.txt permits all crawlers, no ToS/anti-automation
clause found (no such document exists), and the content's purpose is public dissemination of
challenge statements. MANABI's reuse (its own AI-generated summary + deterministic metadata
fields, attribution, per-source removal contact, deep link back) does not republish the
verbatim all-rights-reserved text, which is the main residual right to respect.

Open items that need the owner before Phase 4 proceeds for those pieces:

- **Q1 — Missing years (2025, 2023, 2022) — DECIDED (2026-11-03): proceed with option (a).
  Ingest **only SIH 2026 pages + the official 2024 XLSX** for now. The owner will email
  sih@aicte-india.org to request official historical exports for 2022/2023/2025. Internet
  Archive snapshots (`web.archive.org`) remain **NOT approved**; the owner will be asked
  again only after option (a) is delivered.
- **Q2 — Third-party mirrors — DECIDED (2026-11-03): stay excluded** as data origin or
  stored `source_url`. A mirror may be consulted only for cross-checking IDs/counts
  (never stored as origin).
- **Q3 — `CRAWLER_CONTACT` — DECIDED (2026-11-03):** site URL
  `https://github.com/PIYUSH-NEXTGEN/Manabi` (from `SITE_URL`); a contact email may still
  be added to env later and must win over the URL when present.
- **Re-check date:** verify this record again **by 2027-03-03** (180 days), and after any
  portal relayout (registration changes, new ToS link appearing, robots.txt change).

## 10. Provenance of this check

Robots.txt and the current-year pages were fetched on 2026-11-03 during Phase 0 with
User-Agent `ManabiBot/1.0 (compliance check)`; saved copies (for Phase 4 fixtures):
`sih2026PS.html`, `sih2024PS.html`, `sih2025PS.html`, `SIH_PS_2024.xlsx`. Web search was
used to confirm the absence of a public ToS page and to identify candidate third-party
mirrors (excluded per §9-Q2).
