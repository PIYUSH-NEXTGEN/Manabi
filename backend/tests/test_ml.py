import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app import config
from app.db import Base, get_db
from app.deps import get_current_user, get_optional_user
from app.main import app
from app.models import MLAttempt, MLQuestion, User
from app.services.ratelimit import ML_ATTEMPT_LIMITER

GOOD_ANSWER = (
    "First, I would suspect leakage from post-decision features like days_since_final_push_notification, "
    "because they are computed after the churn decision encodes the outcome. Second, train-serving skew: "
    "online features may be computed differently or filled with defaults on timeout. I would confirm both by "
    "comparing offline and online feature distributions and by shadow scoring. The Monday morning traffic drop "
    "also changes the input distribution, so I would correlate degradation with that window. Retraining needs a "
    "time-based split so validation looks like the future."
)


@pytest.fixture(autouse=True)
def env(monkeypatch):
    get_settings = config.get_settings
    monkeypatch.setenv("LLM_PROVIDER", "mock")
    get_settings.cache_clear()
    yield
    get_settings.cache_clear()


@pytest.fixture
def db_session():
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    Base.metadata.create_all(engine)
    factory = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    session = factory()
    app.dependency_overrides[get_db] = lambda: session
    session.add(
        MLQuestion(
            title="Train-serving skew question",
            scenario="A model degrades weekly.",
            difficulty="intermediate",
            topic="train-serving-skew",
            rubric_json=[{"id": "r1", "point": "Leakage point"}, {"id": "r2", "point": "Skew point"}],
            explanation="Expert explanation of the failure modes.",
        )
    )
    session.commit()
    yield session
    app.dependency_overrides.clear()
    session.close()


@pytest.fixture
def user(db_session):
    u = User(github_id=1, username="octocat", name="O", avatar_url=None)
    db_session.add(u)
    db_session.commit()
    app.dependency_overrides[get_current_user] = lambda: u
    app.dependency_overrides[get_optional_user] = lambda: u
    ML_ATTEMPT_LIMITER._hits.clear()
    return u


@pytest.fixture
def anon():
    app.dependency_overrides.pop(get_current_user, None)
    app.dependency_overrides.pop(get_optional_user, None)


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


def qid(db_session) -> int:
    return db_session.query(MLQuestion).first().id


# ---------------- seeder ----------------

def test_seed_ml_questions_idempotent(tmp_path, monkeypatch):
    from app.seed import seed as seed_mod

    engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    Base.metadata.create_all(engine)
    factory = sessionmaker(bind=engine)
    db = factory()
    first = seed_mod.seed(db)
    second = seed_mod.seed(db)
    assert first["inserted"] >= 5 and first["already_present"] == 0
    assert second["inserted"] == 0 and second["already_present"] == first["inserted"]
    assert db.query(MLQuestion).count() == first["inserted"]
    q = db.query(MLQuestion).first()
    assert q.rubric_json and q.rubric_json[0]["id"] == "r1"
    db.close()


# ---------------- listing (rubric never leaks) ----------------

def test_list_questions_anonymous_attempted_false(client, db_session, anon):
    res = client.get("/api/ml/questions")
    assert res.status_code == 200
    data = res.json()
    assert data[0]["attempted"] is False
    assert "rubric" not in data[0] and "explanation" not in data[0] and "scenario" not in data[0]


def test_question_detail_has_scenario_no_rubric(client, db_session, anon):
    res = client.get(f"/api/ml/questions/{qid(db_session)}")
    assert res.status_code == 200
    data = res.json()
    assert data["scenario"] == "A model degrades weekly."
    assert "rubric_json" not in data and "explanation" not in data


def test_question_detail_404(client, db_session, anon):
    assert client.get("/api/ml/questions/9999").status_code == 404


def test_attempted_flag_true_after_attempt(client, db_session, user, monkeypatch):
    monkeypatch.setattr(
        "app.services.llm._provider_raw_json",
        lambda *a, **k: '{"items": [{"id": "r1", "covered": true, "evidence": null}, {"id": "r2", "covered": true, "evidence": null}], "summary": "ok"}',
        raising=False,
    )
    client.post(f"/api/ml/questions/{qid(db_session)}/attempts", json={"answer": GOOD_ANSWER})
    listed = client.get("/api/ml/questions").json()
    assert listed[0]["attempted"] is True
    detail = client.get(f"/api/ml/questions/{qid(db_session)}").json()
    assert detail["attempted"] is True


# ---------------- attempts ----------------

def test_attempt_requires_auth(client, db_session, anon):
    res = client.post(f"/api/ml/questions/{qid(db_session)}/attempts", json={"answer": GOOD_ANSWER})
    assert res.status_code == 401


