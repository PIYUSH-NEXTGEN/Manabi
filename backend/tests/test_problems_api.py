import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.db import Base, get_db
from app.main import app
from app.models import Problem, Project, User


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


@pytest.fixture
def seed(db_session: Session):
    user = User(github_id=42, username="octocat", name="Octo", avatar_url="http://a/1.png")
    db_session.add(user)
    p_old = Problem(
        title="Old flood model",
        summary="Predict floods early",
        who_affected="Ministry X",
        why_matters="Saves people",
        field="aiml",
        domain="disaster-management",
        difficulty="intermediate",
        est_hours=30,
        tech_tags=["python", "pandas"],
        datasets=[],
        approaches=[],
        source_name="Smart India Hackathon 2026",
        source_id="SIH26001",
        original_text="Old flood model verbatim statement.",
        created_by=None,
    )
    p_new = Problem(
        title="Onion grading camera",
        summary="Grade onions from a photo",
        who_affected="Ministry Y",
        why_matters="Fair procurement",
        field="web-dev",
        domain="agriculture",
        difficulty="beginner",
        est_hours=20,
        tech_tags=["python", "vision"],
        datasets=[],
        approaches=[],
        source_name="TCOE",
        source_id="TCOE PS12",
        original_text="Onion grading camera verbatim statement.",
        created_by=None,
    )
    p_pop = Problem(
        title="Ambulance triage board",
        summary="Route ambulances better",
        who_affected="Ministry Z",
        why_matters="Faster response",
        field="aiml",
        domain="healthcare",
        difficulty="advanced",
        est_hours=60,
        tech_tags=["python", "real-time"],
        datasets=[],
        approaches=[],
        source_name="TCOE",
        source_id="TCOE PS15",
        original_text="Ambulance triage board verbatim statement.",
        created_by=None,
    )
    db_session.add_all([p_old, p_new, p_pop])
    db_session.commit()
    db_session.add(Project(
        problem_id=p_pop.id, user_id=user.id, repo_owner="octocat", repo_name="triage",
        repo_url="https://github.com/octocat/triage", open_for_contributors=True,
        verification_status="verified",
    ))
    db_session.commit()
    return {"user": user, "old": p_old, "new": p_new, "pop": p_pop}


def test_list_returns_all_with_project_count(client, seed):
    res = client.get("/api/problems")
    assert res.status_code == 200
    data = res.json()
    assert data["total"] == 3
    assert len(data["items"]) == 3
    first = data["items"][0]
    assert first["title"] == "Ambulance triage board"  # newest by id desc
    pop = next(it for it in data["items"] if it["id"] == seed["pop"].id)
    assert pop["project_count"] == 1
    others = [it for it in data["items"] if it["id"] != seed["pop"].id]
    assert all(o["project_count"] == 0 for o in others)


def test_list_never_exposes_secret_fields(client, seed):
    res = client.get("/api/problems")
    keys = set(res.json()["items"][0].keys())
    assert "created_by" not in keys
    assert "github_token" not in keys
    assert "original_text" not in keys


def test_list_summary_is_a_complete_sentence_overview(client, db_session: Session):
    long_summary = (
        "Build a tool that helps a small team track shared work. "
        "The tool shows what changed, keeps a short history and sends one daily summary. "
        "It is meant for people who plan their week together and lose time asking for updates. "
        "A working demo needs a simple list, a detail view and a way to mark work as done. "
        "Store changes so the team can see who edited what and when. "
        "Add a filter for open and finished items so the list stays useful as it grows."
    )
    problem = Problem(
        title="Shared work tracker",
        summary=long_summary,
        who_affected="Small teams",
        why_matters="Updates get lost",
        field="web-dev",
        domain="other",
        difficulty="beginner",
        est_hours=20,
        tech_tags=["typescript"],
        datasets=[],
        approaches=[],
        source_name="MANABI Curated",
        source_id="test-card-summary",
        original_text="Shared work tracker.",
        created_by=None,
    )
    db_session.add(problem)
    db_session.commit()

    item = next(
        it
        for it in client.get("/api/problems").json()["items"]
        if it["id"] == problem.id
    )
    card = item["summary"]
    assert len(card) < len(long_summary)
    assert card.endswith(".")
    assert long_summary.startswith(card)
    assert "\n" not in card

    detail = client.get(f"/api/problems/{problem.id}").json()
    assert detail["summary"] == long_summary


