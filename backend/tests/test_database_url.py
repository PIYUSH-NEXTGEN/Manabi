import pytest
from sqlalchemy.engine import make_url

from app.db import normalized_database_url
from app.migrations import alembic_config


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


def test_percent_encoded_password_keeps_host_and_user_intact():
    # An encoded @ must stay part of the password, not become a URL delimiter.
    raw = (
        "postgresql://postgres.abcdefghijklmnop:p%40ss%23word"
        "@aws-0-us-west-1.pooler.supabase.com:5432/postgres?sslmode=require"
    )
    normalized = normalized_database_url(raw)
    parsed = make_url(normalized)
    assert parsed.username == "postgres.abcdefghijklmnop"
    assert parsed.password == "p@ss#word"
    assert parsed.host == "aws-0-us-west-1.pooler.supabase.com"
    assert parsed.port == 5432
    assert parsed.query["sslmode"] == "require"


def test_percent_encoded_url_survives_alembic_config():
    raw = (
        "postgresql://postgres.abcdefghijklmnop:p%40ss"
        "@aws-0-us-west-1.pooler.supabase.com:5432/postgres"
    )
    cfg = alembic_config(raw)
    assert cfg.get_main_option("sqlalchemy.url") == normalized_database_url(raw)


def test_explicit_postgres_driver_is_preserved():
    raw = "postgresql+psycopg2://user:pass@db.example/manabi"
    assert normalized_database_url(raw) == raw


def test_sqlite_url_is_unchanged():
    raw = "sqlite:///./app.db"
    assert normalized_database_url(raw) == raw
