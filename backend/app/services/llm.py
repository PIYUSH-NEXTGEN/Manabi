import json
import logging
import re

import httpx
from pydantic import BaseModel, ValidationError

from app.config import get_settings

logger = logging.getLogger(__name__)

ANTHROPIC_API_BASE = "https://api.anthropic.com/v1"
ANTHROPIC_VERSION = "2023-06-01"
DEFAULT_GEMINI_MODEL = "gemini-3.8-flash"
DEFAULT_ANTHROPIC_MODEL = "claude-sonnet-4-5"
MAX_TOKENS_JSON = 4096
MAX_TOKENS_CHAT = 512


class LLMConfigError(Exception):
    """Selected provider has no key configured. Routers map this to 503."""


class LLMResponseError(Exception):
    """Provider returned garbage twice. Routers map this to 502."""


def provider_name() -> str:
    return get_settings().LLM_PROVIDER.strip().lower()


def is_configured() -> bool:
    provider = provider_name()
    if provider == "mock":
        return True
    settings = get_settings()
    if provider == "gemini":
        return bool(settings.GEMINI_API_KEY)
    if provider == "anthropic":
        return bool(settings.ANTHROPIC_API_KEY)
    return False


def chat(system: str, messages: list[dict], model: str | None = None) -> str:
    """Chat reply. Deterministic for the mock provider. Raises LLMConfigError -> 503."""
    if not is_configured():
        raise LLMConfigError("AI is not configured yet")
    provider = provider_name()
    last_user = [m.get("content", "") for m in messages if m.get("role") == "user"]
    last_user_text = last_user[-1] if last_user else ""
    if provider == "mock":
        return f"MOCK-CHAT-REPLY: saw: {last_user_text[:200]}".strip()
    if provider == "gemini":
        raw = _call_gemini(system, last_user_text, json_mode=False, model=model)
    elif provider == "anthropic":
        raw = _call_anthropic(system, last_user_text, json_mode=False, model=model)
    else:
        raise LLMConfigError(f"Unknown LLM_PROVIDER: {provider}")
    return raw.strip()


def generate_raw_json(system: str, user: str, model: str | None = None) -> dict:
    """Raw JSON object without schema validation. Two tries. For early-exit flows."""
    if not is_configured():
        raise LLMConfigError("AI is not configured yet")
    provider = provider_name()
    if provider == "mock":
        if model == "early-exit-empty":
            return {"is_problem": False}
        model = None
    last_error: str = ""
    for _ in range(2):
        raw = _provider_raw_json(system, user, None, model)
        try:
            return _parse_json_object(raw)
        except _JsonParseFailure as exc:
            last_error = str(exc)
    raise LLMResponseError(f"The AI response could not be parsed: {last_error}")


def prepare_json(system: str, user: str, schema: type[BaseModel], data: dict, model: str | None = None):
    """Validate an already-fetched dict against a schema (shared prompt flow)."""
    return _parse_json_model(json.dumps(data), schema)


def generate_json(system: str, user: str, schema: type[BaseModel], model: str | None = None):
    """Generate + validate JSON. Two tries. Raises LLMConfigError (503) or LLMResponseError (502)."""
    if not is_configured():
        raise LLMConfigError("AI is not configured yet")
    last_error: str = ""
    for _ in range(2):
        raw = _provider_raw_json(system, user, schema, model)
        try:
            return _parse_json_model(raw, schema)
        except _JsonParseFailure as exc:
            last_error = str(exc)
    raise LLMResponseError(f"The AI response could not be parsed: {last_error}")


def _provider_raw_json(system: str, user: str, schema: type[BaseModel], model: str | None) -> str:
    provider = provider_name()
    if provider == "mock":
        if schema is None:
            return '{"is_problem": false}'
        return json.dumps(_model_default_json(schema), separators=(",", ":"))
    if provider == "gemini":
        return _call_gemini(system, user, json_mode=True, model=model)
    if provider == "anthropic":
        return _call_anthropic(system, user, json_mode=True, model=model)
    raise LLMConfigError(f"Unknown LLM_PROVIDER: {provider}")


class _JsonParseFailure(Exception):
    pass


_FENCE_RE = re.compile(r"^```[a-zA-Z]*\s*|\s*```$")
JSON_BLOCK_RE = re.compile(r"\{.*\}|\[.*\]", re.DOTALL)


def _strip_fences(raw: str) -> str:
    text = raw.strip()
    text = _FENCE_RE.sub("", text)
    return text.strip()


