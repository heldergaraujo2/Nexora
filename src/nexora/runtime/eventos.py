"""Event store append-only JSON da NEXORA (ADR-005)."""
from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


class EventStore:
    """Registro imutavel de eventos em JSON append-only.

    O arquivo cresce apenas com adicoes;nunca reescreve ou apaga linhas."""

    def __init__(self, caminho: Path) -> None:
        self.caminho = Path(caminho)
        self.caminho.parent.mkdir(parents=True, exist_ok=True)


    def registrar(self, tipo: str, dados: dict | None = None, *, origem: str = "nexora", correlacao: str | None = None) -> dict:
        """Registra um evento e retorna o evento criado."""
        evento = {
            "id": uuid.uuid4().hex,
            "carimbo": datetime.now(timezone.utc).isoformat(),
            "origem": origem,
            "tipo": tipo,
            "correlacao": correlacao,
            "dados": dados or {},
        }
        with self.caminho.open("a", encoding="utf-8") as f:
            f.write(json.dumps(evento, ensure_ascii=False) + "\n")
        return evento


    def ler(self, limite: int | None = None) -> list[dict[str, Any]]:
        """Le os eventos na ordem de registro."""
        eventos: list[dict[str, Any]] = []
        if not self.caminho.exists() or self.caminho.stat().st_size == 0:
            return eventos
        with self.caminho.open("r", encoding="utf-8") as f:
            for linha in f:
                linha = linha.strip()
                if linha:
                    eventos.append(json.loads(linha))
        return eventos[-limite:] if limite else eventos