from nexora.memoria.hibrida import Memoria, MemoriaHibrida


def test_hibrida_rank_and_rrf():
    m = MemoriaHibrida()
    m.adicionar(Memoria("a", "Python memoria agentes"))
    m.adicionar(Memoria("b", "economia produtos"))
    r = m.buscar("memoria agentes")
    assert r and r[0].memoria.id == "a"
    assert r[0].sinais["rrf"] > 0


def test_semantic_and_graph_candidates_are_fused():
    m = MemoriaHibrida(
        semantic_search=lambda q, n: [("b", 0.9)],
        graph_search=lambda q, n: [("a", 0.8)],
    )
    m.adicionar(Memoria("a", "texto qualquer"))
    m.adicionar(Memoria("b", "outro texto"))
    ids = {x.memoria.id for x in m.buscar("nada")}
    assert ids == {"a", "b"}
