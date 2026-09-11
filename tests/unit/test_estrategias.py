from nexora.estrategias import Estrategia, StrategyEngine


def test_adiciona_e_ranqueia_estrategias():
    engine = StrategyEngine()
    pior = engine.adicionar(
        "meta-1", "Alternativa cara", ["A"], beneficio=0.6, custo=0.9, risco=0.8, alinhamento=0.5
    )
    melhor = engine.adicionar(
        "meta-1", "Alternativa equilibrada", ["A", "B"], beneficio=0.8, custo=0.2, risco=0.2, alinhamento=0.9
    )

    assert isinstance(melhor, Estrategia)
    assert engine.melhor("meta-1").id == melhor.id
    assert melhor.pontuacao > pior.pontuacao


def test_filtra_por_objetivo():
    engine = StrategyEngine()
    engine.adicionar("meta-a", "A", ["passo"])
    engine.adicionar("meta-b", "B", ["passo"])

    resultados = engine.listar(objetivo_id="meta-a")

    assert len(resultados) == 1
    assert resultados[0].objetivo_id == "meta-a"


def test_rejeita_estrategia_sem_passos_ou_score_invalido():
    engine = StrategyEngine()
    try:
        engine.adicionar("meta", "vazia", [])
        assert False
    except ValueError:
        pass

    try:
        engine.adicionar("meta", "invalida", ["A"], risco=1.1)
        assert False
    except ValueError:
        pass
