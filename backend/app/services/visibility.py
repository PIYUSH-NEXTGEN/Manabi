"""Project submission visibility (§7.4): only verified rows are public.

- Anonymous visitors and other users see only `verified` projects, everywhere
  (problem detail, counts, stats, chat context, public profiles).
- The owner and admins see a row in every status.
- Owner/admin-only fields in ProjectOut never appear for anyone else.
"""

from app.config import get_settings
from app.models import Project, User, VERIFICATION_VERIFIED


def admin_usernames() -> set[str]:
    """ADMIN_GITHUB_USERNAMES parsed once here; deps and visibility share it."""
    raw = get_settings().ADMIN_GITHUB_USERNAMES
    return {name.strip().lower() for name in raw.split(",") if name.strip()}


def is_admin(user: User | None) -> bool:
    if user is None:
        return False
    return bool(user.username) and user.username.lower() in admin_usernames()


def is_owner_or_admin(project: Project, user: User | None) -> bool:
    """The single ownership rule: edit/remove rights and private fields."""
    return user is not None and (user.id == project.user_id or is_admin(user))


def can_view_project(project: Project, user: User | None) -> bool:
    """Verified rows are public; owners and admins see every row."""
    if project.verification_status == VERIFICATION_VERIFIED:
        return True
    return is_owner_or_admin(project, user)


def filter_visible(projects: list[Project], user: User | None) -> list[Project]:
    return [p for p in projects if can_view_project(p, user)]
