from nexora.runtime.agente import AgenteRuntime
from nexora.runtime.analise import AnalisadorFalhas
from nexora.runtime.observacao import Observacao


def test_observacao_captura_saida():
    obs = Observacao(etapa_id="t1", ok=True, saida="ola", metadados={"fonte": "fake"})
    assert obs.etapa_id == "t1"
    assert obs.ok is True
    assert obs.saida == "ola"
    assert obs.carimbo


def test_observacao_captura_erro():
    obs = Observacao(etapa_id="t2", ok=False, saida="", erro="timeout")
    assert obs.erro == "timeout"
    assert obs.ok is False


def test_analisador_consumes_observacao_canonica_com_erro():
    observacao = Observacao(
        etapa_id="agent:1",
        ok=False,
        saida="",
        erro="timeout temporario",
        metadados={"tentativa": 1},
    )

    falha = AnalisadorFalhas().analisar(observacao)

    assert falha.retentavel is True
    assert falha.plano == "retry"
    assert falha.motivo == "timeout temporario"


def test_runtime_entrega_observacao_canonica_ao_analisador():
    observacoes = []

    class Falha:
        plano = "abort"
        motivo = "teste"

        def para_dict(self):
            return {"plano": self.plano, "motivo": self.motivo}

    runtime = AgenteRuntime(
        executar=lambda objetivo: "resultado",
        verificar=lambda saida: False,
        analisar=lambda observacao: observacoes.append(observacao) or Falha(),
        corregir=lambda objetivo, falha: "nao usado",
        max_tentativas=1,
    )

    resultado = runtime.executar("objetivo")

    assert resultado.sucesso is False
    assert len(observacoes) == 1
    assert isinstance(observacoes[0], Observacao)
    assert observacoes[0].etapa_id == "agent:1"
    assert observacoes[0].ok is False
    assert observacoes[0].saida == "resultado"
    assert observacoes[0].erro is None
    assert observacoes[0].metadados["tentativa"] == 1


def test_runtime_mantem_historico_serializavel_apos_observacao_canonica():
    runtime = AgenteRuntime(
        executar=lambda objetivo: "ok",
        verificar=lambda saida: True,
        analisar=AnalisadorFalhas().analisar,
        corregir=lambda objetivo, falha: objetivo,
    )

    resultado = runtime.executar("objetivo")

    assert resultado.sucesso is True
    assert resultado.historico == [
        {
            "tentativa": 1,
            "saida": "ok",
            "erro": None,
            "ok": True,
            "etapa_id": "agent:1",
        }
    ]
