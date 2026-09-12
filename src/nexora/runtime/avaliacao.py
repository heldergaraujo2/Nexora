"""Avaliação explícita e determinística do resultado de uma execução."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable


@dataclass(frozen=True)
class ResultadoAvaliacao:
    """Sinal de qualidade derivado de critérios observáveis, sem estimativa."""

    sucesso: bool
    score: float
    criterios: tuple[str, ...] = ()
    evidencias: tuple[str, ...] = ()
    metadados: dict[str, Any] = field(default_factory=dict)

    def para_dict(self) -> dict[str, Any]:
        return {
            "sucesso": self.sucesso,
            "score": self.score,
            "criterios": list(self.criterios),
            "evidencias": list(self.evidencias),
            "metadados": dict(self.metadados),
        }


class AvaliadorResultado:
    """Agrega avaliadores explícitos; não infere qualidade por texto ou custo."""

    def __init__(self, avaliadores: list[Callable[[str, str], ResultadoAvaliacao]] | None = None) -> None:
        self._avaliadores = list(avaliadores or [])

    def adicionar(self, avaliador: Callable[[str, str], ResultadoAvaliacao]) -> None:
        self._avaliadores.append(avaliador)

    def avaliar(self, objetivo: str, saida: str) -> ResultadoAvaliacao:
        if not self._avaliadores:
            return ResultadoAvaliacao(
                sucesso=False,
                score=0.0,
                criterios=("nenhum_criterio_avaliacao",),
                evidencias=(),
            )
        resultados = [avaliador(objetivo, saida) for avaliador in self._avaliadores]
        if any(not isinstance(item, ResultadoAvaliacao) for item in resultados):
            raise TypeError("avaliador deve retornar ResultadoAvaliacao")
        score = sum(item.score for item in resultados) / len(resultados)
        score = max(0.0, min(1.0, score))
        criterios = tuple(criterio for item in resultados for criterio in item.criterios)
        evidencias = tuple(evidencia for item in resultados for evidencia in item.evidencias)
        sucesso = all(item.sucesso for item in resultados)
        return ResultadoAvaliacao(
            sucesso=sucesso,
            score=score,
            criterios=criterios,
            evidencias=evidencias,
            metadados={"avaliadores": len(resultados)},
        )
