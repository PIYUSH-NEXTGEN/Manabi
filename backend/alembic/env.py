import logging
import sys
from logging.config import fileConfig
from pathlib import Path

from alembic import context

BACKEND_DIR = Path(__file__).resolve().parents[1]
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from app.db import normalized_database_url  # noqa: E402
from app.models import Base  # noqa: E402

# Alembic Config object; alembic.ini values are available here.
config = context.config

# The app calls upgrade_to_head() during startup, after configure_logging()
# installed the single JSON/text handler. fileConfig would replace that handler
# and disable every existing logger (it defaults to disable_existing_loggers),
# silently dropping application logs for the rest of the process. Only adopt
# alembic.ini's console config when nothing else configured logging (CLI use).
if config.config_file_name is not None and not logging.getLogger().handlers:
    fileConfig(config.config_file_name, disable_existing_loggers=False)

target_metadata = Base.metadata


def _database_url() -> str:
    url = config.get_main_option("sqlalchemy.url")
    if not url:
        from app.config import get_settings

        url = get_settings().DATABASE_URL
    return normalized_database_url(url)


def run_migrations_offline() -> None:
    context.configure(
        url=_database_url(),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    from sqlalchemy import create_engine

    connectable = create_engine(_database_url())
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()
    connectable.dispose()


if not context.is_offline_mode():
    run_migrations_online()
else:
    run_migrations_offline()
