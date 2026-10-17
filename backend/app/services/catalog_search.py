import re

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Problem

_KEYWORD_RE = re.compile(r"[a-z0-9]+")


def _keywords(text: str) -> set[str]:
    return set(_KEYWORD_RE.findall(text.lower()))


def search_catalog(db: Session, query: str, limit: int = 5) -> list[tuple[Problem, int]]:
    """Keyword match on title, summary, tech_tags, field, source_id. Top (problem, score)."""
    keywords = _keywords(query)
    if not keywords:
        return []
    problems: list[tuple[Problem, int]] = []
    problem_rows = db.scalars(select(Problem).order_by(Problem.id)).all()
    for problem in problem_rows:
        haystack = " ".join(
            [problem.title, problem.summary, problem.field, problem.domain, " ".join(problem.tech_tags)]
        )
        haystack_tokens = _keywords(haystack)
        source_tokens = _keywords(problem.source_id) if problem.source_id else set()
        score = 0
        for keyword in keywords:
            if keyword == (problem.source_id or "").lower():
                score += 10  # exact source-id match, e.g. "sih26017"
            elif keyword in source_tokens:
                score += 5
            elif keyword in haystack_tokens:
                score += 1
        if score > 0:
            problems.append((problem, score))
    problems.sort(key=lambda pair: (-pair[1], -pair[0].id))
    return problems[:limit]
