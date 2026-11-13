import logging
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


class LLMConfigError(Exception):
    """Selected provider has no key configured. Routers map this to 503."""


class LLMResponseError(Exception):
    """Provider returned garbage twice. Routers map this to 502."""


def provider_name() -> str:
    return get_settings().LLM_PROVIDER.strip().lower()


def is_configured(purpose: str = "evaluation") -> bool:
    provider = provider_name()
    if provider == "mock":
        return True
    settings = get_settings()
    if provider == "gemini":
        # The chat feature can carry its own project key; evaluation always
        # rides on the shared key.
        return bool(settings.GEMINI_API_KEY) or (
            purpose == "chat" and bool(settings.GEMINI_API_KEY_CHAT)
        )
    if provider == "anthropic":
        return bool(settings.ANTHROPIC_API_KEY)
    return False


def gemini_chat_key() -> str | None:
    """Key for the chat feature: the chat project's key or the shared one."""
    return get_settings().GEMINI_API_KEY_CHAT or None


def chat(
    system: str,
    messages: list[dict],
    model: str | None = None,
    max_tokens: int | None = None,
    purpose: str = "evaluation",
) -> str:
    """Chat reply. Deterministic for the mock provider. Raises LLMConfigError -> 503.

    purpose="chat" (the catalog assistant) may use a dedicated Gemini project
    key/model; everything else (relevance grading) uses the shared key.
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
            api_key=gemini_chat_key() if purpose == "chat" else None,
            chat_purpose=purpose == "chat",
        ).strip()
    if provider == "anthropic":
        return _call_anthropic(system, last_user_text, model=model, max_tokens=max_tokens).strip()
    raise LLMConfigError(f"Unknown LLM_PROVIDER: {provider}")


_gemini_client = None
_gemini_client_key: str | None = None
_anthropic_client = None
_anthropic_client_key: str | None = None


def _gemini(api_key: str):
    """Cached google-genai client (connection state init is not free per call)."""
    global _gemini_client, _gemini_client_key
    if _gemini_client is None or _gemini_client_key != api_key:
        from google import genai
        from google.genai import types

        # Without an explicit timeout the SDK can hang indefinitely.
        _gemini_client = genai.Client(
            api_key=api_key,
            http_options=types.HttpOptions(timeout=60_000),
        )
        _gemini_client_key = api_key
    return _gemini_client


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
    api_key: str | None = None,
    chat_purpose: bool = False,
) -> str:
    settings = get_settings()
    key = api_key or settings.GEMINI_API_KEY
    if not key:
        raise LLMConfigError("AI is not configured yet")
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
    try:
        client = _gemini(key)
    except Exception as exc:
        logger.exception("Gemini client init failed")
        raise LLMResponseError(f"Gemini request failed: {exc}") from exc
    # Free-tier capacity blips (503 overloaded, 504 deadline) recover within
    # seconds; retry briefly so occasional outages do not silently degrade
    # every submission to the keyword fallback. Chat stays snappier: it
    # retries once after 1s, evaluation waits longer because a failed check
    # degrades a whole submission.
    attempts = 2 if chat_purpose else 3
    backoff = 1 if chat_purpose else 2
    for attempt in range(attempts):
        try:
            response = client.models.generate_content(model=model_name, contents=[prompt], config=config)
            return response.text or ""
        except Exception as exc:
            transient = getattr(exc, "code", None) in (503, 504)
            if not transient or attempt == attempts - 1:
                logger.exception("Gemini call failed (model=%s, attempt=%s)", model_name, attempt + 1)
                raise LLMResponseError(f"Gemini request failed: {exc}") from exc
            time.sleep(backoff * (attempt + 1))


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
