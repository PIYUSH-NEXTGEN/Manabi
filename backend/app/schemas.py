from datetime import datetime
from typing import Annotated, Literal

from pydantic import BaseModel, Field

Difficulty = Literal["beginner", "intermediate", "advanced"]
FieldEnum = Literal[
    "ml", "computer-vision", "nlp-llm", "cybersecurity", "web-fullstack", "mobile",
    "data-engineering", "geospatial", "optimization", "iot-embedded",
    "distributed-systems", "blockchain", "devops-cloud", "other",
]
DomainEnum = Literal[
    "healthcare", "education", "agriculture", "fintech", "climate", "governance",
    "transport", "disaster-management", "industry", "social-impact", "developer-tools", "other",
]


MAX_TITLE = 300
MAX_SUMMARY = 8000
MAX_SHORT = 2000
MAX_TAG = 40
MAX_DATASET_URL = 500

_problem_tag_item = Annotated[str, Field(min_length=1, max_length=MAX_TAG)]


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
    ai_fields: list[str]


class ProjectCreate(BaseModel):
    repo_url: str
    open_for_contributors: bool = False


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


class ProblemDetail(ProblemOut):
    original_text: str
    projects: list[ProjectOut]


class DatasetIn(BaseModel):
    name: str
    url: str | None = None


class IngestRequest(BaseModel):
    url: str | None = None
    text: str | None = None


class IngestOut(BaseModel):
    draft: ProblemCard
    evidence: dict[str, str]
    source_url: str | None


class ProblemIn(ProblemCard):
    """POST /api/problems body: ProblemCard per contract, plus optional ai_fields (see docs/REQUESTS.md)."""

    ai_fields: list[str] = []


class MLQuestionListItem(BaseModel):
    id: int
    title: str
    difficulty: str
    topic: str
    attempted: bool


class MLQuestionDetail(BaseModel):
    id: int
    title: str
    scenario: str
    difficulty: str
    topic: str
    attempted: bool


class AttemptIn(BaseModel):
    answer: str = Field(min_length=20, max_length=4000)


class FeedbackItem(BaseModel):
    point: str
    covered: bool
    evidence: str | None = None


class Feedback(BaseModel):
    covered_count: int
    total: int
    items: list[FeedbackItem]
    summary: str


class AttemptOut(BaseModel):
    id: int
    answer: str
    created_at: datetime
    feedback: Feedback
    explanation: str


class GradedRubricItem(BaseModel):
    """LLM output for one rubric point."""
    id: str
    covered: bool
    evidence: str | None = None


class GradingOut(BaseModel):
    items: list[GradedRubricItem]
    summary: str


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
    ml_questions: int


class ProblemsListOut(BaseModel):
    items: list[ProblemOut]
    total: int
