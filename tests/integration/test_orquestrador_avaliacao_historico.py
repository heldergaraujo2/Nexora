from __future__ import annotations

from nexora.orquestracao.orquestrador import Orquestrador
from nexora.providers.base import GenerationResult
from nexora.providers.manager import ProviderManager
from nexora.runtime.avaliacao import AvaliadorResultado, ResultadoAvaliacao
from nexora.runtime.historico_avaliacao import HistoricoAvaliacao


class _Provider:
    name = "provider-eval"
    modelo = "model-eval"

    def __init__(self) -> None:
        self.chamadas = 0

    def saudavel(self) -> bool:
        return True

    def generate(self, _prompt: str) -> GenerationResult:
        self.chamadas += 1
        return GenerationResult(text="resultado valido", tool_calls=[])


class _Rotador:
    def __init__(self, provider) -> None:
        self.provider = provider

    def obter_provider(self, _objetivo: str, alias=None):
        return self.provider


def test_orquestrador_registra_qualidade_observada_por_tipo_provider_e_modelo(tmp_path) -> None:
    provider = _Provider()
    manager = ProviderManager(persistencia_path=tmp_path / "provider-history.json")
    manager.registrar(provider.name, lambda: provider)
    historico = HistoricoAvaliacao(tmp_path / "evaluation-history.json")
    avaliador = AvaliadorResultado([lambda _objetivo, saida: ResultadoAvaliacao(saida == "resultado valido", 0.9 if saida == "resultado valido" else 0.0, ("saida_valida",), ("resultado_observado",))])
    orquestrador = Orquestrador(
        rotador=_Rotador(provider),
        provider=provider,
        provider_manager=manager,
        avaliador_resultado=avaliador,
        historico_avaliacao=historico,
        planejador=lambda _: [{"id": "t1", "descricao": "executar tarefa", "tipo": "coding"}],
    )

    resultado = orquestrador.executar("executar tarefa")

    assert resultado["sucesso"] is True
    assert provider.chamadas == 1
    assert resultado["etapas"][0]["tipo"] == "coding"
    assert resultado["etapas"][0]["avaliacao"]["score"] == 0.9
    stats = historico.estatisticas("provider-eval", "model-eval", "coding")
    assert stats["avaliacoes"] == 1
    assert stats["sucessos"] == 1
    assert stats["score_medio"] == 0.9

    recarregado = HistoricoAvaliacao(tmp_path / "evaluation-history.json")
    assert recarregado.estatisticas("provider-eval", "model-eval", "coding")["avaliacoes"] == 1
