"""Evolution Engine: aprendizados e recomendacao deterministico (Fase 10)."""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class Aprendizado:
    """Registro de um aprendizado derivado de resultados de experimentos."""

    tarefa: str
    melhor_variante: str
    taxa_sucesso: float
    total_execucoes: int
    metadados: dict[str, Any] = field(default_factory=dict)


class RegistroAprendizados:
    """Persiste aprendizados em JSONL e lista de forma deterministico."""

    def __init__(self, caminho: Path) -> None:
        self.caminho = caminho

    def registrar(self, aprendizado: Aprendizado) -> None:
        """Grava um aprendizado como nova linha JSONL (append-only)."""
        self.caminho.parent.mkdir(parents=True, exist_ok=True)
        with self.caminho.open("a", encoding="utf-8") as arquivo:
            linha = json.dumps(
                {
                    "tarefa": aprendizado.tarefa,
                    "melhor_variante": aprendizado.melhor_variante,
                    "taxa_sucesso": aprendizado.taxa_sucesso,
                    "total_execucoes": aprendizado.total_execucoes,
                    "metadados": aprendizado.metadados,
                },
                ensure_ascii=False,
            )
            arquivo.write(linha + "\n")

    def listar(self) -> list[Aprendizado]:
        """Le todos os aprendizados persistidos, na ordem em que foram gravados."""
        if not self.caminho.exists():
            return []
        resultado = []
        with self.caminho.open("r", encoding="utf-8") as arquivo:
            for linha in arquivo:
                linha = linha.strip()
                if linha:
                    dados = json.loads(linha)
                    resultado.append(Aprendizado(
                        tarefa=dados["tarefa"],
                        melhor_variante=dados["melhor_variante"],
                        taxa_sucesso=dados["taxa_sucesso"],
                        total_execucoes=dados["total_execucoes"],
                        metadados=dados.get("metadados", {}),
                    ))
        return resultado

    def resumir(self) -> dict[str, Any]:
        """Resumo deterministico dos aprendizados ( contagem e taxa media por melhor_variante.)"""
        if len(self.listar()) == 0:
            return {"total": 0, "por_variante": {}}
        itens = self.listar()
        por_variante = {}
        for item in itens:
            chave = item.melhor_variante
            dados = por_variante.setdefault(chave, {"total": 0, "soma_taxas": 0.0})
            dados["total"] += 1
            dados["soma_taxas"] += item.taxa_sucesso
        for chave, dados in por_variante.items():
            dados["taxa_media"] = dados["soma_taxas"] / dados["total"]
        return {"total": len(itens), "por_variante": por_variante}


class RecomendadorEvolucao:


    """Deriva aprendizados de resultados de experimentos e recomenda a melhor abordagem."""
    def __init__(self, registro: RegistroAprendizados) -> None:
        self.registro = registro
        self.aprendizados_gerados: list[Aprendizado] = []


    def evoluir(self, experimento: dict[str, Any]) -> Aprendizado:



        """Consome um resultado de ExecutorExperimentos e gera/registra um aprendizado."""
        resultados = experimento["resultados"]
        sucessos = [r for r in resultados if r["sucesso"]]
        total = len(resultados)
        if total == 0:
            raise ValueError("experimento sem variantes")
        if sucessos:
            melhor = max(sucessos, key=lambda r: (r["sucesso"], -r["tentativas"]))
        else:
            melhor = max(resultados, key=lambda r: r["indice"])
        aprendizado = Aprendizado(
            tarefa=experimento["tarefa"],
            melhor_variante=melhor["variante"],
            taxa_sucesso=(len(sucessos) / total) if total else 0.0,
            total_execucoes=total,
            metadados={"experimento": experimento["experimento"]},
        )
        self.registro.registrar(aprendizado)
        self.aprendizados_gerados.append(aprendizado)
        return aprendizado


    def recomendar(self, tarefa: str) -> Aprendizado | None:
        """Recomenda o aprendizado registrado para uma tarefa (mais recente por prioridade.)"""
        aprendizados = [a for a in self.registro.listar() if a.tarefa == tarefa]
        if not aprendizados:
            return None
        melhor = max(aprendizados, key=lambda a: (a.taxa_sucesso, -a.total_execucoes))
        return melhor


    def registrar_aprendizado(self, aprendizado: Aprendizado) -> None:
        """Registra um aprendizado manualmente (via CLI.)"""
        self.registro.registrar(aprendizado)
        self.aprendizados_gerados.append(aprendizado)
