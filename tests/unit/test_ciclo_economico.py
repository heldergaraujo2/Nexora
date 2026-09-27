import pytest
from nexora.economia.loop import CicloEconomico, EstadoEconomico

def test_economic_loop_requires_ordered_transitions():
    c=CicloEconomico("op-1")
    c.avancar(EstadoEconomico.PROTOTIPO)
    with pytest.raises(ValueError): c.avancar(EstadoEconomico.RECEITA)
    c.avancar(EstadoEconomico.VALIDACAO)
    assert c.estado is EstadoEconomico.VALIDACAO
