from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Problem, User

REC_LIMIT = 8
DIFFICULTY_BONUS = 1
FIELD_DOMAIN_BONUS = 2
TAG_MATCH_BONUS = 3

_FALLBACK_REASON = "Newest on MANABI"


def _score_problem(problem: Problem, languages: set[str], topics: set[str]) -> tuple[int, list[str]]:
    score = 0
    reasons: list[str] = []
    tags = {t.lower() for t in problem.tech_tags}
    matched_tags = tags & (languages | topics)
    score += TAG_MATCH_BONUS * len(matched_tags)
    matched_languages = sorted(matched_tags & languages)
    matched_topics = sorted(matched_tags & topics - languages)
    if matched_languages:
        reasons.append("You write " + ", ".join(t.title() for t in matched_languages))
    for topic in matched_topics:
        reasons.append(f"You use {topic}")
    field_match = problem.field in topics
    domain_match = problem.domain in topics
    if field_match or domain_match:
        score += FIELD_DOMAIN_BONUS
        reason_target = problem.field if field_match else problem.domain
        reasons.append(f"You explore {reason_target} problems")
    if problem.difficulty in ("beginner", "intermediate"):
        score += DIFFICULTY_BONUS
    return score, reasons


def newest_problems(db: Session, limit: int = REC_LIMIT) -> list[Problem]:
    return list(db.scalars(select(Problem).order_by(Problem.id.desc()).limit(limit)).all())


def recommendations_for_user(db: Session, user: User, limit: int = REC_LIMIT) -> list[tuple[Problem, int, list[str]]]:
    """Top problems by 10.4 scoring. No signals -> newest problems with a fallback reason."""
    signals = user.signals_json or {}
    languages = {str(k).lower() for k in (signals.get("languages") or {})}
    topics = {str(t).lower() for t in (signals.get("topics") or [])}
    problems = list(db.scalars(select(Problem)).all())
    if not languages and not topics:
        return [(problem, 0, [_FALLBACK_REASON]) for problem in newest_problems(db, limit)]
    scored: list[tuple[Problem, int, list[str]]] = []
    for problem in problems:
        score, reasons = _score_problem(problem, languages, topics)
        if reasons:
            scored.append((problem, score, reasons))
    scored.sort(key=lambda item: (-item[1], -item[0].id))
    if not scored:
        return [(problem, 0, [_FALLBACK_REASON]) for problem in newest_problems(db, limit)]
    return scored[:limit]
