from nexora.providers.base import GenerationResult, Provider, ProviderCapability
from nexora.providers.manager import ProviderManager
from nexora.providers.modelos import perfil_modelo
from nexora.providers.pricing import PricingEntry, PricingRegistry
from nexora.providers.roteamento import RoteadorInteligente
from nexora.runtime.hardware import PerfilHardware


def hw():
    return PerfilHardware("Windows", "AMD64", 8, 16 * 1024**3)


class ProviderComCusto(Provider):
    def __init__(self, name: str, model: str):
        super().__init__(name, ProviderCapability(max_context_tokens=32768))
        self.modelo = model

    def generate(self, prompt: str, **kwargs):
        return GenerationResult(text=prompt, usage={"prompt_tokens": 100, "completion_tokens": 100, "total_tokens": 200})

    def saudavel(self):
        return True


def registry_custo():
    return PricingRegistry([
        PricingEntry("alpha", "model-a", "USD", 0.10, 0.10, "test-v1", "2026-09-12", "test"),
        PricingEntry("beta", "model-b", "USD", 1.00, 1.00, "test-v1", "2026-09-12", "test"),
    ])


def candidatos():
    return [
        {"provider": "beta", "modelo": "model-b", "perfil": perfil_modelo("model-b", contexto=32768, parametros="7B")},
        {"provider": "alpha", "modelo": "model-a", "perfil": perfil_modelo("model-a", contexto=32768, parametros="7B")},
    ]


def preparar_manager():
    manager = ProviderManager(pricing_registry=registry_custo())
    manager.registrar("alpha", ProviderComCusto("alpha", "model-a"))
    manager.registrar("beta", ProviderComCusto("beta", "model-b"))
    return manager


def test_roteamento_considera_custo_real_historico_sem_estimativa():
    manager = preparar_manager()
    for _ in range(3):
        manager.executar("alpha", "ping")
        manager.executar("beta", "ping")
    resultado = RoteadorInteligente(manager).selecionar(candidatos(), hw())
    assert resultado[0].provider == "alpha"
    assert "historico_custo_real_mais_baixo" in resultado[0].motivos
    beta = next(item for item in resultado if item.provider == "beta")
    assert "historico_custo_real_mais_alto" in beta.motivos


def test_roteamento_nao_considera_custo_com_amostra_insuficiente():
    manager = preparar_manager()
    for _ in range(2):
        manager.executar("alpha", "ping")
        manager.executar("beta", "ping")
    resultado = RoteadorInteligente(manager).selecionar(candidatos(), hw())
    assert not any("historico_custo_real" in motivo for item in resultado for motivo in item.motivos)


def test_roteamento_pode_desativar_consideracao_de_custo():
    manager = preparar_manager()
    for _ in range(3):
        manager.executar("alpha", "ping")
        manager.executar("beta", "ping")
    resultado = RoteadorInteligente(manager).selecionar(candidatos(), hw(), considerar_custo=False)
    assert not any("historico_custo_real" in motivo for item in resultado for motivo in item.motivos)
