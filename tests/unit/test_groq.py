"""Testes do provider Groq sem chamada de rede real."""

from nexora.providers.groq import ProviderGroq


def test_groq_propagates_usage_from_api(monkeypatch):
    provider = ProviderGroq(api_key="teste", modelo="openai/gpt-oss-20b")
    monkeypatch.setattr(
        provider,
        "_post",
        lambda payload: {
            "choices": [{"message": {"content": "ok", "tool_calls": []}}],
            "usage": {"prompt_tokens": 11, "completion_tokens": 7, "total_tokens": 18},
        },
    )
    result = provider.generate("oi")
    assert result.text == "ok"
    assert result.usage == {"prompt_tokens": 11, "completion_tokens": 7, "total_tokens": 18}
    assert provider.modelo == "openai/gpt-oss-20b"


def test_groq_ignora_contadores_invalidos(monkeypatch):
    provider = ProviderGroq(api_key="teste", modelo="openai/gpt-oss-20b")
    monkeypatch.setattr(
        provider,
        "_post",
        lambda payload: {
            "choices": [{"message": {"content": "ok"}}],
            "usage": {"prompt_tokens": -1, "completion_tokens": "7", "total_tokens": 8},
        },
    )
    assert provider.generate("oi").usage == {"total_tokens": 8}
