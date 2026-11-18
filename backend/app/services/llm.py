import datetime
import logging
import re
import threading
import time

import httpx

from app.config import get_settings

logger = logging.getLogger(__name__)

ANTHROPIC_API_BASE = "https://api.anthropic.com/v1"
ANTHROPIC_VERSION = "2023-06-01"
DEFAULT_GEMINI_MODEL = "gemini-3.8-flash"
DEFAULT_GEMINI_CHAT_MODEL = "gemini-3.5-flash-lite"
DEFAULT_ANTHROPIC_MODEL = "claude-sonnet-4-5"
MAX_TOKENS_CHAT = 320

# A key that Gemini rejects outright stays out of rotation for a day.
_INVALID_KEY_COOLDOWN = 24 * 3600
# Rate limits never rotate keys: the call waits and retries the same key.
_MAX_RATE_WAIT_CHAT = 5
_MAX_RATE_WAIT_EVAL = 30


class LLMConfigError(Exception):
    """Selected provider has no usable key configured. Routers map this to 503."""


class LLMResponseError(Exception):
    """Provider returned garbage twice. Routers map this to 502."""


class LLMQuotaExhausted(LLMResponseError):
    """Every Gemini key is out of daily quota. Carries a retry hint for users."""

    def __init__(self, message: str, retry_after: int = 0):
        super().__init__(message)
        self.retry_after = max(int(retry_after), 0)


def provider_name() -> str:
    return get_settings().LLM_PROVIDER.strip().lower()


def _split_keys(raw: str) -> list[str]:
    parts = [part.strip() for part in raw.replace("\n", ",").split(",")]
    # De-duplicate while keeping the configured order.
    return list(dict.fromkeys(part for part in parts if part))


def gemini_keys(purpose: str = "evaluation") -> list[str]:
    """Ordered key pool for one feature. Chat and evaluation never mix pools."""
    settings = get_settings()
    if purpose == "chat":
        keys = _split_keys(settings.GEMINI_API_KEYS_CHAT)
        if not keys and settings.GEMINI_API_KEY_CHAT:
            keys = [settings.GEMINI_API_KEY_CHAT]
        if not keys:
            keys = _split_keys(settings.GEMINI_API_KEYS_EVAL)
        if not keys and settings.GEMINI_API_KEY:
            keys = [settings.GEMINI_API_KEY]
        return keys
    keys = _split_keys(settings.GEMINI_API_KEYS_EVAL)
    if not keys and settings.GEMINI_API_KEY:
        keys = [settings.GEMINI_API_KEY]
    return keys


def is_configured(purpose: str = "evaluation") -> bool:
    provider = provider_name()
    if provider == "mock":
        return True
    if provider == "gemini":
        return bool(gemini_keys(purpose))
    if provider == "anthropic":
        return bool(get_settings().ANTHROPIC_API_KEY)
    return False


def chat(
    system: str,
    messages: list[dict],
    model: str | None = None,
    max_tokens: int | None = None,
    purpose: str = "evaluation",
) -> str:
    """Chat reply. Deterministic for the mock provider. Raises LLMConfigError -> 503.

    purpose="chat" (the catalog assistant) uses the chat key pool; everything
    else (relevance grading) uses the evaluation key pool.
    """
    if not is_configured(purpose):
        raise LLMConfigError("AI is not configured yet")
    provider = provider_name()
    last_user = [m.get("content", "") for m in messages if m.get("role") == "user"]
    last_user_text = last_user[-1] if last_user else ""
    if provider == "mock":
        return f"MOCK-CHAT-REPLY: saw: {last_user_text[:200]}".strip()
    if provider == "gemini":
        return _call_gemini(
            system,
            last_user_text,
            model=model,
            max_tokens=max_tokens,
            chat_purpose=purpose == "chat",
        ).strip()
    if provider == "anthropic":
        return _call_anthropic(system, last_user_text, model=model, max_tokens=max_tokens).strip()
    raise LLMConfigError(f"Unknown LLM_PROVIDER: {provider}")


# --- Gemini key pool -------------------------------------------------------
#
# Cooldowns live in process memory. One worker is the common deployment; with
# several workers each discovers an exhausted key once, which is harmless.

_key_lock = threading.Lock()
_key_cooldown: dict[str, float] = {}
_gemini_clients: dict[str, object] = {}

_clients_lock = threading.Lock()
_anthropic_client = None
_anthropic_client_key: str | None = None


def _key_label(key: str) -> str:
    """Short, non-reversible hint for logs (never log a full key)."""
    return f"...{key[-4:]}" if len(key) >= 4 else "..."


def _available_keys(keys: list[str]) -> list[str]:
    now = time.monotonic()
    with _key_lock:
        return [key for key in keys if _key_cooldown.get(key, 0.0) <= now]


