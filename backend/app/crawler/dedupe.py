"""Idempotency and de-duplication (§6.5)."""

from __future__ import annotations

import hashlib
import re
from difflib import SequenceMatcher

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Problem

SIMILARITY_THRESHOLD = 0.92


def normalise_text(text: str) -> str:
    return " ".join(text.split()).lower()


def content_hash(text: str) -> str:
    return hashlib.sha256(normalise_text(text).encode("utf-8")).hexdigest()


def normalise_title(title: str) -> str:
    return re.sub(r"[^a-z0-9 ]+", " ", title.lower()).strip()


def title_similarity(left: str, right: str) -> float:
    return SequenceMatcher(None, normalise_title(left), normalise_title(right)).ratio()


def source_id_for(title: str, organisation: str | None) -> str:
    digest = hashlib.sha256(
        "|".join([normalise_title(title), normalise_text(organisation or "")]).encode("utf-8")
    ).hexdigest()[:16]
    return f"gen-{digest}"


def find_duplicate(
    db: Session,
    *,
    source_name: str,
    source_id: str | None,
    title: str,
    organisation: str | None,
    exclude_id: int | None = None,
) -> Problem | None:
    """Exact source identity first; then a near-duplicate cross-source check."""
    if source_id:
        exact = db.scalar(
            select(Problem).where(Problem.source_name == source_name, Problem.source_id == source_id)
        )
        if exact is not None and exact.id != exclude_id:
            return exact
    candidates = db.scalars(select(Problem).limit(2000)).all()
    org = normalise_text(organisation or "")
    for candidate in candidates:
        if candidate.id == exclude_id:
            continue
        if title_similarity(title, candidate.title) < SIMILARITY_THRESHOLD:
            continue
        if org and candidate.organisation and normalise_text(candidate.organisation) != org:
            continue
        return candidate
    return None