def test_q_search_title_summary_and_source_id(client, seed):
    assert {it["id"] for it in client.get("/api/problems", params={"q": "onion"}).json()["items"]} == {seed["new"].id}
    assert {it["id"] for it in client.get("/api/problems", params={"q": "flood"}).json()["items"]} == {seed["old"].id}
    assert {it["id"] for it in client.get("/api/problems", params={"q": "sih26001"}).json()["items"]} == {seed["old"].id}
    assert client.get("/api/problems", params={"q": "zzz-no-match"}).json()["total"] == 0


def test_q_search_matches_tech_tags(client, seed):
    res = client.get("/api/problems", params={"q": "real-time"})
    assert {it["id"] for it in res.json()["items"]} == {seed["pop"].id}


def test_single_value_filters(client, seed):
    res = client.get("/api/problems", params={"field": "aiml"})
    assert res.json()["total"] == 2
    res = client.get("/api/problems", params={"domain": "agriculture"})
    assert {it["id"] for it in res.json()["items"]} == {seed["new"].id}
    res = client.get("/api/problems", params={"difficulty": "beginner"})
    assert {it["id"] for it in res.json()["items"]} == {seed["new"].id}
    res = client.get("/api/problems", params={"field": "nonexistent-field"})
    assert res.status_code == 422


def test_tech_filter_repeatable_is_and(client, seed):
    res = client.get("/api/problems", params={"tech": ["python", "vision"]})
    assert {it["id"] for it in res.json()["items"]} == {seed["new"].id}
    res = client.get("/api/problems", params={"tech": ["panda"]})
    assert res.json()["total"] == 0


def test_source_filter_matches_name_or_id(client, seed):
    res = client.get("/api/problems", params={"source": "TCOE PS12"})
    assert {it["id"] for it in res.json()["items"]} == {seed["new"].id}
    res = client.get("/api/problems", params={"source": "smart india hackathon 2026"})
    assert res.json()["total"] == 1


def test_sort_popular_and_newest(client, seed):
    res = client.get("/api/problems", params={"sort": "popular"})
    items = res.json()["items"]
    assert items[0]["id"] == seed["pop"].id
    res = client.get("/api/problems", params={"sort": "newest"})
    items = res.json()["items"]
    assert items[-1]["id"] == seed["old"].id


def test_sort_discover_submitted_first_then_seeded_shuffle(client, seed):
    first = client.get("/api/problems", params={"sort": "discover", "seed": 7}).json()["items"]
    assert first[0]["id"] == seed["pop"].id

    again = client.get("/api/problems", params={"sort": "discover", "seed": 7}).json()["items"]
    assert [it["id"] for it in again] == [it["id"] for it in first]

    orders = {
        tuple(it["id"] for it in client.get(
            "/api/problems", params={"sort": "discover", "seed": value}
        ).json()["items"])
        for value in range(1, 10)
    }
    assert len(orders) > 1
    assert all(order[0] == seed["pop"].id for order in orders)


def test_distinct_keeps_one_brief_per_field_or_domain(client, seed):
    res = client.get("/api/problems", params={"sort": "popular", "distinct": "field"})
    data = res.json()
    assert data["total"] == 2
    assert [item["field"] for item in data["items"]] == ["aiml", "web-dev"]
    assert data["items"][0]["id"] == seed["pop"].id

    domains = client.get("/api/problems", params={"distinct": "domain"}).json()
    assert domains["total"] == 3
    assert len({item["domain"] for item in domains["items"]}) == 3


def test_pagination(client, seed):
    res = client.get("/api/problems", params={"limit": 2, "offset": 0})
    data = res.json()
    assert data["total"] == 3 and len(data["items"]) == 2
    res = client.get("/api/problems", params={"limit": 2, "offset": 2})
    data = res.json()
    assert data["total"] == 3 and len(data["items"]) == 1
    res = client.get("/api/problems", params={"limit": 0})
    assert res.status_code == 422


