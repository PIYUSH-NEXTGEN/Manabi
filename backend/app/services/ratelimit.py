import threading
import time

from app.config import get_settings


class RateLimiter:
    """In-memory sliding-window limiter. True when allowed, False when over the limit."""

    def __init__(self, limit_setting: str):
        self._limit_setting = limit_setting
        self._hits: dict[str, list[float]] = {}
        self._lock = threading.Lock()

    def _window_seconds(self) -> int:
        return 3600

    def _limit(self) -> int:
        value = getattr(get_settings(), self._limit_setting)
        return max(1, int(value))

    def allowed(self, key: str) -> bool:
        now = time.monotonic()
        cutoff = now - self._window_seconds()
        with self._lock:
            hits = [t for t in self._hits.get(key, []) if t > cutoff]
            if len(hits) >= self._limit():
                self._hits[key] = hits
                return False
            hits.append(now)
            self._hits[key] = hits
            return True


INGEST_LIMITER = RateLimiter("AI_RATE_LIMIT_PER_HOUR")
ML_ATTEMPT_LIMITER = RateLimiter("AI_RATE_LIMIT_PER_HOUR")
CHAT_ANON_LIMITER = RateLimiter("CHAT_RATE_LIMIT_ANON_PER_HOUR")
CHAT_USER_LIMITER = RateLimiter("CHAT_RATE_LIMIT_USER_PER_HOUR")
