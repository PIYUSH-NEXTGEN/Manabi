"""Seed the local catalog from the saved official SIH fixtures.

This is an offline fallback for local/demo data when the LLM provider is
unavailable. It parses the stored SIH HTML/XLSX archives and writes generated
summaries (never full verbatim source text). The scheduled crawler, the admin
review queue, and the `/api/admin/*` endpoints were removed; live-source
ingestion is a separate planned effort.
"""

from __future__ import annotations

import argparse
import hashlib
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.db import session_scope
from app.models import Problem
from app.seed.parser import DOMAIN_KEYWORDS, FIELD_KEYWORDS, TECH_TAG_ALIASES

CODE_RE = re.compile(r"[A-Za-z0-9]{4,}")

KEYWORD_BY_TOKEN: dict[str, str] = {}
for keyword, tag in TECH_TAG_ALIASES.items():
    for token in re.findall(r"[a-z0-9]+", keyword.lower()):
        KEYWORD_BY_TOKEN[token] = keyword


def classify(text: str) -> tuple[str, str, list[str]]:
    lowered = re.sub(r"[^A-Za-z0-9]", " ", text.lower())
    field_value = "other"
    for keyword, value in FIELD_KEYWORDS:
        if keyword in lowered:
            field_value = value
            break
    domain_value = "other"
    for keyword, value in DOMAIN_KEYWORDS:
        if keyword in lowered:
            domain_value = value
            break
    seen: set[str] = set()
    tags: list[str] = []
    for token in re.findall(r"[a-z0-9]+", lowered):
        if len(token) < 3:
            continue
        for keyword, tag in TECH_TAG_ALIASES.items():
            if keyword == token or KEYWORD_BY_TOKEN.get(token) == keyword:
                if tag not in seen:
                    seen.add(tag)
                    tags.append(tag)
                break
    return field_value, domain_value, tags


def _attr_value(attrs: str, name: str) -> str:
    m = re.search(rf'{name}="([^"]+)"', attrs)
    return m.group(1) if m else ""


def _strip_html(s: str) -> str:
    return re.sub(r"<[^>]+>", "", s).strip()


def parse_sih_html(text: str, base_url: str, year: int) -> list[dict]:
    """Minimal parser for the SIH HTML problem archive (the <tr
</table> source with <td data-label="..."> columns and freeform <h3
titles). Returns one item per software problem statement.

    The previous crawler implementation used a DOM parser with explicit
Article extraction, but the stored archives are plain HTML tables, so this
simpler regex-based parser is used instead. It is deliberately small and
determinism-driven: the same archive always yields the same rows, and
generated summaries never include full verbatim source text.
    """
    items: list[dict] = []
    current: dict[str, str | None] = {
        "title": None,
        "description": None,
        "organisation": None,
        "theme": None,
        "category": None,
    }
    previous_title: str | None = None
    for tag, attrs, inner in _tokens(text):
        if tag == "h3":
            title = _strip_html(inner)
            if title:
                new = {"title": title}
                if previous_title and current.get("description"):
                    new.setdefault("description", current.get("description"))
                    items.append(_finalise(**{**current, **new}, year=year, base_url=base_url))
                previous_title = title
                current = dict(current)
                current["title"] = title
            continue
        if tag != "td":
            continue
        label = _attr_value(attrs, "data-label")
        if not label:
            continue
        value = _strip_html(inner)
        if label.lower() == "item name":
            current["title"] = value
        elif label.lower() == "problem statement":
            current["description"] = value
        elif label.lower() == "organisation":
            current["organisation"] = value
        elif label.lower() == "theme":
            current["theme"] = value
        elif label.lower() == "category":
            current["category"] = value
    for item in items:
        if not item.get("description"):
            item["description"] = item.get("title") or ""
    return items


def _tokens(html: str) -> list[tuple[str, str, str]]:
    out: list[tuple[str, str, str]] = []
    pattern = re.compile(r"<(/?)(\w+)([^>]*)>", re.IGNORECASE)
    prev_end = 0
    td_building = False
    td_label: str = ""
    td_value: list[str] = []
    for m in pattern.finditer(html):
        close, tag, attrs = m.groups()
        before = html[prev_end:m.start()]
        if td_building:
            td_value.append(before)
            prev_end = m.start()
        if close:
            if tag.lower() == "td" and td_building:
                out.append(("td", td_label, "".join(td_value)))
                td_building = False
            prev_end = m.end()
            continue
        if tag.lower() == "tr":
            if td_building:
                out.append(("td", td_label, "".join(td_value)))
                td_building = False
            prev_end = m.end()
            continue
        if tag.lower() == "h3":
            out.append(("h3", "", before))
            prev_end = m.end()
            continue
        if tag.lower() == "td":
            td_label = _attr_value(attrs, "data-label")
            td_value = []
            td_building = True
            prev_end = m.end()
            continue
        prev_end = m.end()
    if td_building:
        out.append(("td", td_label, "".join(td_value)))
    return out


def parse_sih_xlsx(text: bytes, base_url: str, year: int) -> list[dict]:
    """Thin XLSX parser backed by openpyxl (already pinned in requirements.txt)."""
    from openpyxl import load_workbook

    tmp = Path("/tmp/_sih.xlsx")
    tmp.write_bytes(text)
    try:
        wb = load_workbook(tmp, read_only=True, data_only=True)
    finally:
        tmp.unlink(missing_ok=True)
    ws = wb.worksheets[0]
    header: dict[str, int] = {}
    items: list[dict] = []
    for ri, row in enumerate(ws.iter_rows(values_only=True)):
        if ri == 0:
            header = {str(v).strip().lower(): i for i, v in enumerate(row) if v}
            continue
        values = [str(c).strip() if c is not None else "" for c in row]
        title = values[header.get("item name") or header.get("title") or 0]
        if not title or not CODE_RE.search(title):
            continue
        items.append(
            {
                "title": title,
                "description": values[header.get("problem statement") or header.get("description") or 1] or "",
                "organisation": values[header.get("organisation") or 2] or "",
                "theme": values[header.get("theme") or 3] or (values[header.get("category") or 4] or ""),
                "category": values[header.get("category") or 4] or "",
                "year": year,
                "url": base_url,
            }
        )
    return items


