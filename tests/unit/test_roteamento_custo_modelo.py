from nexora.providers.base import GenerationResult, ProviderCapability
from nexora.providers.manager import ProviderManager
from nexora.providers.modelos import PerfilCapacidadeModelo
from nexora.providers.pricing import PricingEntry, PricingRegistry
from nexora.providers.roteamento import RoteadorInteligente
from nexora.runtime.hardware import PerfilHardware


class ProviderFake:
    name = "groq"

    def __init__(self, modelo: str) -> None:
        self.modelo = modelo
        self.capabilities = ProviderCapability()

    def generate(self, prompt: str, **kwargs):
        return GenerationResult(text="ok", usage={"prompt_tokens": 100, "completion_tokens": 100, "total_tokens": 200})


def test_router_prefere_modelo_com_custo_real_menor():
    pricing = PricingRegistry([
        PricingEntry("groq", "model-a", "USD", 1.0, 1.0, "test", "2026-09-12", "test"),
        PricingEntry("groq", "model-b", "USD", 2.0, 2.0, "test", "2026-09-12", "test"),
    ])
    manager = ProviderManager(pricing_registry=pricing)
    manager.registrar("groq", ProviderFake("model-a"))

    for _ in range(3):
        manager.executar_instancia("groq", ProviderFake("model-a"), "x")
        manager.executar_instancia("groq", ProviderFake("model-b"), "x")

    perfil = PerfilCapacidadeModelo(categoria="general", tamanho_parametros_b=7.0, contexto=4096)
    hardware = PerfilHardware("Linux", "x86_64", 8, 16 * 1024**3)
    candidatos = [
        {"provider": "groq", "modelo": "model-a", "perfil": perfil},
        {"provider": "groq", "modelo": "model-b", "perfil": perfil},
    ]

    resultado = RoteadorInteligente(manager).selecionar(candidatos, hardware, usar_historico=False)
    assert resultado[0].modelo == "model-a"
    assert "historico_custo_modelo_real_mais_baixo" in resultado[0].motivos
    assert "historico_custo_modelo_real_mais_alto" in resultado[1].motivos


def test_router_nao_aplica_custo_modelo_com_amostra_insuficiente():
    pricing = PricingRegistry([
        PricingEntry("groq", "model-a", "USD", 1.0, 1.0, "test", "2026-09-12", "test"),
        PricingEntry("groq", "model-b", "USD", 2.0, 2.0, "test", "2026-09-12", "test"),
    ])
    manager = ProviderManager(pricing_registry=pricing)
    manager.registrar("groq", ProviderFake("model-a"))
    for _ in range(2):
        manager.executar_instancia("groq", ProviderFake("model-a"), "x")
        manager.executar_instancia("groq", ProviderFake("model-b"), "x")

    perfil = PerfilCapacidadeModelo(categoria="general", tamanho_parametros_b=7.0, contexto=4096)
    hardware = PerfilHardware("Linux", "x86_64", 8, 16 * 1024**3)
    candidatos = [
        {"provider": "groq", "modelo": "model-a", "perfil": perfil},
        {"provider": "groq", "modelo": "model-b", "perfil": perfil},
    ]
    resultado = RoteadorInteligente(manager).selecionar(candidatos, hardware, usar_historico=False)
    assert all("historico_custo_modelo_real_" not in " ".join(item.motivos) for item in resultado)
