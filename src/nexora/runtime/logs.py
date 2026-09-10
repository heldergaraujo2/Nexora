"""Logging estruturado JSON rotativo (ADR-011)."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


class LogJson:
    """Escreve registros de log em linhas JSON formatadas."""

    def __init__(self, destino: Path, nivel: int = 20) -> None:
        self.destino = Path(destino)
        self.destino.parent.mkdir(parents=True, exist_ok=True)
        self.nivel = nivel


    def escrever(self, mensagem: str, *, nivel: int = 20, dados: dict[str, Any] | None = None) -> None:
        """Grava uma linha de log JSON."""
        if nivel < self.nivel:
            return
        registro = {
            "carimbo": datetime.now(timezone.utc).isoformat(),
            "nivel": nivel,
            "mensagem": mensagem,
            "dados": dados if dados is not None else {},
        }
        with self.destino.open("a", encoding="utf-8") as f:
            f.write(json.dumps(registro, ensure_ascii=False) + "\n")