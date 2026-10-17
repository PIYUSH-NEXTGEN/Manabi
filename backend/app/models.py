from datetime import datetime, timezone

from sqlalchemy import JSON, Boolean, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


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
    attempts: Mapped[list["MLAttempt"]] = relationship(back_populates="user")


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

    creator: Mapped[User | None] = relationship()
    projects: Mapped[list["Project"]] = relationship(back_populates="problem")


class Project(Base):
    __tablename__ = "projects"
    __table_args__ = (
        UniqueConstraint("problem_id", "user_id", "repo_owner", "repo_name", name="uq_project_repo"),
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

    problem: Mapped[Problem] = relationship(back_populates="projects")
    user: Mapped[User] = relationship(back_populates="projects")


class MLQuestion(Base):
    __tablename__ = "ml_questions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    scenario: Mapped[str] = mapped_column(Text, nullable=False)
    difficulty: Mapped[str] = mapped_column(String(20), nullable=False)
    topic: Mapped[str] = mapped_column(String(50), index=True, nullable=False)
    rubric_json: Mapped[list] = mapped_column(JSON, nullable=False)
    explanation: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow, nullable=False)

    attempts: Mapped[list["MLAttempt"]] = relationship(back_populates="question")


class MLAttempt(Base):
    __tablename__ = "ml_attempts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    question_id: Mapped[int] = mapped_column(ForeignKey("ml_questions.id"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    answer: Mapped[str] = mapped_column(Text, nullable=False)
    feedback_json: Mapped[dict] = mapped_column(JSON, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow, nullable=False)

    question: Mapped[MLQuestion] = relationship(back_populates="attempts")
    user: Mapped[User] = relationship(back_populates="attempts")
