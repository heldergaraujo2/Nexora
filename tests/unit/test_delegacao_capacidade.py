from nexora.agentes import AgenteRegistro, RegistroAgentes
from nexora.comunicacao import CommunicationBus, DelegadorAgentes


def test_delegacao_por_capacidade_seleciona_agente() -> None:
    bus = CommunicationBus()
    registro = RegistroAgentes(
        [
            AgenteRegistro(id="mercado-1", nome="Mercado", capacidades=("pesquisa_mercado",), prioridade=0.7),
            AgenteRegistro(id="mercado-2", nome="Mercado Pro", capacidades=("pesquisa_mercado",), prioridade=0.9),
        ]
    )
    delegador = DelegadorAgentes(bus, registro)

    delegacao = delegador.delegar_por_capacidade(
        solicitante="orchestrator",
        capacidade="pesquisa mercado",
        tarefa="Pesquisar concorrentes",
    )

    assert delegacao.executor == "mercado-2"
    assert delegacao.contexto["capacidade_solicitada"] == "pesquisa mercado"
    mensagem = bus.obter(delegacao.mensagem_id)
    assert mensagem is not None
    assert mensagem.destinatario == "mercado-2"


def test_delegacao_por_capacidade_falha_sem_agente() -> None:
    delegador = DelegadorAgentes(CommunicationBus(), RegistroAgentes())

    try:
        delegador.delegar_por_capacidade(
            solicitante="orchestrator",
            capacidade="pesquisa_mercado",
            tarefa="Pesquisar",
        )
    except LookupError as exc:
        assert "pesquisa_mercado" in str(exc)
    else:
        raise AssertionError("era esperada uma LookupError")
