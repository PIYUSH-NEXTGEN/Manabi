import pytest

from app.db import normalized_database_url


@pytest.mark.parametrize(
    "raw",
    [
        "postgres://user:pass@db.example/manabi",
        "postgresql://user:pass@db.example/manabi",
    ],
)
def test_plain_postgres_urls_select_the_installed_driver(raw):
    normalized = normalized_database_url(raw)
    assert normalized == "postgresql+psycopg2://user:pass@db.example/manabi"


def test_explicit_postgres_driver_is_preserved():
    raw = "postgresql+psycopg2://user:pass@db.example/manabi"
    assert normalized_database_url(raw) == raw


def test_sqlite_url_is_unchanged():
    raw = "sqlite:///./app.db"
    assert normalized_database_url(raw) == raw
