from nexora.contexto import ContextEngine, Contexto


def test_context_engine_monta_contexto():
    contexto = ContextEngine().montar(
        "Criar um produto",
        escopo="projeto",
        tarefa="Pesquisar mercado",
        memorias=["Produto anterior falhou", "Usuario prefere baixo custo"],
        estado={"fase": "pesquisa"},
    )

    assert isinstance(contexto, Contexto)
    assert contexto.objetivo == "Criar um produto"
    assert contexto.tarefa == "Pesquisar mercado"
    assert contexto.memorias == ("Produto anterior falhou", "Usuario prefere baixo custo")
    assert contexto.estado == {"fase": "pesquisa"}


def test_context_engine_remove_memorias_vazias_e_aplica_limite():
    contexto = ContextEngine(limite_memorias=2).montar(
        "objetivo",
        memorias=["  primeira  ", "", "segunda", "terceira"],
    )

    assert contexto.memorias == ("primeira", "segunda")


def test_contexto_serializa_para_dict_e_texto():
    contexto = ContextEngine().montar("objetivo", tarefa="tarefa", estado={"x": 1})

    dados = contexto.para_dict()
    assert dados["objetivo"] == "objetivo"
    assert dados["estado"] == {"x": 1}
    assert "OBJETIVO: objetivo" in contexto.para_texto()
    assert "TAREFA: tarefa" in contexto.para_texto()


def test_context_engine_rejeita_objetivo_vazio():
    try:
        ContextEngine().montar("   ")
    except ValueError as exc:
        assert "objetivo" in str(exc)
    else:
        raise AssertionError("objetivo vazio deveria ser rejeitado")
