from io import BytesIO
from datetime import datetime, timezone

import pytest
from fastapi.testclient import TestClient
from openpyxl import load_workbook
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db import Base, get_db
from app.main import app
from app.models import Problem


@pytest.fixture
def db_session():
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    Base.metadata.create_all(engine)
    session = sessionmaker(bind=engine)()
    app.dependency_overrides[get_db] = lambda: session
    yield session
    app.dependency_overrides.clear()
    session.close()


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


def _problem(db, *, status="published") -> Problem:
    problem = Problem(
        title="Landslide warning system",
        summary="A generated summary for district teams.",
        who_affected="District teams",
        why_matters="Early warnings save lives.",
        field="data-science",
        domain="disaster-management",
        difficulty="intermediate",
        est_hours=40,
        tech_tags=["python", "gis"],
        datasets=[],
        approaches=["Blend sensors"],
        source_name="Smart India Hackathon 2024",
        source_id="SIH26001",
        source_url="https://sih.gov.in/letters/SIH_PS_2024.xlsx",
        original_text="VERBATIM SOURCE TEXT MUST NOT BE EXPORTED",
        status=status,
        source_year=2024,
        organisation="MDoNER",
        created_at=datetime.now(timezone.utc),
    )
    db.add(problem)
    db.commit()
    return problem


def test_export_returns_one_statement_sheet(client, db_session):
    problem = _problem(db_session)
    response = client.get(f"/api/problems/{problem.id}/export.xlsx")
    assert response.status_code == 200
    assert response.headers["content-type"].startswith(
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    assert "MANABI-SIH26001-statement.xlsx" in response.headers["content-disposition"]

    workbook = load_workbook(BytesIO(response.content), read_only=True)
    values = [tuple(cell for cell in row) for row in workbook.active.iter_rows(values_only=True)]
    flat = " | ".join(str(cell) for row in values for cell in row if cell is not None)
    assert ("Statement ID", "SIH26001") in values
    assert ("Organisation", "MDoNER") in values
    assert "A generated summary for district teams." in flat
    assert "VERBATIM SOURCE TEXT MUST NOT BE EXPORTED" not in flat
    assert len(values) < 25  # exactly one problem, not the bulk workbook


def test_export_hides_non_published_problems(client, db_session):
    problem = _problem(db_session, status="pending_review")
    assert client.get(f"/api/problems/{problem.id}/export.xlsx").status_code == 404


def test_export_neutralises_formula_injection(client, db_session):
    """User-controlled text must never become a spreadsheet formula: a victim
    opening the exported sheet otherwise executes e.g. =HYPERLINK(...)"""
    problem = _problem(db_session)
    problem.summary = "=HYPERLINK(\"http://evil.example.com\",\"click\")"
    problem.who_affected = "+1 exploit"
    problem.organisation = "@SUM(1)"
    db_session.commit()

    response = client.get(f"/api/problems/{problem.id}/export.xlsx")
    assert response.status_code == 200
    workbook = load_workbook(BytesIO(response.content), read_only=True)
    cells = [cell for row in workbook.active.iter_rows(values_only=True) for cell in row if cell]
    flat = [str(cell) for cell in cells]
    assert not any(cell.startswith(("=", "+", "@")) for cell in flat)
    assert any(cell.startswith("'=HYPERLINK") for cell in flat)  # literal text, not a formula
    assert any(cell.startswith("'+1 exploit") for cell in flat)
    assert any(cell.startswith("'@SUM(1)") for cell in flat)
