"""Re-run relevance verification for existing projects (one-time production
migration after the 0005 backfill).

Dry run (default): prints what WOULD change and writes backend/scripts/reverify_report.csv.

  python backend/scripts/reverify_projects.py            # dry run, all rows
  python backend/scripts/reverify_projects.py --apply    # write changes
  python backend/scripts/reverify_projects.py --limit 2  # cap how many rows

Notes:
- Uses each project owner's stored GitHub token when there is one (§6.7).
  Tokens are NEVER printed or written to the CSV.
- Never verifies on fallback: no LLM answer -> needs_review at best.
"""

import asyncio
import argparse
import csv
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import select  # noqa: E402

from app.db import get_session_factory  # noqa: E402
from app.models import Problem, Project, User, utcnow  # noqa: E402
from app.services import github  # noqa: E402
from app.services.verification import (  # noqa: E402
    OWNERSHIP_OWNER,
    OWNERSHIP_PUSH_ACCESS,
    RepoFacts,
    VERIFICATION_NEEDS_REVIEW,
    evaluate_relevance,
)


REPORT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "reverify_report.csv")


def _ownership_from_facts(facts: RepoFacts, user: User | None) -> str | None:
    if user is None:
        return None
    if facts.owner_type != "Organization":
        if facts.owner_id is not None and facts.owner_id == user.github_id:
            return OWNERSHIP_OWNER
        return None
    if facts.permissions.get("admin") or facts.permissions.get("push"):
        return OWNERSHIP_PUSH_ACCESS
    return None


async def main(apply: bool, limit: int | None) -> None:
    db = get_session_factory()()
    results = []  # (project_id, user_id, token_display, old, new, reason, action)
    try:
        projects = db.scalars(select(Project).order_by(Project.id)).all()
        problems = {
            p.id: p
            for p in db.scalars(select(Problem).where(Problem.id.in_({pr.problem_id for pr in projects}))).all()
        }
        users = {u.id: u for u in db.scalars(select(User)).all()}

        for project in projects:
            if limit is not None and len(results) >= limit:
                break
            user = users.get(project.user_id)
            token_display = "stored" if user and user.github_token else "none"
            token = user.github_token if user else None
            problem = problems.get(project.problem_id)

            old_status = project.verification_status
            new_status = old_status
            reason = ""
            action = "dry-run"

            if problem is None:
                reason = "no problem row"
            else:
                try:
                    repo = await github.get_repo(project.repo_owner, project.repo_name, token)
                except Exception as exc:  # noqa: BLE001 - report and continue
                    status = getattr(exc, "status", None)
                    reason = f"github error {status or 'unknown'}"
                    if apply and status == 404:
                        project.verification_status = VERIFICATION_NEEDS_REVIEW
                        project.relevance_reason = "Repository no longer found or is no longer public"
                        db.commit()
                        action = "applied"
                        new_status = project.verification_status
                else:
                    facts = RepoFacts.from_repo(repo)
                    readme = await github.fetch_readme_text(facts.owner_login, facts.name, token)
                    try:
                        commits = await github._fetch_commits(facts.owner_login, facts.name, token)
                        commit_count = len(commits) if isinstance(commits, list) else 1
                    except Exception:  # noqa: BLE001
                        commit_count = 1

                    renamed = (
                        project.repo_github_id is not None and facts.github_id != project.repo_github_id
                    ) or (
                        project.repo_github_id is None
                        and facts.owner_login.lower() != project.repo_owner.lower()
                    )
                    evaluation = evaluate_relevance(
                        problem, project.solution_summary or "", facts, readme, commit_count
                    )
                    reason = "Repository was renamed or transferred" if renamed else (evaluation.reason or "")
                    new_status = VERIFICATION_NEEDS_REVIEW if renamed else evaluation.status
                    if apply:
                        project.repo_owner = facts.owner_login
                        project.repo_name = facts.name
                        project.repo_url = facts.url
                        project.repo_github_id = facts.github_id or project.repo_github_id
                        project.relevance_score = evaluation.score
                        project.relevance_reason = reason[:300] or None
                        project.relevance_checked_at = utcnow()
                        project.verification_status = new_status
                        owner_basis = _ownership_from_facts(facts, user)
                        if owner_basis:
                            project.ownership_basis = owner_basis
                        db.commit()
                        action = "applied"

            results.append((project.id, project.user_id, token_display, old_status, new_status, reason, action))
    finally:
        db.close()

    with open(REPORT_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["project_id", "user_id", "token", "old_status", "new_status", "reason", "action"])
        writer.writerows(results)

    mode = "APPLIED" if apply else "DRY RUN"
    print(f"{mode} — {len(results)} projects, report: {REPORT_PATH}")
    for pid, uid, token_display, old, new, reason, action in results:
        print(f"  project {pid} (user {uid}, token: {token_display}): {old} -> {new} — {reason[:120]} [{action}]")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true", help="write changes (default is dry run)")
    parser.add_argument("--limit", type=int, default=None, help="max projects to process")
    args = parser.parse_args()
    asyncio.run(main(args.apply, args.limit))
