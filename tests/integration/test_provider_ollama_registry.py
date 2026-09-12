"""Integração do Ollama com RegistryProviders e ProviderManager."""
from __future__ import annotations

import json
from unittest.mock import MagicMock, patch

from nexora.providers.manager import ProviderManager
from nexora.providers.ollama import ProviderOllama
from nexora.providers.registry import RegistryProviders


def _resposta(payload: dict) -> MagicMock:
    resposta = MagicMock()
    resposta.read.return_value = json.dumps(payload).encode("utf-8")
    resposta.__enter__.return_value = resposta
    return resposta


def test_ollama_pode_ser_registrado_e_executado_pela_camada_de_providers():
    registry = RegistryProviders()
    registry.registrar("ollama", lambda: ProviderOllama(modelo="modelo-teste"), prioridade=1)
    manager = ProviderManager()
    manager.registrar("ollama", lambda: ProviderOllama(modelo="modelo-teste"))

    with patch(
        "urllib.request.urlopen",
        return_value=_resposta({"message": {"content": "ok local"}}),
    ):
        resultado = manager.executar("OLLAMA", "teste")

    assert registry.disponiveis() == ["ollama"]
    assert registry.prioridade("ollama") == 1
    assert resultado.text == "ok local"
    assert manager.estatisticas()["chamadas"] == 1
