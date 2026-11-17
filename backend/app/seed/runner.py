"""Shared runner for the curated seed packs (seed_*_projects.py).

Every pack owns only its PROBLEMS data; inserting rows with the
skip-if-already-present rule lives here once, so the rule cannot drift
between packs:

    python -m app.seed.seed_ml_projects
"""

from sqlalchemy import select

from app.db import get_session_factory
from app.models import Problem, STATUS_PUBLISHED


def _apply_problem_fields(problem: Problem, p: dict) -> None:
    problem.title = p["title"]
    problem.summary = p["summary"]
    problem.who_affected = p["who_affected"]
    problem.why_matters = p["why_matters"]
    problem.field = p["field"]
    problem.domain = p["domain"]
    problem.difficulty = p["difficulty"]
    problem.est_hours = p["est_hours"]
    problem.tech_tags = p["tech_tags"]
    problem.datasets = p["datasets"]
    problem.approaches = p["approaches"]
    problem.source_name = p["source_name"]
    problem.source_url = None
    problem.source_note = p.get("source_note")
    problem.original_text = p["original_text"]
    problem.ai_fields = p["ai_fields"]
    problem.status = STATUS_PUBLISHED
    problem.goal = p.get("goal")
    problem.learning_concepts = p.get("learning_concepts", [])
    problem.build_guide = p.get("build_guide")
    problem.team_plan = p.get("team_plan")
    problem.pitch_guide = p.get("pitch_guide")
    problem.resume_kit = p.get("resume_kit")


def seed_problems(problems: list[dict], label: str = "problems", update: bool = False) -> None:
    session = get_session_factory()()
    inserted = 0
    updated = 0
    skipped = 0
    try:
        for p in problems:
            existing = session.scalar(
                select(Problem).where(Problem.source_id == p["source_id"])
            )
            if existing is not None:
                if update:
                    _apply_problem_fields(existing, p)
                    updated += 1
                else:
                    skipped += 1
                continue
            problem = Problem(source_id=p["source_id"], created_by=None)
            _apply_problem_fields(problem, p)
            session.add(problem)
            inserted += 1
        session.commit()
        print(
            f"Inserted: {inserted}, Updated: {updated}, "
            f"Skipped (already present): {skipped}"
        )
    finally:
        session.close()
