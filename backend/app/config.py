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
