"""Economic Engine: registro deterministico de custos por execucao/experimento (Fase 11)."""
from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


class CustoExecucao:
    """Custo de uma execucao ou variante de experimento."""

    def __init__(
        self,
        *,
        provider: str,
        tokens_entrada: int = 0,
        tokens_saida: int = 0,
        estimativa_monetaria: float =  0.0,
        metadados: dict[str, Any] | None = None,
    ) -> None:
        self.provider = provider
        self.tokens_entrada = tokens_entrada
        self.tokens_saida = tokens_saida
        self.tokens_total = tokens_entrada + tokens_saida
        self.estimativa_monetaria = estimativa_monetaria
        self.metadados = metadados or {}
        self.id = uuid.uuid4().hex
        self.carimbo = datetime.now(timezone.utc).isoformat()


    def para_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "carimbo": self.carimbo,
            "provider": self.provider,
            "tokens_entrada": self.tokens_entrada,
            "tokens_saida": self.tokens_saida,
            "tokens_total": self.tokens_total,
            "estimativa_monetaria": self.estimativa_monetaria,
            "metadados": self.metadados,
        }


class RegistroCustos:
    """Persiste custos append-only em JSONL e deriva resumos deterministicos."""

    def __init__(self, caminho: Path) -> None:
        self.caminho = caminho

    def registrar(self, custo: CustoExecucao) -> None:
        """Grava um custo como nova linha JSONL (append-only)."""
        self.caminho.parent.mkdir(parents=True, exist_ok=True)
        with self.caminho.open("a", encoding="utf-8") as arquivo:
            arquivo.write(json.dumps(custo.para_dict(), ensure_ascii=False) + chr(10))

    def listar(self) -> list[CustoExecucao]:
        """Le todos os custos na ordem em que foram gravados."""
        if not self.caminho.exists():
            return []
        resultado = []
        with self.caminho.open("r", encoding="utf-8") as arquivo:
            for linha in arquivo:
                linha = linha.strip()
                if linha:
                    dados = json.loads(linha)
                    resultado.append(CustoExecucao(
                        provider=dados["provider"],
                        tokens_entrada=dados.get("tokens_entrada",  0),
                        tokens_saida=dados.get("tokens_saida", 0),
                        estimativa_monetaria=dados.get("estimativa_monetaria", 0.0),
                        metadados=dados.get("metadados", {}),
                    ))
        return resultado

    def resumir_por_provider(self) -> dict[str, Any]:
        """Resumo deterministico por provider: total de execucoes, tokens, custo monetario."""
        resumo: dict[str, dict[str, Any]] = {}
        for custo in self.listar():
            chave = custo.provider
            dados = resumo.setdefault(chave, {
                "execucoes": 0,
                "tokens_entrada": 0,
                "tokens_saida": 0,
                "tokens_total": 0,
                "custo_monetario":  0.0,
            })
            dados["execucoes"] += 1
            dados["tokens_entrada"] += custo.tokens_entrada
            dados["tokens_saida"] += custo.tokens_saida
            dados["tokens_total"] += custo.tokens_total
            dados["custo_monetario"] += custo.estimativa_monetaria
        return dict(sorted(resumo.items()))

    def resumir(self) -> dict[str, Any]:
        """Resumo geral deterministico de todos os custos."""
        por_provider = self.resumir_por_provider()
        total_execucoes = sum(d["execucoes"] for d in por_provider.values())
        total_tokens = sum(d["tokens_total"] for d in por_provider.values())
        total_custo = sum(d["custo_monetario"] for d in por_provider.values())
        return {
            "total_execucoes": total_execucoes,
            "total_tokens": total_tokens,
            "custo_monetario_total": total_custo,
            "por_provider": por_provider,
        }
