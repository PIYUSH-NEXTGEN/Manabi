"""Programmatic Alembic entry points: app startup (production) and CLI --help parity.

Production startup must not silently diverge from migrations (§6.1): on Postgres
the app runs `upgrade head` itself; SQLite dev keeps create_all convenience.
"""

from pathlib import Path

from alembic import command
from alembic.config import Config

from app.config import get_settings
from app.db import normalized_database_url

BACKEND_DIR = Path(__file__).resolve().parents[1]


def alembic_config(database_url: str | None = None) -> Config:
    cfg = Config(str(BACKEND_DIR / "alembic.ini"))
    cfg.set_main_option("script_location", str(BACKEND_DIR / "alembic"))
    url = normalized_database_url(database_url or get_settings().DATABASE_URL)
    cfg.set_main_option("sqlalchemy.url", url)
    return cfg


def upgrade_to_head(database_url: str | None = None) -> None:
    command.upgrade(alembic_config(database_url), "head")
