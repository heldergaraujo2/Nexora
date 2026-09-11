"""Testes do Experimentation Engine (Fase 9)."""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path
from typing import Any

from nexora.experimentacao.experimento import ExecutorExperimentos, Experimento
from nexora.providers.base import GenerationResult


class FakeExp:
    """Provider deterministico para testes do ExecutorExperimentos."""
    def __init__(self, respostas: list[str]) -> None:
        self.respostas = list(respostas)
        self.chamadas = []

    def generate(self, prompt: str, **kwargs: Any) -> GenerationResult:
        self.chamadas.append(prompt)
        texto = self.respostas.pop(0) if self.respostas else ""
        return GenerationResult(text=texto, tool_calls=[])


def test_experimento_adiciona_variantes():
    exp = Experimento(nome="prompt-v1", tarefa="resumir texto")
    exp.adicionar_variante("direto")
    exp.adicionar_variante("passo a passo")
    assert len(exp.variantes) == 2
    assert exp.variantes[0] == "direto"


def test_executor_compara_variantes():
    prov = FakeExp(["resposta A", "resposta B"])
    exp = Experimento(nome="x", tarefa="t", variantes=["v1", "v2"])
    resultado = ExecutorExperimentos(prov).executar(exp)
    assert resultado["total_variantes"] == 2
    assert resultado["sucessos"] == 2
    assert len(prov.chamadas) == 2
    assert resultado["resultados"][0]["saida"] == "resposta A"


def test_executor_registra_falha_em_saida_vazia():
    prov = FakeExp([""])
    exp = Experimento(nome="x", tarefa="t", variantes=["v1"])
    resultado = ExecutorExperimentos(prov).executar(exp)
    assert resultado["sucessos"] == 0
    assert resultado["resultados"][0]["sucesso"] is False


def test_executor_respeita_max_tentativas():
    prov = FakeExp(["", ""])
    exp = Experimento(nome="x", tarefa="t", variantes=["v1"])
    resultado = ExecutorExperimentos(prov, max_tentativas=2).executar(exp)
    assert resultado["resultados"][0]["tentativas"] == 2
    assert len(prov.chamadas) == 2


def test_cli_experimento():
    env = {**os.environ, "PYTHONPATH": str(Path.cwd() / "src")}
    resultado = subprocess.run(
        [sys.executable, "-m", "nexora", "experimento", "rodar", "--nome", "demo", "--tarefa", "teste", "--variante", "v1", "--provider", "fake"],
        capture_output=True,
        text=True,
        env=env,
        timeout=30,
    )
    assert resultado.returncode == 0
    assert "experimento" in resultado.stdout

