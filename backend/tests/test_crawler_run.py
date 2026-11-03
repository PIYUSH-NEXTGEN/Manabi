import json
from pathlib import Path

import httpx
import pytest
from sqlalchemy import create_engine, func, select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app import config
from app.crawler.run import run_source
from app.db import Base
from app.models import CrawlItem, CrawlRun, Problem

FIXTURES = Path(__file__).parent / "fixtures" / "crawler" / "sih"
XLSX_URL = "https://sih.gov.in/letters/SIH_PS_2024.xlsx"


@pytest.fixture(autouse=True)
def crawler_env(monkeypatch):
    monkeypatch.setenv("CRAWLER_ENABLED", "true")
    monkeypatch.setenv("CRAWLER_CONTACT", "owner@example.com")
    monkeypatch.setenv("LLM_PROVIDER", "mock")
    monkeypatch.setenv("CRAWLER_MAX_LLM_CALLS", "10")
    config.get_settings.cache_clear()
    yield
    config.get_settings.cache_clear()


@pytest.fixture
def db():
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    Base.metadata.create_all(engine)
    session = sessionmaker(bind=engine)()
    yield session
    session.close()


def _client(xlsx: bytes) -> httpx.AsyncClient:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/robots.txt":
            return httpx.Response(404)
        if str(request.url) == XLSX_URL:
            return httpx.Response(
                200,
                content=xlsx,
                headers={"content-type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"},
            )
        return httpx.Response(404)

    return httpx.AsyncClient(transport=httpx.MockTransport(handler), follow_redirects=False)


async def _public_resolver(host: str) -> list[str]:
    return ["93.184.216.34"]


def _fake_llm(system, messages):
    user = messages[0]["content"]
    source = user.split("<<<SOURCE MATERIAL>>>", 1)[1].split("<<<END SOURCE MATERIAL>>>", 1)[0]
    quote = " ".join(source.split()[:8])
    return json.dumps(
        {
            "is_problem": True,
            "title": "Crawled flood dashboard",
            "summary": "A dashboard for flood response teams.",
            "who_affected": "District teams",
            "why_matters": "Faster warnings matter.",
            "field": "geospatial",
            "domain": "disaster-management",
            "difficulty": "intermediate",
            "est_hours": 30,
            "tech_tags": ["python"],
            "datasets": [],
            "approaches": ["Blend gauges"],
            "evidence": {"title": quote},
            "inferred_fields": [],
        }
    )


async def _run(db, xlsx, *, limit=6, **kwargs):
    client = _client(xlsx)
    try:
        return await run_source(
            "sih",
            db=db,
            limit=limit,
            today=__import__("datetime").date(2026, 11, 3),
            client=client,
            resolve=_public_resolver,
            sleep=lambda seconds: __import__("asyncio").sleep(0),
            call=_fake_llm,
            **kwargs,
        )
    finally:
        await client.aclose()


async def test_full_run_is_idempotent_and_skips_hardware(db):
    content = (FIXTURES / "SIH_PS_2024.xlsx").read_bytes()
    first = await _run(db, content)
    problems = db.scalars(select(Problem)).all()
    assert problems
    assert all(p.origin == "crawler" for p in problems)
    assert all((p.source_name or "").endswith("2024") for p in problems)
    assert first.counts["skipped_out_of_scope"] >= 1
    assert first.counts["new"] >= 1
    assert db.scalar(select(func.count(CrawlRun.id))) == 1
    assert db.scalar(select(func.count(CrawlItem.id))) >= 1

    second = await _run(db, content)
    assert second.counts["unchanged"] >= 1
    assert second.counts["new"] == 0
    assert second.llm_calls == 0
    assert db.scalar(select(func.count(Problem.id))) == len(problems)


async def test_budget_defers_remaining_items(db, monkeypatch):
    monkeypatch.setenv("CRAWLER_MAX_LLM_CALLS", "1")
    config.get_settings.cache_clear()
    content = (FIXTURES / "SIH_PS_2024.xlsx").read_bytes()
    report = await _run(db, content, limit=30)
    assert report.llm_calls == 1
    assert report.counts["deferred"] >= 1


async def test_kill_switch_stops_everything(db, monkeypatch):
    monkeypatch.setenv("CRAWLER_ENABLED", "false")
    config.get_settings.cache_clear()
    report = await run_source("sih", db=db)
    assert report.counts["skipped_compliance"] == 1
    assert db.scalar(select(func.count(Problem.id))) == 0


async def test_missing_contact_fails_closed(db, monkeypatch):
    monkeypatch.setenv("CRAWLER_CONTACT", "")
    config.get_settings.cache_clear()
    report = await run_source("sih", db=db, client=_client(b""), resolve=_public_resolver)
    assert report.counts["failed"] == 1
    assert "CRAWLER_CONTACT" in (report.errors[0] if report.errors else "")


def test_report_markdown_contains_all_counters():
    from app.crawler.report import CrawlReport

    markdown = CrawlReport(source_key="sih").to_markdown()
    assert "`sih`" in markdown
    assert "skipped_robots" in markdown
    assert "published" in markdown
