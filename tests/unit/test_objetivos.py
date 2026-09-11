from nexora.objetivos import GoalEngine, ObjetivoMeta


def test_cria_e_prioriza_objetivos():
    engine = GoalEngine()
    engine.criar("Meta secundaria", prioridade=0.4)
    principal = engine.criar("Meta principal", prioridade=0.9)

    assert isinstance(principal, ObjetivoMeta)
    assert engine.listar()[0].id == principal.id


def test_atualiza_progresso_e_conclui_meta():
    engine = GoalEngine()
    objetivo = engine.criar("Construir produto")

    atualizado = engine.atualizar_progresso(objetivo.id, 1.0)

    assert atualizado.progresso == 1.0
    assert atualizado.concluido is True
    assert engine.listar(apenas_pendentes=True) == []


def test_rejeita_prioridade_e_progresso_invalidos():
    engine = GoalEngine()
    try:
        engine.criar("Meta", prioridade=2.0)
        assert False
    except ValueError:
        pass

    try:
        engine.criar("Meta", progresso=-0.1)
        assert False
    except ValueError:
        pass
