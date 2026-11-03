from datetime import date

import pytest
import yaml

from app.crawler.compliance import ComplianceError, assert_compliant, compliance_error
from app.crawler.registry import load_source, load_sources


def test_loads_sih_registry():
    source = load_source("sih")
    assert source.key == "sih"
    assert source.compliance.verdict == "allowed"
    assert source.display_policy == "summary_only"
    assert source.politeness.min_delay_seconds >= 3
    assert source.discovery.urls[0].startswith("https://sih.gov.in/")


def test_load_sources_includes_sih():
    assert "sih" in load_sources()


def test_unknown_source_raises():
    with pytest.raises(FileNotFoundError):
        load_source("missing-source")


def test_key_must_match_filename(tmp_path):
    payload = {
        "key": "other",
        "name": "Other",
        "base_url": "https://example.com",
        "compliance": {"verdict": "allowed", "checked_on": "2026-11-03", "record": "docs/sources/other.md"},
        "discovery": {"method": "static_list", "urls": []},
    }
    (tmp_path / "other-source.yaml").write_text(yaml.safe_dump(payload), encoding="utf-8")
    with pytest.raises(ValueError, match="must match the filename"):
        load_sources(tmp_path)


def test_compliance_allows_recent_allowed_record():
    assert compliance_error(load_source("sih"), today=date(2026, 11, 3)) is None
    assert_compliant(load_source("sih"), today=date(2026, 11, 3))


def test_compliance_rejects_stale_record():
    source = load_source("sih")
    message = compliance_error(source, today=date(2027, 5, 4))
    assert message is not None
    assert "180" in message
    with pytest.raises(ComplianceError):
        assert_compliant(source, today=date(2027, 5, 4))


def test_compliance_rejects_non_permissive_verdict(tmp_path):
    (tmp_path / "manual.yaml").write_text(
        yaml.safe_dump(
            {
                "key": "manual",
                "name": "Manual",
                "base_url": "https://example.com",
                "compliance": {"verdict": "manual_only", "checked_on": "2026-11-03", "record": "docs/sources/manual.md"},
                "discovery": {"method": "static_list", "urls": []},
            }
        ),
        encoding="utf-8",
    )
    source = load_sources(tmp_path)["manual"]
    message = compliance_error(source, today=date(2026, 11, 3))
    assert message is not None and "manual_only" in message
