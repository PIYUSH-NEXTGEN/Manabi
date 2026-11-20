import httpx
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy import select
from starlette.middleware.sessions import SessionMiddleware

from authlib.integrations.base_client.errors import MismatchingStateError, OAuthError
from authlib.integrations.starlette_client import OAuth

from app.config import get_settings
from app.deps import CurrentUser, DB
from app.models import User
from app.services.ratelimit import RateLimiter, human_wait, rate_limited
from app.services.visibility import is_admin

router = APIRouter(prefix="/api/auth", tags=["auth"])

# Login touches GitHub's OAuth infrastructure on every hit and creates
# session traffic. Keyed per IP: one shared NAT may hold a whole campus, so
# the cap stays generous but still stops scripted hammering.
LOGIN_LIMITER = RateLimiter("AUTH_LOGIN_RATE_LIMIT_PER_HOUR")


def _client_ip(request: Request) -> str:
    return request.client.host if request.client else "unknown"


def _login_block(db, request: Request) -> int | None:
    """Seconds until retry, or None when this attempt may proceed."""
    return LOGIN_LIMITER.check(db, f"login-ip:{_client_ip(request)}")


def _profile_text(value, limit: int) -> str | None:
    """A trimmed, length-bounded profile string; malformed values become None."""
    if not isinstance(value, str):
        return None
    value = value.strip()
    return value[:limit] or None

oauth = OAuth()


def setup_oauth(app) -> None:
    settings = get_settings()
    app.add_middleware(
        SessionMiddleware,
        secret_key=settings.SESSION_SECRET,
        same_site="lax",
        https_only=settings.APP_ENV == "production"
        or settings.BASE_URL.startswith("https://"),
    )


def get_github_client():
    settings = get_settings()
    if not (settings.GITHUB_CLIENT_ID and settings.GITHUB_CLIENT_SECRET):
        return None
    try:
        return oauth.github
    except AttributeError:
        oauth.register(
            name="github",
            client_id=settings.GITHUB_CLIENT_ID,
            client_secret=settings.GITHUB_CLIENT_SECRET,
            access_token_url="https://github.com/login/oauth/access_token",
            authorize_url="https://github.com/login/oauth/authorize",
            api_base_url="https://api.github.com/",
            client_kwargs={"scope": "read:user"},
        )
        return oauth.github


@router.get("/github/login")
async def github_login(request: Request, db: DB):
    if (retry := _login_block(db, request)) is not None:
        raise rate_limited(retry, f"Too many login attempts. Try again in {human_wait(retry)}.")
    client = get_github_client()
    if client is None:
        raise HTTPException(status_code=503, detail="GitHub login is not configured yet")
    redirect_uri = f"{get_settings().BASE_URL}/api/auth/github/callback"
    return await client.authorize_redirect(request, redirect_uri)


@router.get("/github/callback")
async def github_callback(request: Request, db: DB):
    if (retry := _login_block(db, request)) is not None:
        raise rate_limited(retry, f"Too many login attempts. Try again in {human_wait(retry)}.")
    client = get_github_client()
    if client is None:
        raise HTTPException(status_code=503, detail="GitHub login is not configured yet")
    try:
        token = await client.authorize_access_token(request)
    except MismatchingStateError:
        raise HTTPException(status_code=403, detail="Login failed: CSRF state mismatch")
    try:
        profile_response = await client.get("user", token=token)
    except (httpx.HTTPError, OAuthError):
        raise HTTPException(status_code=502, detail="Could not fetch your GitHub profile")
    try:
        profile = profile_response.json()
    except ValueError:
        raise HTTPException(status_code=502, detail="GitHub did not return a user profile")
    if not isinstance(profile, dict):
        raise HTTPException(status_code=502, detail="GitHub did not return a user profile")
    github_id = profile.get("id")
    # A GitHub id is a positive integer. Reject strings, floats and bools so a
    # malformed API payload cannot create an unaddressable user row.
    if not isinstance(github_id, int) or isinstance(github_id, bool) or github_id <= 0:
        raise HTTPException(status_code=502, detail="GitHub did not return a user profile")

    username = _profile_text(profile.get("login"), 255) or f"user-{github_id}"
    name = _profile_text(profile.get("name"), 255)
    avatar_url = _profile_text(profile.get("avatar_url"), 500)
    user = db.scalar(select(User).where(User.github_id == github_id))
    if user is None:
        user = User(
            github_id=github_id,
            username=username,
            name=name,
            avatar_url=avatar_url,
        )
        db.add(user)
    else:
        user.username = username
        user.name = name
        user.avatar_url = avatar_url
    token_string = None
    if isinstance(token, dict) and isinstance(token.get("access_token"), str):
        candidate = token["access_token"]
        if 0 < len(candidate) <= 255:
            token_string = candidate
    if token_string:
        user.github_token = token_string
    db.commit()
    db.refresh(user)

    request.session["user_id"] = user.id
    response = RedirectResponse("/", status_code=302)
    return response


@router.get("/me")
def me(user: CurrentUser):
    return {
        "id": user.id,
        "username": user.username,
        "name": user.name,
        "avatar_url": user.avatar_url,
        "is_admin": is_admin(user),
    }


@router.post("/logout")
def logout(request: Request):
    request.session.pop("user_id", None)
    return {"ok": True}
