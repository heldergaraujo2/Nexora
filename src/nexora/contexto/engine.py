"""Montagem deterministica de contexto para execucoes da NEXORA."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping


@dataclass(frozen=True)
class Contexto:
    """Pacote de contexto pronto para consumo por um agente/provider."""

    objetivo: str
    escopo: str = "global"
    tarefa: str | None = None
    memorias: tuple[str, ...] = ()
    estado: Mapping[str, Any] = field(default_factory=dict)
    metadados: Mapping[str, Any] = field(default_factory=dict)

    def para_dict(self) -> dict[str, Any]:
        return {
            "objetivo": self.objetivo,
            "escopo": self.escopo,
            "tarefa": self.tarefa,
            "memorias": list(self.memorias),
            "estado": dict(self.estado),
            "metadados": dict(self.metadados),
        }

    def para_texto(self) -> str:
        """Gera uma representacao textual estavel e compacta."""
        partes = [f"OBJETIVO: {self.objetivo}", f"ESCOPO: {self.escopo}"]
        if self.tarefa:
            partes.append(f"TAREFA: {self.tarefa}")
        if self.memorias:
            partes.append("MEMORIAS:\n" + "\n".join(f"- {item}" for item in self.memorias))
        if self.estado:
            partes.append("ESTADO: " + repr(dict(self.estado)))
        return "\n\n".join(partes)


class ContextEngine:
    """Constroi contexto sem mutar as entradas fornecidas pelo chamador."""

    def __init__(self, *, limite_memorias: int = 20) -> None:
        if limite_memorias < 0:
            raise ValueError("limite_memorias deve ser >= 0")
        self.limite_memorias = limite_memorias

    def montar(
        self,
        objetivo: str,
        *,
        escopo: str = "global",
        tarefa: str | None = None,
        memorias: list[str] | tuple[str, ...] = (),
        estado: Mapping[str, Any] | None = None,
        metadados: Mapping[str, Any] | None = None,
    ) -> Contexto:
        objetivo_limpo = objetivo.strip()
        if not objetivo_limpo:
            raise ValueError("objetivo nao pode ser vazio")

        memorias_filtradas = tuple(
            memoria.strip()
            for memoria in memorias
            if isinstance(memoria, str) and memoria.strip()
        )[: self.limite_memorias]

        return Contexto(
            objetivo=objetivo_limpo,
            escopo=escopo.strip() or "global",
            tarefa=tarefa.strip() if isinstance(tarefa, str) and tarefa.strip() else None,
            memorias=memorias_filtradas,
            estado=dict(estado or {}),
            metadados=dict(metadados or {}),
        )
