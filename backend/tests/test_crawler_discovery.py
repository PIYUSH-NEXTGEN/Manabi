from pathlib import Path

from app.crawler.discovery.sih import parse_sih_html, parse_sih_xlsx
from app.crawler.split import split_multiproblem_text

FIXTURES = Path(__file__).parent / "fixtures" / "crawler" / "sih"


def test_parse_sih_2026_html_real_fixture():
    page = (FIXTURES / "sih2026PS.html").read_text(encoding="utf-8")
    items = parse_sih_html(page, "https://sih.gov.in/sih2026PS", year=2026)
    assert len(items) == 265
    assert len({item.source_id for item in items}) == 265
    software = [item for item in items if (item.category or "").lower() == "software"]
    hardware = [item for item in items if (item.category or "").lower() == "hardware"]
    assert len(software) == 196
    assert len(hardware) == 69

    first = next(item for item in items if item.source_id == "SIH26001")
    assert first.title
    assert first.organisation
    assert first.description and "landslide" in first.description.lower()
    assert first.theme and first.department
    assert first.year == 2026
    assert first.url.endswith("#SIH26001")
    assert all(item.source_id and item.source_id.startswith("SIH26") for item in items)


def test_parse_sih_2024_xlsx_real_fixture():
    content = (FIXTURES / "SIH_PS_2024.xlsx").read_bytes()
    items = parse_sih_xlsx(content, "https://sih.gov.in/letters/SIH_PS_2024.xlsx", year=2024)
    assert len(items) == 246
    software = [item for item in items if (item.category or "").lower() == "software"]
    assert len(software) == 178
    first = items[0]
    assert first.source_id == "SIH1524"
    assert first.organisation == "Godrej Appliances"
    assert first.theme == "Smart Resource Conservation"
    assert first.year == 2024


def test_split_multiproblem_text_uses_ids():
    text = "intro SIH26001 first problem body SIH26002 second problem body"
    chunks = split_multiproblem_text(text, r"SIH\d{5}")
    assert len(chunks) == 2
    assert chunks[0].startswith("SIH26001")
    assert chunks[1].startswith("SIH26002")


def test_split_without_ids_returns_single_document():
    assert split_multiproblem_text("one problem only", r"SIH\d{5}") == ["one problem only"]
