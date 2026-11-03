"""Discovery adapter protocol and the robots-aware fetch context."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date

from app.crawler.compliance import RobotsCache
from app.crawler.fetcher import FetchResult, HostThrottle, safe_fetch
from app.crawler.registry import Source


class RobotsDisallowed(RuntimeError):
    """Robots.txt forbids this URL; counts as skipped_robots."""


@dataclass
class DiscoveredItem:
    url: str
    source_id: str | None = None
    title: str | None = None
    organisation: str | None = None
    description: str | None = None
    year: int | None = None
    edition: str | None = None
    deadline: date | None = None
    category: str | None = None
    theme: str | None = None
    department: str | None = None
    extra: dict = field(default_factory=dict)


@dataclass
class CrawlContext:
    source: Source
    robots: RobotsCache
    throttle: HostThrottle
    user_agent: str
    max_bytes: int
    resolve: object = None
    client: object = None
    sleep: object = None
    requests: int = 0

    async def get(self, url: str, *, extra_headers: dict[str, str] | None = None, max_bytes: int | None = None) -> FetchResult:
        decision = await self.robots.check(url)
        if not decision.allowed:
            raise RobotsDisallowed(f"{url}: {decision.reason}")
        kwargs = {
            "client": self.client,
            "resolve": self.resolve,
            "throttle": self.throttle,
            "user_agent": self.user_agent,
            "extra_headers": extra_headers,
            "max_bytes": max_bytes or self.max_bytes,
        }
        if self.sleep is not None:
            kwargs["sleep"] = self.sleep
        self.requests += 1
        return await safe_fetch(url, **kwargs)


async def discover(source: Source, ctx: CrawlContext) -> list[DiscoveredItem]:
    method = source.discovery.method
    if method == "static_list":
        from app.crawler.discovery.static_list import discover as adapter
    elif method == "sitemap":
        from app.crawler.discovery.sitemap import discover as adapter
    elif method == "rss":
        from app.crawler.discovery.rss import discover as adapter
    elif method == "json_api":
        from app.crawler.discovery.json_api import discover as adapter
    elif method == "listing_html":
        from app.crawler.discovery.listing_html import discover as adapter
    elif method == "file_table":
        from app.crawler.discovery.file_table import discover as adapter
    else:  # pragma: no cover - registry validation prevents this
        raise ValueError(f"Unsupported discovery method: {method}")
    return await adapter(source, ctx)
