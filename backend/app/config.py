from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    DATABASE_URL: str = "sqlite:///./app.db"
    SESSION_SECRET: str = "change-me-long-random-string"
    BASE_URL: str = "http://localhost:5173"
    GITHUB_CLIENT_ID: str = ""
    GITHUB_CLIENT_SECRET: str = ""
    LLM_PROVIDER: str = "mock"
    GEMINI_API_KEY: str = ""
    GEMINI_MODEL: str = ""
    ANTHROPIC_API_KEY: str = ""
    LLM_MODEL_FAST: str = ""
    CHAT_RATE_LIMIT_ANON_PER_HOUR: int = 10
    CHAT_RATE_LIMIT_USER_PER_HOUR: int = 30

    # --- Content curation ---
    # Problem creation is an authenticated publishing action with LLM/AI cost
    # imports only for ingest; the catalog is admin-curated, so user limits
    # track the moderation posture (admins exempt below).
    PROBLEM_CREATE_PER_HOUR: int = 5
    # Reports against published projects, per user per hour. Independent of the
    # chat limit so tuning one cannot silently retune the other.
    REPORT_RATE_LIMIT_PER_HOUR: int = 30

    # --- Admin ---
    ADMIN_GITHUB_USERNAMES: str = ""

    # --- Project submission verification ---
    RELEVANCE_VERIFY_MIN: float = 0.70
    RELEVANCE_REJECT_BELOW: float = 0.35
    CONTRIBUTOR_MIN_COMMITS: int = 3
    COMPLETE_MIN_COMMITS: int = 5
    MAX_ACTIVE_PROJECTS_PER_USER: int = 10
    MAX_SUBMISSIONS_PER_DAY: int = 5
    PREEXISTING_REPO_DAYS: int = 180
    ALLOW_FORK_SUBMISSIONS: bool = False
    AUTO_REVERIFY_MIN_INTERVAL_HOURS: int = 24
    REPORTS_BEFORE_REVIEW: int = 3


@lru_cache
def get_settings() -> Settings:
    return Settings()
