from datetime import date, datetime
from typing import Annotated, Literal

from pydantic import BaseModel, Field

Difficulty = Literal["beginner", "intermediate", "advanced"]
FieldEnum = Literal[
    "web-dev", "app-dev", "aiml", "data-science", "cyber-security", "devops-cloud", "blockchain",
]
DomainEnum = Literal[
    "healthcare", "education", "agriculture", "fintech", "climate", "governance",
    "transport", "disaster-management", "industry", "social-impact", "developer-tools", "cybersecurity", "computer-vision", "iot-embedded", "distributed-systems", "ml", "devops-cloud", "nlp-llm", "cloud", "blockchain", "web3", "databases", "systems", "other",
]
GoalEnum = Literal["resume", "hackathon", "learning"]


MAX_TITLE = 300
MAX_SUMMARY = 8000
MAX_SHORT = 2000
MAX_TAG = 40
MAX_DATASET_URL = 500

_problem_tag_item = Annotated[str, Field(min_length=1, max_length=MAX_TAG)]


class BuildGuidePhase(BaseModel):
    """One phase of a curated build guide (stack-agnostic roadmap)."""

    title: str = Field(min_length=1, max_length=200)
    summary: str = Field(default="", max_length=2000)
    steps: list[Annotated[str, Field(min_length=1, max_length=600)]] = Field(
        default_factory=list, max_length=12
    )


class TeamRole(BaseModel):
    """One person's job on a hackathon team."""

    role: str = Field(min_length=1, max_length=120)
    covers: str = Field(default="", max_length=2000)


class TeamPlan(BaseModel):
    note: str = Field(default="", max_length=2000)
    roles: list[TeamRole] = Field(default_factory=list, max_length=6)
    milestones: list[Annotated[str, Field(min_length=1, max_length=600)]] = (
        Field(default_factory=list, max_length=8)
    )


class PitchBeat(BaseModel):
    """One spoken part of the pitch, in order."""

    heading: str = Field(min_length=1, max_length=120)
    text: str = Field(default="", max_length=3000)


class JudgeQuestion(BaseModel):
    question: str = Field(min_length=1, max_length=600)
    answer: str = Field(default="", max_length=3000)


class PitchGuide(BaseModel):
    one_liner: str = Field(default="", max_length=600)
    beats: list[PitchBeat] = Field(default_factory=list, max_length=8)
    judge_questions: list[JudgeQuestion] = Field(default_factory=list, max_length=8)


class ScopeLevel(BaseModel):
    """MVP vs standout bar for a resume-track brief."""

    level: str = Field(min_length=1, max_length=120)
    text: str = Field(default="", max_length=3000)
    checks: list[Annotated[str, Field(min_length=1, max_length=600)]] = (
        Field(default_factory=list, max_length=10)
    )


class TargetRole(BaseModel):
    """Which job title this project signals, and how."""

    role: str = Field(min_length=1, max_length=120)
    how_it_helps: str = Field(default="", max_length=2000)


class ResumeBullet(BaseModel):
    """Bullet template for a CV, with a filled example."""

    bullet: str = Field(min_length=1, max_length=800)
    example: str = Field(default="", max_length=800)


class InterviewPoint(BaseModel):
    question: str = Field(min_length=1, max_length=600)
    answer: str = Field(default="", max_length=3000)


class ResumeKit(BaseModel):
    scope_levels: list[ScopeLevel] = Field(default_factory=list, max_length=2)
    target_roles: list[TargetRole] = Field(default_factory=list, max_length=6)
    resume_bullets: list[ResumeBullet] = Field(default_factory=list, max_length=4)
    interview_points: list[InterviewPoint] = Field(
        default_factory=list, max_length=8
    )
    differentiators: list[Annotated[str, Field(min_length=1, max_length=600)]] = (
        Field(default_factory=list, max_length=6)
    )


class ProblemCard(BaseModel):
    title: str = Field(min_length=1, max_length=MAX_TITLE)
    summary: str = Field(min_length=1, max_length=MAX_SUMMARY)
    who_affected: str = Field(min_length=1, max_length=MAX_SHORT)
    why_matters: str = Field(min_length=1, max_length=MAX_SHORT)
    field: FieldEnum
    domain: DomainEnum
    difficulty: Difficulty
    est_hours: int = Field(ge=1, le=1000)
    tech_tags: list[_problem_tag_item] = Field(max_length=25)
    datasets: list[dict] = Field(max_length=15)
    approaches: list[Annotated[str, Field(min_length=1, max_length=800)]] = Field(max_length=8)
    source_name: str = Field(min_length=1, max_length=MAX_TITLE)
    source_id: str | None = Field(default=None, max_length=100)
    source_url: str | None = Field(default=None, max_length=MAX_DATASET_URL)
    source_note: str | None = Field(default=None, max_length=MAX_TITLE)


