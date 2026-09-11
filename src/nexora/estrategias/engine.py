"""Estrategias candidatas e avaliacao deterministica de trade-offs."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable
import uuid


@dataclass(frozen=True)
class Estrategia:
    """Caminho de acao associado a uma meta e seus trade-offs."""

    objetivo_id: str
    nome: str
    passos: tuple[str, ...]
    beneficio: float = 0.5
    custo: float = 0.5
    risco: float = 0.5
    alinhamento: float = 0.5
    id: str = field(default_factory=lambda: uuid.uuid4().hex)

    def __post_init__(self) -> None:
        if not self.objetivo_id.strip():
            raise ValueError("objetivo_id nao pode ser vazio")
        if not self.nome.strip():
            raise ValueError("nome nao pode ser vazio")
        if not self.passos:
            raise ValueError("estrategia precisa de pelo menos um passo")
        for nome, valor in (
            ("beneficio", self.beneficio),
            ("custo", self.custo),
            ("risco", self.risco),
            ("alinhamento", self.alinhamento),
        ):
            if not 0.0 <= valor <= 1.0:
                raise ValueError(f"{nome} deve estar entre 0 e 1")

    @property
    def pontuacao(self) -> float:
        """Score de utilidade: beneficio/alinhamento contra custo/risco."""
        return round(
            (self.beneficio * 0.40)
            + (self.alinhamento * 0.35)
            - (self.custo * 0.15)
            - (self.risco * 0.10),
            6,
        )

    def para_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "objetivo_id": self.objetivo_id,
            "nome": self.nome,
            "passos": list(self.passos),
            "beneficio": self.beneficio,
            "custo": self.custo,
            "risco": self.risco,
            "alinhamento": self.alinhamento,
            "pontuacao": self.pontuacao,
        }


class StrategyEngine:
    """Armazena e ranqueia estrategias; nao decide executar nenhuma acao."""

    def __init__(self) -> None:
        self._estrategias: dict[str, Estrategia] = {}

    def adicionar(
        self,
        objetivo_id: str,
        nome: str,
        passos: Iterable[str],
        *,
        beneficio: float = 0.5,
        custo: float = 0.5,
        risco: float = 0.5,
        alinhamento: float = 0.5,
    ) -> Estrategia:
        estrategia = Estrategia(
            objetivo_id=objetivo_id.strip(),
            nome=nome.strip(),
            passos=tuple(passo.strip() for passo in passos if isinstance(passo, str) and passo.strip()),
            beneficio=beneficio,
            custo=custo,
            risco=risco,
            alinhamento=alinhamento,
        )
        self._estrategias[estrategia.id] = estrategia
        return estrategia

    def obter(self, estrategia_id: str) -> Estrategia | None:
        return self._estrategias.get(estrategia_id)

    def listar(self, *, objetivo_id: str | None = None) -> list[Estrategia]:
        itens = list(self._estrategias.values())
        if objetivo_id is not None:
            itens = [item for item in itens if item.objetivo_id == objetivo_id]
        return sorted(itens, key=lambda item: (-item.pontuacao, item.id))

    def melhor(self, objetivo_id: str) -> Estrategia | None:
        estrategias = self.listar(objetivo_id=objetivo_id)
        return estrategias[0] if estrategias else None
