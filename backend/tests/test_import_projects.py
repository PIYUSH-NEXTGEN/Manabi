from pathlib import Path

import pytest
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from app.db import Base
from app.models import Problem
from app.seed.import_projects import entry_to_problem, import_entries
from app.seed.parser import parse_blocks

FIXTURE = Path(__file__).parent / "fixtures" / "projects_fixture.txt"


def fresh_session() -> Session:
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    Base.metadata.create_all(engine)
    return Session(engine)


@pytest.fixture
def fixture_text() -> str:
    return FIXTURE.read_text(encoding="utf-8")


def test_fixture_exists_and_is_small():
    assert FIXTURE.exists() and FIXTURE.stat().st_size < 2000


def test_parses_all_entries_skipping_headers(fixture_text):
    entries = parse_blocks(fixture_text)
    assert len(entries) == 5
    ids = [e.source_id for e in entries]
    assert ids == ["SIH26017", "SIH26153", "TCOE PS12", "SIH26032", "TCOE PS14"]
    titles = [e.title for e in entries]
    assert "Cybersecurity" not in titles
    assert [e.organisation for e in entries] == [
        "Ministry of Rural Development", "NTRO", "Consumer Affairs", "Consumer Affairs", "",
    ]


def test_consecutive_entries_without_blank_lines_all_parse():
    text = (
        "projects 2\n\n"
        "Entry One (ML · Governance). SIH26017, Ministry of Rural Development. Body one.\n"
        "Entry Two (IoT · Industry 4.0). TCOE PS17, Ministry of Heavy Industries. Body two.\n"
    )
    entries = parse_blocks(text)
    assert [e.title for e in entries] == ["Entry One", "Entry Two"]
    assert [e.source_id for e in entries] == ["SIH26017", "TCOE PS17"]


def test_source_name_from_prefix_and_never_fabricated(fixture_text):
    entries = parse_blocks(fixture_text)
    by_id = {e.source_id: e for e in entries}
    assert by_id["SIH26017"].source_name == "Smart India Hackathon 2026"
    assert by_id["TCOE PS12"].source_name == "TCOE"


def test_original_text_is_verbatim(fixture_text):
    entries = parse_blocks(fixture_text)
    for entry in entries:
        assert entry.original_text.replace("\n", " ") == entry.original_text
        assert entry.title in entry.original_text
        assert entry.source_id in entry.original_text
    first = entries[0]
    assert first.original_text == (
        "Predicting Land Acquisition Delays Before They Happen "
        "(ML, tabular + explainable AI \u00b7 Governance). SIH26017, Ministry of Rural Development. "
        "Infrastructure projects stall on approvals, legal disputes, and late compensation, and nobody "
        "flags them early. Build a model that gives each project a delay-risk score per stage."
    )


def test_field_mapping_and_domain(fixture_text):
    entries = {e.source_id: e for e in parse_blocks(fixture_text)}
    assert entries["SIH26017"].field == "ml"
    assert entries["SIH26017"].domain == "governance"
    assert entries["SIH26153"].field == "cybersecurity"
    assert entries["TCOE PS12"].field == "computer-vision"
    assert entries["TCOE PS12"].domain == "agriculture"
    assert entries["SIH26032"].field == "web-fullstack"
    assert entries["SIH26032"].domain == "agriculture"


def test_tech_tags_lowercase(fixture_text):
    entries = {e.source_id: e for e in parse_blocks(fixture_text)}
    tags = entries["SIH26017"].tech_tags
    assert tags == sorted(set(tags)) and tags == sorted(tags)
    assert all(t == t.lower() for t in tags)
    assert "ml" in tags


def test_datasets_only_named_in_text_with_null_urls(fixture_text):
    entries = {e.source_id: e for e in parse_blocks(fixture_text)}
    assert entries["SIH26153"].datasets == [
        {"name": "CIC-IDS", "url": None},
        {"name": "UNSW-NB15", "url": None},
        {"name": "CTU-13", "url": None},
    ]
    for sid in ("SIH26017", "TCOE PS12", "SIH26032"):
        assert entries[sid].datasets == []
        assert "datasets" in entries[sid].ai_fields


