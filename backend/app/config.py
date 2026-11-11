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
    # Optional dedicated Gemini project for the catalog chat, so chat traffic
    # shares no quota with submission evaluation. Empty falls back to the
    # shared GEMINI_API_KEY (both features on one project's quota).
    GEMINI_API_KEY_CHAT: str = ""
    GEMINI_MODEL_CHAT: str = ""
    ANTHROPIC_API_KEY: str = ""
    LLM_MODEL_FAST: str = ""
    # Chat is login-only. The daily cap is the budget guard (each message is
    # a paid LLM call), keyed per account. No hourly burst cap by choice:
    # a heavy user may spend the whole allowance in one session.
    CHAT_RATE_LIMIT_PER_DAY: int = 20

    # Submit attempts on the "Submit project" button. Every attempt costs
    # 2-3 GitHub API calls even when rejected, so failures and successes
    # share one hourly bucket per account; stacked with the 5/day and
    # 10-active-project quotas.
    SUBMIT_RATE_LIMIT_PER_HOUR: int = 10

    # Login (both the redirect and the OAuth callback) hits GitHub's OAuth
    # infrastructure and creates session traffic; real users log in a few
    # times a day, so this only bites scripted hammering. Keyed per IP.
    AUTH_LOGIN_RATE_LIMIT_PER_HOUR: int = 20

    # Star/unstar toggles on projects and problems; each click is a DB write.
    # Manual users never approach this; it stops accidental loops and scripts.
    STAR_RATE_LIMIT_PER_HOUR: int = 60

    # Sanity cap for admins, who bypass the per-user limits on problem
    # creation and progress refresh. Real admin work stays far below it;
    # a runaway or hijacked admin session gets stopped at 100/h instead of
    # silently draining the shared GitHub API quota.
    ADMIN_RATE_LIMIT_PER_HOUR: int = 100

    # Forcing a progress refresh (refresh=true) makes the server call GitHub's
    # API and can write back to the DB. Project owners are exempt; everyone
    # else (including anonymous visitors) shares this modest quota because
    # GitHub API quota is the finite resource being protected.
    PROGRESS_REFRESH_RATE_LIMIT_PER_HOUR: int = 10

    # --- Content curation ---
    # Problem creation is an authenticated publishing action with LLM/AI cost
    # imports only for ingest; the catalog is admin-curated, so user limits
    # track the moderation posture (admins exempt below).
    PROBLEM_CREATE_PER_HOUR: int = 5
    # Reports against published projects, per user per hour. Independent of the
    # chat limit so tuning one cannot silently retune the other.
    # Project reports (flags for admins to review). The duplicate guard
    # already blocks repeat reports on the same project by the same user, so
    # this caps spray across many projects: a genuine reporter stays far
    # under it, a spammer gets little throughput.
    REPORT_RATE_LIMIT_PER_HOUR: int = 5

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
