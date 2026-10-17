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
    AI_RATE_LIMIT_PER_HOUR: int = 15
    CHAT_RATE_LIMIT_ANON_PER_HOUR: int = 10
    CHAT_RATE_LIMIT_USER_PER_HOUR: int = 30


@lru_cache
def get_settings() -> Settings:
    return Settings()
