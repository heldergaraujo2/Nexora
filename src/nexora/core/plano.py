"""Plano de execucao: lista de tarefas estruturadas (ADR-002 e ADR-009.."""
from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Any


class Tarefa:
    """Unidade atomica de trabalho dentro de um plano."""

    def __init__(
        self,
        descricao: str,
        *,
        ferramenta: str | None = None,
        parametros: dict[str, Any] | None = None,
        depende_de: list[str] | None = None,
    ) -> None:
        self.id = uuid.uuid4().hex
        self.descricao = descricao.strip()
        self.ferramenta = ferramenta
        self.parametros = parametros if parametros is not None else {}
        self.depende_de = depende_de if depende_de is not None else []
        self.status: str = "pendente"
        self.resultado: dict[str, Any] | None = None
        self.erro: str | None = None
        self.iniciada_em: str | None = None
        self.concluida_em: str | None = None


    def para_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "descricao": self.descricao,
            "ferramenta": self.ferramenta,
            "parametros": self.parametros,
            "depende_de": self.depende_de,
            "status": self.status,
            "resultado": self.resultado,
            "erro": self.erro,
            "iniciada_em": self.iniciada_em,
            "concluida_em": self.concluida_em,
        }


class Plano:
    """Plano de acao com tarefas ordenadas por dependencias."""

    def __init__(self, objetivo_id: str, tarefas: list[Tarefa] | None = None) -> None:
        self.id = uuid.uuid4().hex
        self.objetivo_id = objetivo_id
        self.tarefas = tarefas if tarefas is not None else []
        self.criado_em = datetime.now(timezone.utc).isoformat()
        self.status: str = "planejado"


    def adicionar_tarefa(self, tarefa: Tarefa) -> None:

        self.tarefas.append(tarefa)


    def pendentes(self) -> list[Tarefa]:
        return [t for t in self.tarefas if t.status == "pendente"]


    def para_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "objetivo_id": self.objetivo_id,
            "tarefas": [t.para_dict() for t in self.tarefas],
            "criado_em": self.criado_em,
            "status": self.status,
        }