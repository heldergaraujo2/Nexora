from nexora.evolucao.dream_cycle import DreamCycle, HipoteseEvolucao
from nexora.evolucao.engine import AvaliacaoEvolucao, EstadoExperimento

def test_dream_cycle_promotes_only_after_gate():
    d=DreamCycle()
    c=d.propor(HipoteseEvolucao("h1","falha","melhorar","mudar","reverter"))
    result=d.avaliar(c.id, lambda: AvaliacaoEvolucao(c.id,1,1.2,None,0.1,False,("benchmark",)))
    assert result.estado is EstadoExperimento.ACEITO
