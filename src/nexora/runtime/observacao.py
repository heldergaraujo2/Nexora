"""Captura estruturada de saidas e resultados de execucao."""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass
class Observacao:
    """Resultado estruturado de uma etapa."""
    etapa_id: str
    ok: bool
    saida: str = ""
    erro: str | None = None
    metadados: dict[str, Any] = field(default_factory=dict)
    carimbo: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())