import pytest

from nexora.comunicacao import CommunicationBus, DelegadorAgentes, EstadoDelegacao


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
