"""Testes do Economic Engine (Fase 11)."""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

from nexora.economia.registro import CustoExecucao, RegistroCustos


def test_custo_calcula_tokens_total() -> None:
    custo = CustoExecucao(provider="fake", tokens_entrada=10, tokens_saida=4)
    assert custo.tokens_total ==14
    assert custo.estimativa_monetaria == 0.0


def test_registro_registra_e_lista(tmp_path: Path) -> None:
    registro = RegistroCustos(tmp_path / "c.jsonl")
    registro.registrar(CustoExecucao(provider="fake", tokens_entrada=10, tokens_saida=4))
    itens = registro.listar()
    assert len(itens) == 1
    assert itens[0].provider == "fake"
    assert itens[0].tokens_total ==14


def test_registro_resumir_por_provider(tmp_path: Path) -> None:
    registro = RegistroCustos(tmp_path / "c.jsonl")
    registro.registrar(CustoExecucao(provider="fake", tokens_entrada=10, tokens_saida=4, estimativa_monetaria=0.001))
    registro.registrar(CustoExecucao(provider="groq", tokens_entrada=20, tokens_saida=6, estimativa_monetaria=0.002))
    resumo = registro.resumir()
    assert resumo["total_execucoes"] == 2
    assert resumo["total_tokens"] == 40
    assert abs(resumo["custo_monetario_total"] - 0.003) < 1e-9
    assert resumo["por_provider"]["fake"]["execucoes"] == 1


def test_cli_economia_registrar_e_resumir(tmp_path: Path) -> None:
    env = {**os.environ, "PYTHONPATH": str(Path.cwd() / "src")}
    caminho = tmp_path / "custos.jsonl"
    resultado = subprocess.run(
        [sys.executable, "-m", "nexora", "economia", "registrar", "--provider", "fake", "--tokens-entrada", "10", "--tokens-saida", "4", "--arquivo", str(caminho)],
        capture_output=True,
        text=True,
        env=env,
        timeout=30,
    )
    assert resultado.returncode == 0
    assert "custo registrado" in resultado.stdout
    resumo = subprocess.run(
        [sys.executable, "-m", "nexora", "economia", "resumir", "--arquivo", str(caminho)],
        capture_output=True,
        text=True,
        env=env,
        timeout=30,
    )
    assert resumo.returncode == 0
    assert "fake" in resumo.stdout
