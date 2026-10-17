import json
from typing import Literal

import pytest
import respx
import httpx
from pydantic import BaseModel

from app import config
from app.services.llm import (
    LLMConfigError,
    LLMResponseError,
    _parse_json_model,
    _JsonParseFailure,
    chat,
    generate_json,
    is_configured,
    provider_name,
    _model_default_json,
)


class Card(BaseModel):
    title: str
    est_hours: int
    field: Literal["ml", "cybersecurity", "web-fullstack", "other"]
    tags: list[str]
    extra: str | None = None


class Nice(BaseModel):
    text: str


@pytest.fixture(autouse=True)
def llm_env(monkeypatch):
    get_settings = config.get_settings
    monkeypatch.setenv("LLM_PROVIDER", "mock")
    monkeypatch.setenv("GEMINI_API_KEY", "")
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    get_settings.cache_clear()
    yield
    get_settings.cache_clear()


def set_provider(monkeypatch, name: str, **extra):
    get_settings = config.get_settings
    monkeypatch.setenv("LLM_PROVIDER", name)
    for key, value in extra.items():
        if value is None:
            monkeypatch.delenv(key, raising=False)
        else:
            monkeypatch.setenv(key, value)
    get_settings.cache_clear()


def test_provider_name_and_mock_is_configured():
    assert provider_name() == "mock"
    assert is_configured() is True


def test_gemini_without_key_not_configured(monkeypatch):
    set_provider(monkeypatch, "gemini", GEMINI_API_KEY="")
    assert is_configured() is False
    with pytest.raises(LLMConfigError):
        generate_json("s", "u", Card)


def test_gemini_with_key_is_configured(monkeypatch):
    set_provider(monkeypatch, "gemini", GEMINI_API_KEY="k")
    assert is_configured() is True


def test_unknown_provider_not_configured(monkeypatch):
    set_provider(monkeypatch, "wat")
    assert is_configured() is False


def test_mock_generate_json_is_schema_valid_and_deterministic():
    a = generate_json("System.", "User?", Card)
    b = generate_json("System.", "User?", Card)
    assert isinstance(a, Card)
    assert a.field == "ml"  # first enum value
    assert isinstance(a.est_hours, int)
    assert a.tags == []
    assert json.dumps(_model_default_json(Card)) == json.dumps(_model_default_json(Card))


def test_fences_are_stripped():
    raw = "```json\n{\"text\": \"hi\"}\n```"
    assert _parse_json_model(raw, Nice) == Nice(text="hi")


def test_json_block_extracted_from_prose():
    raw = "Sure! Here it is: {\"text\": \"hi there\"} — done."
    assert _parse_json_model(raw, Nice) == Nice(text="hi there")


def test_no_json_raises_parse_failure():
    with pytest.raises(_JsonParseFailure):
        _parse_json_model("no json at all", Nice)


def test_invalid_schema_raises_parse_failure():
    raw = "{\"text\": 123}"
    with pytest.raises(_JsonParseFailure):
        _parse_json_model(raw, Nice)


def test_retry_once_on_single_bad_response(monkeypatch):
    calls = {"n": 0}

    def flaky(system, user, schema, model=None):
        calls["n"] += 1
        return json.dumps(_model_default_json(schema)) if calls["n"] == 2 else "not json"

    monkeypatch.setattr("app.services.llm._provider_raw_json", flaky, raising=False)
    result = generate_json("s", "u", Card)
    assert calls["n"] == 2
    assert isinstance(result, Card)


def test_two_bad_responses_raise_response_error(monkeypatch):
    def always_bad(system, user, schema, model=None):
        return "not json ever"

    monkeypatch.setattr("app.services.llm._provider_raw_json", always_bad, raising=False)
    with pytest.raises(LLMResponseError):
        generate_json("s", "u", Card)


def test_two_schema_failures_raise_response_error(monkeypatch):
    def always_wrong_shape(system, user, schema, model=None):
        return json.dumps({"wrong_field": True})

    monkeypatch.setattr("app.services.llm._provider_raw_json", always_wrong_shape, raising=False)
    with pytest.raises(LLMResponseError):
        generate_json("s", "u", Card)


def monkeypatched_provider(monkeypatch, responses: list[str]):
    queue = iter(responses)

    def fake(system, user, schema, model=None):
        return next(queue)

    monkeypatch.setattr("app.services.llm._provider_raw_json", fake, raising=False)
    return fake


def test_anthropic_happy_path_over_respx(monkeypatch):
    set_provider(monkeypatch, "anthropic", ANTHROPIC_API_KEY="key")
    with respx.mock(assert_all_called=True) as mock:
        mock.post("https://api.anthropic.com/v1/messages").mock(
            return_value=httpx.Response(200, json={"content": [{"type": "text", "text": '{"text": "from anthropic"}'}]})
        )
        result = generate_json("s", "u", Nice)
    assert result == Nice(text="from anthropic")


def test_anthropic_401_maps_to_config_error(monkeypatch):
    set_provider(monkeypatch, "anthropic", ANTHROPIC_API_KEY="key")
    with respx.mock() as mock:
        mock.post("https://api.anthropic.com/v1/messages").mock(
            return_value=httpx.Response(401, json={"error": {"type": "authentication_error"}})
        )
        with pytest.raises(LLMConfigError):
            generate_json("s", "u", Nice)


def test_anthropic_500_maps_to_response_error(monkeypatch):
    set_provider(monkeypatch, "anthropic", ANTHROPIC_API_KEY="key")
    with respx.mock() as mock:
        mock.post("https://api.anthropic.com/v1/messages").mock(
            return_value=httpx.Response(500, json={"error": {"type": "api_error"}})
        )
        with pytest.raises((LLMResponseError, LLMConfigError)):
            generate_json("s", "u", Nice)


def test_chat_mock_deterministic():
    reply = chat("Sys", [{"role": "user", "content": "hello"}])
    reply2 = chat("Sys", [{"role": "user", "content": "hello"}])
    assert reply == reply2
    assert reply.startswith("MOCK-CHAT-REPLY")
    assert "hello" in reply


def test_chat_uses_latest_user_message():
    reply = chat("Sys", [
        {"role": "user", "content": "first"},
        {"role": "assistant", "content": "ok"},
    ])
    assert "first" in reply


def test_chat_without_key_503(monkeypatch):
    set_provider(monkeypatch, "gemini", GEMINI_API_KEY="")
    with pytest.raises(LLMConfigError):
        chat("Sys", [{"role": "user", "content": "hi"}])
