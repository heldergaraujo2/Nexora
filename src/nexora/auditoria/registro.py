"""Registro append-only de eventos de auditoria da NEXORA."""
from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


class RegistroAuditoria:
    """Persiste eventos de auditoria em JSONL para rastreabilidade."""

    def __init__(self, caminho: Path, *, origem: str = "nexora") -> None:
        self.caminho = Path(caminho)
        self.caminho.parent.mkdir(parents=True, exist_ok=True)
        self.origem = origem

    def registrar(
        self,
        evento: str,
        *,
        entidade: str,
        entidade_id: str,
        dados: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        if not evento.strip():
            raise ValueError("evento deve ser uma string nao vazia")
        if not entidade.strip() or not entidade_id.strip():
            raise ValueError("entidade e entidade_id sao obrigatorios")
        registro = {
            "id": uuid.uuid4().hex,
            "carimbo": datetime.now(timezone.utc).isoformat(),
            "origem": self.origem,
            "evento": evento,
            "entidade": entidade,
            "entidade_id": entidade_id,
            "dados": {} if dados is None else dict(dados),
        }
        with self.caminho.open("a", encoding="utf-8") as arquivo:
            arquivo.write(json.dumps(registro, ensure_ascii=False) + "\n")
        return registro

    def listar(
        self,
        *,
        evento: str | None = None,
        entidade: str | None = None,
        entidade_id: str | None = None,
        limite: int | None = None,
    ) -> list[dict[str, Any]]:
        registros: list[dict[str, Any]] = []
        if not self.caminho.exists() or self.caminho.stat().st_size == 0:
            return registros
        with self.caminho.open("r", encoding="utf-8") as arquivo:
            for linha in arquivo:
                linha = linha.strip()
                if not linha:
                    continue
                item = json.loads(linha)
                if evento is not None and item.get("evento") != evento:
                    continue
                if entidade is not None and item.get("entidade") != entidade:
                    continue
                if entidade_id is not None and item.get("entidade_id") != entidade_id:
                    continue
                registros.append(item)
        if limite is not None:
            if limite < 0:
                raise ValueError("limite nao pode ser negativo")
            registros = registros[-limite:] if limite else []
        return registros
