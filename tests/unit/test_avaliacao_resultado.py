import pytest

from nexora.runtime.avaliacao import AvaliadorResultado, ResultadoAvaliacao


def test_resultado_avaliacao_serializa_e_preserva_evidencias():
    resultado = ResultadoAvaliacao(
        sucesso=True,
        score=0.9,
        criterios=("teste_passou",),
        evidencias=("pytest:12_passou",),
    )
    assert resultado.para_dict() == {
        "sucesso": True,
        "score": 0.9,
        "criterios": ["teste_passou"],
        "evidencias": ["pytest:12_passou"],
        "metadados": {},
    }


def test_avaliador_agrega_multiplos_criterios_sem_ultrapassar_intervalo():
    avaliador = AvaliadorResultado([
        lambda objetivo, saida: ResultadoAvaliacao(True, 1.0, ("execucao_ok",), ("v1",)),
        lambda objetivo, saida: ResultadoAvaliacao(True, 0.6, ("criterio_ok",), ("v2",)),
    ])
    resultado = avaliador.avaliar("objetivo", "saida")
    assert resultado.sucesso is True
    assert resultado.score == pytest.approx(0.8)
    assert resultado.criterios == ("execucao_ok", "criterio_ok")
    assert resultado.evidencias == ("v1", "v2")
    assert resultado.metadados == {"avaliadores": 2}


def test_avaliador_nao_inventa_qualidade_sem_criterios():
    resultado = AvaliadorResultado().avaliar("objetivo", "saida")
    assert resultado.sucesso is False
    assert resultado.score == 0.0
    assert resultado.criterios == ("nenhum_criterio_avaliacao",)


def test_avaliador_exige_contrato_de_resultado():
    avaliador = AvaliadorResultado([lambda objetivo, saida: object()])
    with pytest.raises(TypeError, match="ResultadoAvaliacao"):
        avaliador.avaliar("objetivo", "saida")