def _finalise(
    *,
    title: str,
    description: str,
    organisation: str,
    theme: str,
    category: str,
    year: int,
    base_url: str,
) -> dict:
    return {
        "title": title.strip(),
        "description": (description or "").strip(),
        "organisation": (organisation or "").strip() or "the organising body",
        "theme": (theme or category or "").strip() or "the published brief",
        "year": year,
        "url": base_url,
    }


def clean_title(title: str) -> str:
    parts = re.split(r"\s*[-–—|]\s*|\s+#\d+\b", title, maxsplit=1)
    return parts[0].strip()


def clean_summary(summary: str) -> str:
    parts = re.split(r"\s*[-–—|]\s*|\s+Based on:\s*", summary, maxsplit=1)
    return parts[0].splitlines()[-1].strip() or summary


def usable(item: dict) -> bool:
    title = (item.get("title") or "").strip().lower()
    return (item.get("category") or "").strip().lower() == "software" and title not in {"", "student innovation"}


def source(key: str) -> dict:
    return {
        "key": key,
        "source_name": "Smart India Hackathon" + (" 2026" if key == "sih-2026" else ""),
        "source_url": "https://sih.gov.in/sih2026PS" if key == "sih-2026" else "https://sih.gov.in/letters/SIH_PS_2024.xlsx",
        "checked_on": "2026-01-01",
        "display_policy": "summary_only",
    }


def draft(item: dict, year: int) -> dict:
    organisation = item.get("organisation") or "the organising body"
    theme = item.get("theme") or "the published brief"
    text = " ".join(filter(None, [item.get("title"), theme, item.get("description")]))
    field_value, domain_value, tags = classify(text)
    title = (item.get("title") or "Untitled problem statement").strip().rstrip(". ").rstrip()
    if not title:
        title = "Untitled problem statement"
    summary = (
        f"{organisation} needs a software solution for {title}. "
        f"The brief sits under the {theme} theme of Smart India Hackathon {year}; "
        "the expected outcome is a working prototype that addresses the stated need."
    )
    return {
        "title": title[:300],
        "summary": summary[:8000],
        "who_affected": f"{organisation} and the people it serves",
        "why_matters": f"A working prototype would help {organisation} act on the {theme} challenge.",
        "field": field_value,
        "domain": domain_value,
        "difficulty": "intermediate",
        "est_hours": 40,
        "tech_tags": tags,
        "datasets": [],
        "approaches": [],
        "evidence": {},
        "inferred_fields": ["summary", "who_affected", "why_matters"],
    }


def upsert(db, *, source: dict, item: dict, extraction: dict) -> None:
    existing = (
        db.query(Problem)
        .filter(Problem.origin == "crawler")
        .filter(Problem.source_id == item.get("url"))
        .first()
    )
    if existing is not None:
        return
    problem = Problem(
        title=extraction["title"],
        summary=extraction["summary"],
        who_affected=extraction["who_affected"],
        why_matters=extraction["why_matters"],
        field=extraction["field"],
        domain=extraction["domain"],
        difficulty=extraction["difficulty"],
        est_hours=extraction["est_hours"],
        source_name=source["source_name"],
        source_id=item.get("url"),
        source_url=source.get("source_url"),
        source_url_title="View original",
        source_note=None,
        tech_tags=[t for t in extraction["tech_tags"] if CODE_RE.search(t)] + ["python"]
        if extraction["tech_tags"]
        else ["javascript"],
        approaches=extraction["approaches"],
        status="published",
        origin="crawler",
    )
    db.add(problem)
    db.commit()


def problem_hash(text: str) -> int:
    return int(hashlib.md5(re.sub(r"\s+", " ", text or "").encode("utf-8")).hexdigest()[:8], 16) or 1


def main() -> int:
    parser = argparse.ArgumentParser(description="Seed local catalog from saved SIH fixtures")
    parser.add_argument("--limit", type=int, default=40, help="max software problems per year")
    parser.add_argument("--reset", action="store_true", help="remove existing crawler rows first")
    args = parser.parse_args()

    html_path = Path("tests/fixtures/sih/sih2026PS.html")
    html_items = [i for i in parse_sih_html(html_path.read_text(encoding="utf-8"), "https://sih.gov.in/sih2026PS", 2026) if usable(i)]

    xlsx_path = Path("tests/fixtures/sih/SIH_PS_2024.xlsx")
    xlsx_items = [i for i in parse_sih_xlsx(xlsx_path.read_bytes(), "https://sih.gov.in/letters/SIH_PS_2024.xlsx", 2024) if usable(i)]

    written: dict[str, int] = {"2026": 0, "2024": 0}

    with session_scope() as db:
        if args.reset:
            db.query(Problem).filter(Problem.origin == "crawler").delete()
        for item in html_items + xlsx_items:
            year = item.get("year")
            year_key = str(year or 2026)
            if written.get(year_key, 0) >= args.limit:
                continue
            source_dict = source("sih-2026" if year_key == "2026" else "sih")
            extraction = draft(item, year or 2026)
            upsert(db, source=source_dict, item=item, extraction=extraction)
            written[year_key] = written.get(year_key, 0) + 1

    print("seeded SIH problems:", written)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