def _parse_json_object(raw: str) -> dict:
    text = _strip_fences(raw)
    match = JSON_BLOCK_RE.search(text)
    if not match:
        raise _JsonParseFailure("no JSON object in response")
    try:
        data = json.loads(match.group(0))
    except json.JSONDecodeError as exc:
        raise _JsonParseFailure(f"invalid JSON: {exc}")
    if not isinstance(data, dict):
        raise _JsonParseFailure("response was not a JSON object")
    return data


def _parse_json_model(raw: str, schema: type[BaseModel]):
    text = _strip_fences(raw)
    match = JSON_BLOCK_RE.search(text)
    if not match:
        raise _JsonParseFailure("no JSON object in response")
    try:
        data = json.loads(match.group(0))
    except json.JSONDecodeError as exc:
        raise _JsonParseFailure(f"invalid JSON: {exc}")
    try:
        return schema.model_validate(data)
    except ValidationError as exc:
        raise _JsonParseFailure(f"schema validation failed: {exc}")


def _model_default_json(schema: type[BaseModel]) -> dict:
    """Deterministic canned JSON for the mock provider: minimal but schema-valid."""
    schema_json = schema.model_json_schema()
    defs = schema_json.get("$defs", {})
    filled = _fill_schema(defs, schema_json)
    return filled if isinstance(filled, dict) else {}


def _fill_schema(defs: dict, node: dict):
    if "enum" in node:
        return node["enum"][0]
    if "const" in node:
        return node["const"]
    if ref := node.get("$ref"):
        return _fill_schema(defs, defs.get(ref.split("/")[-1], {}))
    if any_of := node.get("anyOf"):
        return _fill_schema(defs, any_of[0])
    type_name = node.get("type")
    if type_name == "object":
        return {name: _fill_schema(defs, prop) for name, prop in node.get("properties", {}).items()}
    if type_name == "array":
        return [_fill_schema(defs, node.get("items", {}))][:0]
    if type_name == "string":
        return ""
    if type_name == "integer":
        return 0
    if type_name == "number":
        return 0.0
    if type_name == "boolean":
        return False
    return None


_gemini_client = None
_gemini_client_key: str | None = None
_anthropic_client = None
_anthropic_client_key: str | None = None


def _gemini(api_key: str):
    """Cached google-genai client (connection state init is not free per call)."""
    global _gemini_client, _gemini_client_key
    if _gemini_client is None or _gemini_client_key != api_key:
        from google import genai

        _gemini_client = genai.Client(api_key=api_key)
        _gemini_client_key = api_key
    return _gemini_client


def _anthropic_http(api_key: str) -> httpx.Client:
    """Cached httpx.Client so TLS connections are reused across calls."""
    global _anthropic_client, _anthropic_client_key
    if _anthropic_client is None or _anthropic_client_key != api_key:
        _anthropic_client = httpx.Client(timeout=60.0)
        _anthropic_client_key = api_key
    return _anthropic_client


def _call_gemini(system: str, user: str, json_mode: bool, model: str | None) -> str:
    settings = get_settings()
    if not settings.GEMINI_API_KEY:
        raise LLMConfigError("AI is not configured yet")
    model_name = model or settings.GEMINI_MODEL or DEFAULT_GEMINI_MODEL
    config = {
        "temperature": 0,
        "max_output_tokens": MAX_TOKENS_JSON if json_mode else MAX_TOKENS_CHAT,
        "response_mime_type": "application/json" if json_mode else "text/plain",
    }
    prompt = f"{system}\n\n{user}" if user else system
    try:
        client = _gemini(settings.GEMINI_API_KEY)
        response = client.models.generate_content(model=model_name, contents=[prompt], config=config)
        return response.text or ""
    except Exception as exc:  # SDK (quota/safety/model) and transport errors must not leak as 500s
        logger.exception("Gemini call failed (model=%s)", model_name)
        raise LLMResponseError(f"Gemini request failed: {exc}") from exc


def _call_anthropic(system: str, user: str, json_mode: bool, model: str | None) -> str:
    settings = get_settings()
    if not settings.ANTHROPIC_API_KEY:
        raise LLMConfigError("AI is not configured yet")
    model_name = model or settings.LLM_MODEL_FAST or DEFAULT_ANTHROPIC_MODEL
    final_system = system
    if json_mode:
        final_system = f"{system}\n\nRespond with ONLY raw JSON matching the requested shape. No markdown fences."
    body = {
        "model": model_name,
        "max_tokens": MAX_TOKENS_JSON if json_mode else MAX_TOKENS_CHAT,
        "temperature": 0,
        "system": final_system,
        "messages": [{"role": "user", "content": user or final_system}],
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
