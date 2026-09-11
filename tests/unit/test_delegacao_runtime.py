from nexora.comunicacao import CommunicationBus, DelegadorAgentes, EstadoDelegacao, ExecutorDelegacoes
from nexora.runtime.agente import AgenteRuntime


class FalhaAbort:
    plano = "abort"
    motivo = "verificacao falhou"

    def para_dict(self):
        return {"plano": self.plano, "motivo": self.motivo}


def test_executor_integra_agente_runtime_com_verificacao():
    bus = CommunicationBus()
    delegador = DelegadorAgentes(bus)
    executor = ExecutorDelegacoes(bus, delegador)
    runtime = AgenteRuntime(
        executar=lambda objetivo: f"resultado: {objetivo}",
        verificar=lambda saida: saida.startswith("resultado:"),
        analisar=lambda observacao: FalhaAbort(),
        corregir=lambda objetivo, falha: objetivo,
        max_tentativas=2,
    )
    executor.registrar_runtime("coding-agent", runtime)

    delegacao = delegador.delegar(
        solicitante="orchestrator",
        executor="coding-agent",
        tarefa="implementar componente",
    )

    assert delegacao.estado is EstadoDelegacao.CONCLUIDA
    assert delegacao.resultado.sucesso is True
    assert delegacao.resultado.tentativas == 1
    assert delegacao.resultado.objetivo == "implementar componente"


def test_executor_propaga_falha_de_verificacao_do_runtime():
    bus = CommunicationBus()
    delegador = DelegadorAgentes(bus)
    executor = ExecutorDelegacoes(bus, delegador)
    runtime = AgenteRuntime(
        executar=lambda objetivo: "resultado invalido",
        verificar=lambda saida: False,
        analisar=lambda observacao: FalhaAbort(),
        corregir=lambda objetivo, falha: objetivo,
        max_tentativas=2,
    )
    executor.registrar_runtime("research-agent", runtime)

    delegacao = delegador.delegar(
        solicitante="orchestrator",
        executor="research-agent",
        tarefa="validar oportunidade",
    )

    assert delegacao.estado is EstadoDelegacao.FALHOU
    assert delegacao.resultado.sucesso is False
    assert delegacao.erro == "resultado invalido"
