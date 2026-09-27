from nexora.economia.oportunidades import AvaliadorOportunidades, Oportunidade


def test_expected_value_and_ranking():
    a = Oportunidade("a", "problema", 1000, 500, 100, 0.8, 0.1)
    b = Oportunidade("b", "problema", 1000, 100, 100, 0.5, 0.1)
    assert a.valor_esperado == 300
    assert AvaliadorOportunidades().ordenar([b, a])[0].oportunidade.id == "a"
