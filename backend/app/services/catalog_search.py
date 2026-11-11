import re

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import STATUS_PUBLISHED, Problem

_KEYWORD_RE = re.compile(r"[a-z0-9]+")

# Students describe projects loosely ("login app", "ai project", "webapps").
# Each token expands into a few aliases so keyword matching catches the brief
# vocabulary that actually appears in titles, summaries, and tech_tags.
_SYNONYMS: dict[str, set[str]] = {
    "login": {"login", "authentication", "auth"},
    "auth": {"auth", "authentication", "login"},
    "authentication": {"authentication", "auth", "login"},
    "ml": {"ml", "model", "prediction"},
    "ai": {"ai", "ml", "model"},
    "chatbot": {"chatbot", "chat", "assistant", "bot"},
    "bot": {"bot", "chatbot", "chat"},
    "app": {"app", "application", "web"},
    "webapp": {"webapp", "web", "app"},
    "website": {"website", "web", "app"},
    "dashboard": {"dashboard", "portal", "admin"},
    "tracker": {"tracker", "tracking", "monitor"},
    "monitor": {"monitor", "monitoring", "tracker"},
    "recommendation": {"recommendation", "recommendations", "suggest"},
    "detect": {"detect", "detection", "identify"},
    "detection": {"detection", "detect", "classify"},
    "predict": {"predict", "prediction", "forecast"},
    "forecast": {"forecast", "prediction", "predict"},
    "map": {"map", "maps", "gis"},
    "resume": {"resume", "cv", "portfolio"},
    "cv": {"cv", "resume"},
    "game": {"game", "games"},
    "translate": {"translate", "translation", "language"},
    "scanner": {"scanner", "scan", "ocr"},
    "ocr": {"ocr", "scan", "scanner"},
    "IoT": {"iot", "sensor", "device"},
    "sensor": {"sensor", "iot", "device"},
}


def _keywords(text: str) -> set[str]:
    """Lowercase tokens, plus safe aliases for loose student vocabulary."""
    raw = set(_KEYWORD_RE.findall(text.lower()))
    expanded = set(raw)
    for token in raw:
        expanded |= _SYNONYMS.get(token, set())
        # cheap plural/singular merge: "webapps"->"webapp", "alerts"->"alert"
        if token.endswith("ies") and len(token) > 4:
            expanded.add(token[:-3] + "y")
        elif token.endswith("es") and len(token) > 3:
            expanded.add(token[:-2])
        elif token.endswith("s") and len(token) > 2:
            expanded.add(token[:-1])
    return expanded


def search_catalog(db: Session, query: str, limit: int = 3) -> list[tuple[Problem, int]]:
    """Keyword match on title, summary, tech_tags, field, source_id. Top (problem, score)."""
    keywords = _keywords(query)
    if not keywords:
        return []
    problems: list[tuple[Problem, int]] = []
    problem_rows = db.scalars(
        select(Problem).where(Problem.status == STATUS_PUBLISHED).order_by(Problem.id)
    ).all()
    for problem in problem_rows:
        title_tokens = _keywords(problem.title)
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
                # title hits are the strongest signal a user means this problem
                score += 2 if keyword in title_tokens else 1
        if score > 0:
            problems.append((problem, score))
    problems.sort(key=lambda pair: (-pair[1], -pair[0].id))
    return problems[:limit]
