"""Testes do Long-Term Autonomy (Fase  16)."""
from __future__ import annotations

from pathlib import Path

from nexora.autonomia.registro import MetaLongoPrazo, RegistroAutonomia


def test_meta_campos_padrao() -> None:
    meta = MetaLongoPrazo(nome="meta-nexora")
    assert meta.nome == "meta-nexora"
    assert meta.status == "ativa"
    assert meta.descricao == ""


def test_autonomia_definir_e_listar(tmp_path: Path) -> None:
    reg = RegistroAutonomia(tmp_path / "autonomia.jsonl")
    reg.definir(nome="meta-1", descricao="primeira")
    reg.definir(nome="meta-2", descricao="segunda")
    metas = reg.listar()
    assert len(metas) ==  2
    assert metas[0].nome == "meta-1"


def test_autonomia_atualizar_status(tmp_path: Path) -> None:
    reg = RegistroAutonomia(tmp_path / "autonomia.jsonl")
    reg.definir(nome="meta-1")
    vid = reg.listar()[0].id
    assert reg.atualizar_status(vid, "concluida")is True
    assert reg.listar()[0].status == "concluida"


def test_autonomia_atualizar_id_inexistente(tmp_path: Path) -> None:
    reg = RegistroAutonomia(tmp_path / "autonomia.jsonl")
    reg.definir(nome="meta-1")
    assert reg.atualizar_status("nao-existe", "concluida")is False
    assert reg.listar()[0].status == "ativa"


def test_cli_autonomia_definir_e_resumir(tmp_path: Path) -> None:
    import os
    import subprocess
    import sys
    env = {**os.environ, "PYTHONPATH": str(Path.cwd() / "src")}
    caminho = tmp_path / "autonomia.jsonl"
    add_cmd = subprocess.run(
        [sys.executable, "-m", "nexora", "autonomia", "definir", "--nome", "meta-x", "--arquivo", str(caminho)],
        capture_output=True, text=True, env=env, timeout=30,
    )
    assert add_cmd.returncode ==  0
    res_cmd = subprocess.run(
        [sys.executable, "-m", "nexora", "autonomia", "resumir", "--arquivo", str(caminho)],
        capture_output=True, text=True, env=env, timeout=30,
    )
    assert res_cmd.returncode ==  0
    assert "ativa" in res_cmd.stdout


def test_autonomia_resumir_por_status(tmp_path: Path) -> None:
    reg = RegistroAutonomia(tmp_path / "autonomia.jsonl")
    reg.definir(nome="a", status="concluida")
    reg.definir(nome="b", status="concluida")
    resumo = reg.resumir()
    assert resumo["concluida"] ==  2
