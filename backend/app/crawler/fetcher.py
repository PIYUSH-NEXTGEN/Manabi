"""Polite, SSRF-safe fetcher shared by every crawler adapter (§7.2).

The rules mirror the old user-ingest extractor: http(s) only, ports 80/443,
no credentials, every host/IP must resolve to a public address (re-checked on
each redirect), three-redirect cap, size and timeout caps. On top of that it
adds per-host throttling, conditional requests and 429/503 backoff.
"""

from __future__ import annotations

import asyncio
import ipaddress
import json
import socket
import time
from dataclasses import dataclass, field
from urllib.parse import urljoin, urlsplit

import httpx

REDIRECT_STATUSES = {301, 302, 303, 307, 308}
RETRY_STATUSES = {429, 503}
MAX_REDIRECTS = 3
DEFAULT_MAX_BYTES = 500_000
DEFAULT_TIMEOUT = 8.0

TEXT_CONTENT_TYPES = {
    "text/html",
    "application/xhtml+xml",
    "text/plain",
    "text/xml",
    "application/xml",
    "application/json",
    "text/csv",
    "application/pdf",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "application/vnd.ms-excel",
}


class FetchError(RuntimeError):
    """A request failed, was blocked, or returned an unsupported response."""


@dataclass
class FetchResult:
    url: str
    status: int
    content: bytes
    content_type: str
    etag: str | None = None
    last_modified: str | None = None
    not_modified: bool = False
    headers: dict[str, str] = field(default_factory=dict)

    @property
    def text(self) -> str:
        return self.content.decode("utf-8", errors="replace")



def _default_resolve(host: str) -> list[str]:
    infos = socket.getaddrinfo(host, None, proto=socket.IPPROTO_TCP)
    return sorted({info[4][0] for info in infos})


async def resolve_host(host: str) -> list[str]:
    return await asyncio.get_running_loop().run_in_executor(None, _default_resolve, host)


def _assert_public_ip(address: str, host: str) -> None:
    ip = ipaddress.ip_address(address)
    if (
        ip.is_private
        or ip.is_loopback
        or ip.is_link_local
        or ip.is_reserved
        or ip.is_multicast
        or ip.is_unspecified
    ):
        raise FetchError(f"Blocked non-public address for {host}: {address}")


def validate_url(url: str) -> None:
    parts = urlsplit(url)
    if parts.scheme not in ("http", "https"):
        raise FetchError("Only http/https URLs are allowed")
    if parts.username or parts.password:
        raise FetchError("URLs with credentials are not allowed")
    if not parts.hostname:
        raise FetchError("URL has no host")
    port = parts.port
    if port not in (None, 80, 443):
        raise FetchError(f"Port {port} is not allowed")
    host = parts.hostname.lower().rstrip(".")
    if host in ("localhost", "localhost.localdomain") or host.endswith(".local") or host.endswith(".internal"):
        raise FetchError(f"Blocked host: {host}")
    try:
        ipaddress.ip_address(host)
    except ValueError:
        return  # hostname; resolved below
    _assert_public_ip(host, host)


async def _assert_public_host(url: str, resolve) -> None:
    host = urlsplit(url).hostname or ""
    addresses = await resolve(host)
    if not addresses:
        raise FetchError(f"Could not resolve {host}")
    for address in addresses:
        _assert_public_ip(address, host)


class HostThrottle:
    """Serialise requests per host and never go faster than min_delay."""

    def __init__(self, min_delay: float = 3.0, clock=time.monotonic, sleep=asyncio.sleep) -> None:
        self.min_delay = max(0.0, min_delay)
        self._clock = clock
        self._sleep = sleep
        self._last: dict[str, float] = {}
        self._locks: dict[str, asyncio.Lock] = {}

    async def wait(self, host: str, crawl_delay: float | None = None) -> None:
        lock = self._locks.setdefault(host, asyncio.Lock())
        async with lock:
            delay = max(self.min_delay, crawl_delay or 0.0)
            last = self._last.get(host)
            if last is not None:
                remaining = delay - (self._clock() - last)
                if remaining > 0:
                    await self._sleep(remaining)
            self._last[host] = self._clock()