def _cooldown_key(key: str, seconds: float) -> None:
    until = time.monotonic() + max(float(seconds), 1.0)
    with _key_lock:
        _key_cooldown[key] = max(_key_cooldown.get(key, 0.0), until)


def _seconds_until_keys_back(keys: list[str]) -> int:
    now = time.monotonic()
    with _key_lock:
        waits = [
            _key_cooldown[key] - now
            for key in keys
            if _key_cooldown.get(key, 0.0) > now
        ]
    if not waits:
        return 0
    return max(1, int(min(waits)))


def _next_quota_reset_seconds() -> int:
    """Seconds until Gemini's daily quota resets (midnight Pacific)."""
    try:
        from zoneinfo import ZoneInfo

        tz = ZoneInfo("America/Los_Angeles")
    except Exception:  # no tzdata on some Windows installs; PST is close enough
        tz = datetime.timezone(datetime.timedelta(hours=-8))
    now = datetime.datetime.now(tz)
    reset = datetime.datetime.combine(
        now.date() + datetime.timedelta(days=1),
        datetime.time.min,
        tzinfo=tz,
    )
    return max(60, int((reset - now).total_seconds()))


def _error_blob(exc: Exception) -> str:
    parts = [
        str(getattr(exc, "status", "") or ""),
        str(getattr(exc, "message", "") or ""),
        str(getattr(exc, "details", "") or ""),
        str(exc),
    ]
    return " ".join(parts).lower()


def _retry_delay_seconds(exc: Exception) -> int:
    match = re.search(r"retrydelay\D{0,20}(\d+)s", _error_blob(exc))
    return int(match.group(1)) if match else 0


def _classify_gemini_error(exc: Exception) -> str:
    """exhausted | invalid | rate | transient | other.

    Only "exhausted" and "invalid" rotate to the next key. A per-minute rate
    limit is retried on the same key because the other keys face the same
    limit; a 503/504 blip is retried on the same key too.
    """
    code = getattr(exc, "code", None)
    blob = _error_blob(exc)
    is_quota = code == 429 or "resource_exhausted" in blob or "quota" in blob
    if is_quota:
        retry_delay = _retry_delay_seconds(exc)
        if "perday" in blob or "per day" in blob or "daily" in blob:
            return "exhausted"
        if "perminute" in blob or "per minute" in blob or "persecond" in blob:
            return "rate"
        # A short retryDelay is a rolling-window limit; wait it out on the same
        # key. Anything else that reports quota is treated as an empty key.
        if retry_delay and retry_delay <= 120:
            return "rate"
        return "exhausted"
    if code in (401, 403) or "api_key_invalid" in blob or "permission_denied" in blob:
        return "invalid"
    if code in (500, 502, 503, 504) or "unavailable" in blob:
        return "transient"
    return "other"


def _humanize_wait(seconds: int) -> str:
    if seconds >= 3600:
        hours = max(1, round(seconds / 3600))
        return f"about {hours} hour" + ("" if hours == 1 else "s")
    minutes = max(1, round(seconds / 60))
    return f"about {minutes} minute" + ("" if minutes == 1 else "s")


def _quota_user_message(retry_after: int) -> str:
    return (
        "Manabi's AI has reached its daily usage limit. "
        f"Please try again in {_humanize_wait(retry_after)}."
    )


def _gemini(api_key: str):
    """Cached google-genai client per key (client init is not free per call)."""
    with _clients_lock:
        client = _gemini_clients.get(api_key)
        if client is not None:
            return client
        from google import genai
        from google.genai import types

        # Without an explicit timeout the SDK can hang indefinitely.
        client = genai.Client(
            api_key=api_key,
            http_options=types.HttpOptions(timeout=60_000),
        )
        _gemini_clients[api_key] = client
        return client


def _anthropic_http(api_key: str) -> httpx.Client:
    """Cached httpx.Client so TLS connections are reused across calls."""
    global _anthropic_client, _anthropic_client_key
    if _anthropic_client is None or _anthropic_client_key != api_key:
        _anthropic_client = httpx.Client(timeout=60.0)
        _anthropic_client_key = api_key
    return _anthropic_client


