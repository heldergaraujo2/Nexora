"""Testes do LogJson estruturado."""
from pathlib import Path

from nexora.runtime.logs import LogJson


def test_log_json_escreve_linha(tmp_path: Path) -> None:
    log = LogJson(tmp_path / "app.jsonl")
    log.escrever("iniciou", dados={"modo": "teste"})

    linhas = (tmp_path / "app.jsonl").read_text(encoding="utf-8").strip().splitlines()
    assert len(linhas) ==1
    assert "iniciou" in linhas[0]


def test_log_json_respeita_nivel(tmp_path: Path) -> None:
    log = LogJson(tmp_path / "app.jsonl", nivel=30)
    log.escrever("debug", nivel=10)
    log.escrever("erro", nivel=40)

    linhas = (tmp_path / "app.jsonl").read_text(encoding="utf-8").strip().splitlines()
    assert len(linhas) ==1
    assert "erro" in linhas[0]