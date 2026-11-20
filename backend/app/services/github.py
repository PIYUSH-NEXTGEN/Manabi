import asyncio
import base64
import logging
import re
from datetime import datetime, timedelta, timezone
from urllib.parse import unquote, urlparse
from collections import Counter

import httpx

logger = logging.getLogger(__name__)

API_BASE = "https://api.github.com"
STATUS_WINDOW_DAYS = 7
SIGNAL_TOPIC_SAMPLE = 10

# GitHub owner names are [A-Za-z0-9-], repo names additionally use . and _;
# anything else (spaces, %xx, unicode lookalikes) never comes from a real
# github.com URL and would smuggle separators into API paths.
_SEGMENT_RE = re.compile(r"^[A-Za-z0-9_.-]+$")


class GitHubError(Exception):
    def __init__(self, status: int, message: str):
        self.status = status
        super().__init__(message)


_shared_client: httpx.AsyncClient | None = None


def get_client() -> httpx.AsyncClient:
    global _shared_client
    if _shared_client is None:
        _shared_client = httpx.AsyncClient(base_url=API_BASE, timeout=15.0, follow_redirects=True)
    return _shared_client


async def close_client() -> None:
    """Release the shared connection pool during application shutdown."""
    global _shared_client
    client, _shared_client = _shared_client, None
    if client is not None:
        await client.aclose()


def _segment_is_literally_github_name(segment: str) -> bool:
    """True when the path segment is exactly what GitHub would name it.

    Rejects percent-encodings that change when decoded (e.g. %2F -> '/'),
    double encodings, dot-segments and characters GitHub never allows, so a
    crafted URL cannot make our API-path fetch resolve to a different
    repository than the URL the visitor actually sees.
    """
    if not _SEGMENT_RE.match(segment):
        return False
    # "." and ".." match the character class but are path dot-segments: httpx
    # normalises them against api.github.com, so the fetched repository would
    # not be the one in the URL.
    if segment in (".", ".."):
        return False
    decoded = segment
    for _round in range(3):
        try:
            if unquote(decoded) == decoded:
                break
        except Exception:  # noqa: BLE001 - malformed escapes: reject outright
            return False
        decoded = unquote(decoded)
    return decoded == segment


def parse_repo_url(url: str) -> tuple[str, str] | None:
    if not url:
        return None
    parsed = urlparse(url.strip())
    if parsed.scheme not in ("http", "https"):
        return None
    if parsed.hostname not in ("github.com", "www.github.com"):
        return None
    parts = [p for p in parsed.path.split("/") if p]
    if len(parts) != 2:
        return None
    owner, name = parts
    if name.endswith(".git"):
        name = name[: -len(".git")]
    if not name:
        return None
    if not _segment_is_literally_github_name(owner) or not _segment_is_literally_github_name(name):
        return None
    return owner, name


