"""Long-Term Autonomy: autonomia de longo prazo da NEXORA (Fase  16)."""
from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


class MetaLongoPrazo:

    """Uma meta de longo prazo perseguida pela plataforma."""

    def __init__(self, *, nome: str, descricao: str = "", status: str = "ativa", metadados: dict | None = None) -> None:
        self.nome = nome
        self.descricao = descricao
        self.status = status
        self.metadados = metadados or {}
        self.id = uuid.uuid4().hex
        self.carimbo = datetime.now(timezone.utc).isoformat()

    def para_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,

 "carimbo": self.carimbo,
 "nome": self.nome,
 "descricao": self.descricao,
 "status": self.status,
 "metadados": self.metadados,
 }


class RegistroAutonomia:

    def __init__(self, caminho: Path) -> None:
        self.caminho = caminho


    def definir(self, *, nome: str, descricao: str = "", status: str = "ativa", metadados: dict | None = None) -> None:
        meta = MetaLongoPrazo(nome=nome, descricao=descricao, status=status, metadados=metadados)
        self.caminho.parent.mkdir(parents=True, exist_ok=True)
        with self.caminho.open("a", encoding="utf-8")as arquivo:



            arquivo.write(json.dumps(meta.para_dict(), ensure_ascii=False) + "\n")


    def listar(self) -> list[MetaLongoPrazo]:
        """Le todas as metas na ordem em que foram gravadas."""
        if not self.caminho.exists():
            return []
        resultado = []
        with self.caminho.open("r", encoding="utf-8")as arquivo:

            for linha in arquivo:
                linha = linha.strip()
                if linha:
                    dados = json.loads(linha)
                    resultado.append(MetaLongoPrazo(
                        nome=dados["nome"],
                        descricao=dados.get("descricao", ""),
                        status=dados.get("status", "ativa"),
                        metadados=dados.get("metadados", {}),
                    ))
                    resultado[-1].id = dados["id"]
        return resultado


    def atualizar_status(self, id: str, status: str) -> bool:
        """Atualiza o status de uma meta ( sem reescrever o historico."""
        metas = self.listar()
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
        """Resumo deterministico por status."""
        resumo: dict[str, int] = {}
        for meta in self.listar():
            resumo[meta.status] = resumo.get(meta.status, 0) + 1
        return dict(sorted(resumo.items()))
