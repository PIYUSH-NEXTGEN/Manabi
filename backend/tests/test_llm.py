import httpx
import pytest
import respx

from app import config
from app.services import llm as llm_module
from app.services.llm import (
    LLMConfigError,
    LLMQuotaExhausted,
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
    monkeypatch.setenv("GEMINI_API_KEYS_EVAL", "")
    monkeypatch.setenv("GEMINI_API_KEYS_CHAT", "")
    monkeypatch.setenv("GEMINI_MODEL", "")
    monkeypatch.setenv("GEMINI_MODEL_CHAT", "")
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    get_settings.cache_clear()
    llm_module._key_cooldown.clear()
    llm_module._gemini_clients.clear()
    yield
    llm_module._key_cooldown.clear()
    llm_module._gemini_clients.clear()
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


# --- Gemini key pool -------------------------------------------------------


def _quota_error(*, daily: bool) -> Exception:
    from google.genai import errors as genai_errors

    quota_id = (
        "GenerateRequestsPerDayPerProjectPerModel-FreeTier"
        if daily
        else "GenerateRequestsPerMinutePerProjectPerModel-FreeTier"
    )
    return genai_errors.APIError(
        429,
        {
            "error": {
                "code": 429,
                "message": "You exceeded your current quota",
                "status": "RESOURCE_EXHAUSTED",
                "details": [
                    {
                        "@type": "type.googleapis.com/google.rpc.QuotaFailure",
                        "violations": [{"quotaId": quota_id}],
                    },
                    {
                        "@type": "type.googleapis.com/google.rpc.RetryInfo",
                        "retryDelay": "1s" if not daily else "86400s",
                    },
                ],
            }
        },
    )


class _Reply:
    def __init__(self, text: str):
        self.text = text


def _sequence_gemini(monkeypatch, behaviors: dict):
    """Fake SDK: each key returns its text or raises its exception; logs calls."""
    calls: list[str] = []

    class Client:
        def __init__(self, key: str):
            self.key = key

        @property
        def models(self):
            return self

        def generate_content(self, **_kwargs):
            calls.append(self.key)
            action = behaviors[self.key]
            if isinstance(action, Exception):
                raise action
            return _Reply(action)

    monkeypatch.setattr("app.services.llm._gemini", lambda key: Client(key))
    return calls


def test_gemini_pool_switches_when_first_key_is_exhausted(monkeypatch):
    set_provider(monkeypatch, "gemini", GEMINI_API_KEYS_CHAT="k1,k2")
    calls = _sequence_gemini(
        monkeypatch,
        {"k1": _quota_error(daily=True), "k2": "from second"},
    )

    reply = chat("Sys", [{"role": "user", "content": "hi"}], purpose="chat")

    assert reply == "from second"
    assert calls == ["k1", "k2"]
    # The exhausted key stays out of rotation, so the next call goes straight
    # to the backup (the user never sees the switch).
    calls.clear()
    assert chat("Sys", [{"role": "user", "content": "hi"}], purpose="chat") == "from second"
    assert calls == ["k2"]


def test_gemini_rate_limit_retries_same_key_and_never_switches(monkeypatch):
    set_provider(monkeypatch, "gemini", GEMINI_API_KEYS_EVAL="k1,k2")
    calls = _sequence_gemini(
        monkeypatch,
        {"k1": _quota_error(daily=False), "k2": "must not be used"},
    )
    sleeps: list[float] = []
    monkeypatch.setattr("app.services.llm.time.sleep", lambda s: sleeps.append(s))

    with pytest.raises(LLMResponseError) as info:
        chat("Sys", [{"role": "user", "content": "hi"}])

    assert calls == ["k1", "k1", "k1"]
    assert sleeps == [2, 4]
    assert not isinstance(info.value, LLMQuotaExhausted)


def test_gemini_invalid_key_switches_to_next(monkeypatch):
    from google.genai import errors as genai_errors

    invalid = genai_errors.APIError(
        403,
        {"error": {"code": 403, "message": "API key not valid", "status": "PERMISSION_DENIED"}},
    )
    set_provider(monkeypatch, "gemini", GEMINI_API_KEYS_EVAL="k1,k2")
    calls = _sequence_gemini(monkeypatch, {"k1": invalid, "k2": "from backup"})

    assert chat("Sys", [{"role": "user", "content": "hi"}]) == "from backup"
    assert calls == ["k1", "k2"]


def test_gemini_all_keys_exhausted_reports_retry_hint(monkeypatch):
    set_provider(monkeypatch, "gemini", GEMINI_API_KEYS_EVAL="k1,k2")
    calls = _sequence_gemini(
        monkeypatch,
        {"k1": _quota_error(daily=True), "k2": _quota_error(daily=True)},
    )

    with pytest.raises(LLMQuotaExhausted) as info:
        chat("Sys", [{"role": "user", "content": "hi"}])

    assert calls == ["k1", "k2"]
    assert info.value.retry_after > 0
    message = str(info.value)
    assert "try again in about" in message
    assert "k1" not in message and "k2" not in message


def test_gemini_switches_back_to_first_key_after_quota_resets(monkeypatch):
    set_provider(monkeypatch, "gemini", GEMINI_API_KEYS_EVAL="k1,k2")
    behaviors = {"k1": _quota_error(daily=True), "k2": "from second"}
    calls = _sequence_gemini(monkeypatch, behaviors)

    assert chat("Sys", [{"role": "user", "content": "hi"}]) == "from second"
    assert calls == ["k1", "k2"]

    # Simulate the daily quota reset: the primary is selectable again.
    behaviors["k1"] = "back on first"
    llm_module._key_cooldown["k1"] = 0
    calls.clear()

    assert chat("Sys", [{"role": "user", "content": "hi"}]) == "back on first"
    assert calls == ["k1"]


def test_chat_and_evaluation_use_separate_pools(monkeypatch):
    set_provider(
        monkeypatch,
        "gemini",
        GEMINI_API_KEYS_CHAT="c1,c2",
        GEMINI_API_KEYS_EVAL="e1,e2",
    )
    calls = _sequence_gemini(
        monkeypatch,
        {"c1": "chat", "c2": "chat2", "e1": "eval", "e2": "eval2"},
    )

    assert chat("Sys", [{"role": "user", "content": "hi"}], purpose="chat") == "chat"
    assert chat("Sys", [{"role": "user", "content": "hi"}]) == "eval"
    assert calls == ["c1", "e1"]


def test_pool_configures_both_features(monkeypatch):
    set_provider(
        monkeypatch,
        "gemini",
        GEMINI_API_KEYS_CHAT="c1",
        GEMINI_API_KEYS_EVAL="e1",
    )
    assert is_configured("chat") is True
    assert is_configured() is True
