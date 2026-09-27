"""Ciclo de melhoria contínua seguro: observar -> hipótese -> experimento -> gate."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Callable
from nexora.evolucao.engine import AvaliacaoEvolucao, CandidatoEvolucao, DecisaoEvolucao, EvolutionEngine


@dataclass(frozen=True)
class HipoteseEvolucao:
    id:str
    observacao:str
    hipotese:str
    mudanca:str
    rollback:str


class DreamCycle:
    """Coordena propostas de melhoria, mas nunca promove uma mutação sem o EvolutionEngine."""
    def __init__(self, engine:EvolutionEngine|None=None)->None:
        self.engine=engine or EvolutionEngine()
    def propor(self,h:HipoteseEvolucao)->CandidatoEvolucao:
        candidato=CandidatoEvolucao(h.id,None,h.hipotese,h.mudanca,h.rollback,{"observacao":h.observacao})
        self.engine.propor(candidato); return candidato
    def avaliar(self,candidato_id:str, medir:Callable[[],AvaliacaoEvolucao])->DecisaoEvolucao:
        avaliacao=medir()
        if avaliacao.candidato_id != candidato_id: raise ValueError("avaliação não corresponde ao candidato")
        return self.engine.avaliar(avaliacao)