def _headers(token: str | None) -> dict[str, str]:
    headers = {"Accept": "application/vnd.github+json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


async def _fetch_json(path: str, token: str | None, params: dict | None = None):
    try:
        response = await get_client().get(path, headers=_headers(token), params=params)
    except httpx.HTTPError as exc:
        logger.warning(
            "GitHub request failed path=%s error=%s",
            path,
            type(exc).__name__,
            extra={
                "event": "external_api_failed",
                "operation": "github_fetch",
                "path": path,
                "error_type": type(exc).__name__,
            },
        )
        raise GitHubError(502, "Could not reach GitHub")
    if response.status_code == 200:
        try:
            return response.json()
        except ValueError:
            logger.warning(
                "GitHub returned unreadable JSON path=%s",
                path,
                extra={
                    "event": "external_api_failed",
                    "operation": "github_fetch",
                    "path": path,
                    "error_type": "ValueError",
                },
            )
            raise GitHubError(502, "GitHub returned an invalid response")
    if response.status_code == 404:
        logger.debug("GitHub not found path=%s", path)
        raise GitHubError(404, "Not found on GitHub")
    if response.status_code == 403:
        logger.warning(
            "GitHub rate limit reached path=%s",
            path,
            extra={
                "event": "external_api_rate_limited",
                "operation": "github_fetch",
                "path": path,
                "status": response.status_code,
            },
        )
        raise GitHubError(403, "GitHub rate limit reached")
    logger.warning(
        "GitHub unavailable path=%s status=%s",
        path,
        response.status_code,
        extra={
            "event": "external_api_failed",
            "operation": "github_fetch",
            "path": path,
            "status": response.status_code,
        },
    )
    raise GitHubError(502, "GitHub unavailable")


async def get_repo(owner: str, name: str, token: str | None = None) -> dict:
    """Public repo lookup. Raises 404-style GitHubError for missing or private repos."""
    data = await _fetch_json(f"/repos/{owner}/{name}", token)
    if not isinstance(data, dict):
        raise GitHubError(502, "GitHub returned an invalid repository response")
    if data.get("private"):
        raise GitHubError(404, "Repository not found or not public")
    return data


def canonical_repo_url(repo: dict) -> str:
    """Canonical https://github.com/owner/name URL from a repo API payload."""
    name = repo.get("full_name")
    if not name:
        owner = (repo.get("owner") or {}).get("login", "")
        name = f"{owner}/{repo.get('name', '')}"
    return f"https://github.com/{name}"


def repo_created_at(repo: dict) -> datetime | None:
    raw = repo.get("created_at")
    if not raw:
        return None
    try:
        return datetime.fromisoformat(str(raw).replace("Z", "+00:00")).replace(tzinfo=None)
    except ValueError:
        return None


async def fetch_readme_text(owner: str, name: str, token: str | None = None, max_chars: int = 4000) -> str | None:
    """README body as decoded text (truncated), or None when absent/unreadable."""
    try:
        data = await _fetch_json(f"/repos/{owner}/{name}/readme", token)
    except (httpx.HTTPError, GitHubError):
        return None
    if not isinstance(data, dict):
        return None
    content = data.get("content")
    if not content or not isinstance(content, str):
        return None
    try:
        decoded = base64.b64decode(content).decode("utf-8", errors="replace")
    except (ValueError, TypeError):
        return None
    return decoded[:max_chars]


async def fetch_contributors(owner: str, name: str, token: str | None = None) -> list[dict] | None:
    """Contributor list or None when GitHub could not answer (rate limit etc.).

    An empty list means the repo genuinely has no contributors (GitHub may
    also answer 204 for an empty list)."""
    try:
        response = await get_client().get(
            f"/repos/{owner}/{name}/contributors", headers=_headers(token), params={"per_page": 100}
        )
    except httpx.HTTPError as exc:
        logger.warning(
            "GitHub contributors request failed repo=%s/%s error=%s",
            owner,
            name,
            type(exc).__name__,
            extra={
                "event": "external_api_failed",
                "operation": "github_contributors",
                "error_type": type(exc).__name__,
            },
        )
        raise GitHubError(502, "Could not reach GitHub")
    if response.status_code in (200, 204):
        data = response.json() if response.status_code == 200 else []
        return data if isinstance(data, list) else []
    if response.status_code == 404:
        return []
    if response.status_code == 403:
        logger.warning(
            "GitHub rate limit reached repo=%s/%s",
            owner,
            name,
            extra={
                "event": "external_api_rate_limited",
                "operation": "github_contributors",
                "status": response.status_code,
            },
        )
        raise GitHubError(403, "GitHub rate limit reached")
    logger.warning(
        "GitHub contributors unavailable repo=%s/%s status=%s",
        owner,
        name,
        response.status_code,
        extra={
            "event": "external_api_failed",
            "operation": "github_contributors",
            "status": response.status_code,
        },
    )
    raise GitHubError(502, "GitHub unavailable")


def _commit_date(raw: str) -> datetime | None:
    try:
        return datetime.fromisoformat(raw.replace("Z", "+00:00"))
    except ValueError:
        return None


def _status_for(commit_count: int, last_commit_at: datetime | None) -> str:
    if commit_count <= 1:
        return "not_started"
    if last_commit_at is None:
        return "stale"
    if last_commit_at >= datetime.now(timezone.utc) - timedelta(days=STATUS_WINDOW_DAYS):
        return "active"
    return "stale"


async def fetch_commits(owner: str, name: str, token: str | None) -> list[dict]:
    data = await _fetch_json(f"/repos/{owner}/{name}/commits", token, params={"per_page": 100})
    if not isinstance(data, list) or any(not isinstance(item, dict) for item in data):
        raise GitHubError(502, "GitHub returned an invalid commits response")
    return data


async def _fetch_readme(owner: str, name: str, token: str | None) -> bool:
    await _fetch_json(f"/repos/{owner}/{name}/readme", token)
    return True


async def _fetch_issues(owner: str, name: str, token: str | None) -> list[dict]:
    return await _fetch_json(
        f"/repos/{owner}/{name}/issues", token, params={"state": "open", "per_page": 50}
    )
async def get_progress(owner: str, name: str, token: str | None = None) -> dict | None:
    """Returns a Progress-dict. None if core data (commits) cannot be fetched."""
    try:
        commits, has_readme, issues = await asyncio.gather(
            fetch_commits(owner, name, token),
            _fetch_readme(owner, name, token),
            _fetch_issues(owner, name, token),
            return_exceptions=True,
        )
    except (httpx.HTTPError, GitHubError) as exc:
        logger.warning(
            "GitHub progress fetch failed repo=%s/%s error=%s",
            owner,
            name,
            type(exc).__name__,
            extra={
                "event": "external_api_failed",
                "operation": "github_progress",
                "error_type": type(exc).__name__,
            },
        )
        return None
    if isinstance(commits, Exception):
        logger.warning(
            "GitHub progress has no commit data repo=%s/%s error=%s",
            owner,
            name,
            type(commits).__name__,
            extra={
                "event": "external_api_failed",
                "operation": "github_progress",
                "error_type": type(commits).__name__,
            },
        )
        return None
    dates = [
        d
        for commit in commits
        if isinstance(commit.get("commit"), dict)
        and isinstance(commit["commit"].get("committer"), dict)
        for d in [
            _commit_date(str(commit["commit"]["committer"].get("date", "")))
        ]
        if d
    ]
    last_commit_at = max(dates) if dates else None

    recent = []
    for commit in commits[:5]:
        details = commit.get("commit") if isinstance(commit.get("commit"), dict) else {}
        committer = details.get("committer") if isinstance(details.get("committer"), dict) else {}
        date = _commit_date(str(committer.get("date", "")))
        message = details.get("message")
        recent.append(
            {
                "sha": commit.get("sha") if isinstance(commit.get("sha"), str) else None,
                "message": message[:200] if isinstance(message, str) else "",
                "date": date.isoformat() if date else None,
            }
        )

    open_issues = []
    if isinstance(issues, list):
        priority = []
        rest = []
        for issue in issues:
            if not isinstance(issue, dict) or "pull_request" in issue:
                continue
            raw_labels = issue.get("labels")
            labels = {
                label.get("name", "")
                for label in raw_labels
                if isinstance(label, dict) and isinstance(label.get("name"), str)
            } if isinstance(raw_labels, list) else set()
            entry = {
                "number": issue.get("number"),
                "title": issue.get("title"),
                "url": issue.get("html_url"),
                "labels": sorted(labels),
            }
            if labels & {"good first issue", "help wanted"}:
                priority.append(entry)
            else:
                rest.append(entry)
        open_issues = (priority + rest)[:10]

    return {
        "status": _status_for(len(commits), last_commit_at),
        "commit_count": len(commits),
        "last_commit_at": last_commit_at.isoformat() if last_commit_at else None,
        "has_readme": bool(has_readme) if not isinstance(has_readme, Exception) else False,
        "recent_commits": recent,
        "open_issues": open_issues,
    }


async def get_user_signals(token: str | None) -> dict | None:
    """Top languages (by repo count) and repo topics for the authenticated user."""
    try:
        repos = await _fetch_json("/user/repos", token, params={"per_page": 100, "sort": "updated"})
    except (httpx.HTTPError, GitHubError) as exc:
        logger.warning(
            "GitHub user signals unavailable error=%s",
            type(exc).__name__,
            extra={
                "event": "external_api_failed",
                "operation": "github_user_signals",
                "error_type": type(exc).__name__,
            },
        )
        return None
    if not isinstance(repos, list):
        logger.warning(
            "GitHub user signals had the wrong shape",
            extra={"event": "external_api_failed", "operation": "github_user_signals"},
        )
        return None
    repos = [repo for repo in repos if isinstance(repo, dict)]
    languages = Counter(
        repo["language"] for repo in repos if isinstance(repo.get("language"), str)
    )
    sample = [
        repo
        for repo in repos[:SIGNAL_TOPIC_SAMPLE]
        if isinstance(repo.get("owner"), dict)
        and isinstance(repo["owner"].get("login"), str)
        and isinstance(repo.get("name"), str)
    ]
    topic_lists = await asyncio.gather(
        *[_fetch_repo_topics(repo["owner"]["login"], repo["name"], token) for repo in sample],
        return_exceptions=True,
    )
    topics = [t for result in topic_lists if isinstance(result, list) for t in result]
    return {
        "languages": dict(languages.most_common()),
        "topics": sorted(set(topics)),
    }


async def _fetch_repo_topics(owner: str, name: str, token: str | None) -> list[str]:
    try:
        data = await _fetch_json(f"/repos/{owner}/{name}/topics", token)
    except (httpx.HTTPError, GitHubError):
        return []
    names = data.get("names") if isinstance(data, dict) else None
    return [str(item) for item in names] if isinstance(names, list) else []


HEATMAP_DAYS = 91


async def fetch_contribution_histogram(username: str, token: str | None) -> list[dict] | None:
    """Daily public-push histogram for the last HEATMAP_DAYS days.

    Aggregates the GitHub public events API (PushEvents only) into a
    date-sorted [{date, count}] list. Returns None when GitHub is
    unreachable so the UI can degrade honestly instead of a fake grid.
    """
    pages: list[list] = []
    for page in (1, 2, 3):
        try:
            events = await _fetch_json(
                f"/users/{username}/events/public",
                token,
                params={"per_page": 100, "page": page},
            )
        except (httpx.HTTPError, GitHubError) as exc:
            logger.warning(
                "GitHub contribution histogram unavailable user=%s error=%s",
                username,
                type(exc).__name__,
                extra={
                    "event": "external_api_failed",
                    "operation": "github_heatmap",
                    "error_type": type(exc).__name__,
                },
            )
            return None
        if not isinstance(events, list):
            break
        pages.append(events)
        if len(events) < 100:
            break
    cutoff = datetime.now(timezone.utc) - timedelta(days=HEATMAP_DAYS)
    daily: Counter[str] = Counter()
    for events in pages:
        for event in events:
            if not isinstance(event, dict) or event.get("type") != "PushEvent":
                continue
            created = event.get("created_at")
            if not isinstance(created, str) or not created:
                continue
            try:
                at = datetime.fromisoformat(created.replace("Z", "+00:00"))
            except ValueError:
                continue
            if at < cutoff:
                continue
            daily[at.strftime("%Y-%m-%d")] += 1
    return [{"date": date, "count": count} for date, count in sorted(daily.items())]
