import httpx
import pytest

from app.crawler.fetcher import FetchError, HostThrottle, safe_fetch, validate_url


def _client(handler):
    return httpx.AsyncClient(transport=httpx.MockTransport(handler), follow_redirects=False)


async def _public_resolver(host: str) -> list[str]:
    return ["93.184.216.34"]


@pytest.mark.parametrize(
    "url",
    [
        "ftp://example.com/file",
        "http://user:pass@example.com/",
        "http://example.com:8080/",
        "http://localhost/",
        "http://127.0.0.1/",
        "http://evil.internal/",
    ],
)
def test_validate_url_blocks_unsafe_targets(url):
    with pytest.raises(FetchError):
        validate_url(url)


async def test_private_dns_target_is_blocked():
    async def resolver(host):
        return ["10.0.0.5"]

    client = _client(lambda request: httpx.Response(200, text="ok"))
    with pytest.raises(FetchError, match="non-public"):
        await safe_fetch("https://example.com/", client=client, resolve=resolver)
    await client.aclose()


async def test_fetches_html_and_records_conditional_headers():
    async def handler(request):
        return httpx.Response(
            200,
            content=b"<html>ok</html>",
            headers={"content-type": "text/html", "etag": '"v1"'},
        )

    client = _client(handler)
    result = await safe_fetch("https://example.com/page", client=client, resolve=_public_resolver)
    assert result.text == "<html>ok</html>"
    assert result.etag == '"v1"'
    await client.aclose()


async def test_304_is_not_modified():
    client = _client(lambda request: httpx.Response(304, headers={"content-type": "text/html"}))
    result = await safe_fetch("https://example.com/page", client=client, resolve=_public_resolver)
    assert result.not_modified is True
    await client.aclose()


async def test_redirect_is_revalidated_and_capped():
    calls: list[str] = []

    async def handler(request):
        calls.append(str(request.url))
        return httpx.Response(302, headers={"location": "http://127.0.0.1/private"})

    client = _client(handler)
    with pytest.raises(FetchError, match="Blocked host|non-public"):
        await safe_fetch("https://example.com/start", client=client, resolve=_public_resolver)
    assert calls == ["https://example.com/start"]
    await client.aclose()


async def test_size_cap():
    client = _client(lambda request: httpx.Response(200, content=b"x" * 100, headers={"content-type": "text/html"}))
    with pytest.raises(FetchError, match="exceeds"):
        await safe_fetch("https://example.com/", client=client, resolve=_public_resolver, max_bytes=50)
    await client.aclose()


async def test_unsupported_content_type():
    client = _client(lambda request: httpx.Response(200, content=b"img", headers={"content-type": "image/png"}))
    with pytest.raises(FetchError, match="Unsupported content type"):
        await safe_fetch("https://example.com/", client=client, resolve=_public_resolver)
    await client.aclose()


async def test_retries_503_then_succeeds_and_honours_retry_after():
    responses = iter(
        [
            httpx.Response(503, headers={"retry-after": "0"}),
            httpx.Response(200, content=b"ok", headers={"content-type": "text/plain"}),
        ]
    )
    waits: list[float] = []

    async def fake_sleep(seconds: float) -> None:
        waits.append(seconds)

    client = _client(lambda request: next(responses))
    result = await safe_fetch("https://example.com/", client=client, resolve=_public_resolver, sleep=fake_sleep)
    assert result.text == "ok"
    assert waits == [0.0]
    await client.aclose()


async def test_throttle_waits_between_requests_to_same_host():
    times = iter([0.0, 0.0, 1.0])
    waits: list[float] = []

    async def fake_sleep(seconds: float) -> None:
        waits.append(seconds)

    throttle = HostThrottle(3.0, clock=lambda: next(times), sleep=fake_sleep)
    await throttle.wait("example.com")
    await throttle.wait("example.com")
    assert waits == [3.0]
