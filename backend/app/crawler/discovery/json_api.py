"""Official JSON API adapter (preferred over HTML when offered)."""

from app.crawler.discovery.base import CrawlContext, DiscoveredItem
from app.crawler.fetcher import extract_json
from app.crawler.registry import Source


def _walk(data, path: str | None):
    if not path:
        return data
    current = data
    for part in path.split("."):
        current = current[part]
    return current


async def discover(source: Source, ctx: CrawlContext) -> list[DiscoveredItem]:
    result = await ctx.get(source.discovery.urls[0])
    rows = _walk(extract_json(result.content), source.discovery.json_path)
    if isinstance(rows, dict):
        rows = list(rows.values())
    column_map = source.discovery.column_map
    items: list[DiscoveredItem] = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        url = row.get(column_map.get("url", "url"))
        if not url:
            continue
        items.append(
            DiscoveredItem(
                url=url,
                source_id=row.get(column_map.get("source_id", "source_id")),
                title=row.get(column_map.get("title", "title")),
                organisation=row.get(column_map.get("organisation", "organisation")),
                description=row.get(column_map.get("description", "description")),
                year=row.get(column_map.get("year", "year")) or source.discovery.year,
            )
        )
    return items
