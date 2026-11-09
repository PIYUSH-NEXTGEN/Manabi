"""Shared runner for the curated seed packs (seed_*_projects.py).

Every pack owns only its PROBLEMS data; inserting rows with the
skip-if-already-present rule lives here once, so the rule cannot drift
between packs:

    python -m app.seed.seed_ml_projects
"""

from sqlalchemy import select

from app.db import get_session_factory
from app.models import Problem, STATUS_PUBLISHED


def seed_problems(problems: list[dict], label: str = "problems") -> None:
    session = get_session_factory()()
    inserted = 0
    skipped = 0
    try:
        for p in problems:
            existing = session.scalar(
                select(Problem).where(Problem.source_id == p["source_id"])
            )
            if existing is not None:
                skipped += 1
                continue
            problem = Problem(
                title=p["title"],
                summary=p["summary"],
                who_affected=p["who_affected"],
                why_matters=p["why_matters"],
                field=p["field"],
                domain=p["domain"],
                difficulty=p["difficulty"],
                est_hours=p["est_hours"],
                tech_tags=p["tech_tags"],
                datasets=p["datasets"],
                approaches=p["approaches"],
                source_name=p["source_name"],
                source_id=p["source_id"],
                source_url=None,
                source_note=p.get("source_note"),
                original_text=p["original_text"],
                ai_fields=p["ai_fields"],
                created_by=None,
                status=STATUS_PUBLISHED,
            )
            session.add(problem)
            inserted += 1
        session.commit()
        print(f"Inserted: {inserted}, Skipped (already present): {skipped}")
    finally:
        session.close()
