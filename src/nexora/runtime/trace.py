"""Rastreamento estruturado de execucoes da NEXORA.

O ExecutionTrace fornece um contrato comum para correlacionar observabilidade,
governanca, custo e falhas sem acoplar o runtime a um backend de telemetria.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4


@dataclass
class ExecutionTrace:
    """Contexto observavel de uma execucao e de seus spans."""

    execution_id: str = field(default_factory=lambda: uuid4().hex)
    trace_id: str = field(default_factory=lambda: uuid4().hex)
    span_id: str = field(default_factory=lambda: uuid4().hex)
    agent_id: str = ""
    task_id: str = ""
    provider: str = ""
    model: str = ""
    tokens: int | None = None
    latency_ms: float | None = None
    cost: float | None = None
    retry_count: int = 0
    failure_type: str = ""
    policy_version: str = ""
    policy_fingerprint: str = ""
    checkpoint_id: str = ""
    status: str = "running"
    started_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    finished_at: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def finalizar(self, *, status: str, failure_type: str = "") -> None:
        """Finaliza o trace sem apagar os dados coletados."""
        if status.strip() == "":
            raise ValueError("status deve ser uma string nao vazia")
        self.status = status
        self.failure_type = failure_type
        self.finished_at = datetime.now(timezone.utc).isoformat()

    def incrementar_retry(self) -> int:
        """Incrementa e retorna o contador de retries."""
        self.retry_count += 1
        return self.retry_count

    def para_dict(self) -> dict[str, Any]:
        """Serializa o trace para persistencia/auditoria."""
        return asdict(self)
