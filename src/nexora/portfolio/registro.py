"""Portfolio Engine: portfolio de trabalhos da NEXORA (Fase  15)."""
from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


class ItemPortfolio:

    """Um item do portfolio: um trabalho acompanhado pela plataforma."""

    def __init__(self, *, nome: str, categoria: str = "geral", status: str = "ativo", metadados: dict | None = None) -> None:
        self.nome = nome
        self.categoria = categoria
        self.status = status
        self.metadados = metadados or {}
        self.id = uuid.uuid4().hex
        self.carimbo = datetime.now(timezone.utc).isoformat()

    def para_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,

 "carimbo": self.carimbo,
 "nome": self.nome,
 "categoria": self.categoria,
 "status": self.status,
 "metadados": self.metadados,
 }


class RegistroPortfolio:

    def __init__(self, caminho: Path) -> None:
        self.caminho = caminho


    def adicionar(self, *, nome: str, categoria: str = "geral", status: str = "ativo", metadados: dict | None = None) -> None:
        item = ItemPortfolio(nome=nome, categoria=categoria, status=status, metadados=metadados)
        self.caminho.parent.mkdir(parents=True, exist_ok=True)
        with self.caminho.open("a", encoding="utf-8")as arquivo:


            arquivo.write(json.dumps(item.para_dict(), ensure_ascii=False) + "\n")


    def listar(self) -> list[ItemPortfolio]:
        """Le todos os itens na ordem em que foram gravados."""
        if not self.caminho.exists():
            return []
        resultado = []
        with self.caminho.open("r", encoding="utf-8")as arquivo:

            for linha in arquivo:
                linha = linha.strip()
                if linha:
                    dados = json.loads(linha)
                    resultado.append(ItemPortfolio(
                        nome=dados["nome"],
                        categoria=dados.get("categoria", "geral"),
                        status=dados.get("status", "ativo"),
                        metadados=dados.get("metadados", {}),
                    ))
                    resultado[-1].id = dados["id"]
        return resultado


    def atualizar_status(self, id: str, status: str) -> bool:
        """Atualiza o status de um item pelo id( sem reescrever o historico."""
        itens = self.listar()
        encontrado = False
        linhas: list[str] = []
        with self.caminho.open("r", encoding="utf-8")as arquivo:


            for linha in arquivo:
                linha = linha.strip()
                if not linha:
                    linhas.append("")


                    continue
                dados = json.loads(linha)


                if dados.get("id") == id:
                    dados["status"] = status


                    encontrado = True


                linhas.append(json.dumps(dados, ensure_ascii=False))


        if encontrado:
            with self.caminho.open("w", encoding="utf-8")as arquivo:
                for linha in linhas:
                    if linha:
                        arquivo.write(linha + "\n")


        return encontrado


    def resumir(self) -> dict[str, Any]:
        """Resumo deterministico por categoria: total por status."""
        resumo: dict[str, dict[str, int]] = {}
        for item in self.listar():
            dados = resumo.setdefault(item.categoria, {})
            dados[item.status] = dados.get(item.status, 0) + 1
        return dict(sorted(resumo.items()))
