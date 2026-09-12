"""Testes do verificador determinístico de adequação de evidência."""
from __future__ import annotations

import pytest

from nexora.runtime.verificacao_evidencia import verificar_adequacao


def test_claim_claramente_sustentado_por_trecho():
    resultado = verificar_adequacao(
        "NEXORA possui pesquisa estruturada",
        "A NEXORA possui pesquisa estruturada com fontes verificáveis.",
    )
    assert resultado.status == "SUSTENTADA"
    assert resultado.cobertura == 1.0


def test_claim_sem_sobreposicao_e_insuficiente():
    resultado = verificar_adequacao(
        "NEXORA possui pesquisa estruturada",
        "O documento descreve somente política de preços para produtos.",
    )
    assert resultado.status == "INSUFICIENTE"
    assert resultado.cobertura == 0.0


def test_fonte_valida_mas_nao_sustenta_claim():
    resultado = verificar_adequacao(
        "A plataforma usa pesquisa estruturada",
        "A fonte é válida e foi publicada por uma organização conhecida, mas trata apenas de faturamento.",
    )
    assert resultado.status == "INSUFICIENTE"


def test_trecho_vazio_e_indeterminado():
    resultado = verificar_adequacao("NEXORA possui pesquisa estruturada", "")
    assert resultado.status == "INDETERMINADA"
    assert resultado.motivo == "trecho_vazio"


def test_multiplas_fontes_podem_ser_avaliadas_independentemente():
    resultados = [
        verificar_adequacao("NEXORA possui pesquisa estruturada", "A pesquisa estruturada da NEXORA usa fontes."),
        verificar_adequacao("NEXORA possui pesquisa estruturada", "O sistema descreve apenas cobrança e faturamento."),
    ]
    assert [r.status for r in resultados] == ["SUSTENTADA", "INSUFICIENTE"]


def test_claim_sem_termos_relevantes_e_indeterminado():
    resultado = verificar_adequacao("e um", "texto qualquer")
    assert resultado.status == "INDETERMINADA"


@pytest.mark.parametrize("limiar", [0, -0.1, 1.1])
def test_limiar_invalido(limiar):
    with pytest.raises(ValueError):
        verificar_adequacao("claim relevante", "trecho relevante", limiar_sustentacao=limiar)
