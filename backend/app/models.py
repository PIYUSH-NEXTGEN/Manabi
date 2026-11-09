from datetime import date, datetime, timezone

from sqlalchemy import JSON, Boolean, Date, DateTime, Float, ForeignKey, Index, Integer, String, Text, UniqueConstraint, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


# Review-lifecycle values for Problem.status (§6.2). Public read paths only
# ever surface PUBLISHED rows; everything else lives in the review queue.
STATUS_PUBLISHED = "published"
STATUS_PENDING_REVIEW = "pending_review"
STATUS_REJECTED = "rejected"
STATUS_REMOVED = "removed"

ORIGIN_MANUAL = "manual"

# Project submission verification (§5). Hard GitHub/LLM failures mean a
# submission is rejected at submit time with no row at all; this column tracks
# the lifecycle of stored rows.
VERIFICATION_VERIFIED = "verified"
VERIFICATION_NEEDS_REVIEW = "needs_review"
VERIFICATION_REJECTED = "rejected"
VERIFICATION_STATUSES = (VERIFICATION_VERIFIED, VERIFICATION_NEEDS_REVIEW, VERIFICATION_REJECTED)

OWNERSHIP_OWNER = "owner"
OWNERSHIP_PUSH_ACCESS = "push_access"
OWNERSHIP_CONTRIBUTOR = "contributor"

# Manual track curation (§ board "Browse by goal"): admins label a problem as
# resume / hackathon / learning material. Null = unlabelled (never filtered in).
GOAL_RESUME = "resume"
GOAL_HACKATHON = "hackathon"
GOAL_LEARNING = "learning"
GOAL_VALUES = (GOAL_RESUME, GOAL_HACKATHON, GOAL_LEARNING)


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    github_id: Mapped[int] = mapped_column(Integer, unique=True, index=True)
    username: Mapped[str] = mapped_column(String(255), index=True)
    name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    avatar_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    github_token: Mapped[str | None] = mapped_column(String(255), nullable=True)
    signals_json: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    signals_updated_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow, nullable=False)

    projects: Mapped[list["Project"]] = relationship(back_populates="user")


class Problem(Base):
    __tablename__ = "problems"
    __table_args__ = (UniqueConstraint("source_name", "source_id", name="uq_problem_source"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    who_affected: Mapped[str] = mapped_column(Text, nullable=False)
    why_matters: Mapped[str] = mapped_column(Text, nullable=False)
    field: Mapped[str] = mapped_column(String(50), index=True, nullable=False)
    domain: Mapped[str] = mapped_column(String(50), index=True, nullable=False)
    difficulty: Mapped[str] = mapped_column(String(20), index=True, nullable=False)
    est_hours: Mapped[int] = mapped_column(Integer, nullable=False)
    tech_tags: Mapped[list] = mapped_column(JSON, default=list, nullable=False)
    datasets: Mapped[list] = mapped_column(JSON, default=list, nullable=False)
    approaches: Mapped[list] = mapped_column(JSON, default=list, nullable=False)
    source_name: Mapped[str] = mapped_column(String(255), nullable=False)
    source_id: Mapped[str | None] = mapped_column(String(100), nullable=True)
    source_url: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    source_note: Mapped[str | None] = mapped_column(Text, nullable=True)
    original_text: Mapped[str] = mapped_column(Text, nullable=False)
    ai_fields: Mapped[list] = mapped_column(JSON, default=list, nullable=False)
    created_by: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow, nullable=False)

    # Review lifecycle: public read paths only ever surface published rows;
    # origin marks manual curation now that the crawler is gone.
    status: Mapped[str] = mapped_column(String(20), default=STATUS_PUBLISHED, nullable=False)
    origin: Mapped[str] = mapped_column(String(20), default=ORIGIN_MANUAL, nullable=False)
    source_year: Mapped[int | None] = mapped_column(Integer, nullable=True)
    edition: Mapped[str | None] = mapped_column(String(100), nullable=True)
    organisation: Mapped[str | None] = mapped_column(String(255), nullable=True)
    deadline: Mapped[date | None] = mapped_column(Date, nullable=True)
    goal: Mapped[str | None] = mapped_column(String(20), nullable=True)

    creator: Mapped[User | None] = relationship()
    projects: Mapped[list["Project"]] = relationship(back_populates="problem")


class Project(Base):
    __tablename__ = "projects"
    __table_args__ = (
        UniqueConstraint("problem_id", "user_id", "repo_owner", "repo_name", name="uq_project_repo"),
        # One GitHub repo (immutable id) may be submitted by a user at most once
        # across everything; null repo_github_id (legacy rows) is exempt.
        Index(
            "uq_project_repo_github_id_user_id",
            "repo_github_id",
            "user_id",
            unique=True,
            sqlite_where=text("repo_github_id IS NOT NULL"),
            postgresql_where=text("repo_github_id IS NOT NULL"),
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    problem_id: Mapped[int] = mapped_column(ForeignKey("problems.id"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    repo_owner: Mapped[str] = mapped_column(String(255), nullable=False)
    repo_name: Mapped[str] = mapped_column(String(255), nullable=False)
    repo_url: Mapped[str] = mapped_column(String(1000), nullable=False)
    open_for_contributors: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    progress_json: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    progress_updated_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow, nullable=False)

    # --- submission verification (0005) ---
    verification_status: Mapped[str] = mapped_column(
        String(20), default=VERIFICATION_NEEDS_REVIEW, nullable=False, index=True
    )
    ownership_basis: Mapped[str | None] = mapped_column(String(20), nullable=True)
    solution_summary: Mapped[str] = mapped_column(Text, default="", nullable=False)
    relevance_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    relevance_reason: Mapped[str | None] = mapped_column(String(300), nullable=True)
    relevance_checked_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    review_note: Mapped[str | None] = mapped_column(Text, nullable=True)
    repo_github_id: Mapped[int | None] = mapped_column(Integer, nullable=True, index=True)
    repo_created_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    demo_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    reflection: Mapped[str | None] = mapped_column(Text, nullable=True)

    problem: Mapped[Problem] = relationship(back_populates="projects")
    user: Mapped[User] = relationship(back_populates="projects")
    reports: Mapped[list["ProjectReport"]] = relationship(
        back_populates="project", cascade="all, delete-orphan"
    )


class ProjectReport(Base):
    __tablename__ = "project_reports"
    __table_args__ = (UniqueConstraint("project_id", "reporter_user_id", name="uq_project_report_project_reporter"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    project_id: Mapped[int] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True
    )
    reporter_user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    reason: Mapped[str] = mapped_column(String(300), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow, nullable=False)

    project: Mapped[Project] = relationship(back_populates="reports")
