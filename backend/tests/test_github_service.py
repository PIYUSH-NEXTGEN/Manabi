import httpx
import pytest
import respx
from httpx import Response as HTTPResponse

from app.services import github
from app.services.github import GitHubError


@pytest.mark.anyio
async def test_get_repo_treats_private_repo_as_not_found():
    with respx.mock(assert_all_called=False) as mock:
        mock.get("https://api.github.com/repos/owner/private").mock(
            return_value=HTTPResponse(200, json={"private": True, "full_name": "owner/private"})
        )
        with pytest.raises(GitHubError) as caught:
            await github.get_repo("owner", "private")
    assert caught.value.status == 404


@pytest.mark.anyio
async def test_contributors_status_mapping():
    with respx.mock(assert_all_called=False) as mock:
        mock.get("https://api.github.com/repos/o/r/contributors").mock(
            return_value=HTTPResponse(403, json={"message": "rate limit"})
        )
        with pytest.raises(GitHubError) as caught:
            await github.fetch_contributors("o", "r")
        assert caught.value.status == 403

    with respx.mock(assert_all_called=False) as mock:
        mock.get("https://api.github.com/repos/o/missing/contributors").mock(
            return_value=HTTPResponse(404, json={})
        )
        assert await github.fetch_contributors("o", "missing") == []


@pytest.mark.anyio
async def test_fetch_json_maps_transport_failure_to_502():
    with respx.mock(assert_all_called=False) as mock:
        mock.get("https://api.github.com/repos/o/r").mock(
            side_effect=httpx.ConnectError("network down")
        )
        with pytest.raises(GitHubError) as caught:
            await github.get_repo("o", "r")
    assert caught.value.status == 502


@pytest.mark.anyio
async def test_user_signals_aggregate_languages_and_topics():
    repos = [
        {"name": "alpha", "language": "Python", "owner": {"login": "octo"}},
        {"name": "beta", "language": "Python", "owner": {"login": "octo"}},
        {"name": "gamma", "language": None, "owner": {"login": "octo"}},
    ]
    with respx.mock(assert_all_called=False) as mock:
        mock.get("https://api.github.com/user/repos").mock(
            return_value=HTTPResponse(200, json=repos)
        )
        mock.get("https://api.github.com/repos/octo/alpha/topics").mock(
            return_value=HTTPResponse(200, json={"names": ["flask", "ml"]})
        )
        mock.get("https://api.github.com/repos/octo/beta/topics").mock(
            return_value=HTTPResponse(500, json={})
        )
        mock.get("https://api.github.com/repos/octo/gamma/topics").mock(
            return_value=HTTPResponse(200, json={"names": ["flask"]})
        )
        signals = await github.get_user_signals("token")

    assert signals == {"languages": {"Python": 2}, "topics": ["flask", "ml"]}


@pytest.mark.anyio
async def test_user_signals_returns_none_when_github_fails():
    with respx.mock(assert_all_called=False) as mock:
        mock.get("https://api.github.com/user/repos").mock(
            return_value=HTTPResponse(403, json={"message": "rate limit"})
        )
        assert await github.get_user_signals("token") is None


def test_repo_created_at_rejects_missing_or_invalid_values():
    assert github.repo_created_at({}) is None
    assert github.repo_created_at({"created_at": "not-a-date"}) is None
