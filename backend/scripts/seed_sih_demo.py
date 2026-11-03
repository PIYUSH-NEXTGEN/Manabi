"""Seed the local catalog from the saved official SIH fixtures.

This is an offline fallback for local/demo data when the LLM provider is
unavailable. It uses the real SIH parsers and deterministic metadata, and writes
generated summaries (never full verbatim source text). Production runs should use
`python -m app.crawler.run`, which extracts with the LLM and enforces the full gate.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.crawler.dedupe import content_hash
from app.crawler.discovery.sih import parse_sih_html, parse_sih_xlsx
from app.crawler.extract import Extraction, ExtractedFields
from app.crawler.publish import upsert_problem
from app.crawler.registry import load_source
from app.crawler.registry import Publish
from app.db import session_scope
from app.seed.parser import DOMAIN_KEYWORDS, FIELD_KEYWORDS, TECH_TAG_ALIASES

FIXTURES = Path(__file__).resolve().parents[1] / "tests" / "fixtures" / "crawler" / "sih"


def _hits(keyword: str, text: str) -> bool:
    return re.search(rf"\b{re.escape(keyword)}\b", text, re.IGNORECASE) is not None


def _classify(text: str) -> tuple[str, str, list[str]]:
    lowered = re.sub(r"[+/,]", " ", text.lower())
    field_value = "other"
    for keyword, value in FIELD_KEYWORDS:
        if _hits(keyword, lowered):
            field_value = value
            break
    domain_value = "other"
    for keyword, value in DOMAIN_KEYWORDS:
        if _hits(keyword, lowered):
            domain_value = value
            break
    tags = sorted({tag for keyword, tag in TECH_TAG_ALIASES.items() if _hits(keyword, lowered)})
    return field_value, domain_value, tags


def _draft(item, year: int) -> Extraction:
    title = (item.title or "Untitled problem statement").strip()
    title_clean = title.rstrip(" .")
    organisation = item.organisation or "the organising body"
    theme = item.theme or item.category or "the published brief"
    field_value, domain_value, tags = _classify(
        " ".join(filter(None, [title, theme, item.department, item.description]))
    )
    summary = (
        f"{organisation} needs a software solution for {title_clean}. "
        f"The brief sits under the {theme} theme of Smart India Hackathon {year}; "
        "the expected outcome is a working prototype that addresses the stated need."
    )
    fields = ExtractedFields(
        title=title[:300],
        summary=summary[:8000],
        who_affected=f"{organisation} and the people it serves",
        why_matters=f"A working prototype would help {organisation} act on the {theme} challenge.",
        field=field_value,
        domain=domain_value,
        difficulty="intermediate",
        est_hours=40,
        tech_tags=tags,
        datasets=[],
        approaches=[],
        evidence={},
        inferred_fields=["summary", "who_affected", "why_matters"],
    )
    return Extraction(
        fields=fields,
        source_text=item.description or title,
        verified_evidence={},
        confidence=0.5,
        quality_notes=["offline deterministic seed; rerun the LLM crawler for polished summaries"],
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Seed local catalog from saved SIH fixtures")
    parser.add_argument("--limit", type=int, default=40, help="max software problems per year")
    parser.add_argument("--reset", action="store_true", help="remove existing crawler rows first")
    args = parser.parse_args()

    source_2026 = load_source("sih-2026").model_copy(
        update={"publish": Publish(auto_publish=True, min_confidence=0.4)}
    )
    source_2024 = load_source("sih").model_copy(
        update={"publish": Publish(auto_publish=True, min_confidence=0.4)}
    )

    page = (FIXTURES / "sih2026PS.html").read_text(encoding="utf-8")
    def usable(item) -> bool:
        title = (item.title or "").strip().lower()
        return (item.category or "").lower() == "software" and title not in {"", "student innovation"}

    items = [item for item in parse_sih_html(page, "https://sih.gov.in/sih2026PS", 2026) if usable(item)]
    xlsx = (FIXTURES / "SIH_PS_2024.xlsx").read_bytes()
    items += [item for item in parse_sih_xlsx(xlsx, "https://sih.gov.in/letters/SIH_PS_2024.xlsx", 2024) if usable(item)]

    written = {"2026": 0, "2024": 0}
    with session_scope() as db:
        if args.reset:
            from app.models import Problem

            db.query(Problem).filter(Problem.origin == "crawler").delete()
        for item in items:
            year = str(item.year)
            if written.get(year, 0) >= args.limit:
                continue
            source = source_2026 if item.year == 2026 else source_2024
            extraction = _draft(item, item.year or 2026)
            upsert_problem(
                db,
                source=source,
                item=item,
                extraction=extraction,
                digest=content_hash(item.description or item.title or ""),
            )
            written[year] = written.get(year, 0) + 1
    print(f"seeded SIH problems: {written}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
