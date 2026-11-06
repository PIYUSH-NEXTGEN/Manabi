"""Project submission visibility (§7.4): only verified rows are public.

- Anonymous visitors and other users see only `verified` projects, everywhere
  (problem detail, counts, stats, chat context, public profiles).
- The owner and admins see a row in every status.
- Owner/admin-only fields in ProjectOut never appear for anyone else.
"""

from app.config import get_settings
from app.models import Project, User, VERIFICATION_VERIFIED


def is_admin(user: User | None) -> bool:
    if user is None:
        return False
    raw = get_settings().ADMIN_GITHUB_USERNAMES
    admins = {name.strip().lower() for name in raw.split(",") if name.strip()}
    return bool(user.username) and user.username.lower() in admins


def can_view_project(project: Project, user: User | None) -> bool:
    """Verified rows are public; owners and admins see every row."""
    if project.verification_status == VERIFICATION_VERIFIED:
        return True
    return user is not None and (user.id == project.user_id or is_admin(user))


def filter_visible(projects: list[Project], user: User | None) -> list[Project]:
    return [p for p in projects if can_view_project(p, user)]
