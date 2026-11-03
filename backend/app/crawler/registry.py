"""Source registry: one validated YAML file per crawl source (§7.1)."""

from datetime import date
from pathlib import Path
from typing import Literal

import yaml
from pydantic import BaseModel, Field, field_validator

from app.crawler.config import SOURCES_DIR

Verdict = Literal["allowed", "api_only", "manual_only", "forbidden", "unclear"]
DiscoveryMethod = Literal["static_list", "sitemap", "listing_html", "rss", "json_api", "file_table"]
DisplayPolicy = Literal["summary_only", "summary_plus_excerpt"]

ALLOWED_VERDICTS = {"allowed", "api_only"}


class Compliance(BaseModel):
    verdict: Verdict
    checked_on: date
    record: str = Field(min_length=1)
    contact: str | None = None


class Discovery(BaseModel):
    method: DiscoveryMethod
    urls: list[str] = Field(default_factory=list)
    parser: str | None = None
    selectors: dict[str, str] = Field(default_factory=dict)
    sitemap_url: str | None = None
    json_path: str | None = None
    column_map: dict[str, str] = Field(default_factory=dict)
    id_regex: str | None = None
    year: int | None = None


class Politeness(BaseModel):
    min_delay_seconds: float = Field(default=3.0, ge=0)
    max_pages_per_run: int = Field(default=200, ge=1)
    max_concurrency: int = Field(default=1, ge=1)
    max_bytes: int = Field(default=500_000, ge=1)


class Parse(BaseModel):
    source_id_regex: str | None = None
    edition_from: Literal["url_or_title", "title", "url"] = "url_or_title"


class Publish(BaseModel):
    auto_publish: bool = False
    min_confidence: float = Field(default=0.75, ge=0, le=1)


class Source(BaseModel):
    key: str = Field(pattern=r"^[a-z0-9][a-z0-9_-]*$")
    name: str = Field(min_length=1)
    base_url: str
    compliance: Compliance
    discovery: Discovery
    politeness: Politeness = Field(default_factory=Politeness)
    parse: Parse = Field(default_factory=Parse)
    display_policy: DisplayPolicy = "summary_only"
    publish: Publish = Field(default_factory=Publish)

    @field_validator("base_url")
    @classmethod
    def _http_base(cls, value: str) -> str:
        if not value.startswith(("http://", "https://")):
            raise ValueError("base_url must be http(s)")
        return value.rstrip("/")


def _source_from_file(path: Path) -> Source:
    try:
        raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError as exc:  # pragma: no cover - defensive
        raise ValueError(f"{path.name}: invalid YAML: {exc}") from exc
    source = Source.model_validate(raw)
    if source.key != path.stem:
        raise ValueError(f"{path.name}: key '{source.key}' must match the filename")
    return source


def load_sources(directory: Path = SOURCES_DIR) -> dict[str, Source]:
    sources: dict[str, Source] = {}
    for path in sorted(directory.glob("*.yaml")):
        source = _source_from_file(path)
        sources[source.key] = source
    return sources


def load_source(key: str, directory: Path = SOURCES_DIR) -> Source:
    path = directory / f"{key}.yaml"
    if not path.is_file():
        raise FileNotFoundError(f"Unknown crawl source: {key}")
    return _source_from_file(path)


__all__ = [
    "ALLOWED_VERDICTS",
    "Compliance",
    "Discovery",
    "DiscoveryMethod",
    "Parse",
    "Politeness",
    "Publish",
    "Source",
    "Verdict",
    "load_source",
    "load_sources",
]
