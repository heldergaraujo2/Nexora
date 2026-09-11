import pytest

from nexora.comunicacao import (
    CommunicationBus,
    DelegadorAgentes,
    EstadoDelegacao,
    ExecutorDelegacoes,
)


def test_delegacao_envia_solicitacao_e_correlaciona_resposta():
    bus = CommunicationBus()
    delegador = DelegadorAgentes(bus)

    delegacao = delegador.delegar(
        solicitante="orchestrator",
        executor="research-agent",
        tarefa="pesquisar mercado",
        prioridade=0.9,
        contexto={"objetivo": "validar oportunidade"},
    )

    assert delegacao.estado is EstadoDelegacao.SOLICITADA
    solicitacao = bus.listar(tipo="delegacao.solicitada")[0]
    assert solicitacao.destinatario == "research-agent"
    assert solicitacao.correlacao_id == delegacao.id

    delegador.atualizar(delegacao.id, estado=EstadoDelegacao.CONCLUIDA, resultado={"achados": 3})
    resposta = bus.listar(tipo="delegacao.resultado")[0]
    assert resposta.destinatario == "orchestrator"
    assert resposta.correlacao_id == delegacao.id
    assert resposta.resposta_a == delegacao.mensagem_id


def test_delegacao_rejeita_prioridade_invalida():
    bus = CommunicationBus()
    delegador = DelegadorAgentes(bus)
    with pytest.raises(ValueError):
        delegador.delegar(solicitante="a", executor="b", tarefa="x", prioridade=1.5)


def test_executor_processa_delegacao_e_publica_resultado():
    bus = CommunicationBus()
    delegador = DelegadorAgentes(bus)
    executor = ExecutorDelegacoes(bus, delegador)
    executor.registrar("research-agent", lambda delegacao: {"tarefa": delegacao.tarefa, "ok": True})

    delegacao = delegador.delegar(
        solicitante="orchestrator",
        executor="research-agent",
        tarefa="pesquisar mercado",
    )

    assert delegacao.estado is EstadoDelegacao.CONCLUIDA
    assert delegacao.resultado == {"tarefa": "pesquisar mercado", "ok": True}
    estados = [m.tipo for m in bus.listar(correlacao_id=delegacao.id)]
    assert estados == ["delegacao.solicitada", "delegacao.estado", "delegacao.resultado"]


def test_executor_registra_falha_do_handler():
    bus = CommunicationBus()
    delegador = DelegadorAgentes(bus)
    executor = ExecutorDelegacoes(bus, delegador)
    executor.registrar("coding-agent", lambda delegacao: (_ for _ in ()).throw(RuntimeError("falha de execucao")))

    delegacao = delegador.delegar(
        solicitante="orchestrator",
        executor="coding-agent",
        tarefa="implementar componente",
    )

    assert delegacao.estado is EstadoDelegacao.FALHOU
    assert delegacao.erro == "falha de execucao"