class ProblemOut(ProblemCard):
    id: int
    project_count: int
    completed_count: int = 0
    ai_fields: list[str]
    origin: str = "manual"
    source_year: int | None = None
    edition: str | None = None
    organisation: str | None = None
    deadline: date | None = None
    goal: GoalEnum | None = None
    learning_concepts: list[str] = []
    build_guide: list[BuildGuidePhase] | None = None
    team_plan: TeamPlan | None = None
    pitch_guide: PitchGuide | None = None
    resume_kit: ResumeKit | None = None


class ProjectCreate(BaseModel):
    repo_url: str
    solution_summary: str | None = Field(default=None, max_length=400)
    demo_url: str | None = Field(default=None, max_length=500)
    open_for_contributors: bool = False


class ProjectPatch(BaseModel):
    """PATCH /api/projects/{id}: the repo link itself is immutable (§7.2)."""

    solution_summary: str | None = Field(default=None, max_length=400)
    open_for_contributors: bool | None = None
    demo_url: str | None = Field(default=None, max_length=500)


class CompleteIn(BaseModel):
    demo_url: str | None = Field(default=None, max_length=500)
    reflection: str | None = Field(default=None, max_length=800)


class CompletionChecklistItem(BaseModel):
    item: str
    ok: bool


class HeatmapDay(BaseModel):
    """One day of public GitHub push activity (UTC date)."""

    date: str  # YYYY-MM-DD
    count: int


class HeatmapOut(BaseModel):
    days: list[HeatmapDay]
    total: int
    window_days: int


class ReportIn(BaseModel):
    reason: str = Field(min_length=1, max_length=300)


class AdminSubmissionOut(BaseModel):
    id: int
    problem_id: int
    problem_title: str
    repo_url: str
    repo_owner: str
    repo_name: str
    submitter: str
    submitter_avatar_url: str | None = None
    verification_status: str
    ownership_basis: str | None = None
    relevance_score: float | None = None
    relevance_reason: str | None = None
    solution_summary: str | None = None
    review_note: str | None = None
    demo_url: str | None = None
    reflection: str | None = None
    open_for_contributors: bool
    report_count: int = 0
    created_at: datetime
    completed_at: datetime | None = None


class AdminSubmissionsOut(BaseModel):
    items: list[AdminSubmissionOut]
    total: int


class AdminSubmissionActionOut(BaseModel):
    ok: bool
    project_id: int
    verification_status: str


class Progress(BaseModel):
    status: Literal["not_started", "active", "stale"]
    commit_count: int
    last_commit_at: str | None
    has_readme: bool
    recent_commits: list[dict]
    open_issues: list[dict]


class ProjectOut(BaseModel):
    id: int
    problem_id: int
    problem_title: str
    repo_url: str
    repo_owner: str
    repo_name: str
    open_for_contributors: bool
    owner: dict
    progress: Progress | None
    progress_updated_at: datetime | None
    verification_status: str = "needs_review"
    solution_summary: str | None = None
    completed_at: datetime | None = None
    demo_url: str | None = None
    reflection: str | None = None
    # stars: total count is public; starred_by_me needs a logged-in viewer
    # (False for anonymous requests)
    star_count: int = 0
    starred_by_me: bool = False
    # owner/admin-only fields: never shown to anonymous viewers or other users
    relevance_reason: str | None = None
    ownership_basis: str | None = None
    review_note: str | None = None


class ProblemDetail(ProblemOut):
    original_text: str
    projects: list[ProjectOut]
    display_policy: Literal["summary_only", "summary_plus_excerpt"] = "summary_plus_excerpt"


class ProblemIn(ProblemCard):
    """POST /api/problems body: the ProblemCard contract above, plus optional
    ai_fields (a curated ingest may mark which fields the AI authored)."""

    ai_fields: list[str] = []


class RecommendationItem(BaseModel):
    problem: ProblemOut
    score: int
    reasons: list[str]


class RecommendationsOut(BaseModel):
    items: list[RecommendationItem]


class ChatMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str = Field(min_length=1, max_length=1000)


class ChatPageContext(BaseModel):
    problem_id: int | None = Field(default=None, ge=1)


class ChatIn(BaseModel):
    messages: list[ChatMessage] = Field(max_length=12, min_length=1)
    page_context: ChatPageContext | None = None


class ChatProblemItem(BaseModel):
    id: int
    title: str
    field: FieldEnum
    difficulty: Difficulty


class ChatOut(BaseModel):
    reply: str
    problems: list[ChatProblemItem]


class Facet(BaseModel):
    value: str
    count: int
    last_updated: datetime | None = None


class FacetsOut(BaseModel):
    fields: list[Facet]
    domains: list[Facet]
    difficulties: list[Facet]
    tech_tags: list[Facet]
    sources: list[Facet]


class StatsOut(BaseModel):
    problems: int
    sources: int
    fields: int
    projects: int


class ProblemsListOut(BaseModel):
    items: list[ProblemOut]
    total: int


class AdminGoalSetIn(BaseModel):
    goal: GoalEnum | None = None


class AdminGoalOut(BaseModel):
    ok: bool
    problem_id: int
    goal: GoalEnum | None = None


