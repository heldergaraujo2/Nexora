from nexora.economia.reinvestimento import GateReinvestimento, PedidoReinvestimento

def test_financial_effect_requires_human_authorization():
    g=GateReinvestimento()
    d=g.decidir(PedidoReinvestimento("op",100,150,0.1,False))
    assert not d.permitido and "humana" in d.motivo

def test_authorized_reinvestment_passes_gate():
    d=GateReinvestimento().decidir(PedidoReinvestimento("op",100,150,0.1,True))
    assert d.permitido
