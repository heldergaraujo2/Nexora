"""Registro de experiencias da NEXORA: consultas deterministicas e resumo por tipo ( Fase  8)."""
from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


class RegistroExperiencias:
    """Experiencias append-only em JSONL, consultaveis e resumiveis."""

    def __init__(self, caminho: Path, *, origem: str = "nexora") -> None:
        self.caminho = Path(caminho)
        self.caminho.parent.mkdir(parents=True, exist_ok=True)
        self.origem = origem

    def registrar(self, tipo_de_tarefa: str, sucesso: bool, *, metadados: dict = None) -> dict:
        """Registra uma experiencia e retorna o registro criado."""
        registro = {
            "id": uuid.uuid4().hex,
            "carimbo": datetime.now(timezone.utc).isoformat(),
            "origem": self.origem,
            "tipo_de_tarefa": tipo_de_tarefa,
            "sucesso": bool(sucesso),
            "metadados": metadados or {},
        }
        with self.caminho.open("a", encoding="utf-8") as f:
            f.write(json.dumps(registro, ensure_ascii=False) + "\n")
        return registro

    def listar(self, *, tipo_de_tarefa: str = None, limite: int = None) -> list:
        """Lista experiencias, filtrando por tipo e limitando."""
        registros: list = []
        if not self.caminho.exists() or self.caminho.stat().st_size == 0:
            return registros
        with self.caminho.open("r", encoding="utf-8") as f:
            for linha in f:
                linha = linha.strip()
                if linha:
                    item = json.loads(linha)
                    if tipo_de_tarefa is None or item.get("tipo_de_tarefa") == tipo_de_tarefa:
                        registros.append(item)
        if limite:
            registros = registros[-limite:]
        return registros

    def resumir(self) -> dict:
        """Resumo deterministico por tipo: total, sucesso, falhas e taxa."""
        registros = self.listar()
        resumo: dict = {"tipos": {}, "geral": {"total": len(registros), "sucesso": 0, "falhas":  0, "taxa_sucesso": 0.0}}
        for r in registros:
            tipo = r.get("tipo_de_tarefa", "desconhecido")
            if tipo not in resumo["tipos"]:
                resumo["tipos"][tipo] = {"total": 0, "sucesso":  0, "falhas":  0, "taxa_sucesso":  0.0}
            resumo["tipos"][tipo]["total"] += 1
            if r.get("sucesso") is True:
                resumo["tipos"][tipo]["sucesso"] += 1
                resumo["geral"]["sucesso"] += 1
            else:
                resumo["tipos"][tipo]["falhas"] += 1
                resumo["geral"]["falhas"] += 1
        for tipo in resumo["tipos"]:
            total_tipo = resumo["tipos"][tipo]["total"]
            if total_tipo:
                resumo["tipos"][tipo]["taxa_sucesso"] = resumo["tipos"][tipo]["sucesso"] / total_tipo
        if resumo["geral"]["total"]:
            resumo["geral"]["taxa_sucesso"] = resumo["geral"]["sucesso"] / resumo["geral"]["total"]
        return resumo

