"""Engine de experimentacao e evolucao segura da NEXORA."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
import time
from typing import Any, Callable


class EstadoExperimento(str, Enum):
    PROPOSTO = "proposto"
    AVALIANDO = "avaliando"
    ACEITO = "aceito"
    REJEITADO = "rejeitado"


@dataclass(frozen=True)
class CandidatoEvolucao:
    id: str
    pai_id: str | None
    hipotese: str
    mudanca: str
    rollback: str
    metadados: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class AvaliacaoEvolucao:
    candidato_id: str
    baseline: float
    resultado: float
    custo: float | None
    risco: float
    regressao: bool
    evidencias: tuple[str, ...] = ()

    @property
    def delta(self) -> float:
        return self.resultado - self.baseline


@dataclass(frozen=True)
class DecisaoEvolucao:
    estado: EstadoExperimento
    motivo: str


class EvolutionEngine:
    """Gate conservador: melhoria só é promovida com evidência e sem regressão."""

    def __init__(self, *, melhoria_minima: float = 0.0, risco_maximo: float = 0.25) -> None:
        if melhoria_minima < 0 or risco_maximo < 0:
            raise ValueError("limites devem ser nao negativos")
        self.melhoria_minima = melhoria_minima
        self.risco_maximo = risco_maximo
        self._arquivo: dict[str, CandidatoEvolucao] = {}
        self._avaliacoes: dict[str, AvaliacaoEvolucao] = {}

    def propor(self, candidato: CandidatoEvolucao) -> None:
        if not candidato.id.strip() or not candidato.hipotese.strip() or not candidato.rollback.strip():
            raise ValueError("candidato exige id, hipotese e rollback")
        self._arquivo[candidato.id] = candidato

    def avaliar(self, avaliacao: AvaliacaoEvolucao) -> DecisaoEvolucao:
        if avaliacao.candidato_id not in self._arquivo:
            raise KeyError(avaliacao.candidato_id)
        self._avaliacoes[avaliacao.candidato_id] = avaliacao
        if avaliacao.regressao:
            return DecisaoEvolucao(EstadoExperimento.REJEITADO, "regressao detectada")
        if avaliacao.risco > self.risco_maximo:
            return DecisaoEvolucao(EstadoExperimento.REJEITADO, "risco acima do limite")
        if not avaliacao.evidencias:
            return DecisaoEvolucao(EstadoExperimento.REJEITADO, "evidencia insuficiente")
        if avaliacao.delta < self.melhoria_minima:
            return DecisaoEvolucao(EstadoExperimento.REJEITADO, "melhoria minima nao atingida")
        return DecisaoEvolucao(EstadoExperimento.ACEITO, "gate de evolucao aprovado")

    def candidato(self, candidato_id: str) -> CandidatoEvolucao:
        return self._arquivo[candidato_id]

    def avaliacao(self, candidato_id: str) -> AvaliacaoEvolucao | None:
        return self._avaliacoes.get(candidato_id)

    def arquivo(self) -> list[CandidatoEvolucao]:
        return sorted(self._arquivo.values(), key=lambda c: c.id)
