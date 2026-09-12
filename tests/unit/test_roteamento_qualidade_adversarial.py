from nexora.providers.base import GenerationResult, Provider, ProviderCapability
from nexora.providers.manager import ProviderManager
from nexora.providers.modelos import perfil_modelo
from nexora.providers.roteamento import RoteadorInteligente
from nexora.runtime.avaliacao import ResultadoAvaliacao
from nexora.runtime.hardware import PerfilHardware
from nexora.runtime.historico_avaliacao import HistoricoAvaliacao


def hw() -> PerfilHardware:
    return PerfilHardware("Windows", "AMD64", 8, 16 * 1024**3)


def avaliacao(score: float, sucesso: bool = True) -> ResultadoAvaliacao:
    return ResultadoAvaliacao(sucesso, score, ("criterio",), ("evidencia",))


class ProviderTeste(Provider):
    def __init__(self) -> None:
        super().__init__("teste", ProviderCapability(max_context_tokens=32768))

    def generate(self, prompt: str, **kwargs):
        return GenerationResult(text=prompt)

    def saudavel(self):
        return True


class ProviderFalho(ProviderTeste):
    def generate(self, prompt: str, **kwargs):
        raise RuntimeError("falha de teste")


def candidato(provider: str, modelo: str, *, coding: bool = True, contexto: int = 32768, parametros: str = "7B"):
    return {
        "provider": provider,
        "modelo": modelo,
        "perfil": perfil_modelo(modelo, contexto=contexto, parametros=parametros),
    }


def registrar_qualidade(historico: HistoricoAvaliacao, provider: str, modelo: str, score: float, *, quantidade: int = 10):
    for _ in range(quantidade):
        historico.registrar(provider, modelo, "coding", avaliacao(score, score >= 0.5))


def test_qualidade_nao_domina_capacidade_do_modelo(tmp_path):
    manager = ProviderManager()
    manager.registrar("general", ProviderTeste())
    manager.registrar("coder", ProviderTeste())
    historico = HistoricoAvaliacao(tmp_path / "evaluation.json")
    registrar_qualidade(historico, "general", "general-7b", 1.0)
    registrar_qualidade(historico, "coder", "coder-7b", 0.0, quantidade=10)

    resultado = RoteadorInteligente(manager, historico_avaliacao=historico).selecionar(
        [
            candidato("general", "general-7b"),
            candidato("coder", "coder-7b"),
        ],
        hw(),
        tarefa="coding",
    )

    assert resultado[0].provider == "coder"
    assert resultado[0].score > resultado[1].score
    assert "qualidade_tarefa_historica_abaixo_media" in resultado[0].motivos
    assert "qualidade_tarefa_historica_acima_media" in resultado[1].motivos


def test_qualidade_nao_domina_confiabilidade_historica(tmp_path):
    manager = ProviderManager()
    manager.registrar("falho", ProviderFalho())
    manager.registrar("bom", ProviderTeste())
    for _ in range(3):
        try:
            manager.executar("falho", "ping")
        except RuntimeError:
            pass
        manager.executar("bom", "ping")

    historico = HistoricoAvaliacao(tmp_path / "evaluation.json")
    registrar_qualidade(historico, "falho", "coder-falho", 1.0)
    registrar_qualidade(historico, "bom", "coder-bom", 0.0, quantidade=10)

    resultado = RoteadorInteligente(manager, historico_avaliacao=historico).selecionar(
        [
            candidato("falho", "coder-falho"),
            candidato("bom", "coder-bom"),
        ],
        hw(),
        tarefa="coding",
    )

    assert resultado[0].provider == "bom"
    falho = next(item for item in resultado if item.provider == "falho")
    assert "historico_alta_taxa_erro" in falho.motivos
    assert "qualidade_tarefa_historica_acima_media" in falho.motivos


def test_qualidade_tem_influencia_limitada_e_nao_reordena_capacidade_forte(tmp_path):
    manager = ProviderManager()
    manager.registrar("forte", ProviderTeste())
    manager.registrar("fraco", ProviderTeste())
    historico = HistoricoAvaliacao(tmp_path / "evaluation.json")
    registrar_qualidade(historico, "forte", "coder-32b", 0.0)
    registrar_qualidade(historico, "fraco", "general-1b", 1.0)

    resultado = RoteadorInteligente(manager, historico_avaliacao=historico).selecionar(
        [
            candidato("fraco", "general-1b", parametros="1B"),
            candidato("forte", "coder-32b", parametros="32B"),
        ],
        hw(),
        tarefa="coding",
    )

    assert resultado[0].provider == "forte"
    assert resultado[0].score - resultado[1].score >= 7.0
