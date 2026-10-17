import argparse
import sys
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import Base, get_session_factory
from app.models import Problem
from app.seed.parser import ParsedEntry, parse_blocks

DEFAULT_FILE = Path(__file__).resolve().parents[3] / "projects.txt"
DEFAULT_PATHS = [DEFAULT_FILE, Path(__file__).resolve().parents[3] / "frontend" / "projects.txt"]


def entry_to_problem(entry: ParsedEntry) -> Problem:
    who_affected = entry.organisation or "Not stated in source"
    ai_fields = list(entry.ai_fields)
    if not entry.organisation and "who_affected" not in ai_fields:
        ai_fields.append("who_affected")
    return Problem(
        title=entry.title,
        summary=entry.body,
        who_affected=who_affected,
        why_matters=entry.body.split(".")[0].strip() + ".",
        field=entry.field,
        domain=entry.domain,
        difficulty=entry.difficulty,
        est_hours=entry.est_hours,
        tech_tags=entry.tech_tags,
        datasets=entry.datasets,
        approaches=[],
        source_name=entry.source_name,
        source_id=entry.source_id,
        source_url=None,
        source_note=None,
        original_text=entry.original_text,
        ai_fields=ai_fields,
        created_by=None,
    )


def import_entries(session: Session, text: str, create_tables: bool = False) -> dict:
    if create_tables:
        from app import models  # noqa: F401

        Base.metadata.create_all(session.get_bind())
    entries = parse_blocks(text)
    found_ids, unparsed_ids = _id_coverage(text, entries)
    inserted, skipped = 0, 0
    for entry in entries:
        existing = session.scalar(
            select(Problem).where(Problem.source_name == entry.source_name, Problem.source_id == entry.source_id)
        )
        if existing is not None:
            skipped += 1
            continue
        session.add(entry_to_problem(entry))
        inserted += 1
    session.commit()
    missing_ids = [entry.source_id for entry in entries if not entry.source_id]
    missing_urls = [entry.title for entry in entries if not _has_any_url(entry.original_text)]
    return {
        "parsed": len(entries),
        "inserted": inserted,
        "skipped": skipped,
        "found_ids": found_ids,
        "unparsed_ids": unparsed_ids,
        "missing_ids": missing_ids,
        "missing_urls": missing_urls,
    }


def _id_coverage(text: str, entries) -> tuple[dict[str, int], list[str]]:
    """Count source IDs in raw text vs parsed entries; anything missed is reported, never silently dropped."""
    import re as _re

    from app.seed.parser import SOURCE_ID_RE

    found: dict[str, int] = {}
    for sid in SOURCE_ID_RE.findall(text):
        found[sid] = found.get(sid, 0) + 1
    parsed: dict[str, int] = {}
    for entry in entries:
        parsed[entry.source_id] = parsed.get(entry.source_id, 0) + 1
    unparsed = [sid for sid, count in found.items() if count > parsed.get(sid, 0)]
    return found, unparsed


def _has_any_url(text: str) -> bool:
    return "http://" in text or "https://" in text


def resolve_file(path: str | None) -> Path:
    if path:
        candidates = [Path(path)]
    else:
        candidates = DEFAULT_PATHS
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return candidates[0]


def main(argv: list[str] | None = None) -> int:
    arg_parser = argparse.ArgumentParser(description="Import problems from projects.txt")
    arg_parser.add_argument("--file", help="path to projects.txt (default: repo root, then frontend/)")
    args = arg_parser.parse_args(argv)

    target = resolve_file(args.file)
    if not target.exists():
        print(f"ERROR: {target} not found. Use --file <path>.")
        return 1
    text = target.read_text(encoding="utf-8")
    session = get_session_factory()()
    try:
        result = import_entries(session, text, create_tables=True)
    finally:
        session.close()
    print(f"File: {target}")
    print(f"Entries parsed: {result['parsed']}")
    print(f"Rows inserted: {result['inserted']}")
    print(f"Rows skipped (already present): {result['skipped']}")
    if result["unparsed_ids"]:
        print(f"WARNING: source IDs present in file but not parsed into entries: {result['unparsed_ids']}")
    if result["missing_ids"]:
        print(f"Entries missing a source ID: {result['missing_ids']}")
    if result["missing_urls"]:
        print(f"Entries with no source URL: {result['missing_urls']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
