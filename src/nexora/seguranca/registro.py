"""Security Engine: politica de permissoes de acoes da NEXORA (Fase 12)."""
from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


class Acao:
    """Definicao de uma acao com politica de permissao."""

    def __init__(self, *, nome: str, permitida: bool = False, escopo: str = "global", metadados: dict | None = None) -> None:
        self.nome = nome
        self.permitida = permitida
        self.escopo = escopo
        self.metadados = metadados or {}
        self.id = uuid.uuid4().hex
        self.carimbo = datetime.now(timezone.utc).isoformat()

    def para_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
 "carimbo": self.carimbo,
 "nome": self.nome,
 "permitida": self.permitida,
 "escopo": self.escopo,
 "metadados": self.metadados,
 }

class RegistroPolitica:
    """Persiste acoes e politicas de permissao em JSONL deterministico."""

    def __init__(self, caminho: Path) -> None:
        self.caminho = caminho

    def definir(self, *, nome: str, permitida: bool, escopo: str = "global", metadados: dict | None = None) -> None:
        """Define(ou atualiza)a politica de uma acao."""
        acao = Acao(nome=nome, permitida=permitida, escopo=escopo, metadados=metadados)
        self.caminho.parent.mkdir(parents=True, exist_ok=True)
        with self.caminho.open("a", encoding="utf-8") as arquivo:
            arquivo.write(json.dumps(acao.para_dict(), ensure_ascii=False) + "\n")


    def avaliar(self, nome: str, escopo: str = "global") -> bool:
        """Avalia se uma acao esta permitida no escopo dado(ultima definicao vence."""
        itens = self.listar()
        permitida = None
        for item in itens:

            if item.nome == nome and item.escopo == escopo:
                permitida = item.permitida
            elif item.nome == nome and item.escopo == "global":
                permitida = item.permitida
        if permitida is None:
            raise KeyError(f"acao sem politica:{nome} no escopo {escopo}")
        return permitida

    def listar(self) -> list[Acao]:
        """Le todas as acoes na ordem em que foram gravadas."""
        if not self.caminho.exists():
            return []
        resultado = []
        with self.caminho.open("r", encoding="utf-8") as arquivo:

            for linha in arquivo:
                linha = linha.strip()
                if linha:
                    dados = json.loads(linha)
                    resultado.append(Acao(
                        nome=dados["nome"],
                        permitida=dados["permitida"],
                        escopo=dados.get("escopo", "global"),
                        metadados=dados.get("metadados", {}),
                    ))
        return resultado

    def resumir(self) -> dict[str, Any]:
        """Resumo deterministico por escopo: total, permitidas e bloqueadas."""
        resumo: dict[str, dict[str, Any]] = {}
        for item in self.listar():
            dados = resumo.setdefault(item.escopo, {"total": 0, "permitidas": 0, "bloqueadas": 0})
            dados["total"] += 1
            if item.permitida:

                dados["permitidas"] += 1
            else:
                dados["bloqueadas"] +=  1
        return dict(sorted(resumo.items()))
