from nexora.evolucao.engine import AvaliacaoEvolucao, CandidatoEvolucao, EvolutionEngine, EstadoExperimento


def test_evolution_gate_requires_evidence_and_rejects_regression():
    e = EvolutionEngine(melhoria_minima=0.1)
    e.propor(CandidatoEvolucao("c1", None, "melhorar", "mudanca", "reverter"))
    assert e.avaliar(AvaliacaoEvolucao("c1", 1, 1.2, None, 0.1, False, ("t1",))).estado is EstadoExperimento.ACEITO
    assert e.avaliar(AvaliacaoEvolucao("c1", 1, 2, None, 0.1, True, ("t1",))).estado is EstadoExperimento.REJEITADO
