"""Testes do Resource Management (Fase 14)."""
from __future__ import annotations

from pathlib import Path

from nexora.recursos.registro import Recurso, RegistroRecursos


def test_recurso_campos_padrao() -> None:
    recurso = Recurso(tipo="tokens", quantidade=10.0, executor="groq")
    assert recurso.tipo == "tokens"
    assert recurso.quantidade == 10.0
    assert recurso.executor == "groq"
    assert recurso.escopo == "global"


def test_recursos_registrar_e_listar(tmp_path: Path) -> None:
    reg = RegistroRecursos(tmp_path / "recursos.jsonl")
    reg.registrar(tipo="tokens", quantidade=10.0, executor="groq")
    reg.registrar(tipo="cpu", quantidade=2.0, executor="fake")
    itens = reg.listar()
    assert len(itens) == 2
    assert itens[0].tipo == "tokens"


def test_recursos_resumir_por_tipo_e_executor(tmp_path: Path) -> None:
    reg = RegistroRecursos(tmp_path / "recursos.jsonl")
    reg.registrar(tipo="tokens", quantidade=100.0, executor="groq")
    reg.registrar(tipo="tokens", quantidade=50.0, executor="groq")
    reg.registrar(tipo="cpu", quantidade=2.0, executor="fake")
    resumo = reg.resumir()
    assert resumo["tokens"]["groq"] ==  150.0
    assert resumo["cpu"]["fake"] ==  2.0


def test_recursos_vazio(tmp_path: Path) -> None:
    reg = RegistroRecursos(tmp_path / "recursos.jsonl")
    assert reg.resumir() == {}
    assert reg.listar() == []


def test_cli_recursos_registrar_e_resumir(tmp_path: Path) -> None:
    import os
    import subprocess
    import sys
    env = {**os.environ, "PYTHONPATH": str(Path.cwd() / "src")}
    caminho = tmp_path / "recursos.jsonl"
    registrar = subprocess.run(
        [sys.executable, "-m", "nexora", "recursos", "registrar", "--tipo", "tokens", "--quantidade", "100", "--executor", "groq", "--arquivo", str(caminho)],
        capture_output=True, text=True, env=env, timeout=30,
    )
    assert registrar.returncode == 0
    resumir = subprocess.run(
        [sys.executable, "-m", "nexora", "recursos", "resumir", "--arquivo", str(caminho)],
        capture_output=True, text=True, env=env, timeout=30,
    )
    assert resumir.returncode == 0
    assert "tokens" in resumir.stdout



def test_recurso_metadados_opcionais(tmp_path: Path) -> None:
    reg = RegistroRecursos(tmp_path / "recursos.jsonl")
    reg.registrar(tipo="tokens", quantidade=5.0, executor="groq", metadados={"projeto": "nexora"})
    itens = reg.listar()
    assert itens[0].metadados == {"projeto": "nexora"}

