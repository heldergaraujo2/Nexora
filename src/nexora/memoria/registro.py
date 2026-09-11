"""Memory Engine: memoria persistente da NEXORA (Fase 13)."""
from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


class ItemMemoria:
    """Um item de memoria com chave determinística e conteudo."""

    def __init__(self, *, chave: str, conteudo: str, escopo: str = "global", metadados: dict | None = None) -> None:
        self.chave = chave
        self.conteudo = conteudo
        self.escopo = escopo
        self.metadados = metadados or {}
        self.id = uuid.uuid4().hex
        self.carimbo = datetime.now(timezone.utc).isoformat()

    def para_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
 "carimbo": self.carimbo,
 "chave": self.chave,
 "conteudo": self.conteudo,
 "escopo": self.escopo,
 "metadados": self.metadados,
 }

class RegistroMemorias:

    def __init__(self, caminho: Path) -> None:
        self.caminho = caminho


    def lembrar(self, *, chave: str, conteudo: str, escopo: str = "global", metadados: dict | None = None) -> None:
        item = ItemMemoria(chave=chave, conteudo=conteudo, escopo=escopo, metadados=metadados)
        self.caminho.parent.mkdir(parents=True, exist_ok=True)
        with self.caminho.open("a", encoding="utf-8") as arquivo:


            arquivo.write(json.dumps(item.para_dict(), ensure_ascii=False) + "\n")


    def buscar(self, *, chave: str, escopo: str = "global") -> str | None:
        """Ultima ocorrencia vence"""
        itens = self.listar()
        encontrado = None
        for item in itens:
            if item.chave == chave and item.escopo == escopo:
                encontrado = item
            elif item.chave == chave and item.escopo == "global":
                encontrado = item
        return encontrado.conteudo if encontrado is not None else None

    def listar(self) -> list[ItemMemoria]:
        """Le todas as memorias na ordem em que foram gravadas."""
        if not self.caminho.exists():
            return []
        resultado = []
        with self.caminho.open("r", encoding="utf-8") as arquivo:

            for linha in arquivo:
                linha = linha.strip()
                if linha:
                    dados = json.loads(linha)
                    resultado.append(ItemMemoria(
                        chave=dados["chave"],
                        conteudo=dados["conteudo"],
                        escopo=dados.get("escopo", "global"),
                        metadados=dados.get("metadados", {}),
                    ))
        return resultado


    def resumir(self) -> dict[str, Any]:
        """Resumo deterministico por escopo: total de memorias."""
        resumo: dict[str, int] = {}
        for item in self.listar():
            resumo[item.escopo] = resumo.get(item.escopo, 0) + 1
        return dict(sorted(resumo.items()))
