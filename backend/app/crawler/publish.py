"""Decide published vs pending_review and write Problem rows (§7.3)."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.crawler.dedupe import find_duplicate, source_id_for
from app.crawler.discovery.base import DiscoveredItem
from app.crawler.extract import Extraction
from app.crawler.registry import Source
from app.models import (
    ORIGIN_CRAWLER,
    STATUS_PENDING_REVIEW,
    STATUS_PUBLISHED,
    Problem,
)

HUMAN_MARKERS = ("human edit", "approved by admin")


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


def is_human_touched(problem: Problem) -> bool:
    notes = (problem.review_notes or "").lower()
    return any(marker in notes for marker in HUMAN_MARKERS)


def source_display_name(source: Source, year: int | None) -> str:
    return f"{source.name} {year}" if year else source.name


def deterministic_source_id(item: DiscoveredItem, title: str | None = None) -> str:
    """Real source ID when present, else a stable hash of title + organisation."""
    return item.source_id or source_id_for(title or item.title or "", item.organisation)


def _source_status(item: DiscoveredItem) -> str:
    if item.deadline is None:
        return "unknown"
    return "open" if item.deadline >= date.today() else "closed"


@dataclass
class PublishOutcome:
    action: str
    problem_id: int | None = None
    status: str | None = None
    note: str | None = None


def _apply_fields(problem: Problem, source: Source, item: DiscoveredItem, extraction: Extraction, digest: str) -> None:
    fields = extraction.fields
    problem.title = fields.title.strip()
    problem.summary = fields.summary.strip()
    problem.who_affected = fields.who_affected.strip()
    problem.why_matters = fields.why_matters.strip()
    problem.field = fields.field
    problem.domain = fields.domain
    problem.difficulty = fields.difficulty
    problem.est_hours = fields.est_hours
    problem.tech_tags = [tag.strip().lower() for tag in fields.tech_tags]
    problem.datasets = [dataset.model_dump() for dataset in fields.datasets]
    problem.approaches = fields.approaches
    problem.source_name = source_display_name(source, item.year)
    problem.source_id = deterministic_source_id(item, fields.title)
    problem.source_url = item.url
    problem.source_note = item.extra.get("dataset_file") if item.extra else None
    # §5: never republish crawled source text. The detail API returns the
    # generated summary for crawler-origin problems.
    problem.original_text = ""
    problem.ai_fields = list(extraction.fields.inferred_fields)
    problem.origin = ORIGIN_CRAWLER
    problem.content_hash = digest
    problem.source_year = item.year
    problem.edition = item.edition or (str(item.year) if item.year else None)
    problem.organisation = item.organisation
    problem.deadline = item.deadline
    problem.source_status = _source_status(item)
    problem.extraction_confidence = extraction.confidence
    problem.crawl_source_key = source.key


def upsert_problem(
    db: Session,
    *,
    source: Source,
    item: DiscoveredItem,
    extraction: Extraction,
    digest: str,
    dry_run: bool = False,
) -> PublishOutcome:
    source_name = source_display_name(source, item.year)
    identity = deterministic_source_id(item)
    existing = db.scalar(
        select(Problem).where(
            Problem.source_name == source_name,
            Problem.source_id == identity,
        )
    )

    if existing is not None and existing.content_hash == digest:
        # Same content means no LLM call and no field writes (§6.5).
        if not dry_run:
            existing.last_seen_at = utcnow()
            existing.last_crawled_at = utcnow()
            if item.deadline is not None:
                existing.deadline = item.deadline
                existing.source_status = _source_status(item)
        return PublishOutcome("unchanged", existing.id, existing.status)

    duplicate = find_duplicate(
        db,
        source_name=source_name,
        source_id=item.source_id,
        title=extraction.fields.title,
        organisation=item.organisation,
        exclude_id=existing.id if existing else None,
    )

    review_note = None
    human_touched = existing is not None and is_human_touched(existing)
    if duplicate is not None and (existing is None or duplicate.id != existing.id):
        review_note = f"possible duplicate of #{duplicate.id}"
    publish_ok = (
        source.publish.auto_publish
        and extraction.confidence >= source.publish.min_confidence
        and review_note is None
        and not human_touched
    )
    target_status = STATUS_PUBLISHED if publish_ok else STATUS_PENDING_REVIEW
    if human_touched and review_note is None:
        review_note = "source changed after a human edit; pending re-review"
    evidence_note = (
        "verified evidence: " + ", ".join(sorted(extraction.verified_evidence))
        if extraction.verified_evidence
        else "no verified evidence"
    )
    notes = "; ".join(filter(None, [review_note, evidence_note, *extraction.quality_notes])) or None

    if dry_run:
        return PublishOutcome("new" if existing is None else "updated", existing.id if existing else None, target_status, notes)

    if existing is None:
        problem = Problem(
            title="",
            summary="",
            who_affected="",
            why_matters="",
            field=extraction.fields.field,
            domain=extraction.fields.domain,
            difficulty=extraction.fields.difficulty,
            est_hours=extraction.fields.est_hours,
            tech_tags=[],
            datasets=[],
            approaches=[],
            source_name=source_name,
            source_id=deterministic_source_id(item, extraction.fields.title),
            original_text="",
            first_seen_at=utcnow(),
            last_seen_at=utcnow(),
            created_at=utcnow(),
        )
        _apply_fields(problem, source, item, extraction, digest)
        problem.status = target_status
        problem.review_notes = notes
        db.add(problem)
        db.flush()
        action = "new"
    else:
        _apply_fields(existing, source, item, extraction, digest)
        existing.status = target_status
        existing.review_notes = notes
        existing.last_seen_at = utcnow()
        existing.last_crawled_at = utcnow()
        action = "updated"

    problem = existing or problem
    return PublishOutcome(
        action,
        problem.id,
        target_status,
        notes,
    )
