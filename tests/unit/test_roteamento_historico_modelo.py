from nexora.providers.base import GenerationResult, Provider, ProviderCapability
from nexora.providers.manager import ProviderManager
from nexora.providers.modelos import perfil_modelo
from nexora.providers.pricing import PricingRegistry
from nexora.providers.roteamento import RoteadorInteligente
from nexora.runtime.hardware import PerfilHardware


def hw():
    return PerfilHardware("Windows", "AMD64", 8, 16 * 1024**3)


class ProviderHistorico(Provider):
    def __init__(self, name: str, model: str, falhar: bool = False):
        super().__init__(name, ProviderCapability(max_context_tokens=32768))
        self.modelo = model
        self.falhar = falhar

    def generate(self, prompt: str, **kwargs):
        if self.falhar:
            raise RuntimeError("falha controlada")
        return GenerationResult(text=prompt)

    def saudavel(self):
        return True


def candidatos():
    return [
        {"provider": "alpha", "modelo": "model-a", "perfil": perfil_modelo("model-a", contexto=32768, parametros="7B")},
        {"provider": "beta", "modelo": "model-b", "perfil": perfil_modelo("model-b", contexto=32768, parametros="7B")},
    ]


def manager():
    m = ProviderManager(pricing_registry=PricingRegistry())
    m.registrar("alpha", ProviderHistorico("alpha", "model-a"))
    m.registrar("beta", ProviderHistorico("beta", "model-b"))
    return m


def test_roteamento_prefere_confiabilidade_do_modelo_quando_ha_amostra():
    m = manager()
    for _ in range(3):
        m.executar("alpha", "ok")
        m.executar("beta", "ok")
    # Injeta duas falhas adicionais somente no modelo beta.
    m._fabricas["beta"] = ProviderHistorico("beta", "model-b", falhar=True)
    for _ in range(2):
        try:
            m.executar("beta", "falhar")
        except RuntimeError:
            pass
    resultado = RoteadorInteligente(m).selecionar(candidatos(), hw())
    alpha = next(item for item in resultado if item.provider == "alpha")
    beta = next(item for item in resultado if item.provider == "beta")
    assert alpha.score > beta.score
    assert "historico_alta_taxa_sucesso" in alpha.motivos
    assert "historico_alta_taxa_erro" in beta.motivos


def test_roteamento_usa_latencia_do_modelo_sem_misturar_outros_modelos():
    m = manager()
    for _ in range(3):
        m.executar("alpha", "ok")
        m.executar("beta", "ok")
    # A latência do provider alpha é artificialmente menor somente no modelo alpha.
    m._metricas_modelo["alpha"]["model-a"]["tempo_total"] = 0.3
    m._metricas_modelo["beta"]["model-b"]["tempo_total"] = 3.0
    resultado = RoteadorInteligente(m).selecionar(candidatos(), hw())
    alpha = next(item for item in resultado if item.provider == "alpha")
    beta = next(item for item in resultado if item.provider == "beta")
    assert "historico_baixa_latencia" in alpha.motivos
    assert "historico_alta_latencia" in beta.motivos
