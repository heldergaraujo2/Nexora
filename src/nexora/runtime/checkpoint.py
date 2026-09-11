"""Checkpoints de execucao para recuperacao controlada da NEXORA.

O engine captura estado antes de uma acao e permite recuperar uma copia desse
estado. Ele nao executa ferramentas, nao faz rollback de efeitos externos e
nao substitui a camada de verificacao.
"""
from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from nexora.auditoria import RegistroAuditoria


@dataclass(frozen=True)
class Checkpoint:
    """Snapshot logico de um estado de execucao."""

    id: str
    execucao_id: str
    estado: dict[str, Any]
    motivo: str
    carimbo: str


class CheckpointEngine:
    """Cria e recupera snapshots logicos sem executar efeitos externos."""

    def __init__(self, *, auditoria: RegistroAuditoria | None = None) -> None:
        self._checkpoints: dict[str, Checkpoint] = {}
        self._auditoria = auditoria

    def criar(
        self,
        execucao_id: str,
        estado: dict[str, Any],
        *,
        motivo: str = "antes_da_acao",
    ) -> Checkpoint:
        if not execucao_id.strip():
            raise ValueError("execucao_id deve ser uma string nao vazia")
        if not isinstance(estado, dict):
            raise TypeError("estado deve ser um dicionario")
        if not motivo.strip():
            raise ValueError("motivo deve ser uma string nao vazia")

        checkpoint = Checkpoint(
            id=uuid4().hex,
            execucao_id=execucao_id.strip(),
            estado=deepcopy(estado),
            motivo=motivo.strip(),
            carimbo=datetime.now(timezone.utc).isoformat(),
        )
        self._checkpoints[checkpoint.id] = checkpoint
        self._auditar(
            "checkpoint.criado",
            checkpoint,
            {"motivo": checkpoint.motivo},
        )
        return self._copia(checkpoint)

    def obter(self, checkpoint_id: str) -> Checkpoint:
        if not checkpoint_id.strip():
            raise ValueError("checkpoint_id deve ser uma string nao vazia")
        try:
            checkpoint = self._checkpoints[checkpoint_id.strip()]
        except KeyError as exc:
            raise KeyError(f"Checkpoint inexistente: {checkpoint_id}") from exc
        return self._copia(checkpoint)

    def recuperar(self, checkpoint_id: str) -> dict[str, Any]:
        """Retorna uma copia do estado; nao executa nem desfaz efeitos externos."""
        checkpoint = self.obter(checkpoint_id)
        self._auditar(
            "checkpoint.recuperado",
            checkpoint,
            {"motivo": checkpoint.motivo},
        )
        return deepcopy(checkpoint.estado)

    def listar(self, *, execucao_id: str | None = None) -> list[Checkpoint]:
        checkpoints = self._checkpoints.values()
        if execucao_id is not None:
            if not execucao_id.strip():
                raise ValueError("execucao_id nao pode ser vazio")
            checkpoints = (
                item for item in checkpoints if item.execucao_id == execucao_id.strip()
            )
        return [self._copia(item) for item in checkpoints]

    @staticmethod
    def _copia(checkpoint: Checkpoint) -> Checkpoint:
        return Checkpoint(
            id=checkpoint.id,
            execucao_id=checkpoint.execucao_id,
            estado=deepcopy(checkpoint.estado),
            motivo=checkpoint.motivo,
            carimbo=checkpoint.carimbo,
        )

    def _auditar(
        self,
        evento: str,
        checkpoint: Checkpoint,
        dados: dict[str, Any],
    ) -> None:
        if self._auditoria is not None:
            self._auditoria.registrar(
                evento,
                entidade="checkpoint",
                entidade_id=checkpoint.id,
                dados={
                    "execucao_id": checkpoint.execucao_id,
                    **dados,
                },
            )
