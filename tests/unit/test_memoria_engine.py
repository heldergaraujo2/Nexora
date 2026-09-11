"""Testes do Memory Engine (Fase 13)."""
from __future__ import annotations

from pathlib import Path

from nexora.memoria.registro import ItemMemoria, RegistroMemorias


def test_item_campos_padrao() -> None:
    item = ItemMemoria(chave="perfil", conteudo="joao")
    assert item.chave == "perfil"
    assert item.conteudo == "joao"
    assert item.escopo == "global"


def test_memoria_lembrar_e_listar(tmp_path: Path) -> None:
    reg = RegistroMemorias(tmp_path / "mem.jsonl")
    reg.lembrar(chave="perfil", conteudo="ana")
    reg.lembrar(chave="preferencia", conteudo="rust", escopo="dev")
    itens = reg.listar()
    assert len(itens) == 2
    assert itens[0].chave == "perfil"


def test_memoria_buscar_ultima_ocorrencia_vence(tmp_path: Path) -> None:
    reg = RegistroMemorias(tmp_path / "mem.jsonl")
    reg.lembrar(chave="perfil", conteudo="ana")
    reg.lembrar(chave="perfil", conteudo="bia")
    assert reg.buscar(chave="perfil") == "bia"


def test_memoria_buscar_fallbacks_para_escopo_global(tmp_path: Path) -> None:
    reg = RegistroMemorias(tmp_path / "mem.jsonl")
    reg.lembrar(chave="perfil", conteudo="ana", escopo="dev")
    reg.lembrar(chave="perfil", conteudo="bia", escopo="global")
    assert reg.buscar(chave="perfil", escopo="dev") == "bia"


def test_memoria_resumir_por_escopo(tmp_path: Path) -> None:
    reg = RegistroMemorias(tmp_path / "mem.jsonl")
    reg.lembrar(chave="perfil", conteudo="ana")
    reg.lembrar(chave="preferencia", conteudo="rust", escopo="dev")
    resumo = reg.resumir()
    assert resumo["global"] ==  1
    assert resumo["dev"] ==  1


def test_cli_memoria_lembrar_e_buscar(tmp_path: Path) -> None:
    import os
    import subprocess
    import sys
    env = {**os.environ, "PYTHONPATH": str(Path.cwd() / "src")}
    caminho = tmp_path / "mem.jsonl"
    lembrar = subprocess.run(
        [sys.executable, "-m", "nexora", "memoria", "lembrar", "--chave", "perfil", "--conteudo", "ana", "--arquivo", str(caminho)],
        capture_output=True, text=True, env=env, timeout=30,
    )
    assert lembrar.returncode == 0
    buscar = subprocess.run(
        [sys.executable, "-m", "nexora", "memoria", "buscar", "--chave", "perfil", "--arquivo", str(caminho)],
        capture_output=True, text=True, env=env, timeout=30,
    )
    assert buscar.returncode == 0
    assert "valor=ana" in buscar.stdout
