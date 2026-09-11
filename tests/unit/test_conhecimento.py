from nexora.conhecimento import Conhecimento, KnowledgeEngine


def test_adiciona_conhecimento_com_proveniencia():
    engine = KnowledgeEngine()
    item = engine.adicionar(
        "Python suporta dataclasses.",
        fonte="documentacao",
        confianca=0.9,
        tags=["python", "programacao"],
        evidencias=["fonte-a"],
    )

    assert isinstance(item, Conhecimento)
    assert item.fonte == "documentacao"
    assert item.confianca == 0.9
    assert item.tags == ("python", "programacao")
    assert item.evidencias == ("fonte-a",)
    assert item.validado is False


def test_busca_lexical_prioriza_confianca():
    engine = KnowledgeEngine()
    engine.adicionar("Python e uma linguagem.", fonte="a", confianca=0.4)
    melhor = engine.adicionar("Python e usada em IA.", fonte="b", confianca=0.9)

    resultados = engine.buscar("python")

    assert resultados[0].id == melhor.id


def test_busca_respeita_escopo_e_limite():
    engine = KnowledgeEngine()
    engine.adicionar("NEXORA usa Python.", fonte="a", escopo="projeto", confianca=0.8)
    engine.adicionar("Python e popular.", fonte="b", escopo="global", confianca=0.9)

    resultados = engine.buscar("python", escopo="projeto", limite=1)

    assert len(resultados) == 1
    assert resultados[0].escopo == "projeto"


def test_validar_preserva_identidade():
    engine = KnowledgeEngine()
    item = engine.adicionar("Fato", fonte="fonte", confianca=0.7)

    validado = engine.validar(item.id)

    assert validado.id == item.id
    assert validado.validado is True
    assert engine.obter(item.id) == validado


def test_rejeita_confianca_invalida_e_termo_vazio():
    engine = KnowledgeEngine()

    try:
        engine.adicionar("Fato", fonte="fonte", confianca=1.1)
        assert False
    except ValueError:
        pass

    try:
        engine.buscar("   ")
        assert False
    except ValueError:
        pass
