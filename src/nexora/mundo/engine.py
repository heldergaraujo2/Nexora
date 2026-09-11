"""Representacao deterministica do estado percebido do mundo pela NEXORA."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Mapping
import uuid


@dataclass(frozen=True)
class Observacao:
    """Evidencia observada sobre uma entidade ou aspecto do mundo."""

    entidade: str
    atributo: str
    valor: Any
    fonte: str
    confianca: float = 0.5
    id: str = field(default_factory=lambda: uuid.uuid4().hex)
    observado_em: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    def __post_init__(self) -> None:
        if not self.entidade.strip():
            raise ValueError("entidade nao pode ser vazia")
        if not self.atributo.strip():
            raise ValueError("atributo nao pode ser vazio")
        if not self.fonte.strip():
            raise ValueError("fonte nao pode ser vazia")
        if not 0.0 <= self.confianca <= 1.0:
            raise ValueError("confianca deve estar entre 0 e 1")

    def para_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "entidade": self.entidade,
            "atributo": self.atributo,
            "valor": self.valor,
            "fonte": self.fonte,
            "confianca": self.confianca,
            "observado_em": self.observado_em,
        }


@dataclass(frozen=True)
class EstadoMundo:
    """Snapshot imutavel do melhor estado conhecido para cada fato."""

    observacoes: tuple[Observacao, ...]

    def para_dict(self) -> dict[str, Any]:
        return {"observacoes": [item.para_dict() for item in self.observacoes]}


class WorldModelEngine:
    """Mantem observacoes e produz snapshots do estado conhecido.

    O MVP nao afirma que o estado observado e a realidade. Ele registra
    evidencias, resolve conflitos pela maior confianca e preserva a origem
    para permitir verificacao posterior.
    """

    def __init__(self) -> None:
        self._observacoes: dict[str, Observacao] = {}

    def observar(
        self,
        entidade: str,
        atributo: str,
        valor: Any,
        *,
        fonte: str,
        confianca: float = 0.5,
    ) -> Observacao:
        nova = Observacao(
            entidade=entidade.strip(),
            atributo=atributo.strip(),
            valor=valor,
            fonte=fonte.strip(),
            confianca=confianca,
        )
        chave = self._chave(nova.entidade, nova.atributo)
        atual = self._observacoes.get(chave)
        if atual is None or nova.confianca >= atual.confianca:
            self._observacoes[chave] = nova
        return nova

    def obter(self, entidade: str, atributo: str) -> Observacao | None:
        return self._observacoes.get(self._chave(entidade.strip(), atributo.strip()))

    def estado(self, *, entidade: str | None = None) -> EstadoMundo:
        observacoes = tuple(self._observacoes.values())
        if entidade is not None:
            observacoes = tuple(
                item for item in observacoes if item.entidade == entidade.strip()
            )
        observacoes = tuple(
            sorted(observacoes, key=lambda item: (item.entidade, item.atributo)
        )
        )
        return EstadoMundo(observacoes=observacoes)

    def listar_observacoes(self, *, fonte: str | None = None) -> list[Observacao]:
        itens = list(self._observacoes.values())
        if fonte is not None:
            itens = [item for item in itens if item.fonte == fonte]
        return sorted(itens, key=lambda item: (item.entidade, item.atributo))

    @staticmethod
    def _chave(entidade: str, atributo: str) -> str:
        if not entidade:
            raise ValueError("entidade nao pode ser vazia")
        if not atributo:
            raise ValueError("atributo nao pode ser vazio")
        return f"{entidade}\x00{atributo}"