def test_attempt_answer_length_bounds(client, db_session, user):
    short = client.post(f"/api/ml/questions/{qid(db_session)}/attempts", json={"answer": "too short"})
    assert short.status_code == 422
    long = client.post(f"/api/ml/questions/{qid(db_session)}/attempts", json={"answer": "x" * 4001})
    assert long.status_code == 422


def test_attempt_grading_happy_path(client, db_session, user, monkeypatch):
    monkeypatch.setattr(
        "app.services.llm._provider_raw_json",
        lambda *a, **k: '{"items": [{"id": "r1", "covered": true, "evidence": "post-decision features like days_since_final_push_notification"}, {"id": "r2", "covered": true, "evidence": "online features may be computed differently"}], "summary": "You identified 2 of 2 key factors."}',
        raising=False,
    )
    res = client.post(f"/api/ml/questions/{qid(db_session)}/attempts", json={"answer": GOOD_ANSWER})
    assert res.status_code == 200
    data = res.json()
    assert data["explanation"] == "Expert explanation of the failure modes."  # revealed only now
    fb = data["feedback"]
    assert fb["total"] == 2 and fb["covered_count"] == 2
    assert fb["items"][0]["point"] == "Leakage point"
    assert fb["items"][0]["evidence"].startswith("post-decision")


def test_evidence_not_in_answer_is_nulled(client, db_session, user, monkeypatch):
    """Fabricated or rubric-quoting 'evidence' must not count as covered."""
    monkeypatch.setattr(
        "app.services.llm._provider_raw_json",
        lambda *a, **k: '{"items": [{"id": "r1", "covered": true, "evidence": "a crucial leakage check"}, {"id": "r2", "covered": true, "evidence": "A model degrades weekly."}], "summary": "You identified 2 of 2 key factors."}',
        raising=False,
    )
    res = client.post(f"/api/ml/questions/{qid(db_session)}/attempts", json={"answer": GOOD_ANSWER})
    fb = res.json()["feedback"]
    assert fb["covered_count"] == 0, "fabricated evidence and scenario quotes must not count"
    assert fb["items"][0]["evidence"] is None


def test_mock_grades_uncovered(client, db_session, user):
    res = client.post(f"/api/ml/questions/{qid(db_session)}/attempts", json={"answer": GOOD_ANSWER})
    assert res.status_code == 200
    fb = res.json()["feedback"]
    assert fb["covered_count"] == 0 and fb["total"] == 2  # mock default: nothing covered
    assert fb["items"][0]["evidence"] is None


def test_attempt_saved_and_latest_me(client, db_session, user, monkeypatch):
    monkeypatch.setattr(
        "app.services.llm._provider_raw_json",
        lambda *a, **k: '{"items": [{"id": "r1", "covered": false, "evidence": null}, {"id": "r2", "covered": false, "evidence": null}], "summary": "s"}',
        raising=False,
    )
    post = client.post(f"/api/ml/questions/{qid(db_session)}/attempts", json={"answer": GOOD_ANSWER})
    attempt_id = post.json()["id"]
    me = client.get(f"/api/ml/questions/{qid(db_session)}/attempts/me")
    assert me.status_code == 200 and me.json()["id"] == attempt_id
    assert db_session.query(MLAttempt).count() == 1


def test_latest_me_404_when_none(client, db_session, user):
    assert client.get(f"/api/ml/questions/{qid(db_session)}/attempts/me").status_code == 404


def test_latest_me_404_for_other_question(client, db_session, user, monkeypatch):
    monkeypatch.setattr(
        "app.services.llm._provider_raw_json",
        lambda *a, **k: '{"items": [{"id": "r1", "covered": false, "evidence": null}], "summary": "s"}',
        raising=False,
    )
    client.post(f"/api/ml/questions/{qid(db_session)}/attempts", json={"answer": GOOD_ANSWER})
    assert client.get("/api/ml/questions/9999/attempts/me").status_code == 404


def test_attempt_rate_limited(client, db_session, user, monkeypatch):
    monkeypatch.setattr(
        "app.services.llm._provider_raw_json",
        lambda *a, **k: '{"items": [{"id": "r1", "covered": false, "evidence": null}], "summary": "s"}',
        raising=False,
    )
    codes = []
    for _ in range(int(config.get_settings().AI_RATE_LIMIT_PER_HOUR) + 1):
        res = client.post(f"/api/ml/questions/{qid(db_session)}/attempts", json={"answer": GOOD_ANSWER})
        codes.append(res.status_code)
    assert codes[-1] == 429 and 200 in codes
