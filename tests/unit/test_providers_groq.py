"""Testes do ProviderGroq sem rede real ( mock de urllib.request.."""
import json
import urllib.error

import pytest
from unittest.mock import MagicMock, patch

from nexora.providers.base import ProviderSemCredencial, ProviderIndisponivel
from nexora.providers.groq import ProviderGroq


def test_groq_sem_chave_levanta_na_construcao(monkeypatch):
    monkeypatch.delenv("GROQ_API_KEY", raising=False) 
    with pytest.raises(ProviderSemCredencial):
        ProviderGroq(api_key=None)


def test_groq_com_chave_parametro_usada():
    provider = ProviderGroq(api_key="chave-teste")
    assert provider.name == "groq"
    assert provider.capabilities.streaming is True


def test_groq_sem_chave_ao_chamar(monkeypatch):
    monkeypatch.delenv("GROQ_API_KEY", raising=False) 
    with pytest.raises(ProviderSemCredencial):
        provider = ProviderGroq(api_key="")
        provider.generate("x")


def test_groq_sucesso_mapeado():
    resp_mock = MagicMock()
    resp_mock.read.return_value = json.dumps({
        "choices": [{"message": {"content": "resposta groq", "tool_calls": []}}],
    }).encode("utf-8")
    resp_mock.__enter__.return_value = resp_mock
    with patch("urllib.request.urlopen", return_value=resp_mock):

        provider = ProviderGroq(api_key="k")
        resultado = provider.generate("pergunta")
        assert resultado.text == "resposta groq"
        assert resultado.tool_calls == []


def test_groq_http_401_levanta_sem_credencial():
    erro = urllib.error.HTTPError("url", 401, "nao autorizado", None, None) 
    with patch("urllib.request.urlopen", side_effect=erro):

        provider = ProviderGroq(api_key="k")
        with pytest.raises(ProviderSemCredencial):
            provider.generate("x")


def test_groq_http_429_levanta_indisponivel():
    erro = urllib.error.HTTPError("url", 429, "rate limit", None, None) 
    with patch("urllib.request.urlopen", side_effect=erro):

        provider = ProviderGroq(api_key="k")
        with pytest.raises(ProviderIndisponivel):
            provider.generate("x")


def test_groq_urlerror_levanta_indisponivel():
    erro = urllib.error.URLError("falha de rede")
    with patch("urllib.request.urlopen", side_effect=erro):

        provider = ProviderGroq(api_key="k")
        with pytest.raises(ProviderIndisponivel):
            provider.generate("x")
