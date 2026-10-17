import asyncio
from datetime import datetime, timedelta, timezone
from urllib.parse import urlparse
from collections import Counter

import httpx

API_BASE = "https://api.github.com"
STATUS_WINDOW_DAYS = 7
SIGNAL_TOPIC_SAMPLE = 10


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
    return owner, name


def _headers(token: str | None) -> dict[str, str]:
    headers = {"Accept": "application/vnd.github+json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


async def _fetch_json(path: str, token: str | None, params: dict | None = None):
    try:
        response = await get_client().get(path, headers=_headers(token), params=params)
    except httpx.HTTPError:
        raise GitHubError(502, "Could not reach GitHub")
    if response.status_code == 200:
        return response.json()
    if response.status_code == 404:
        raise GitHubError(404, "Not found on GitHub")
    if response.status_code == 403:
        raise GitHubError(403, "GitHub rate limit reached")
    raise GitHubError(502, "GitHub unavailable")


async def get_repo(owner: str, name: str, token: str | None = None) -> dict:
    """Public repo lookup. Raises 404-style GitHubError for missing or private repos."""
    data = await _fetch_json(f"/repos/{owner}/{name}", token)
    if data.get("private"):
        raise GitHubError(404, "Repository not found or not public")
    return data


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


async def _fetch_commits(owner: str, name: str, token: str | None) -> list[dict]:
    return await _fetch_json(f"/repos/{owner}/{name}/commits", token, params={"per_page": 100})


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
            _fetch_commits(owner, name, token),
            _fetch_readme(owner, name, token),
            _fetch_issues(owner, name, token),
            return_exceptions=True,
        )
    except (httpx.HTTPError, GitHubError):
        return None
    if isinstance(commits, Exception):
        return None
    dates = [d for c in commits for d in [_commit_date(c.get("commit", {}).get("committer", {}).get("date", ""))] if d]
    last_commit_at = max(dates) if dates else None

    recent = []
    for commit in commits[:5]:
        date = _commit_date(commit.get("commit", {}).get("committer", {}).get("date", ""))
        recent.append(
            {
                "sha": commit.get("sha"),
                "message": (commit.get("commit", {}).get("message") or "")[:200],
                "date": date.isoformat() if date else None,
            }
        )

    open_issues = []
    if isinstance(issues, list):
        priority = []
        rest = []
        for issue in issues:
            if "pull_request" in issue:
                continue
            labels = {label.get("name", "") for label in issue.get("labels", [])}
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
    except (httpx.HTTPError, GitHubError):
        return None
    if not isinstance(repos, list):
        return None
    languages = Counter(repo.get("language") for repo in repos if repo.get("language"))
    sample = repos[:SIGNAL_TOPIC_SAMPLE]
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
    return [str(item) for item in data.get("names", [])]
