from typing import Annotated

from fastapi import Depends, HTTPException, Request
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.config import get_settings
from app.db import get_db
from app.models import User

DB = Annotated[Session, Depends(get_db)]


def _admin_usernames() -> set[str]:
    raw = get_settings().ADMIN_GITHUB_USERNAMES
    return {name.strip().lower() for name in raw.split(",") if name.strip()}


def get_current_user(request: Request, db: DB) -> User:
    user_id = request.session.get("user_id")
    if user_id is None:
        raise HTTPException(status_code=401, detail="Not logged in")
    user = db.scalar(select(User).where(User.id == user_id))
    if user is None:
        raise HTTPException(status_code=401, detail="Not logged in")
    return user


# Annotations are evaluated when a module is imported on Python < 3.14, so each
# alias below must be defined before the dependency that annotates with it.
CurrentUser = Annotated[User, Depends(get_current_user)]


def get_optional_user(request: Request, db: DB) -> User | None:
    user_id = request.session.get("user_id")
    if user_id is None:
        return None
    return db.scalar(select(User).where(User.id == user_id))

OptionalUser = Annotated[User | None, Depends(get_optional_user)]


def get_current_admin(user: CurrentUser) -> User:
    if user.username.lower() not in _admin_usernames():
        raise HTTPException(status_code=403, detail="Admin access required")
    return user


AdminUser = Annotated[User, Depends(get_current_admin)]


def public_user(user: User) -> dict:
    return {"id": user.id, "username": user.username, "name": user.name, "avatar_url": user.avatar_url}


__all__ = [
    "get_current_user",
    "get_optional_user",
    "get_current_admin",
    "public_user",
    "get_db",
    "DB",
    "CurrentUser",
    "OptionalUser",
    "AdminUser",
]
