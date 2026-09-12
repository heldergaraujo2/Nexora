"""Testes do ProviderOllama sem depender de um daemon real."""
from __future__ import annotations

import json
import urllib.error
from unittest.mock import MagicMock, patch

import pytest

from nexora.providers.base import ProviderIndisponivel
from nexora.providers.ollama import ProviderOllama


def _resposta_json(payload: dict) -> MagicMock:
    resposta = MagicMock()
    resposta.read.return_value = json.dumps(payload).encode("utf-8")
    resposta.__enter__.return_value = resposta
    return resposta


def test_ollama_usa_padrao_local_e_modelo_configuravel():
    provider = ProviderOllama(modelo="modelo-teste")
    assert provider.name == "ollama"
    assert provider.url == "http://localhost:11434"
    assert provider.modelo == "modelo-teste"
    assert provider.capabilities.tool_calling is False


def test_ollama_respeita_variaveis_de_ambiente(monkeypatch):
    monkeypatch.setenv("NEXORA_OLLAMA_URL", "http://127.0.0.1:9999/")
    monkeypatch.setenv("NEXORA_OLLAMA_MODEL", "modelo-env")
    provider = ProviderOllama()
    assert provider.url == "http://127.0.0.1:9999"
    assert provider.modelo == "modelo-env"


def test_ollama_generate_mapeia_chat():
    resposta = _resposta_json({"message": {"content": "resposta local", "tool_calls": []}})
    with patch("urllib.request.urlopen", return_value=resposta) as urlopen:
        provider = ProviderOllama(modelo="qwen-teste")
        resultado = provider.generate("ola", temperature=0.2, system="responda curto")

    assert resultado.text == "resposta local"
    assert resultado.tool_calls == []
    pedido = urlopen.call_args.args[0]
    corpo = json.loads(pedido.data.decode("utf-8"))
    assert corpo["model"] == "qwen-teste"
    assert corpo["stream"] is False
    assert corpo["messages"][0] == {"role": "system", "content": "responda curto"}
    assert corpo["options"] == {"temperature": 0.2}


def test_ollama_http_e_rede_viram_indisponivel():
    erro = urllib.error.HTTPError("url", 503, "indisponivel", None, None)
    with patch("urllib.request.urlopen", side_effect=erro):
        with pytest.raises(ProviderIndisponivel):
            ProviderOllama().generate("x")

    with patch("urllib.request.urlopen", side_effect=urllib.error.URLError("falha")):
        with pytest.raises(ProviderIndisponivel):
            ProviderOllama().generate("x")


def test_ollama_healthcheck_consulta_tags_sem_gerar():
    resposta = _resposta_json({"models": [{"name": "qwen-teste"}]})
    with patch("urllib.request.urlopen", return_value=resposta) as urlopen:
        assert ProviderOllama().saudavel() is True
    pedido = urlopen.call_args.args[0]
    assert pedido.full_url == "http://localhost:11434/api/tags"
    assert pedido.method == "GET"


def test_ollama_healthcheck_falha_quando_daemon_indisponivel():
    with patch("urllib.request.urlopen", side_effect=urllib.error.URLError("offline")):
        assert ProviderOllama().saudavel() is False
