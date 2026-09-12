"""Testes do ProviderManager."""
import json

import pytest

from nexora.providers.base import GenerationResult
from nexora.providers.base import Provider, ProviderCapability, ProviderError
from nexora.providers.manager import ProviderManager


class ProviderSaudavel(Provider):
    def __init__(self):
        super().__init__(name="saudavel", capabilities=ProviderCapability())
        self.chamadas = 0

    def generate(self, prompt, **kwargs):
        self.chamadas += 1
        return GenerationResult(text="ok")

    def saudavel(self):
        return True


class ProviderDoente(Provider):
    def __init__(self):
        super().__init__(name="doente", capabilities=ProviderCapability())

    def generate(self, prompt, **kwargs):
        raise ProviderError("fora do ar")

    def saudavel(self):
        return False


def test_manager_estatisticas_contam_chamadas_e_erros():
    manager = ProviderManager()
    manager.registrar("saudavel", ProviderSaudavel)
    manager.registrar("doente", ProviderDoente)
    resultado = manager.executar("saudavel", "oi")
    assert resultado.text == "ok"
    with pytest.raises(ProviderError):
        manager.executar("doente", "oi")
    stats = manager.estatisticas()
    assert stats["chamadas"] == 2
    assert stats["erros"] == 1
    assert "doente" in stats["ultimas_falhas"]


def test_manager_healthcheck_reporta_estado():
    manager = ProviderManager()
    manager.registrar("saudavel", ProviderSaudavel)
    assert manager.obter_healthcheck("saudavel")["saudavel"] is True
    assert manager.obter_healthcheck("nao-existe")["saudavel"] is False


def test_manager_persiste_e_recarrega_historico(tmp_path):
    caminho = tmp_path / "provider-history.json"
    primeiro = ProviderManager(persistencia_path=caminho)
    primeiro.registrar("saudavel", ProviderSaudavel)
    assert primeiro.executar("saudavel", "oi").text == "ok"

    segundo = ProviderManager(persistencia_path=caminho)
    segundo.registrar("saudavel", ProviderSaudavel)
    stats = segundo.estatisticas_provider("saudavel")
    assert stats["chamadas"] == 1
    assert stats["sucessos"] == 1
    assert stats["erros"] == 0
    assert stats["latencia_media"] is not None


def test_manager_persistencia_registra_falha_e_sobrevive_a_novo_processo(tmp_path):
    caminho = tmp_path / "provider-history.json"
    primeiro = ProviderManager(persistencia_path=caminho)
    primeiro.registrar("doente", ProviderDoente)
    with pytest.raises(ProviderError):
        primeiro.executar("doente", "oi")

    segundo = ProviderManager(persistencia_path=caminho)
    segundo.registrar("doente", ProviderDoente)
    stats = segundo.estatisticas_provider("doente")
    assert stats["chamadas"] == 1
    assert stats["erros"] == 1
    assert stats["ultima_falha"] == "fora do ar"


def test_manager_persistencia_tem_schema_e_escrita_atomica(tmp_path):
    caminho = tmp_path / "provider-history.json"
    manager = ProviderManager(persistencia_path=caminho)
    manager.registrar("saudavel", ProviderSaudavel)
    manager.executar("saudavel", "oi")

    dados = json.loads(caminho.read_text(encoding="utf-8"))
    assert dados["schema_version"] == 1
    assert dados["providers"]["saudavel"]["chamadas"] == 1
    assert not caminho.with_name(".provider-history.json.tmp").exists()


def test_manager_persistencia_ignora_arquivo_invalido(tmp_path):
    caminho = tmp_path / "provider-history.json"
    caminho.write_text("{invalido", encoding="utf-8")
    manager = ProviderManager(persistencia_path=caminho)
    manager.registrar("saudavel", ProviderSaudavel)
    assert manager.estatisticas_provider("saudavel")["chamadas"] == 0


def test_manager_persistencia_pode_ser_configurada_por_variavel_de_ambiente(tmp_path, monkeypatch):
    caminho = tmp_path / "env-history.json"
    monkeypatch.setenv("NEXORA_PROVIDER_HISTORY_PATH", str(caminho))
    manager = ProviderManager()
    manager.registrar("saudavel", ProviderSaudavel)
    manager.executar("saudavel", "oi")

    assert caminho.exists()
    dados = json.loads(caminho.read_text(encoding="utf-8"))
    assert dados["providers"]["saudavel"]["sucessos"] == 1