def test_facets_counts(client, seed):
    res = client.get("/api/problems/facets")
    assert res.status_code == 200
    data = res.json()
    fields = {f["value"]: f["count"] for f in data["fields"]}
    assert fields == {"aiml": 2, "web-dev": 1}
    domains = {f["value"]: f["count"] for f in data["domains"]}
    assert domains["agriculture"] == 1 and domains["healthcare"] == 1 and domains["disaster-management"] == 1
    difficulties = {f["value"]: f["count"] for f in data["difficulties"]}
    assert difficulties == {"beginner": 1, "intermediate": 1, "advanced": 1}
    tech = {f["value"]: f["count"] for f in data["tech_tags"]}
    assert tech["python"] == 3 and tech["pandas"] == 1 and tech["vision"] == 1
    sources = {f["value"]: f["count"] for f in data["sources"]}
    assert sources == {"Smart India Hackathon 2026": 1, "TCOE": 2}


def test_facets_difficulty_counts_follow_field_and_goal(client, seed, db_session):
    seed["old"].goal = "learning"
    seed["new"].goal = "learning"
    seed["pop"].goal = "resume"
    db_session.commit()

    data = client.get(
        "/api/problems/facets", params={"field": "aiml", "goal": "learning"}
    ).json()
    difficulties = {f["value"]: f["count"] for f in data["difficulties"]}
    assert difficulties == {"intermediate": 1}
    listed = client.get(
        "/api/problems",
        params={"field": "aiml", "goal": "learning", "limit": 100},
    ).json()
    assert sum(difficulties.values()) == listed["total"]

    data = client.get("/api/problems/facets", params={"field": "aiml"}).json()
    difficulties = {f["value"]: f["count"] for f in data["difficulties"]}
    assert difficulties == {"intermediate": 1, "advanced": 1}

    data = client.get("/api/problems/facets", params={"goal": "learning"}).json()
    difficulties = {f["value"]: f["count"] for f in data["difficulties"]}
    assert difficulties == {"beginner": 1, "intermediate": 1}


def test_detail_contains_original_text_projects_owner(client, seed):
    res = client.get(f"/api/problems/{seed['pop'].id}")
    assert res.status_code == 200
    data = res.json()
    assert data["original_text"] == "Ambulance triage board verbatim statement."
    assert data["project_count"] == 1
    assert len(data["projects"]) == 1
    project = data["projects"][0]
    assert project["repo_url"] == "https://github.com/octocat/triage"
    assert project["owner"] == {"username": "octocat", "avatar_url": "http://a/1.png"}
    assert project["problem_title"] == "Ambulance triage board"
    assert project["progress"] is None


def test_detail_degrades_invalid_json_sections(db_session, client):
    """Hand-edited/curated JSON must hide its section, not 500 the detail."""
    problem = Problem(
        title="Broken JSON brief",
        summary="Summary",
        who_affected="People",
        why_matters="Matters",
        field="aiml",
        domain="healthcare",
        difficulty="beginner",
        est_hours=5,
        tech_tags=["python"],
        datasets=[],
        approaches=[],
        source_name="Source",
        source_id="BROKEN-JSON",
        original_text="verbatim",
        build_guide=[{"title": 5}],
        team_plan={"roles": "not-a-list"},
        pitch_guide={"beats": "not-a-list"},
        resume_kit={"scope_levels": "not-a-list"},
    )
    db_session.add(problem)
    db_session.commit()

    res = client.get(f"/api/problems/{problem.id}")

    assert res.status_code == 200
    data = res.json()
    assert data["build_guide"] is None
    assert data["team_plan"] is None
    assert data["pitch_guide"] is None
    assert data["resume_kit"] is None


def test_detail_404(client, db_session):
    res = client.get("/api/problems/9999")
    assert res.status_code == 404
    assert res.json() == {"detail": "Problem not found"}


def test_stats_counts(client, seed):
    res = client.get("/api/stats")
    assert res.status_code == 200
    data = res.json()
    assert data["problems"] == 3
    assert data["sources"] == 2
    assert data["fields"] == 2
    assert data["projects"] == 1
