import httpx
import pytest
import respx

from app import config
from app.services.llm import (
    LLMConfigError,
    LLMResponseError,
    chat,
    is_configured,
    provider_name,
)


@pytest.fixture(autouse=True)
def llm_env(monkeypatch):
    get_settings = config.get_settings
    monkeypatch.setenv("LLM_PROVIDER", "mock")
    # Blank env entries override anything in the real backend/.env file,
    # so developer machines with live keys cannot leak into tests.
    monkeypatch.setenv("GEMINI_API_KEY", "")
    monkeypatch.setenv("GEMINI_API_KEY_CHAT", "")
    monkeypatch.setenv("GEMINI_MODEL", "")
    monkeypatch.setenv("GEMINI_MODEL_CHAT", "")
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
        chat("s", [{"role": "user", "content": "u"}])


def test_gemini_with_key_is_configured(monkeypatch):
    set_provider(monkeypatch, "gemini", GEMINI_API_KEY="k")
    assert is_configured() is True


def test_anthropic_with_key_is_configured(monkeypatch):
    set_provider(monkeypatch, "anthropic", ANTHROPIC_API_KEY="k")
    assert is_configured() is True


def test_unknown_provider_not_configured(monkeypatch):
    set_provider(monkeypatch, "wat")
    assert is_configured() is False
    with pytest.raises(LLMConfigError):
        chat("s", [{"role": "user", "content": "u"}])


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


def _recording_gemini(monkeypatch, used):
    class Reply:
        text = "gemini said"

    class Client:
        class models:
            @staticmethod
            def generate_content(**kwargs):
                used.update(kwargs)
                return Reply()

    monkeypatch.setattr(
        "app.services.llm._gemini",
        lambda api_key: (used.setdefault("key", api_key), Client())[1],
    )


def test_chat_uses_dedicated_chat_key_and_model(monkeypatch):
    set_provider(
        monkeypatch,
        "gemini",
        GEMINI_API_KEY="shared",
        GEMINI_API_KEY_CHAT="chatk",
        GEMINI_MODEL_CHAT="lite",
    )
    used = {}
    _recording_gemini(monkeypatch, used)

    reply = chat("Sys", [{"role": "user", "content": "hi"}], purpose="chat")

    assert reply == "gemini said"
    assert used["key"] == "chatk"
    assert used["model"] == "lite"


def test_chat_falls_back_to_shared_key_without_chat_key(monkeypatch):
    set_provider(monkeypatch, "gemini", GEMINI_API_KEY="shared")
    used = {}
    _recording_gemini(monkeypatch, used)

    chat("Sys", [{"role": "user", "content": "hi"}], purpose="chat")

    assert used["key"] == "shared"
    assert used["model"] == "gemini-3.5-flash-lite"


def test_evaluation_keeps_the_shared_key(monkeypatch):
    set_provider(
        monkeypatch,
        "gemini",
        GEMINI_API_KEY="shared",
        GEMINI_API_KEY_CHAT="chatk",
    )
    used = {}
    _recording_gemini(monkeypatch, used)

    chat("Sys", [{"role": "user", "content": "hi"}])

    assert used["key"] == "shared"
    assert used["model"] == "gemini-3.8-flash"


def test_chat_only_key_configures_chat_but_not_evaluation(monkeypatch):
    set_provider(monkeypatch, "gemini", GEMINI_API_KEY="", GEMINI_API_KEY_CHAT="chatk")
    assert is_configured("chat") is True
    assert is_configured() is False
    with pytest.raises(LLMConfigError):
        chat("Sys", [{"role": "user", "content": "hi"}])


def test_anthropic_happy_path_over_respx(monkeypatch):
    set_provider(monkeypatch, "anthropic", ANTHROPIC_API_KEY="key")
    with respx.mock(assert_all_called=True) as mock:
        mock.post("https://api.anthropic.com/v1/messages").mock(
            return_value=httpx.Response(200, json={"content": [{"type": "text", "text": "from anthropic"}]})
        )
        result = chat("s", [{"role": "user", "content": "u"}])
    assert result == "from anthropic"