def test_no_urls_invented_and_url_flagged_missing(fixture_text):
    entries = parse_blocks(fixture_text)
    for entry in entries:
        assert "http" not in entry.original_text
    session = fresh_session()
    result = import_entries(session, fixture_text)
    assert set(result["missing_urls"]) == {e.title for e in entries}
    assert result["missing_ids"] == []
    assert result["unparsed_ids"] == []
    session.close()


def test_difficulty_rule_and_est_hours(fixture_text):
    entries = {e.source_id: e for e in parse_blocks(fixture_text)}
    assert entries["SIH26032"].difficulty == "beginner"
    assert entries["SIH26017"].difficulty == "intermediate"
    assert all(e.est_hours == 40 for e in entries.values())
    assert all("est_hours" in e.ai_fields for e in entries.values())


def test_importer_inserts_rows(fixture_text):
    session = fresh_session()
    result = import_entries(session, fixture_text)
    assert result["parsed"] == 5 and result["inserted"] == 5 and result["skipped"] == 0
    rows = list(session.scalars(select(Problem)))
    assert len(rows) == 5
    first = session.scalar(select(Problem).where(Problem.source_id == "SIH26017"))
    assert first.title == "Predicting Land Acquisition Delays Before They Happen"
    assert first.who_affected == "Ministry of Rural Development"
    assert first.source_name == "Smart India Hackathon 2026"
    no_org = session.scalar(select(Problem).where(Problem.source_id == "TCOE PS14"))
    assert no_org.who_affected == "Not stated in source"
    assert "who_affected" in no_org.ai_fields
    session.close()


def test_importer_idempotent_on_rerun(fixture_text):
    session = fresh_session()
    first = import_entries(session, fixture_text)
    second = import_entries(session, fixture_text)
    assert (first["inserted"], first["skipped"]) == (5, 0)
    assert (second["inserted"], second["skipped"]) == (0, 5)
    assert len(list(session.scalars(select(Problem)))) == 5
    session.close()


def test_nothing_invented_for_missing_values(fixture_text):
    session = fresh_session()
    import_entries(session, fixture_text)
    rows = list(session.scalars(select(Problem)))
    for row in rows:
        assert row.source_url is None
        assert row.source_note is None
        assert row.approaches == []
        assert row.created_by is None
    session.close()


def test_entry_to_problem_maps_all_columns(fixture_text):
    entry = parse_blocks(fixture_text)[0]
    problem = entry_to_problem(entry)
    assert problem.summary == entry.body
    assert problem.tech_tags == entry.tech_tags
    assert problem.datasets == entry.datasets
    assert problem.ai_fields == entry.ai_fields
    assert problem.original_text == entry.original_text


def test_rwml_real_world_entries_parse():
    from app.seed.parser import parse_blocks

    lines = (
        "projects 33\n\n"
        "Real-world ML additions\n\n"
        "Wheat Leaf Disease Grading from a Smartphone Photo (Computer vision · Agriculture). RWML01, "
        "ICAR research network. Detect rust severity per leaf for extension officers. "
        "Datasets (PlantVillage, Global Wheat Rust monitoring open sets).\n\n"
        "Fraud Detection for Real-Time Digital Payments (ML · Fintech). RWML08, Unified banks. "
        "Score each payment under the authorisation budget across merchant categories. "
        "Datasets (IEEE-CIS Fraud Detection, PaySim simulated payments).\n"
    )
    entries = parse_blocks(lines)
    assert len(entries) == 2
    wheat, fraud = entries
    assert wheat.source_id == "RWML01" and wheat.source_name == "Real-World ML"
    assert wheat.field == "computer-vision" and wheat.domain == "agriculture"
    assert wheat.tech_tags == ["computer-vision"]
    assert wheat.datasets == [{"name": "PlantVillage", "url": None}, {"name": "Global Wheat Rust monitoring open sets", "url": None}]
    assert fraud.field == "ml" and fraud.domain == "fintech"  # new parser domain mapping
    assert "sih" not in fraud.source_id
