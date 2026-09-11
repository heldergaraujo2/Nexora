"""Testes do Security Engine (Fase 12)."""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

from nexora.seguranca.registro import Acao, RegistroPolitica


def test_acao_campos_padrao() -> None:
    acao = Acao(nome="excluir")
    assert acao.nome == "excluir"
    assert acao.permitida is False
    assert acao.escopo == "global"


def test_politica_definir_e_listar(tmp_path: Path) -> None:
    registro = RegistroPolitica(tmp_path / "politica.jsonl")
    registro.definir(nome="excluir", permitida=False)
    registro.definir(nome="listar", permitida=True, escopo="admin")
    itens = registro.listar()
    assert len(itens) == 2
    assert itens[0].nome == "excluir"
    assert itens[0].permitida is False


def test_politica_avaliar_permite_e_bloqueia(tmp_path: Path) -> None:
    registro = RegistroPolitica(tmp_path / "politica.jsonl")
    registro.definir(nome="excluir", permitida=False)
    registro.definir(nome="listar", permitida=True, escopo="admin")
    assert registro.avaliar("excluir") is False
    assert registro.avaliar("listar", escopo="admin") is True


def test_politica_avaliar_sem_politica_levanta_erro(tmp_path: Path) -> None:
    registro = RegistroPolitica(tmp_path / "politica.jsonl")
    try:
        registro.avaliar("inexistente")
    except KeyError:
        return
    raise AssertionError("deveria levantar KeyError")
def test_politica_resumir_por_escopo(tmp_path: Path) -> None:
    registro = RegistroPolitica(tmp_path / "politica.jsonl")
    registro.definir(nome="excluir", permitida=False)
    registro.definir(nome="listar", permitida=True, escopo="admin")
    resumo = registro.resumir()
    assert resumo["global"]["total"] == 1
    assert resumo["global"]["bloqueadas"] == 1
    assert resumo["admin"]["permitidas"] == 1


def test_cli_seguranca_definir_e_avaliar(tmp_path: Path) -> None:
    env = {**os.environ, "PYTHONPATH": str(Path.cwd() / "src")}
    caminho = tmp_path / "politica.jsonl"
    definir = subprocess.run(
        [sys.executable, "-m", "nexora", "seguranca", "definir", "--acao", "executar", "--permitir", "--arquivo", str(caminho)],
        capture_output=True,
        text=True,
        env=env,
        timeout=30,
    )
    assert definir.returncode == 0
    avaliar = subprocess.run(
        [sys.executable, "-m", "nexora", "seguranca", "avaliar", "--acao", "executar", "--arquivo", str(caminho)],
        capture_output=True,
        text=True,
        env=env,
        timeout=30,
    )
    assert avaliar.returncode == 0
    assert "permitida=True" in avaliar.stdout
