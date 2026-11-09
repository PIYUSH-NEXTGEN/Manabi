"""Tests for the curated Intermediate Web Development project ideas.

Verifies that the 10 curated intermediate web projects are stored correctly,
are discoverable through the existing field / difficulty / search / facets
filters, and expose a working detail page. Also verifies the seed logic is
idempotent.
"""
import pytest
from fastapi.testclient import TestClient
from app.db import Base, get_db
from sqlalchemy import create_engine, func, select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.main import app
from app.models import Problem, User
from scripts.seed_intermediate_web_projects import PROJECTS, SOURCE_NAME


@pytest.fixture
def _client():
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    Base.metadata.create_all(engine)
    factory = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    session = factory()
    app.dependency_overrides[get_db] = lambda: session
    yield TestClient(app), session
    app.dependency_overrides.clear()
    session.close()


def _seed_curated(session):
    session.add(User(github_id=1, username="tester"))
    for data in PROJECTS:
        session.add(Problem(**data))
    session.commit()


def _curated_count(session):
    return session.scalar(select(func.count(Problem.id)).where(Problem.source_name == SOURCE_NAME))


def test_all_curated_projects_are_intermediate_web(_client):
    _, session = _client
    _seed_curated(session)

    rows = session.scalars(select(Problem).where(Problem.source_name == SOURCE_NAME)).all()
    assert len(rows) == 10
    for row in rows:
        assert row.field == "web-fullstack"
        assert row.difficulty == "intermediate"
        assert row.status == "published"
        assert row.origin == "manual"
        assert row.source_url is None
        assert row.ai_fields == []


def test_curated_discoverable_via_filters(_client):
    client, session = _client
    _seed_curated(session)
    session.add(Problem(
        title="Old beginner problem", summary="s", who_affected="w", why_matters="m",
        field="ml", domain="healthcare", difficulty="beginner",
        est_hours=20, tech_tags=["html"], datasets=[], approaches=[],
        source_name="Other", source_id="old-beginner-001", original_text="ot",
        ai_fields=[], created_by=None,
    ))
    session.commit()

    r = client.get("/api/problems", params={"field": "web-fullstack", "difficulty": "intermediate"})
    data = r.json()
    assert data["total"] == 10
    assert len(data["items"]) == 10
    for it in data["items"]:
        assert it["field"] == "web-fullstack"
        assert it["difficulty"] == "intermediate"

    f = client.get("/api/problems/facets").json()
    difs = {d["value"]: d["count"] for d in f["difficulties"]}
    assert difs.get("intermediate", 0) >= 10


def test_curated_search_and_detail(_client):
    client, session = _client
    _seed_curated(session)
    first_title = PROJECTS[0]["title"]
    session.commit()

    r = client.get("/api/problems", params={"q": first_title.split()[0]})
    assert r.json()["total"] >= 1

    row = session.scalar(select(Problem).where(Problem.source_name == SOURCE_NAME).order_by(Problem.id))
    r2 = client.get(f"/api/problems/{row.id}")
    assert r2.status_code == 200
    assert r2.json()["title"] == first_title
    assert r2.json()["field"] == "web-fullstack"
    assert r2.json()["domain"] == PROJECTS[0]["domain"]
    assert r2.json()["original_text"]


def test_seed_logic_is_idempotent(_client):
    _, session = _client
    _seed_curated(session)
    assert _curated_count(session) == 10

    # Re-running the same check-then-add seed logic must not create duplicates.
    added = 0
    for data in PROJECTS:
        existing = session.scalar(select(Problem).where(
            Problem.source_name == data["source_name"],
            Problem.source_id == data["source_id"],
        ))
        if existing is None:
            session.add(Problem(**data))
            added += 1
    session.commit()
    assert added == 0
    assert _curated_count(session) == 10
