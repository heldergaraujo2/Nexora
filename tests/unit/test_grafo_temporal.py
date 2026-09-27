from nexora.world.grafo_temporal import Entidade, FatoTemporal, GrafoTemporal


def test_grafo_temporal_consulta_as_of():
    g = GrafoTemporal()
    g.registrar_entidade(Entidade("alice", "pessoa"))
    g.registrar_entidade(Entidade("nexora", "sistema"))
    g.registrar_fato(FatoTemporal("f1", "alice", "criou", "nexora", 10, 20))
    assert len(g.consultar(sujeito="alice", em=15)) == 1
    assert g.consultar(sujeito="alice", em=25) == []


def test_encerrar_fato():
    g = GrafoTemporal()
    g.registrar_fato(FatoTemporal("f", "a", "r", "b", 1))
    g.encerrar_fato("f", 5)
    assert g.consultar(em=6) == []
