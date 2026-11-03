"""Hard compliance gate (§3.3): verdict/age checks and robots.txt enforcement."""

from __future__ import annotations

from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from datetime import date
from urllib.parse import urlsplit
from urllib.robotparser import RobotFileParser

from app.crawler.config import COMPLIANCE_MAX_AGE_DAYS
from app.crawler.registry import ALLOWED_VERDICTS, Source


class ComplianceError(RuntimeError):
    """Raised when a source must not be crawled."""


def compliance_error(source: Source, today: date | None = None) -> str | None:
    today = today or date.today()
    verdict = source.compliance.verdict
    if verdict not in ALLOWED_VERDICTS:
        return f"source '{source.key}' has compliance verdict '{verdict}' — refusing to crawl"
    age = (today - source.compliance.checked_on).days
    if age < 0:
        return f"source '{source.key}' has a future checked_on date {source.compliance.checked_on}"
    if age > COMPLIANCE_MAX_AGE_DAYS:
        return (
            f"source '{source.key}' compliance record is {age} days old "
            f"(max {COMPLIANCE_MAX_AGE_DAYS}) — re-check and update it"
        )
    if not source.compliance.record:
        return f"source '{source.key}' has no compliance record"
    return None


def assert_compliant(source: Source, today: date | None = None) -> None:
    message = compliance_error(source, today)
    if message is not None:
        raise ComplianceError(message)


@dataclass(frozen=True)
class RobotsDecision:
    allowed: bool
    crawl_delay: float | None = None
    reason: str = ""


FetchText = Callable[[str], Awaitable[tuple[int, str]]]
"""Fetches a URL and returns (status_code, text). Must not follow redirects."""


class RobotsCache:
    """Per-origin robots.txt cache. Fails closed when robots cannot be read."""

    def __init__(self, fetch_text: FetchText, user_agent: str) -> None:
        self._fetch_text = fetch_text
        self._user_agent = user_agent
        self._cache: dict[str, RobotsDecision | RobotFileParser] = {}

    async def _load(self, origin: str) -> RobotFileParser | RobotsDecision:
        cached = self._cache.get(origin)
        if cached is not None:
            return cached
        try:
            status, text = await self._fetch_text(f"{origin}/robots.txt")
        except Exception as exc:  # network failure: fail closed
            decision = RobotsDecision(False, reason=f"robots.txt fetch failed: {exc}")
            self._cache[origin] = decision
            return decision
        if status == 404:
            parser = RobotFileParser()
            parser.parse([])  # no restrictions
            self._cache[origin] = parser
            return parser
        if status >= 400:  # 401/403/5xx etc. are not evidence of permission
            decision = RobotsDecision(False, reason=f"robots.txt returned HTTP {status}")
            self._cache[origin] = decision
            return decision
        parser = RobotFileParser()
        parser.parse(text.splitlines())
        self._cache[origin] = parser
        return parser

    async def check(self, url: str) -> RobotsDecision:
        parts = urlsplit(url)
        if not parts.scheme or not parts.netloc:
            return RobotsDecision(False, reason="URL has no origin")
        origin = f"{parts.scheme}://{parts.netloc}"
        loaded = await self._load(origin)
        if isinstance(loaded, RobotsDecision):
            return loaded
        allowed = loaded.can_fetch(self._user_agent, url)
        delay = loaded.crawl_delay(self._user_agent)
        return RobotsDecision(
            allowed=allowed,
            crawl_delay=float(delay) if delay is not None else None,
            reason="" if allowed else "disallowed by robots.txt",
        )
