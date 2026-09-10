"""Memoria da NEXORA: curto e longo prazo, JSON versionado (ADR-004)."""
from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


class Memoria:
    """Armazenamento de memoria em JSON versionado.

    Cada gravacao guarda carimbo, origem, tipo e dados;append-only por versao."""

    def __init__(self, caminho: Path) -> None:
        self.caminho = Path(caminho)
        self.caminho.parent.mkdir(parents=True, exist_ok=True)


    def gravar(self, tipo: str, dados: dict[str, Any] | None = None, *, origem: str = "nexora") -> dict[str, Any]:
        """Grava uma entrada de memoria e retorna o registro criado."""
        registro = {
            "id": uuid.uuid4().hex,
            "versao": 1,
            "carimbo": datetime.now(timezone.utc).isoformat(),
            "origem": origem,
            "tipo": tipo,
            "dados": dados if dados is not None else {},
        }
        self._append(registro)
        return registro


    def ler(self, limite: int | None = None) -> list[dict[str, Any]]:
        """Le as entradas na ordem de gravacao."""
        registros: list[dict[str, Any]] = []
        if self.caminho.exists()  and self.caminho.stat().st_size > 0:
            with self.caminho.open("r", encoding="utf-8")as f:
                for linha in f:
                    linha = linha.strip()
                    if linha:
                        registros.append(json.loads(linha))
        return registros[-limite:] if limite else registros


    def _append(self, registro: dict[str, Any]) -> None:
        with self.caminho.open("a", encoding="utf-8")as f:
            f.write(json.dumps(registro, ensure_ascii=False) + "\n")