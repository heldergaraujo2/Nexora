from nexora.orquestracao.orquestrador import Orquestrador
from nexora.providers.base import GenerationResult, Provider, ProviderCapability
from nexora.providers.manager import ProviderManager
from nexora.providers.modelos import perfil_modelo
from nexora.providers.roteamento import RoteadorInteligente
from nexora.runtime.avaliacao import AvaliadorResultado, ResultadoAvaliacao
from nexora.runtime.hardware import PerfilHardware
from nexora.runtime.historico_avaliacao import HistoricoAvaliacao


class _Provider(Provider):
    def __init__(self, name: str, model: str):
        super().__init__(name, ProviderCapability(max_context_tokens=32768))
        self.modelo = model
        self.chamadas = 0

    def generate(self, prompt: str, **kwargs):
        self.chamadas += 1
        return GenerationResult(text=f"{self.name}:{prompt}")

    def saudavel(self):
        return True


def _candidatos():
    return [
        {"provider": "alpha", "modelo": "model-a", "perfil": perfil_modelo("model-a", contexto=32768, parametros="7B")},
        {"provider": "beta", "modelo": "model-b", "perfil": perfil_modelo("model-b", contexto=32768, parametros="7B")},
    ]


def _registrar(historico, provider, model, score, quantidade=5):
    avaliacao = ResultadoAvaliacao(True, score, ("qualidade",), ("observada",))
    for _ in range(quantidade):
        historico.registrar(provider, model, "coding", avaliacao)


def test_orquestrador_seleciona_modelo_por_qualidade_observada_do_tipo(tmp_path):
    alpha = _Provider("alpha", "model-a")
    beta = _Provider("beta", "model-b")
    manager = ProviderManager(persistencia_path=tmp_path / "provider-history.json")
    manager.registrar("alpha", lambda: alpha)
    manager.registrar("beta", lambda: beta)
    historico = HistoricoAvaliacao(tmp_path / "evaluation-history.json")
    _registrar(historico, "alpha", "model-a", 0.95)
    _registrar(historico, "beta", "model-b", 0.55)

    router = RoteadorInteligente(manager, historico)
    avaliador = AvaliadorResultado([lambda _objetivo, saida: ResultadoAvaliacao(True, 0.9, ("resultado",), (saida,))])
    orquestrador = Orquestrador(
        rotador=type("Rotador", (), {"obter_provider": lambda _self, _objetivo, alias=None: alpha})(),
        provider=alpha,
        provider_manager=manager,
        roteador_inteligente=router,
        candidatos_roteamento=_candidatos(),
        hardware=PerfilHardware("Windows", "AMD64", 8, 16 * 1024**3),
        avaliador_resultado=avaliador,
        historico_avaliacao=historico,
        planejador=lambda _: [{"id": "t1", "descricao": "implementar codigo", "tipo": "coding"}],
    )

    resultado = orquestrador.executar("implementar codigo")

    assert resultado["sucesso"] is True
    assert alpha.chamadas == 1
    assert beta.chamadas == 0
    decisao = resultado["etapas"][0]["trace"]["metadata"]["routing_decision"]
    assert decisao["selected"]["provider"] == "alpha"
    assert "qualidade_tarefa_historica_acima_media" in decisao["selected"]["motivos"]
