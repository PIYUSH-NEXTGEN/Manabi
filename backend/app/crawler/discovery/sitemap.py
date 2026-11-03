"""sitemap.xml adapter (no crawling of disallowed URLs)."""

import re

from app.crawler.discovery.base import CrawlContext, DiscoveredItem
from app.crawler.registry import Source

LOC_RE = re.compile(r"<loc>\s*(.*?)\s*</loc>", re.IGNORECASE | re.DOTALL)


async def discover(source: Source, ctx: CrawlContext) -> list[DiscoveredItem]:
    url = source.discovery.sitemap_url or f"{source.base_url}/sitemap.xml"
    result = await ctx.get(url)
    pattern = re.compile(source.discovery.id_regex) if source.discovery.id_regex else None
    items: list[DiscoveredItem] = []
    for loc in LOC_RE.findall(result.text):
        if pattern and not pattern.search(loc):
            continue
        items.append(DiscoveredItem(url=loc, year=source.discovery.year))
    return items
