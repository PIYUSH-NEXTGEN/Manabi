"""Listing-page adapter. Dedicated parsers live beside it (e.g. sih.py)."""

import re

from app.crawler.discovery.base import CrawlContext, DiscoveredItem
from app.crawler.registry import Source

ANCHOR_RE = re.compile(r'<a\s+[^>]*href="([^"]+)"[^>]*>(.*?)</a>', re.IGNORECASE | re.DOTALL)


def _strip(fragment: str) -> str:
    import html as html_lib

    return " ".join(html_lib.unescape(re.sub(r"<[^>]+>", " ", fragment)).split())


def _generic_links(source: Source, page: str, url: str) -> list[DiscoveredItem]:
    pattern = re.compile(source.discovery.id_regex) if source.discovery.id_regex else None
    items: list[DiscoveredItem] = []
    for href, label in ANCHOR_RE.findall(page):
        if pattern and not pattern.search(href):
            continue
        if href.startswith(("mailto:", "javascript:", "#")):
            continue
        items.append(DiscoveredItem(url=href if href.startswith("http") else source.base_url + href, title=_strip(label) or None, year=source.discovery.year))
    return items


async def discover(source: Source, ctx: CrawlContext) -> list[DiscoveredItem]:
    items: list[DiscoveredItem] = []
    for url in source.discovery.urls:
        result = await ctx.get(url)
        if source.discovery.parser == "sih":
            from app.crawler.discovery.sih import parse_sih_html

            items.extend(parse_sih_html(result.text, url, year=source.discovery.year))
        else:
            items.extend(_generic_links(source, result.text, url))
    return items
