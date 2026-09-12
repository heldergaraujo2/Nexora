from nexora.runtime.avaliacao import ResultadoAvaliacao
from nexora.runtime.historico_avaliacao import HistoricoAvaliacao


def avaliacao(score: float, sucesso: bool = True) -> ResultadoAvaliacao:
    return ResultadoAvaliacao(sucesso, score, ("criterio",), ("evidencia",))


def test_qualidade_para_roteamento_bloqueia_amostra_insuficiente(tmp_path):
    historico = HistoricoAvaliacao(tmp_path / "evaluation.json")
    for _ in range(4):
        historico.registrar("alpha", "model-a", "coding", avaliacao(1.0))

    resultado = historico.qualidade_para_roteamento("alpha", "model-a", "coding", min_amostra=5)

    assert resultado["amostra_suficiente"] is False
    assert resultado["avaliacoes"] == 4
    assert resultado["score_medio"] is None


def test_qualidade_para_roteamento_expoe_score_somente_com_amostra_suficiente(tmp_path):
    historico = HistoricoAvaliacao(tmp_path / "evaluation.json")
    for score in (1.0, 0.8, 0.6, 1.0, 0.6):
        historico.registrar("alpha", "model-a", "coding", avaliacao(score))

    resultado = historico.qualidade_para_roteamento("alpha", "model-a", "coding", min_amostra=5)

    assert resultado["amostra_suficiente"] is True
    assert resultado["avaliacoes"] == 5
    assert resultado["score_medio"] == 0.8
    assert resultado["taxa_sucesso"] == 1.0


def test_qualidade_para_roteamento_isola_provider_modelo_e_tipo(tmp_path):
    historico = HistoricoAvaliacao(tmp_path / "evaluation.json")
    for _ in range(5):
        historico.registrar("alpha", "model-a", "coding", avaliacao(1.0))
        historico.registrar("alpha", "model-a", "research", avaliacao(0.2, False))
        historico.registrar("beta", "model-a", "coding", avaliacao(0.2, False))

    coding_alpha = historico.qualidade_para_roteamento("alpha", "model-a", "coding", min_amostra=5)
    research_alpha = historico.qualidade_para_roteamento("alpha", "model-a", "research", min_amostra=5)
    coding_beta = historico.qualidade_para_roteamento("beta", "model-a", "coding", min_amostra=5)

    assert coding_alpha["score_medio"] == 1.0
    assert research_alpha["score_medio"] == 0.2
    assert coding_beta["score_medio"] == 0.2


def test_qualidade_para_roteamento_valida_limiar():
    historico = HistoricoAvaliacao()
    try:
        historico.qualidade_para_roteamento("alpha", "model-a", "coding", min_amostra=0)
    except ValueError as exc:
        assert "min_amostra" in str(exc)
    else:
        raise AssertionError("deveria rejeitar limiar invalido")
