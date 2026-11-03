"""Explicit URL list from the registry (used for owner-supplied SIH links)."""

from app.crawler.discovery.base import CrawlContext, DiscoveredItem
from app.crawler.registry import Source


async def discover(source: Source, ctx: CrawlContext) -> list[DiscoveredItem]:
    return [DiscoveredItem(url=url, year=source.discovery.year) for url in source.discovery.urls]
