from app.crawler.compliance import RobotsCache

USER_AGENT = "ManabiBot/1.0 (test)"


async def test_robots_allows_when_absent():
    async def fetch(url):
        assert url.endswith("/robots.txt")
        return 404, ""

    cache = RobotsCache(fetch, USER_AGENT)
    decision = await cache.check("https://example.com/problem/1")
    assert decision.allowed


async def test_robots_disallow_and_crawl_delay():
    async def fetch(url):
        return 200, "User-agent: *\nDisallow: /private\nCrawl-delay: 7\n"

    cache = RobotsCache(fetch, USER_AGENT)
    blocked = await cache.check("https://example.com/private/page")
    allowed = await cache.check("https://example.com/public/page")
    assert blocked.allowed is False
    assert "robots" in blocked.reason
    assert allowed.allowed is True
    assert allowed.crawl_delay == 7


async def test_robots_5xx_fails_closed():
    async def fetch(url):
        return 503, ""

    decision = await RobotsCache(fetch, USER_AGENT).check("https://example.com/")
    assert decision.allowed is False


async def test_robots_network_error_fails_closed():
    async def fetch(url):
        raise RuntimeError("offline")

    decision = await RobotsCache(fetch, USER_AGENT).check("https://example.com/")
    assert decision.allowed is False


async def test_robots_cached_per_origin():
    calls: list[str] = []

    async def fetch(url):
        calls.append(url)
        return 200, "User-agent: *\nAllow: /\n"

    cache = RobotsCache(fetch, USER_AGENT)
    await cache.check("https://example.com/a")
    await cache.check("https://example.com/b")
    assert calls == ["https://example.com/robots.txt"]
