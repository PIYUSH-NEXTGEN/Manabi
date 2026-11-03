"""RSS/Atom adapter using the standard library XML parser."""

from xml.etree import ElementTree

from app.crawler.discovery.base import CrawlContext, DiscoveredItem
from app.crawler.registry import Source


def _local(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


async def discover(source: Source, ctx: CrawlContext) -> list[DiscoveredItem]:
    url = source.discovery.urls[0]
    result = await ctx.get(url)
    root = ElementTree.fromstring(result.content)
    items: list[DiscoveredItem] = []
    for node in root.iter():
        if _local(node.tag) not in ("item", "entry"):
            continue
        title = None
        link = None
        for child in node:
            name = _local(child.tag)
            if name == "title" and child.text:
                title = child.text.strip()
            elif name == "link":
                link = child.get("href") or (child.text or "").strip() or None
        if link:
            items.append(DiscoveredItem(url=link, title=title, year=source.discovery.year))
    return items
