import json
from datetime import date

import pytest
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.crawler.dedupe import find_duplicate, title_similarity
from app.crawler.discovery.base import DiscoveredItem
from app.crawler.extract import (
    Extraction,
    ExtractedFields,
    NoClearProblem,
    compute_confidence,
    extract_draft,
    verify_evidence,
)
from app.crawler.publish import upsert_problem
from app.crawler.registry import load_source
from app.db import Base
from app.models import Problem, STATUS_PENDING_REVIEW, STATUS_PUBLISHED


@pytest.fixture
def db():
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    Base.metadata.create_all(engine)
    session = sessionmaker(bind=engine)()
    yield session
    session.close()


def _payload(**overrides):
    payload = {
        "is_problem": True,
        "title": "Flood early warning dashboard",
        "summary": "Build a dashboard that blends rainfall and river gauges.",
        "who_affected": "District disaster teams",
        "why_matters": "Earlier warnings save lives.",
        "field": "geospatial",
        "domain": "disaster-management",
        "difficulty": "intermediate",
        "est_hours": 40,
        "tech_tags": ["python", "gis"],
        "datasets": [],
        "approaches": ["Blend gauges with rainfall", "Show uncertainty bands"],
        "evidence": {},
        "inferred_fields": [],
    }
    payload.update(overrides)
    return payload


def _extraction(confidence=0.9, title="Flood early warning dashboard", text="source body"):
    fields = ExtractedFields.model_validate(
        _payload(title=title, evidence={"title": "river gauges"})
    )
    return Extraction(fields=fields, source_text=text, verified_evidence={"title": "river gauges"}, confidence=confidence)


def test_extract_validates_json_and_overrides_nothing(db):
    source = load_source("sih")
    item = DiscoveredItem(url="https://sih.gov.in/x", source_id="SIH26001", title="T", year=2026)
    text = "Flood warnings for river gauges and district teams."
    calls = []

    def fake_call(system, messages):
        calls.append((system, messages))
        return json.dumps(_payload(evidence={"title": "river gauges"}))

    result = extract_draft(source=source, item=item, text=text, call=fake_call)
    assert result.fields.title == "Flood early warning dashboard"
    assert result.verified_evidence == {"title": "river gauges"}
    assert result.confidence >= 0.75
    assert calls and "untrusted data" in calls[0][0]


def test_extract_rejects_non_problem():
    source = load_source("sih")
    item = DiscoveredItem(url="https://sih.gov.in/x", source_id="SIH26001")
    with pytest.raises(NoClearProblem):
        extract_draft(source=source, item=item, text="About us page", call=lambda s, m: '{"is_problem": false}')


def test_extract_rejects_invalid_enums():
    source = load_source("sih")
    item = DiscoveredItem(url="https://sih.gov.in/x", source_id="SIH26001")
    bad = _payload(field="astrology")
    with pytest.raises(RuntimeError, match="validation"):
        extract_draft(source=source, item=item, text="x", call=lambda s, m: json.dumps(bad))


def test_evidence_must_be_verbatim():
    verified = verify_evidence("The river gauges feed a dashboard.", {"title": "river gauges", "summary": "invented claim"})
    assert verified == {"title": "river gauges"}


def test_confidence_rewards_verified_evidence_and_penalises_inference():
    fields = ExtractedFields.model_validate(_payload())
    high, _ = compute_confidence(fields, {"title": "a" * 20, "summary": "b" * 20, "who_affected": "c" * 20, "why_matters": "d" * 20}, "text")
    inferred = fields.model_copy(update={"inferred_fields": ["summary", "approaches"]})
    low, notes = compute_confidence(inferred, {}, "text")
    assert high > low
    assert notes


def test_near_duplicate_detection(db):
    db.add(
        Problem(
            title="Flood Early Warning System",
            summary="s",
            who_affected="w",
            why_matters="y",
            field="geospatial",
            domain="disaster-management",
            difficulty="beginner",
            est_hours=10,
            tech_tags=[],
            datasets=[],
            approaches=[],
            source_name="Other",
            source_id="X1",
            original_text="",
        )
    )
    db.commit()
    assert title_similarity("Flood Early Warning System", "Flood early-warning system!") > 0.9
    duplicate = find_duplicate(
        db,
        source_name="Smart India Hackathon 2026",
        source_id="SIH26001",
        title="Flood early-warning system",
        organisation=None,
    )
    assert duplicate is not None


def test_upsert_is_idempotent_and_publishes(db):
    source = load_source("sih")
    item = DiscoveredItem(
        url="https://sih.gov.in/sih2024PS#SIH26001",
        source_id="SIH26001",
        organisation="Ministry",
        year=2024,
        deadline=date(2027, 1, 1),
    )
    first = upsert_problem(db, source=source, item=item, extraction=_extraction(), digest="hash-1")
    db.commit()
    assert first.action == "new" and first.status == STATUS_PUBLISHED
    problem = db.scalar(select(Problem).where(Problem.source_id == "SIH26001"))
    assert problem.origin == "crawler"
    assert problem.original_text == ""
    assert problem.source_status == "open"
    assert problem.source_name == "Smart India Hackathon 2024"

    second = upsert_problem(db, source=source, item=item, extraction=None, digest="hash-1")
    db.commit()
    assert second.action == "unchanged"


def test_human_edited_problem_is_not_overwritten_silently(db):
    source = load_source("sih")
    item = DiscoveredItem(url="https://sih.gov.in/x#SIH26002", source_id="SIH26002", year=2026)
    upsert_problem(db, source=source, item=item, extraction=_extraction(), digest="old")
    db.commit()
    problem = db.scalar(select(Problem).where(Problem.source_id == "SIH26002"))
    problem.review_notes = "human edit: approved wording"
    db.commit()

    outcome = upsert_problem(db, source=source, item=item, extraction=_extraction(title="Changed title"), digest="new")
    db.commit()
    assert outcome.status == STATUS_PENDING_REVIEW
    assert "human edit" in (outcome.note or "")


def test_low_confidence_goes_to_pending_review(db):
    source = load_source("sih")
    item = DiscoveredItem(url="https://sih.gov.in/x#SIH26003", source_id="SIH26003", year=2026)
    outcome = upsert_problem(db, source=source, item=item, extraction=_extraction(confidence=0.4), digest="low")
    db.commit()
    assert outcome.status == STATUS_PENDING_REVIEW
