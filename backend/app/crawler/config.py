"""Crawler-only settings derived from the shared app config (§7)."""

from dataclasses import dataclass
from pathlib import Path

from app.config import get_settings

CRAWLER_DIR = Path(__file__).resolve().parent
SOURCES_DIR = CRAWLER_DIR / "sources"
COMPLIANCE_MAX_AGE_DAYS = 180


@dataclass(frozen=True)
class CrawlLimits:
    max_requests: int
    max_llm_calls: int


def enabled() -> bool:
    return get_settings().CRAWLER_ENABLED


def require_postgres() -> bool:
    return get_settings().CRAWLER_REQUIRE_POSTGRES


def limits() -> CrawlLimits:
    settings = get_settings()
    return CrawlLimits(
        max_requests=max(1, settings.CRAWLER_MAX_REQUESTS_PER_RUN),
        max_llm_calls=max(0, settings.CRAWLER_MAX_LLM_CALLS),
    )


def user_agent() -> str:
    """Identify the bot and a way to contact its owner (§3.3)."""
    settings = get_settings()
    contact = settings.CRAWLER_CONTACT.strip()
    if not contact:
        raise RuntimeError("CRAWLER_CONTACT is required before crawling")
    return f"ManabiBot/1.0 (+{settings.SITE_URL}/about; contact: {contact})"


def admin_usernames() -> set[str]:
    raw = get_settings().ADMIN_GITHUB_USERNAMES
    return {name.strip().lower() for name in raw.split(",") if name.strip()}
