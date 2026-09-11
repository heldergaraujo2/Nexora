"""Testes do ProviderManager."""
import pytest

from nexora.providers.base import GenerationResult
from nexora.providers.base import Provider, ProviderCapability, ProviderError
from nexora.providers.manager import ProviderManager


class ProviderSaudavel(Provider):
    def __init__(self):
        super().__init__(name="saudavel", capabilities=ProviderCapability())
        self.chamadas = 0

    def generate(self, prompt, **kwargs):
        self.chamadas +=  1
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
    assert manager.obter_healthcheck("saudavel") ["saudavel"] is True
    assert manager.obter_healthcheck("nao-existe") ["saudavel"] is False
