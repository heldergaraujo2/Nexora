from types import SimpleNamespace

import pytest

from nexora.runtime.reconciliacao_evidencia import (
    ReconciliadorEvidencias,
    ResultadoReconciliacao,
    StatusReconciliacao,
)


def evidencia(ref: str, trecho: str, status: str = "SUSTENTADA"):
    return SimpleNamespace(
        source_ref=ref,
        titulo="Fonte sobre NEXORA",
        trecho=trecho,
        adequacao=SimpleNamespace(status=status),
    )


def test_duas_fontes_independentes_corrobora():
    r = ReconciliadorEvidencias()
    resultado = r.reconciliar(
        "NEXORA possui pesquisa estruturada",
        [
            evidencia("a", "NEXORA possui pesquisa estruturada e rastreável."),
            evidencia("b", "NEXORA possui pesquisa estruturada com fontes."),
        ],
    )
    assert isinstance(resultado, ResultadoReconciliacao)
    assert resultado.status == StatusReconciliacao.CORROBORADA
    assert resultado.fontes_independentes == 2
    assert resultado.confianca is None


def test_uma_unica_fonte_nao_corrobora():
    resultado = ReconciliadorEvidencias().reconciliar(
        "NEXORA possui pesquisa estruturada",
        [evidencia("a", "NEXORA possui pesquisa estruturada.")],
    )
    assert resultado.status == StatusReconciliacao.NAO_CORROBORADA
    assert resultado.fontes_independentes == 1


def test_fontes_nao_relacionadas_nao_corroboram():
    resultado = ReconciliadorEvidencias().reconciliar(
        "NEXORA possui pesquisa estruturada",
        [
            evidencia("a", "O clima possui temperatura estável."),
            evidencia("b", "Um produto possui embalagem reciclável."),
        ],
    )
    assert resultado.status == StatusReconciliacao.NAO_CORROBORADA


def test_evidencias_inadequadas_nao_contam():
    resultado = ReconciliadorEvidencias().reconciliar(
        "NEXORA possui pesquisa estruturada",
        [
            evidencia("a", "NEXORA possui pesquisa estruturada.", "INSUFICIENTE"),
            evidencia("b", "NEXORA possui pesquisa estruturada.", "INDETERMINADA"),
        ],
    )
    assert resultado.status == StatusReconciliacao.NAO_CORROBORADA
    assert resultado.evidencias_consideradas == 0


def test_mesma_source_ref_nao_cria_falsa_independencia():
    resultado = ReconciliadorEvidencias().reconciliar(
        "NEXORA possui pesquisa estruturada",
        [
            evidencia("mesma", "NEXORA possui pesquisa estruturada."),
            evidencia("mesma", "NEXORA possui pesquisa estruturada com fontes."),
        ],
    )
    assert resultado.status == StatusReconciliacao.NAO_CORROBORADA
    assert resultado.fontes_independentes == 1


def test_polaridade_negativa_explicita_gera_conflito():
    resultado = ReconciliadorEvidencias().reconciliar(
        "NEXORA possui pesquisa estruturada",
        [
            evidencia("a", "NEXORA possui pesquisa estruturada e rastreável."),
            evidencia("b", "NEXORA não possui pesquisa estruturada."),
        ],
    )
    assert resultado.status == StatusReconciliacao.CONFLITANTE
    assert len(resultado.pares_conflitantes) == 1


def test_resultado_para_dict_preserva_auditoria():
    resultado = ReconciliadorEvidencias().reconciliar(
        "NEXORA possui pesquisa estruturada",
        [evidencia("a", "NEXORA possui pesquisa estruturada.")],
    )
    payload = resultado.para_dict()
    assert payload["status"] == StatusReconciliacao.NAO_CORROBORADA
    assert payload["confianca"] is None


def test_min_termos_e_validado():
    with pytest.raises(ValueError):
        ReconciliadorEvidencias(min_termos=0)


def test_claim_vazio_e_rejeitado():
    with pytest.raises(ValueError):
        ReconciliadorEvidencias().reconciliar("  ", [])
