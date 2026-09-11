"""Testes do Experience Engine ( Fase  8)."""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

from nexora.experiencia.registro import RegistroExperiencias


def test_registrar_persiste_json(tmp_path):
    arquivo = tmp_path / "experiencias.jsonl"
    reg = RegistroExperiencias(arquivo)
    r = reg.registrar("codar", True, metadados={"linguagem": "python"})
    assert r["tipo_de_tarefa"] == "codar"
    assert r["sucesso"] is True
    assert arquivo.exists()
    linhas = arquivo.read_text(encoding="utf-8").strip().splitlines()
    assert len(linhas) == 1


def test_listar_filtra_por_tipo(tmp_path):
    arquivo = tmp_path / "experiencias.jsonl"
    reg = RegistroExperiencias(arquivo)
    reg.registrar("codar", True)
    reg.registrar("pesquisar", False)
    reg.registrar("codar", False)
    so_codar = reg.listar(tipo_de_tarefa="codar")
    assert len(so_codar) == 2
    assert all(r["tipo_de_tarefa"] == "codar" for r in so_codar)


def test_resumir_deterministico(tmp_path):
    arquivo = tmp_path / "experiencias.jsonl"
    reg = RegistroExperiencias(arquivo)
    reg.registrar("codar", True)
    reg.registrar("codar", True)
    reg.registrar("codar", False)
    resumo = reg.resumir()
    assert resumo["geral"]["total"] == 3
    assert resumo["geral"]["sucesso"] == 2
    assert resumo["geral"]["falhas"] == 1
    assert resumo["tipos"]["codar"]["taxa_sucesso"] == 2 / 3


def test_resumir_vazio(tmp_path):
    arquivo = tmp_path / "experiencias.jsonl"
    reg = RegistroExperiencias(arquivo)
    resumo = reg.resumir()
    assert resumo["geral"]["total"] == 0
    assert resumo["geral"]["taxa_sucesso"] == 0.0
    assert resumo["tipos"] == {}


def test_cli_experiencia(tmp_path):
    env = {**os.environ, "PYTHONPATH": str(Path.cwd() / "src")}
    caminho = tmp_path / "exp.jsonl"
    resultado = subprocess.run(
        [sys.executable, "-m", "nexora", "experiencia", "resumir", "--arquivo", str(caminho)],
        capture_output=True,
        text=True,
        env=env,
        timeout=30,
    )
    assert resultado.returncode == 0
    assert "total" in resultado.stdout

