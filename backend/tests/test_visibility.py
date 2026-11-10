"""§6.4 regression tests: public read paths must only show published problems.

One test per consumer: list, facets, detail, stats, recommendations,
catalog search (chat), chat [P<id>] postprocess, project submission, profile.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.db import Base, get_db
from app.main import app
from app.models import Problem, Project, STATUS_PUBLISHED, User
from app.routers.chat import postprocess_reply
from app.services.catalog_search import search_catalog
from app.services.recommender import newest_problems, recommendations_for_user

STATUSES = ["published", "pending_review", "rejected", "removed"]


@pytest.fixture
def db_session():
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    Base.metadata.create_all(engine)
    factory = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    session = factory()
    app.dependency_overrides[get_db] = lambda: session
    yield session
    app.dependency_overrides.clear()
    session.close()


@pytest.fixture
def client(db_session):
    with TestClient(app) as test_client:
        yield test_client


def _problem(db: Session, i: int, status: str) -> Problem:
    p = Problem(
        title=f"Problem {i}",
        summary="s",
        who_affected="w",
        why_matters="y",
        field="aiml",
        domain="other",
        difficulty="beginner",
        est_hours=5,
        tech_tags=["python"],
        datasets=[],
        approaches=[],
        source_name="S",
        source_id=f"S{i}",
        original_text="verbatim",
    )
    p.status = status
    db.add(p)
    return p


@pytest.fixture
def mixed(db_session: Session):
    """One problem per status, deterministic titles."""
    problems = [_problem(db_session, i, status) for i, status in enumerate(STATUSES)]
    db_session.commit()
    return problems


# ---------------- list ----------------

def test_list_only_published(client, db_session, mixed):
    db_session.commit()
    res = client.get("/api/problems")
    assert res.status_code == 200
    items = res.json()["items"]
    assert [i["title"] for i in items] == ["Problem 0"]
    assert res.json()["total"] == 1


# ---------------- facets ----------------

def test_facets_only_published(client, db_session, mixed):
    db_session.commit()
    res = client.get("/api/problems/facets")
    assert res.status_code == 200
    facets = res.json()
    # 4 same-valued problems; only the published one may be counted anywhere
    assert facets["fields"] == [{"value": "aiml", "count": 1}]
    assert facets["domains"] == [{"value": "other", "count": 1}]
    assert facets["difficulties"] == [{"value": "beginner", "count": 1}]
    assert facets["tech_tags"] == [{"value": "python", "count": 1}]
    assert [(f["value"], f["count"]) for f in facets["sources"]] == [("S", 1)]


# ---------------- detail ----------------

def test_detail_published_200(client, db_session, mixed):
    db_session.commit()
    res = client.get(f"/api/problems/{mixed[0].id}")
    assert res.status_code == 200


@pytest.mark.parametrize("status", ["pending_review", "rejected", "removed"])
def test_detail_non_published_404(client, db_session, mixed, status):
    db_session.commit()
    problem = next(p for p in mixed if p.status == status)
    res = client.get(f"/api/problems/{problem.id}")
    assert res.status_code == 404


# ---------------- stats ----------------

def test_stats_only_published(client, db_session, mixed):
    db_session.commit()
    res = client.get("/api/stats")
    assert res.status_code == 200
    assert res.json()["problems"] == 1
    assert res.json()["sources"] == 1
    assert res.json()["fields"] == 1


# ---------------- recommendations (service) ----------------

def test_recommender_only_published(db_session, mixed):
    db_session.commit()
    user = User(github_id=1, username="u", signals_json={"languages": {"python": 3}, "topics": []})
    db_session.add(user)
    db_session.commit()
    assert all(p.status == STATUS_PUBLISHED for p in newest_problems(db_session))
    scored = recommendations_for_user(db_session, user)
    assert scored and all(p.status == STATUS_PUBLISHED for p, _score, _r in scored)


# ---------------- catalog search / chat ----------------

def test_chat_catalog_search_only_published(db_session, mixed):
    db_session.commit()
    hits = search_catalog(db_session, "Problem")
    assert [p for p, _s in hits] == [mixed[0]]


def test_chat_postprocess_strips_non_published_refs(db_session, mixed):
    db_session.commit()
    reply, items = postprocess_reply(db_session, f"See [P{mixed[1].id}] and [P{mixed[0].id}]")
    assert f"[P{mixed[1].id}]" not in reply  # pending_review ref stripped
    assert f"[P{mixed[0].id}]" in reply  # published ref kept
    assert [i.id for i in items] == [mixed[0].id]


# ---------------- projects ----------------

def test_cannot_submit_project_to_non_published_problem(client, db_session, mixed):
    db_session.commit()
    user = User(github_id=2, username="u2")
    db_session.add(user)
    db_session.commit()
    from app.deps import get_current_user

    app.dependency_overrides[get_current_user] = lambda: user
    for problem in mixed[1:]:
        res = client.post(
            f"/api/problems/{problem.id}/projects",
            json={
                "repo_url": "https://github.com/u2/repo",
                "solution_summary": "A repository is linked here with a full-ish solution summary description.",
                "open_for_contributors": False,
            },
        )
        assert res.status_code == 404
    app.dependency_overrides.pop(get_current_user)


# ---------------- profile ----------------

def test_profile_hides_projects_on_non_published_problems(client, db_session, mixed):
    db_session.commit()
    user = User(github_id=3, username="u3")
    db_session.add(user)
    db_session.commit()
    for problem in mixed:
        db_session.add(
            Project(
                problem_id=problem.id,
                user_id=user.id,
                repo_owner="u3",
                repo_name=f"repo-{problem.id}",
                repo_url=f"https://github.com/u3/repo-{problem.id}",
                verification_status="verified",
            )
        )
    db_session.commit()
    res = client.get("/api/u/u3")
    assert res.status_code == 200
    assert [p["repo_name"] for p in res.json()["projects"]] == [f"repo-{mixed[0].id}"]
