"""Deterministic parsers for the two approved SIH layouts (§8).

2026: server-rendered `/sih2026PS` table rows, one modal per problem statement.
2024: the official `SIH_PS_2024.xlsx` release.
"""

from __future__ import annotations

import html as html_lib
import re
from datetime import date, datetime

from app.crawler.discovery.base import DiscoveredItem

DATE_FORMATS = ("%d %B %Y", "%d %b %Y", "%d-%m-%Y", "%Y-%m-%d")
COMMENT_RE = re.compile(r"<!--.*?-->", re.DOTALL)


def _text(fragment: str) -> str:
    fragment = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", fragment, flags=re.DOTALL | re.IGNORECASE)
    fragment = re.sub(r"<br\s*/?>", "\n", fragment, flags=re.IGNORECASE)
    fragment = re.sub(r"</p\s*>", "\n", fragment, flags=re.IGNORECASE)
    fragment = re.sub(r"<[^>]+>", " ", fragment)
    text = html_lib.unescape(fragment)
    lines = [" ".join(line.split()) for line in text.splitlines()]
    return "\n".join(line for line in lines if line).strip()


def _first(pattern: str, fragment: str) -> str | None:
    match = re.search(pattern, fragment, re.DOTALL | re.IGNORECASE)
    return _text(match.group(1)) if match else None


def _date(raw: str | None) -> date | None:
    if not raw:
        return None
    for fmt in DATE_FORMATS:
        try:
            return datetime.strptime(raw.strip(), fmt).date()
        except ValueError:
            continue
    return None


def _year_from_url(url: str) -> int | None:
    match = re.search(r"sih(\d{4})PS", url, re.IGNORECASE)
    return int(match.group(1)) if match else None


def _row_chunks(page: str) -> list[str]:
    """A modal contains nested <tr>s, so split on row starts instead of row ends."""
    parts = re.split(r"(?=<tr>\s*<td class=\"colomn_border\">)", page)
    return [part for part in parts if part.lstrip().startswith("<tr>")]


def parse_sih_html(page: str, page_url: str, year: int | None = None) -> list[DiscoveredItem]:
    page = COMMENT_RE.sub("", page)
    year = year or _year_from_url(page_url)
    items: list[DiscoveredItem] = []
    for chunk in _row_chunks(page):
        source_id = _first(r"<td>\s*(SIH\d{4,5})\s*</td>", chunk)
        if not source_id:
            continue
        title = _first(
            r'<a[^>]*data-target="#ViewProblemStatement\d+"[^>]*>(.*?)</a>',
            chunk,
        )
        cells = chunk.split('<td class="colomn_border">')[1:]
        organisation = _text(cells[1].split("</td>", 1)[0]) if len(cells) > 1 else None
        description = _first(
            r"<th[^>]*>\s*Description\s*</th>(.*?)(?:<th[^>]*>\s*(?:Organization|Organisation|Department)\s*</th>|</table>)",
            chunk,
        )
        theme = _first(r"<th[^>]*>\s*Theme\s*</th>\s*<td>(.*?)</td>", chunk)
        department = _first(r"<th[^>]*>\s*Department\s*</th>\s*<td>(.*?)</td>", chunk)
        category = None
        for match in re.finditer(r"<td>\s*(Software|Hardware)\s*</td>", chunk, re.IGNORECASE):
            category = match.group(1).strip()
        dates = re.findall(r"<td>\s*(\d{1,2}\s+[A-Za-z]+\s+\d{4})\s*</td>", chunk)
        items.append(
            DiscoveredItem(
                url=f"{page_url}#{source_id}",
                source_id=source_id,
                title=title,
                organisation=organisation,
                description=description,
                year=year,
                edition=f"{year}" if year else None,
                deadline=_date(dates[-1]) if dates else None,
                category=category,
                theme=theme,
                department=department,
            )
        )
    return items


def _cell(row: dict, name: str) -> str | None:
    for key, value in row.items():
        if key and key.strip().lower() == name.lower() and value is not None:
            text = str(value).strip()
            return text or None
    return None


def parse_sih_xlsx(content: bytes, url: str, year: int | None = None) -> list[DiscoveredItem]:
    import openpyxl
    from io import BytesIO

    workbook = openpyxl.load_workbook(BytesIO(content), read_only=True, data_only=True)
    sheet = workbook[workbook.sheetnames[0]]
    rows = sheet.iter_rows(values_only=True)
    header = [str(cell or "").strip() for cell in next(rows)]
    year = year or 2024
    items: list[DiscoveredItem] = []
    for values in rows:
        row = dict(zip(header, values))
        source_id = _cell(row, "Statement_id")
        title = _cell(row, "Title")
        if not source_id and not title:
            continue
        dataset = _cell(row, "Datasetfile")
        items.append(
            DiscoveredItem(
                url=url,
                source_id=source_id,
                title=title,
                organisation=_cell(row, "Organisation"),
                department=_cell(row, "Department"),
                description=_cell(row, "Description") or title,
                category=_cell(row, "Category"),
                theme=_cell(row, "Technology_Bucket"),
                year=year,
                edition=str(year),
                extra={"dataset_file": dataset} if dataset and dataset.upper() != "NULL" else {},
            )
        )
    return items
