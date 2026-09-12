from nexora.runtime.agente import AgenteRuntime
from nexora.runtime.avaliacao import AvaliadorResultado, ResultadoAvaliacao


class Falha:
    plano = "abort"
    motivo = "falha"


def test_runtime_anexa_avaliacao_real_ao_resultado_e_trace():
    avaliador = AvaliadorResultado([
        lambda objetivo, saida: ResultadoAvaliacao(
            sucesso=saida == "ok",
            score=1.0 if saida == "ok" else 0.0,
            criterios=("saida_exata",),
            evidencias=("verificador:ok",),
        )
    ])
    runtime = AgenteRuntime(
        executar=lambda objetivo: "ok",
        verificar=lambda saida: True,
        analisar=lambda observacao: Falha(),
        corregir=lambda objetivo, falha: "ok",
        avaliador=avaliador,
    )
    resultado = runtime.executar("teste")
    assert resultado.sucesso is True
    assert resultado.avaliacao["score"] == 1.0
    assert resultado.avaliacao["evidencias"] == ["verificador:ok"]
    assert resultado.trace["metadata"]["evaluation"]["score"] == 1.0
    assert resultado.metricas["evaluation_score"] == 1.0


def test_runtime_sem_avaliador_preserva_contrato_legacy():
    runtime = AgenteRuntime(
        executar=lambda objetivo: "ok",
        verificar=lambda saida: True,
        analisar=lambda observacao: Falha(),
        corregir=lambda objetivo, falha: "ok",
    )
    resultado = runtime.executar("teste")
    assert resultado.sucesso is True
    assert resultado.avaliacao == {}
    assert "evaluation_score" not in resultado.metricas