def _content_type(headers: httpx.Headers) -> str:
    return (headers.get("content-type") or "").split(";", 1)[0].strip().lower()


async def safe_fetch(
    url: str,
    *,
    client: httpx.AsyncClient | None = None,
    resolve=None,
    throttle: HostThrottle | None = None,
    user_agent: str = "ManabiBot/1.0",
    accept: str | None = None,
    extra_headers: dict[str, str] | None = None,
    max_bytes: int = DEFAULT_MAX_BYTES,
    timeout: float = DEFAULT_TIMEOUT,
    allow_statuses: set[int] | None = None,
    sleep=asyncio.sleep,
) -> FetchResult:
    resolve = resolve or resolve_host
    throttle = throttle or HostThrottle(0.0, sleep=sleep)
    owns_client = client is None
    client = client or httpx.AsyncClient(timeout=timeout, follow_redirects=False)
    headers = {"User-Agent": user_agent, "Accept": accept or "*/*"}
    headers.update(extra_headers or {})
    current = url

    async def attempt(target: str) -> httpx.Response:
        await _assert_public_host(target, resolve)
        await throttle.wait(urlsplit(target).hostname or "")
        return await client.get(target, headers=headers)

    try:
        response: httpx.Response | None = None
        for _ in range(MAX_REDIRECTS + 1):
            validate_url(current)
            retries = 0
            while True:
                response = await attempt(current)
                if response.status_code in RETRY_STATUSES and retries < 2:
                    retry_after = response.headers.get("retry-after")
                    try:
                        wait_for = min(float(retry_after), 60.0) if retry_after else 2.0 ** retries
                    except ValueError:
                        wait_for = 2.0 ** retries
                    await sleep(wait_for)
                    retries += 1
                    continue
                break

            if response.status_code in REDIRECT_STATUSES:
                location = response.headers.get("location")
                if not location:
                    raise FetchError(f"Redirect without Location from {current}")
                current = urljoin(current, location)
                continue
            break

        assert response is not None
        content_type = _content_type(response.headers)
        if response.status_code == 304:
            return FetchResult(
                url=current,
                status=304,
                content=b"",
                content_type=content_type,
                etag=response.headers.get("etag"),
                last_modified=response.headers.get("last-modified"),
                not_modified=True,
                headers=dict(response.headers),
            )
        if response.status_code >= 400 and response.status_code in (allow_statuses or set()):
            return FetchResult(
                url=current,
                status=response.status_code,
                content=response.content,
                content_type=content_type,
                etag=response.headers.get("etag"),
                last_modified=response.headers.get("last-modified"),
                headers=dict(response.headers),
            )
        if response.status_code >= 400:
            raise FetchError(f"HTTP {response.status_code} for {current}")
        if content_type not in TEXT_CONTENT_TYPES:
            raise FetchError(f"Unsupported content type '{content_type}' for {current}")

        declared = response.headers.get("content-length")
        if declared and declared.isdigit() and int(declared) > max_bytes:
            raise FetchError(f"Response exceeds {max_bytes} bytes for {current}")
        content = response.content
        if len(content) > max_bytes:
            raise FetchError(f"Response exceeds {max_bytes} bytes for {current}")
        if not content:
            raise FetchError(f"Empty response for {current}")
        return FetchResult(
            url=current,
            status=response.status_code,
            content=content,
            content_type=content_type,
            etag=response.headers.get("etag"),
            last_modified=response.headers.get("last-modified"),
            headers=dict(response.headers),
        )
    except httpx.HTTPError as exc:
        raise FetchError(f"Request failed for {current}: {exc}") from exc
    finally:
        if owns_client:
            await client.aclose()


def extract_pdf_text(content: bytes) -> str:
    """Text-based PDFs only; no OCR (§7.2)."""
    from io import BytesIO

    from pypdf import PdfReader

    reader = PdfReader(BytesIO(content))
    return "\n".join(page.extract_text() or "" for page in reader.pages)


def extract_json(content: bytes) -> object:
    return json.loads(content.decode("utf-8", errors="replace"))
