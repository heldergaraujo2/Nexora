from nexora.comunicacao import CommunicationBus, EstadoMensagem, MensagemAgente


def test_publicar_entrega_para_destinatario_e_assinante_global() -> None:
    bus = CommunicationBus()
    recebidas: list[str] = []
    globais: list[str] = []

    bus.assinar("agente_b", lambda mensagem: recebidas.append(mensagem.id))
    bus.assinar("*", lambda mensagem: globais.append(mensagem.id))

    mensagem = bus.publicar(
        remetente="agente_a",
        destinatario="agente_b",
        tipo="delegacao",
        payload={"tarefa": "pesquisar mercado"},
    )

    assert recebidas == [mensagem.id]
    assert globais == [mensagem.id]
    assert bus.obter(mensagem.id) == mensagem
    assert bus.estado(mensagem.id) == EstadoMensagem.ENTREGUE


def test_listar_filtra_por_correlacao_tipo_e_agentes() -> None:
    bus = CommunicationBus()
    primeiro = bus.publicar(
        remetente="planner",
        destinatario="research",
        tipo="delegacao",
        correlacao_id="corr-1",
    )
    bus.publicar(
        remetente="research",
        destinatario="planner",
        tipo="resultado",
        correlacao_id="corr-1",
    )
    bus.publicar(
        remetente="planner",
        destinatario="coding",
        tipo="delegacao",
        correlacao_id="corr-2",
    )

    assert bus.listar(correlacao_id="corr-1") == bus.listar(correlacao_id="corr-1")
    assert bus.listar(destinatario="research") == [primeiro]
    assert bus.listar(tipo="resultado")[0].remetente == "research"


def test_marcar_lida() -> None:
    bus = CommunicationBus()
    mensagem = bus.publicar(
        remetente="a",
        destinatario="b",
        tipo="pedido",
    )

    bus.marcar_lida(mensagem.id)

    assert bus.estado(mensagem.id) == EstadoMensagem.LIDA


def test_mensagem_rejeita_dados_invalidos() -> None:
    try:
        MensagemAgente(remetente="", destinatario="b", tipo="pedido")
    except ValueError as exc:
        assert "remetente" in str(exc)
    else:
        raise AssertionError("mensagem invalida deveria falhar")


def test_mensagem_delegacao_preserva_correlacao_e_resposta() -> None:
    mensagem = MensagemAgente(
        remetente="planner",
        destinatario="coding",
        tipo="resultado",
        payload={"status": "ok"},
        correlacao_id="corr-7",
        resposta_a="msg-1",
    )

    dados = mensagem.para_dict()

    assert dados["correlacao_id"] == "corr-7"
    assert dados["resposta_a"] == "msg-1"
    assert dados["payload"] == {"status": "ok"}
