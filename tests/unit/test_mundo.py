from nexora.mundo import EstadoMundo, Observacao, WorldModelEngine


def test_registra_observacao():
    engine = WorldModelEngine()

    observacao = engine.observar(
        "NEXORA", "status", "ativa", fonte="runtime", confianca=0.9
    )

    assert isinstance(observacao, Observacao)
    assert engine.obter("NEXORA", "status") == observacao


def test_conflito_prefere_maior_confianca():
    engine = WorldModelEngine()
    antiga = engine.observar("servico", "status", "offline", fonte="a", confianca=0.4)
    nova = engine.observar("servico", "status", "online", fonte="b", confianca=0.9)

    assert engine.obter("servico", "status") == nova
    assert engine.obter("servico", "status") != antiga


def test_observacao_de_menor_confianca_nao_substitui_estado():
    engine = WorldModelEngine()
    melhor = engine.observar("api", "status", "online", fonte="a", confianca=0.9)
    engine.observar("api", "status", "offline", fonte="b", confianca=0.2)

    assert engine.obter("api", "status") == melhor


def test_snapshot_filtra_entidade_e_serializa():
    engine = WorldModelEngine()
    engine.observar("a", "x", 1, fonte="sensor")
    engine.observar("b", "x", 2, fonte="sensor")

    estado = engine.estado(entidade="b")

    assert isinstance(estado, EstadoMundo)
    assert len(estado.observacoes) == 1
    assert estado.observacoes[0].valor == 2
    assert estado.para_dict()["observacoes"][0]["entidade"] == "b"


def test_valida_dados_basicos():
    engine = WorldModelEngine()

    try:
        engine.observar("", "status", "ok", fonte="teste")
        assert False
    except ValueError:
        pass

    try:
        engine.observar("x", "status", "ok", fonte="teste", confianca=2)
        assert False
    except ValueError:
        pass
