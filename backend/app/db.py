from collections.abc import Generator
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine, make_url
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.config import get_settings


class Base(DeclarativeBase):
    pass


_engine = None
_SessionLocal = None


def normalized_database_url(raw: str) -> str:
    """Accept libpq-style 'postgres://' URLs (Neon/Supabase/shears copy-paste) — SQLAlchemy 2 rejects that scheme."""
    url = make_url(raw)
    if url.drivername == "postgres":
        return raw.replace("postgres://", "postgresql://", 1)
    return raw


def get_engine() -> Engine:
    global _engine
    if _engine is None:
        database_url = normalized_database_url(get_settings().DATABASE_URL)
        _engine = create_engine(
            database_url,
            connect_args={"check_same_thread": False}
            if database_url.startswith("sqlite")
            else {},
            pool_pre_ping=not database_url.startswith("sqlite"),
            pool_recycle=280 if not database_url.startswith("sqlite") else 0,
        )
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
