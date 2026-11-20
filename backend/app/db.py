from collections.abc import Generator
from contextlib import contextmanager
from urllib.parse import unquote

from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine, make_url
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.config import get_settings


class Base(DeclarativeBase):
    pass


_engine = None
_SessionLocal = None


def normalized_database_url(raw: str) -> str:
    """Normalize provider URLs to the Postgres driver this project installs.

    SQLAlchemy 2.1 resolves plain ``postgresql://`` to psycopg 3, while the
    runtime pins psycopg2-binary. Selecting the driver explicitly keeps
    Neon/Supabase/Render connection strings working without adding a second
    database driver or changing the deployment contract.
    """
    # URL-decode first so that %0A, %2F, etc. are resolved before Alembic's
    # configparser tries to interpret % as interpolation syntax.
    raw = unquote(raw)
    url = make_url(raw)
    if url.drivername in {"postgres", "postgresql"}:
        return url.set(drivername="postgresql+psycopg2").render_as_string(
            hide_password=False
        )
    return raw


def _enable_sqlite_foreign_keys(engine: Engine) -> None:
    """SQLite ignores declared foreign keys unless this pragma is enabled.

    Postgres enforces them by default; local/dev SQLite should not silently
    accept orphaned rows or skip the CASCADE on project_reports/project_stars.
    """

    @event.listens_for(engine, "connect")
    def _set_sqlite_pragma(dbapi_connection, _connection_record):
        cursor = dbapi_connection.cursor()
        try:
            cursor.execute("PRAGMA foreign_keys=ON")
        finally:
            cursor.close()


def get_engine() -> Engine:
    global _engine
    if _engine is None:
        database_url = normalized_database_url(get_settings().DATABASE_URL)
        is_sqlite = database_url.startswith("sqlite")
        _engine = create_engine(
            database_url,
            # Bound connection establishment and checkout waits. Without these
            # a dead Postgres endpoint or exhausted pool can hold a worker
            # indefinitely. SQLite local connections do not need them.
            connect_args={"check_same_thread": False}
            if is_sqlite
            else {
                "connect_timeout": 10,
                # A pathological query must not hold an app worker forever.
                # Migrations use their own engine, so schema upgrades are not
                # subject to this per-request statement limit.
                "options": "-c statement_timeout=60000",
            },
            pool_pre_ping=not is_sqlite,
            pool_recycle=280 if not is_sqlite else 0,
            pool_size=5,
            max_overflow=5 if not is_sqlite else 10,
            pool_timeout=10,
        )
        if database_url.startswith("sqlite"):
            _enable_sqlite_foreign_keys(_engine)
    return _engine


def get_session_factory() -> sessionmaker[Session]:
    global _SessionLocal
    if _SessionLocal is None:
        _SessionLocal = sessionmaker(bind=get_engine(), autoflush=False, autocommit=False)
    return _SessionLocal


def get_db() -> Generator[Session, None, None]:
    db = get_session_factory()()
    try:
        yield db
    finally:
        db.close()


@contextmanager
def session_scope() -> Generator[Session, None, None]:
    """Commit on success, rollback on error. For CLI scripts."""
    db = get_session_factory()()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()