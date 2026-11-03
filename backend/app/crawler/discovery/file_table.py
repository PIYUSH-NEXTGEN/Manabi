"""Official CSV/XLSX/PDF release adapter (§7.2)."""

import csv
from io import BytesIO, StringIO

from app.crawler.discovery.base import CrawlContext, DiscoveredItem
from app.crawler.fetcher import extract_pdf_text
from app.crawler.registry import Source


def _xlsx_rows(content: bytes) -> list[dict]:
    import openpyxl

    workbook = openpyxl.load_workbook(BytesIO(content), read_only=True, data_only=True)
    sheet = workbook[workbook.sheetnames[0]]
    rows = sheet.iter_rows(values_only=True)
    header = [str(cell or "").strip() for cell in next(rows)]
    return [dict(zip(header, values)) for values in rows]


def _map_rows(source: Source, rows: list[dict], url: str) -> list[DiscoveredItem]:
    mapping = source.discovery.column_map
    items: list[DiscoveredItem] = []
    for row in rows:
        def pick(field: str, default: str):
            return row.get(mapping.get(field, default))

        source_id = pick("source_id", "source_id")
        title = pick("title", "title")
        if not source_id and not title:
            continue
        items.append(
            DiscoveredItem(
                url=url,
                source_id=str(source_id).strip() if source_id else None,
                title=str(title).strip() if title else None,
                organisation=str(pick("organisation", "organisation") or "").strip() or None,
                description=str(pick("description", "description") or "").strip() or None,
                category=str(pick("category", "category") or "").strip() or None,
                theme=str(pick("theme", "theme") or "").strip() or None,
                department=str(pick("department", "department") or "").strip() or None,
                year=source.discovery.year,
            )
        )
    return items


async def discover(source: Source, ctx: CrawlContext) -> list[DiscoveredItem]:
    url = source.discovery.urls[0]
    result = await ctx.get(url, max_bytes=max(ctx.max_bytes, 5_000_000))
    parser = source.discovery.parser or ""
    if parser == "sih_xlsx":
        from app.crawler.discovery.sih import parse_sih_xlsx

        return parse_sih_xlsx(result.content, url, year=source.discovery.year)
    if "pdf" in result.content_type or url.lower().endswith(".pdf"):
        from app.crawler.split import split_multiproblem_text

        text = extract_pdf_text(result.content)
        return [
            DiscoveredItem(url=url, description=chunk, year=source.discovery.year)
            for chunk in split_multiproblem_text(text, source.parse.source_id_regex)
        ]
    if "csv" in result.content_type or url.lower().endswith(".csv"):
        rows = list(csv.DictReader(StringIO(result.text)))
        return _map_rows(source, rows, url)
    return _map_rows(source, _xlsx_rows(result.content), url)
