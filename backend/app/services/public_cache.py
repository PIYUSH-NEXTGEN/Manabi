"""In-process TTL cache for anonymous public GET responses.

The API runs as a single instance, so a bounded dict is a complete cache: no
cross-process invalidation and no extra network hop. TTLs are short (30-60 s)
so a newly published brief or a freshly verified project still shows up within
one cycle, while repeat traffic stops hitting Postgres at all.

Only viewer-independent payloads belong here. Anything that depends on the
session (stars, dashboard, admin) must stay uncached.
"""

from __future__ import annotations

import threading
import time
from typing import Any

MAX_ENTRIES = 256

# Bump the version when the payload shape changes, so a deploy never serves a
# response built by the previous schema.
LIST_KEY_PREFIX = "problems:list:v2"
FACETS_KEY_PREFIX = "problems:facets:v2"
STATS_KEY_PREFIX = "stats:v2"

LIST_TTL_SECONDS = 30
AGGREGATE_TTL_SECONDS = 60

# Browser revalidation is immediate (the client cache already holds the data);
# the shared-cache lifetime is what removes the round trip to Render. A logged
# in viewer never gets these headers: their response is per-viewer (stars) and
# the middleware's no-store stays in place.
LIST_CACHE_CONTROL = "public, max-age=0, s-maxage=30, stale-while-revalidate=120"
AGGREGATE_CACHE_CONTROL = "public, max-age=30, s-maxage=60, stale-while-revalidate=300"


class TTLCache:
    """Small thread-safe map with per-entry expiry.

    Endpoints are sync ``def`` handlers, so they run in the threadpool and can
    touch this concurrently; a lock around the dict keeps eviction honest
    without making reads wait on a query.
    """

    def __init__(self, max_entries: int = MAX_ENTRIES) -> None:
        self._entries: dict[tuple, tuple[float, Any]] = {}
        self._lock = threading.Lock()
        self._max_entries = max_entries

    def get(self, key: tuple) -> Any | None:
        now = time.monotonic()
        with self._lock:
            entry = self._entries.get(key)
            if entry is None:
                return None
            expires_at, value = entry
            if expires_at <= now:
                self._entries.pop(key, None)
                return None
            return value

    def set(self, key: tuple, value: Any, ttl_seconds: float) -> None:
        now = time.monotonic()
        with self._lock:
            if len(self._entries) >= self._max_entries:
                for stale_key in [
                    existing
                    for existing, (expires_at, _) in self._entries.items()
                    if expires_at <= now
                ]:
                    self._entries.pop(stale_key, None)
                while len(self._entries) >= self._max_entries:
                    oldest = min(
                        self._entries, key=lambda existing: self._entries[existing][0]
                    )
                    self._entries.pop(oldest, None)
            self._entries[key] = (now + ttl_seconds, value)

    def delete_prefix(self, prefix: str) -> None:
        """Drop entries whose key starts with prefix, keeping unrelated
        aggregates warm. Keys are tuples whose first element names the kind."""
        with self._lock:
            for key in [
                existing
                for existing in self._entries
                if isinstance(existing, tuple) and existing and existing[0] == prefix
            ]:
                self._entries.pop(key, None)

    def clear(self) -> None:
        with self._lock:
            self._entries.clear()


PUBLIC_CACHE = TTLCache()
