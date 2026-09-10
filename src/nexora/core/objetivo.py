"""Representacao de um objetivo em linguagem natural (ADR-001 nao exigido aqui)."""
from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Any


class Objetivo:
    """Objetivo recebido de um usuario, com estado de execucao."""

    def __init__(
        self,
        texto: str,
        *,
        objetivos_secundarios: list[str] | None = None,
    ) -> None:
        self.id = uuid.uuid4().hex
        self.texto = texto.strip()
        self.objetivos_secundarios = objetivos_secundarios or []
        self.criado_em = datetime.now(timezone.utc).isoformat()
        self.concluido_em: str | None = None
        self.sucesso: bool | None = None
        self.metricas: dict[str, Any] = {}


    def para_dict(self) -> dict[str, Any]:
        """Serializa o objetivo para o contrato JSON."""
        return {
            "id": self.id,
            "texto": self.texto,
            "objetivos_secundarios": self.objetivos_secundarios,
            "criado_em": self.criado_em,
            "concluido_em": self.concluido_em,
            "sucesso": self.sucesso,
            "metricas": self.metricas,
        }