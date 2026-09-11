"""Registro de agentes e capacidades da NEXORA."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable


def _normalizar(valor: str) -> str:
    return "_".join(valor.strip().lower().split())


@dataclass(frozen=True)
class AgenteRegistro:
    """Metadados de um agente disponível para receber trabalho."""

    id: str
    nome: str
    descricao: str = ""
    capacidades: tuple[str, ...] = ()
    tags: tuple[str, ...] = ()
    prioridade: float = 0.5
    disponivel: bool = True
    metadados: dict[str, object] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.id.strip() or not self.nome.strip():
            raise ValueError("id e nome sao obrigatorios")
        if not 0 <= self.prioridade <= 1:
            raise ValueError("prioridade deve estar entre 0 e 1")
        capacidades = tuple(dict.fromkeys(_normalizar(item) for item in self.capacidades if item.strip()))
        tags = tuple(dict.fromkeys(_normalizar(item) for item in self.tags if item.strip()))
        object.__setattr__(self, "capacidades", capacidades)
        object.__setattr__(self, "tags", tags)
        object.__setattr__(self, "metadados", dict(self.metadados))

    def para_dict(self) -> dict[str, object]:
        return {
            "id": self.id,
            "nome": self.nome,
            "descricao": self.descricao,
            "capacidades": list(self.capacidades),
            "tags": list(self.tags),
            "prioridade": self.prioridade,
            "disponivel": self.disponivel,
            "metadados": dict(self.metadados),
        }


class RegistroAgentes:
    """Catálogo determinístico de agentes e suas capacidades."""

    def __init__(self, agentes: Iterable[AgenteRegistro] = ()) -> None:
        self._agentes: dict[str, AgenteRegistro] = {}
        for agente in agentes:
            self.registrar(agente)

    def registrar(self, agente: AgenteRegistro) -> AgenteRegistro:
        if agente.id in self._agentes:
            raise ValueError(f"agente ja registrado: {agente.id}")
        self._agentes[agente.id] = agente
        return agente

    def remover(self, agente_id: str) -> AgenteRegistro:
        try:
            return self._agentes.pop(agente_id)
        except KeyError as exc:
            raise KeyError(agente_id) from exc

    def obter(self, agente_id: str) -> AgenteRegistro | None:
        return self._agentes.get(agente_id)

    def listar(self, *, apenas_disponiveis: bool = False) -> list[AgenteRegistro]:
        agentes = list(self._agentes.values())
        if apenas_disponiveis:
            agentes = [agente for agente in agentes if agente.disponivel]
        return sorted(agentes, key=lambda item: (-item.prioridade, item.id))

    def descobrir(self, capacidade: str, *, apenas_disponiveis: bool = True) -> list[AgenteRegistro]:
        capacidade_normalizada = _normalizar(capacidade)
        if not capacidade_normalizada:
            raise ValueError("capacidade deve ser uma string nao vazia")
        candidatos = [
            agente
            for agente in self._agentes.values()
            if capacidade_normalizada in agente.capacidades
            and (not apenas_disponiveis or agente.disponivel)
        ]
        return sorted(candidatos, key=lambda item: (-item.prioridade, item.id))

    def melhor_para(self, capacidade: str) -> AgenteRegistro | None:
        encontrados = self.descobrir(capacidade)
        return encontrados[0] if encontrados else None
