from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy import select
from starlette.middleware.sessions import SessionMiddleware
from typing import Annotated

from authlib.integrations.base_client.errors import MismatchingStateError
from authlib.integrations.starlette_client import OAuth
from fastapi import Depends

from app.config import get_settings
from app.deps import DB, get_current_user
from app.models import User

router = APIRouter(prefix="/api/auth", tags=["auth"])

oauth = OAuth()


def setup_oauth(app) -> None:
    settings = get_settings()
    app.add_middleware(
        SessionMiddleware,
        secret_key=settings.SESSION_SECRET,
        same_site="lax",
        https_only=settings.BASE_URL.startswith("https"),
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


CurrentUser = Annotated[User, Depends(get_current_user)]


@router.get("/github/login")
async def github_login(request: Request):
    client = get_github_client()
    if client is None:
        raise HTTPException(status_code=503, detail="GitHub login is not configured yet")
    redirect_uri = f"{get_settings().BASE_URL}/api/auth/github/callback"
    return await client.authorize_redirect(request, redirect_uri)


@router.get("/github/callback")
async def github_callback(request: Request, db: DB):
    client = get_github_client()
    if client is None:
        raise HTTPException(status_code=503, detail="GitHub login is not configured yet")
    try:
        token = await client.authorize_access_token(request)
    except MismatchingStateError:
        raise HTTPException(status_code=403, detail="Login failed: CSRF state mismatch")
    profile_response = await client.get("user", token=token)
    profile = profile_response.json()
    github_id = profile.get("id")
    if github_id is None:
        raise HTTPException(status_code=502, detail="GitHub did not return a user profile")

    user = db.scalar(select(User).where(User.github_id == github_id))
    if user is None:
        user = User(
            github_id=github_id,
            username=profile.get("login") or f"user-{github_id}",
            name=profile.get("name"),
            avatar_url=profile.get("avatar_url"),
        )
        db.add(user)
    else:
        user.username = profile.get("login") or user.username
        user.name = profile.get("name")
        user.avatar_url = profile.get("avatar_url")
    token_string = None
    if isinstance(token, dict) and token.get("access_token"):
        token_string = token["access_token"]
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
    }


@router.post("/logout")
def logout(request: Request):
    request.session.pop("user_id", None)
    return {"ok": True}
