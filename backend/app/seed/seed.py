"""Idempotent ML question seeder: inserts only questions whose title is not present."""
import json
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import session_scope
from app.models import MLQuestion

SEED_FILE = Path(__file__).parent / "ml_questions.json"


def seed(db: Session) -> dict:
    questions = json.loads(SEED_FILE.read_text(encoding="utf-8"))
    existing_titles = set(db.scalars(select(MLQuestion.title)).all())
    inserted = 0
    for item in questions:
        if item["title"] in existing_titles:
            continue
        db.add(
            MLQuestion(
                title=item["title"],
                scenario=item["scenario"],
                difficulty=item["difficulty"],
                topic=item["topic"],
                rubric_json=item["rubric"],
                explanation=item["explanation"],
            )
        )
        inserted += 1
    db.commit()
    return {"inserted": inserted, "already_present": len(questions) - inserted, "total_in_file": len(questions)}


def main() -> None:
    with session_scope() as db:
        result = seed(db)
    print(f"ML seed: {result}")


if __name__ == "__main__":
    main()
