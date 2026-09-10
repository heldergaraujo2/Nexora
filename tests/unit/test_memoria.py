"""Testes da Memoria JSON versionada."""
from pathlib import Path

from nexora.runtime.memoria import Memoria


def test_memoria_gravar_e_ler(tmp_path: Path) -> None:
    memo = Memoria(tmp_path / "memoria.json")
    registro = memo.gravar("observacao", {"t": 1})

    assert registro["tipo"] == "observacao"
    assert registro["versao"] ==1
    assert "carimbo" in registro

    leituras = memo.ler()
    assert len(leituras) ==1
    assert leituras[0]["origem"] == "nexora"


def test_memoria_preserva_ordem(tmp_path: Path) -> None:
    memo = Memoria(tmp_path / "memoria.json")
    memo.gravar("a")
    memo.gravar("b")

    assert [e["tipo"] for e in memo.ler()] == ["a", "b"]


def test_memoria_vazia(tmp_path: Path) -> None:
    memo = Memoria(tmp_path / "memoria.json")
    assert memo.ler() == []