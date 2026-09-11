from nexora.comunicacao import CommunicationBus, DelegadorAgentes, EstadoDelegacao, ExecutorDelegacoes


def test_executor_recupera_falha_transitoria():
    bus = CommunicationBus()
    delegador = DelegadorAgentes(bus)
    executor = ExecutorDelegacoes(bus, delegador, max_tentativas=2)
    chamadas = 0

    def handler(delegacao):
        nonlocal chamadas
        chamadas += 1
        if chamadas == 1:
            raise RuntimeError("falha transitoria")
        return {"ok": True}

    executor.registrar("research-agent", handler)
    delegacao = delegador.delegar(
        solicitante="orchestrator",
        executor="research-agent",
        tarefa="tentar novamente",
    )

    assert delegacao.estado is EstadoDelegacao.CONCLUIDA
    assert delegacao.tentativas == 2
    assert delegacao.resultado == {"ok": True}


def test_executor_esgota_tentativas_e_falha():
    bus = CommunicationBus()
    delegador = DelegadorAgentes(bus)
    executor = ExecutorDelegacoes(bus, delegador, max_tentativas=3)
    chamadas = 0

    def handler(delegacao):
        nonlocal chamadas
        chamadas += 1
        raise RuntimeError("falha permanente")

    executor.registrar("coding-agent", handler)
    delegacao = delegador.delegar(
        solicitante="orchestrator",
        executor="coding-agent",
        tarefa="falhar com recuperacao limitada",
    )

    assert delegacao.estado is EstadoDelegacao.FALHOU
    assert delegacao.tentativas == 3
    assert chamadas == 3
    assert delegacao.erro == "falha permanente"


def test_executor_rejeita_max_tentativas_invalido():
    bus = CommunicationBus()
    delegador = DelegadorAgentes(bus)
    try:
        ExecutorDelegacoes(bus, delegador, max_tentativas=0)
    except ValueError as exc:
        assert "max_tentativas" in str(exc)
    else:
        raise AssertionError("deveria rejeitar max_tentativas=0")
