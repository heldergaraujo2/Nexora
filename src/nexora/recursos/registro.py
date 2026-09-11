"""Resource Management: registro de recursos consumidos da NEXORA (Fase 14)."""
from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


class Recurso:

    """Um recurso consumido por um executor da plataforma."""

    def __init__(self, *, tipo: str, quantidade: float, executor: str, escopo: str = "global", metadados: dict | None = None) -> None:
        self.tipo = tipo
        self.quantidade = quantidade
        self.executor = executor
        self.escopo = escopo
        self.metadados = metadados or {}
        self.id = uuid.uuid4().hex
        self.carimbo = datetime.now(timezone.utc).isoformat()

    def para_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
 "carimbo": self.carimbo,
 "tipo": self.tipo,
 "quantidade": self.quantidade,
 "executor": self.executor,
 "escopo": self.escopo,
 "metadados": self.metadados,
 }

class RegistroRecursos:

    def __init__(self, caminho: Path) -> None:
        self.caminho = caminho


    def registrar(self, *, tipo: str, quantidade: float, executor: str, escopo: str = "global", metadados: dict | None = None) -> None:
        recurso = Recurso(tipo=tipo, quantidade=quantidade, executor=executor, escopo=escopo, metadados=metadados)
        self.caminho.parent.mkdir(parents=True, exist_ok=True)
        with self.caminho.open("a", encoding="utf-8")as arquivo:


            arquivo.write(json.dumps(recurso.para_dict(), ensure_ascii=False) + "\n")


    def listar(self) -> list[Recurso]:
        """Le todos os recursos na ordem em que foram gravados."""
        if not self.caminho.exists():
            return []
        resultado = []
        with self.caminho.open("r", encoding="utf-8")as arquivo:

            for linha in arquivo:
                linha = linha.strip()
                if linha:
                    dados = json.loads(linha)
                    resultado.append(Recurso(
                        tipo=dados["tipo"],
                        quantidade=dados["quantidade"],
                        executor=dados["executor"],
                        escopo=dados.get("escopo", "global"),
                        metadados=dados.get("metadados", {}),
                    ))
        return resultado


    def resumir(self) -> dict[str, Any]:
        """Resumo deterministico por tipo: quantidade total por executor."""
        resumo: dict[str, dict[str, float]] = {}
        for item in self.listar():
            dados = resumo.setdefault(item.tipo, {})
            dados[item.executor] = dados.get(item.executor, 0) + item.quantidade
        return dict(sorted(resumo.items()))