def test_anthropic_401_maps_to_config_error(monkeypatch):
    set_provider(monkeypatch, "anthropic", ANTHROPIC_API_KEY="key")
    with respx.mock() as mock:
        mock.post("https://api.anthropic.com/v1/messages").mock(
            return_value=httpx.Response(401, json={"error": {"type": "authentication_error"}})
        )
        with pytest.raises(LLMConfigError):
            chat("s", [{"role": "user", "content": "u"}])


def test_anthropic_500_maps_to_response_error(monkeypatch):
    set_provider(monkeypatch, "anthropic", ANTHROPIC_API_KEY="key")
    with respx.mock() as mock:
        mock.post("https://api.anthropic.com/v1/messages").mock(
            return_value=httpx.Response(500, json={"error": {"type": "api_error"}})
        )
        with pytest.raises(LLMResponseError):
            chat("s", [{"role": "user", "content": "u"}])


def test_gemini_transport_error_maps_to_response_error(monkeypatch):
    """SDK/transport failures must surface as LLMResponseError (502), never a raw 500."""
    set_provider(monkeypatch, "gemini", GEMINI_API_KEY="k")

    class OfflineClient:
        class models:
            @staticmethod
            def generate_content(**_kwargs):
                raise ConnectionError("network down")

    monkeypatch.setattr("app.services.llm._gemini", lambda api_key: OfflineClient())
    with pytest.raises(LLMResponseError):
        chat("Sys", [{"role": "user", "content": "hi"}])


def test_gemini_api_error_maps_to_response_error(monkeypatch):
    from google.genai import errors as genai_errors

    set_provider(monkeypatch, "gemini", GEMINI_API_KEY="k")
    quota = genai_errors.APIError(429, {"error": {"message": "quota exceeded"}})

    class LimitedClient:
        class models:
            @staticmethod
            def generate_content(**_kwargs):
                raise quota

    monkeypatch.setattr("app.services.llm._gemini", lambda api_key: LimitedClient())
    with pytest.raises(LLMResponseError):
        chat("Sys", [{"role": "user", "content": "hi"}])


def test_chat_purpose_retries_once_evaluation_twice(monkeypatch):
    """Chat fails fast (1 retry, 1s); relevance grading retries longer."""
    from google.genai import errors as genai_errors

    set_provider(monkeypatch, "gemini", GEMINI_API_KEY="k")
    blip = genai_errors.APIError(503, {"error": {"message": "overloaded"}})
    calls = []
    sleeps = []

    class FlakyClient:
        class models:
            @staticmethod
            def generate_content(**_kwargs):
                calls.append(1)
                raise blip

    monkeypatch.setattr("app.services.llm._gemini", lambda api_key: FlakyClient())
    monkeypatch.setattr("app.services.llm.time.sleep", lambda s: sleeps.append(s))

    with pytest.raises(LLMResponseError):
        chat("Sys", [{"role": "user", "content": "hi"}], purpose="chat")
    assert len(calls) == 2 and sleeps == [1]

    calls.clear()
    sleeps.clear()
    with pytest.raises(LLMResponseError):
        chat("Sys", [{"role": "user", "content": "hi"}])
    assert len(calls) == 3 and sleeps == [2, 4]


def test_chat_recovers_from_one_transient_blip(monkeypatch):
    from google.genai import errors as genai_errors

    set_provider(monkeypatch, "gemini", GEMINI_API_KEY="k", GEMINI_API_KEY_CHAT="chatk")
    blip = genai_errors.APIError(503, {"error": {"message": "overloaded"}})
    calls = []

    class RecoversClient:
        class models:
            @staticmethod
            def generate_content(**_kwargs):
                calls.append(1)
                if len(calls) == 1:
                    raise blip
                return _Reply()

    class _Reply:
        text = "recovered"

    monkeypatch.setattr("app.services.llm._gemini", lambda api_key: RecoversClient())
    monkeypatch.setattr("app.services.llm.time.sleep", lambda _s: None)

    assert chat("Sys", [{"role": "user", "content": "hi"}], purpose="chat") == "recovered"
    assert len(calls) == 2


def test_anthropic_transport_error_maps_to_response_error(monkeypatch):
    set_provider(monkeypatch, "anthropic", ANTHROPIC_API_KEY="key")
    with respx.mock() as mock:
        mock.post("https://api.anthropic.com/v1/messages").mock(
            side_effect=httpx.ConnectError("connection refused")
        )
        with pytest.raises(LLMResponseError):
            chat("s", [{"role": "user", "content": "u"}])