def _call_gemini(
    system: str,
    user: str,
    model: str | None,
    max_tokens: int | None = None,
    chat_purpose: bool = False,
) -> str:
    keys = gemini_keys("chat" if chat_purpose else "evaluation")
    if not keys:
        raise LLMConfigError("AI is not configured yet")

    available = _available_keys(keys)
    if not available:
        retry_after = _seconds_until_keys_back(keys)
        raise LLMQuotaExhausted(_quota_user_message(retry_after), retry_after)

    last_exc: Exception | None = None
    saw_exhausted = False
    for key in available:
        try:
            return _gemini_attempt(
                key,
                system,
                user,
                model=model,
                max_tokens=max_tokens,
                chat_purpose=chat_purpose,
            )
        except Exception as exc:
            kind = _classify_gemini_error(exc)
            if kind == "exhausted":
                saw_exhausted = True
                _cooldown_key(key, _next_quota_reset_seconds())
                logger.warning(
                    "Gemini key %s is out of daily quota; trying the next key",
                    _key_label(key),
                )
                last_exc = exc
                continue
            if kind == "invalid":
                _cooldown_key(key, _INVALID_KEY_COOLDOWN)
                logger.warning(
                    "Gemini key %s was rejected; trying the next key",
                    _key_label(key),
                )
                last_exc = exc
                continue
            logger.exception("Gemini call failed (model=%s)", model or "default")
            raise LLMResponseError(f"Gemini request failed: {exc}") from exc

    if saw_exhausted:
        retry_after = _seconds_until_keys_back(keys)
        raise LLMQuotaExhausted(
            _quota_user_message(retry_after), retry_after
        ) from last_exc
    raise LLMConfigError("AI is not configured yet") from last_exc


def _gemini_attempt(
    key: str,
    system: str,
    user: str,
    model: str | None,
    max_tokens: int | None,
    chat_purpose: bool,
) -> str:
    settings = get_settings()
    if chat_purpose:
        model_name = model or settings.GEMINI_MODEL_CHAT or DEFAULT_GEMINI_CHAT_MODEL
    else:
        model_name = model or settings.GEMINI_MODEL or DEFAULT_GEMINI_MODEL
    config = {
        # Chat wants warmth; grading wants determinism.
        "temperature": 0.25 if chat_purpose else 0,
        "max_output_tokens": max_tokens or MAX_TOKENS_CHAT,
    }
    prompt = f"{system}\n\n{user}" if user else system
    client = _gemini(key)
    # Free-tier capacity blips (503 overloaded, 504 deadline) recover within
    # seconds; retry briefly so occasional outages do not silently degrade
    # every submission to the keyword fallback. Chat stays snappier.
    attempts = 2 if chat_purpose else 3
    backoff = 1 if chat_purpose else 2
    max_rate_wait = _MAX_RATE_WAIT_CHAT if chat_purpose else _MAX_RATE_WAIT_EVAL
    last_exc: Exception | None = None
    for attempt in range(attempts):
        try:
            response = client.models.generate_content(
                model=model_name, contents=[prompt], config=config
            )
            return response.text or ""
        except Exception as exc:
            kind = _classify_gemini_error(exc)
            last_exc = exc
            # Quota/invalid errors rotate keys; bad requests fail immediately.
            if kind not in ("rate", "transient"):
                raise
            if attempt == attempts - 1:
                raise
            wait = backoff * (attempt + 1)
            if kind == "rate":
                # Same key only: the next key shares the same rate window.
                wait = max(wait, min(_retry_delay_seconds(exc), max_rate_wait))
            time.sleep(wait)
    raise last_exc if last_exc else LLMResponseError("Gemini request failed")


def _call_anthropic(system: str, user: str, model: str | None, max_tokens: int | None = None) -> str:
    settings = get_settings()
    if not settings.ANTHROPIC_API_KEY:
        raise LLMConfigError("AI is not configured yet")
    model_name = model or settings.LLM_MODEL_FAST or DEFAULT_ANTHROPIC_MODEL
    body = {
        "model": model_name,
        "max_tokens": max_tokens or MAX_TOKENS_CHAT,
        "temperature": 0,
        "system": system,
        "messages": [{"role": "user", "content": user or system}],
    }
    try:
        response = _anthropic_http(settings.ANTHROPIC_API_KEY).post(
            f"{ANTHROPIC_API_BASE}/messages",
            headers={
                "x-api-key": settings.ANTHROPIC_API_KEY,
                "anthropic-version": ANTHROPIC_VERSION,
                "content-type": "application/json",
            },
            json=body,
            timeout=60.0,
        )
        if response.status_code in (401, 403):
            raise LLMConfigError("AI is not configured yet (invalid API key)")
        if response.status_code >= 400:
            raise LLMResponseError(f"Anthropic error {response.status_code}")
        content = response.json().get("content") or []
        return "".join(part.get("text") or "" for part in content if isinstance(part, dict))
    except (LLMConfigError, LLMResponseError):
        raise
    except Exception as exc:  # transport failures and unreadable bodies must not leak as 500s
        logger.exception("Anthropic call failed (model=%s)", model_name)
        raise LLMResponseError(f"Anthropic request failed: {exc}") from exc
