"""Motor deterministico de oportunidades economicas para a NEXORA."""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Oportunidade:
    id: str
    problema: str
    mercado_estimado: float
    receita_estimada: float
    custo_estimado: float
    probabilidade: float
    risco: float
    capacidade_requerida: tuple[str, ...] = ()
    metadados: dict[str, object] = field(default_factory=dict)

    @property
    def valor_esperado(self) -> float:
        return self.receita_estimada * self.probabilidade - self.custo_estimado

    @property
    def retorno_sobre_custo(self) -> float | None:
        if self.custo_estimado <= 0:
            return None
        return (self.receita_estimada * self.probabilidade - self.custo_estimado) / self.custo_estimado


@dataclass(frozen=True)
class ScoreOportunidade:
    oportunidade: Oportunidade
    score: float
    componentes: dict[str, float]


class AvaliadorOportunidades:
    """Não executa negócios; apenas prioriza oportunidades com sinais explícitos."""

    def avaliar(self, oportunidade: Oportunidade) -> ScoreOportunidade:
        if not 0 <= oportunidade.probabilidade <= 1:
            raise ValueError("probabilidade deve estar entre 0 e 1")
        if not 0 <= oportunidade.risco <= 1:
            raise ValueError("risco deve estar entre 0 e 1")
        valor = oportunidade.valor_esperado
        mercado = max(0.0, oportunidade.mercado_estimado)
        score = valor + (mercado * 0.05) - (oportunidade.risco * max(1.0, mercado) * 0.05)
        return ScoreOportunidade(
            oportunidade,
            score,
            {"valor_esperado": valor, "mercado": mercado, "risco": oportunidade.risco},
        )

    def ordenar(self, oportunidades: list[Oportunidade]) -> list[ScoreOportunidade]:
        return sorted((self.avaliar(o) for o in oportunidades), key=lambda s: (-s.score, s.oportunidade.id))
