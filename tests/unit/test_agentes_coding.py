"""Testes do Coding Agent (Fase 6)."""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path
from typing import Any

from nexora.agentes.coding import CodingAgent
from nexora.providers.base import GenerationResult


class FakeCodigo:
    "Provider deterministico para testes do CodingAgent."
    def __init__(self, respostas: list[str]) -> None:
        self.respostas = list(respostas)
        self.chamadas = []

    def generate(self, prompt: str, **kwargs: Any) -> GenerationResult:
        self.chamadas.append(prompt)
        texto = self.respostas.pop(0) if self.respostas else ""
        return GenerationResult(text=texto, tool_calls=[])


def test_codar_gera_codigo_valido():
    prov = FakeCodigo(["def oi(): return 1"])
    ag = CodingAgent(prov)
    r = ag.codar("funcao oi")
    assert r.sucesso is True
    assert len(prov.chamadas) ==1

def test_codar_corrige_codigo_invalido():
    prov = FakeCodigo([
        "def oi():",
        "def oi(): return 1",
    ])
    ag = CodingAgent(prov, max_tentativas=3)
    r = ag.codar("funcao oi")
    assert r.sucesso is True
    assert r.tentativas ==2
    assert len(prov.chamadas) ==2

def test_codar_respeita_limite():
    prov = FakeCodigo(["def oi():"])
    ag = CodingAgent(prov, max_tentativas=2)
    r = ag.codar("funcao oi")
    assert r.sucesso is False
    assert r.tentativas ==2
    assert len(prov.chamadas) ==2

def test_cli_agente_codar():
    env = {**os.environ, "PYTHONPATH": str(Path.cwd() / "src")}
    resultado = subprocess.run(
        [sys.executable, "-m", "nexora", "agente", "codar", "escreva uma funcao oi", "--provider", "fake"],
        capture_output=True,
        text=True,
        env=env,
        timeout=30,
    )
    assert resultado.returncode ==0
    assert "sucesso=True" in resultado.stdout

