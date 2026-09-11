"""Objetivos persistentes em memoria e priorizacao deterministica."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable
import uuid


@dataclass(frozen=True)
class ObjetivoMeta:
    """Meta operacional com prioridade, progresso e criterios mensuraveis."""

    titulo: str
    prioridade: float = 0.5
    progresso: float = 0.0
    metricas: tuple[str, ...] = ()
    restricoes: tuple[str, ...] = ()
    id: str = field(default_factory=lambda: uuid.uuid4().hex)
    concluido: bool = False

    def __post_init__(self) -> None:
        if not self.titulo.strip():
            raise ValueError("titulo nao pode ser vazio")
        if not 0.0 <= self.prioridade <= 1.0:
            raise ValueError("prioridade deve estar entre 0 e 1")
        if not 0.0 <= self.progresso <= 1.0:
            raise ValueError("progresso deve estar entre 0 e 1")

    def para_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "titulo": self.titulo,
            "prioridade": self.prioridade,
            "progresso": self.progresso,
            "metricas": list(self.metricas),
            "restricoes": list(self.restricoes),
            "concluido": self.concluido,
        }


class GoalEngine:
    """Registra, prioriza e atualiza metas sem depender de um modelo de IA."""

    def __init__(self) -> None:
        self._objetivos: dict[str, ObjetivoMeta] = {}

    def criar(
        self,
        titulo: str,
        *,
        prioridade: float = 0.5,
        progresso: float = 0.0,
        metricas: Iterable[str] = (),
        restricoes: Iterable[str] = (),
    ) -> ObjetivoMeta:
        objetivo = ObjetivoMeta(
            titulo=titulo.strip(),
            prioridade=prioridade,
            progresso=progresso,
            metricas=self._limpar(metricas),
            restricoes=self._limpar(restricoes),
        )
        self._objetivos[objetivo.id] = objetivo
        return objetivo

    def obter(self, objetivo_id: str) -> ObjetivoMeta | None:
        return self._objetivos.get(objetivo_id)

    def listar(self, *, apenas_pendentes: bool = False) -> list[ObjetivoMeta]:
        itens = list(self._objetivos.values())
        if apenas_pendentes:
            itens = [item for item in itens if not item.concluido]
        return sorted(itens, key=lambda item: (-item.prioridade, -item.progresso, item.id))

    def atualizar_progresso(self, objetivo_id: str, progresso: float) -> ObjetivoMeta:
        atual = self._objetivos.get(objetivo_id)
        if atual is None:
            raise KeyError(objetivo_id)
        atualizado = ObjetivoMeta(
            titulo=atual.titulo,
            prioridade=atual.prioridade,
            progresso=progresso,
            metricas=atual.metricas,
            restricoes=atual.restricoes,
            id=atual.id,
            concluido=progresso >= 1.0,
        )
        self._objetivos[objetivo_id] = atualizado
        return atualizado

    @staticmethod
    def _limpar(valores: Iterable[str]) -> tuple[str, ...]:
        return tuple(valor.strip() for valor in valores if isinstance(valor, str) and valor.strip())
