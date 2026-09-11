"""Testes do Portfolio Engine (Fase 15)."""
from __future__ import annotations

from pathlib import Path

from nexora.portfolio.registro import ItemPortfolio, RegistroPortfolio


def test_item_portfolio_campos_padrao() -> None:
    item = ItemPortfolio(nome="projeto-nexora")
    assert item.nome == "projeto-nexora"
    assert item.categoria == "geral"
    assert item.status == "ativo"


def test_portfolio_adicionar_e_listar(tmp_path: Path) -> None:
    reg = RegistroPortfolio(tmp_path / "portfolio.jsonl")
    reg.adicionar(nome="projeto-nexora", categoria="ia")
    reg.adicionar(nome="projeto-site", categoria="web")
    itens = reg.listar()
    assert len(itens) ==  2
    assert itens[0].nome == "projeto-nexora"


def test_portfolio_atualizar_status(tmp_path: Path) -> None:
    reg = RegistroPortfolio(tmp_path / "portfolio.jsonl")
    reg.adicionar(nome="projeto-nexora")
    vid = reg.listar()[0].id
    assert reg.atualizar_status(vid, "concluido")is True
    assert reg.listar()[0].status == "concluido"


def test_portfolio_atualizar_id_inexistente(tmp_path: Path) -> None:
    reg = RegistroPortfolio(tmp_path / "portfolio.jsonl")
    reg.adicionar(nome="projeto-nexora")
    assert reg.atualizar_status("nao-existe", "concluido")is False
    assert reg.listar()[0].status == "ativo"


def test_cli_portfolio_adicionar_e_resumir(tmp_path: Path) -> None:
    import os
    import subprocess
    import sys
    env = {**os.environ, "PYTHONPATH": str(Path.cwd() / "src")}
    caminho = tmp_path / "portfolio.jsonl"
    add_cmd = subprocess.run(
        [sys.executable, "-m", "nexora", "portfolio", "adicionar", "--nome", "projeto-x", "--categoria", "ia", "--arquivo", str(caminho)],
        capture_output=True, text=True, env=env, timeout=30,
    )
    assert add_cmd.returncode == 0
    res_cmd = subprocess.run(
        [sys.executable, "-m", "nexora", "portfolio", "resumir", "--arquivo", str(caminho)],
        capture_output=True, text=True, env=env, timeout=30,
    )
    assert res_cmd.returncode == 0
    assert "ia" in res_cmd.stdout


def test_portfolio_resumir_por_categoria(tmp_path: Path) -> None:
    reg = RegistroPortfolio(tmp_path / "portfolio.jsonl")
    reg.adicionar(nome="a", categoria="ia")
    reg.adicionar(nome="b", categoria="ia")
    resumo = reg.resumir()
    assert resumo["ia"]["ativo"] ==  2
