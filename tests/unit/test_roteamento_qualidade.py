from nexora.providers.base import Provider, ProviderCapability
from nexora.providers.manager import ProviderManager
from nexora.providers.modelos import perfil_modelo
from nexora.providers.roteamento import RoteadorInteligente
from nexora.runtime.hardware import PerfilHardware
from nexora.runtime.historico_avaliacao import HistoricoAvaliacao
from nexora.runtime.avaliacao import ResultadoAvaliacao


def hw():
    return PerfilHardware("Windows", "AMD64", 8, 16 * 1024**3)


class ProviderQualidade(Provider):
    def __init__(self, name: str, model: str):
        super().__init__(name, ProviderCapability(max_context_tokens=32768))
        self.modelo = model

    def generate(self, prompt: str, **kwargs):
        return prompt

    def saudavel(self):
        return True


def candidatos():
    return [
        {"provider": "alpha", "modelo": "model-a", "perfil": perfil_modelo("model-a", contexto=32768, parametros="7B")},
        {"provider": "beta", "modelo": "model-b", "perfil": perfil_modelo("model-b", contexto=32768, parametros="7B")},
    ]


def registrar(historico, provider, modelo, tipo, score, quantidade=5):
    avaliacao = ResultadoAvaliacao(score >= 0.5, score, ("criterio",), ("evidencia",))
    for _ in range(quantidade):
        historico.registrar(provider, modelo, tipo, avaliacao)


def manager():
    m = ProviderManager()
    m.registrar("alpha", lambda: ProviderQualidade("alpha", "model-a"))
    m.registrar("beta", lambda: ProviderQualidade("beta", "model-b"))
    return m


def test_qualidade_so_influencia_apos_amostra_minima_e_no_tipo_exato(tmp_path):
    historico = HistoricoAvaliacao(tmp_path / "evaluation-history.json")
    registrar(historico, "alpha", "model-a", "coding", 0.95, 4)
    registrar(historico, "beta", "model-b", "coding", 0.55, 4)
    router = RoteadorInteligente(manager(), historico)
    antes = router.selecionar(candidatos(), hw(), tarefa="coding")
    assert all("qualidade_tarefa_historica" not in motivo for item in antes for motivo in item.motivos)

    historico.registrar("alpha", "model-a", "coding", ResultadoAvaliacao(True, 0.95))
    historico.registrar("beta", "model-b", "coding", ResultadoAvaliacao(True, 0.55))
    depois = router.selecionar(candidatos(), hw(), tarefa="coding")
    alpha = next(item for item in depois if item.provider == "alpha")
    beta = next(item for item in depois if item.provider == "beta")
    assert alpha.score > beta.score
    assert "qualidade_tarefa_historica_acima_media" in alpha.motivos
    assert "qualidade_tarefa_historica_abaixo_media" in beta.motivos

    outro_tipo = router.selecionar(candidatos(), hw(), tarefa="research")
    assert all("qualidade_tarefa_historica" not in motivo for item in outro_tipo for motivo in item.motivos)


def test_qualidade_nao_influencia_sem_dois_candidatos_com_amostra(tmp_path):
    historico = HistoricoAvaliacao(tmp_path / "evaluation-history.json")
    registrar(historico, "alpha", "model-a", "coding", 0.99, 5)
    router = RoteadorInteligente(manager(), historico)
    resultado = router.selecionar(candidatos(), hw(), tarefa="coding")
    alpha = next(item for item in resultado if item.provider == "alpha")
    assert "qualidade_tarefa_historica_acima_media" not in alpha.motivos
