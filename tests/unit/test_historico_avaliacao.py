from nexora.runtime.avaliacao import ResultadoAvaliacao
from nexora.runtime.historico_avaliacao import HistoricoAvaliacao


def test_historico_persiste_por_provider_modelo_e_tipo(tmp_path) -> None:
    caminho = tmp_path / "evaluation-history.json"
    historico = HistoricoAvaliacao(caminho)
    historico.registrar("Provider-A", "model-1", "coding", ResultadoAvaliacao(True, 0.9, ("teste",), ("e1",)))
    historico.registrar("Provider-A", "model-1", "coding", ResultadoAvaliacao(False, 0.3, ("teste",), ("e2",)))
    historico.registrar("Provider-A", "model-2", "coding", ResultadoAvaliacao(True, 1.0))
    historico.registrar("Provider-A", "model-1", "research", ResultadoAvaliacao(True, 0.8))

    assert historico.estatisticas("provider-a", "model-1", "coding") == {
        "avaliacoes": 2,
        "sucessos": 1,
        "score_medio": 0.6,
        "taxa_sucesso": 0.5,
    }
    assert historico.estatisticas("provider-a", "model-2", "coding")["avaliacoes"] == 1
    assert historico.estatisticas("provider-a", "model-1", "research")["score_medio"] == 0.8

    recarregado = HistoricoAvaliacao(caminho)
    assert recarregado.estatisticas("provider-a", "model-1", "coding")["score_medio"] == 0.6


def test_historico_nao_inventa_qualidade_sem_registro(tmp_path) -> None:
    historico = HistoricoAvaliacao(tmp_path / "evaluation-history.json")
    stats = historico.estatisticas("provider", "model", "coding")
    assert stats["avaliacoes"] == 0
    assert stats["score_medio"] is None
    assert stats["taxa_sucesso"] is None


def test_historico_rejeita_score_fora_do_intervalo(tmp_path) -> None:
    historico = HistoricoAvaliacao(tmp_path / "evaluation-history.json")
    try:
        historico.registrar("provider", "model", "coding", {"sucesso": True, "score": 1.1})
    except ValueError as erro:
        assert "score" in str(erro)
    else:
        raise AssertionError("score invalido deveria ser rejeitado")
