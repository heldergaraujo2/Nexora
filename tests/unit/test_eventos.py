"""Testes do EventStore append-only JSON."""
from pathlib import Path

from nexora.runtime.eventos import EventStore


def test_registrar_e_ler_evento(tmp_path: Path) -> None:
    store = EventStore(tmp_path / "eventos.jsonl")
    evento = store.registrar("teste", {"valor": 1}, origem="pytest")

    assert evento["tipo"] == "teste"
    assert evento["dados"]["valor"] == 1
    assert "carimbo" in evento

    eventos = store.ler()
    assert len(eventos) == 1
    assert eventos[0]["correlacao"] is None


def test_append_only_preserva_ordem(tmp_path: Path) -> None:
    store = EventStore(tmp_path / "eventos.jsonl")
    store.registrar("a", {"n": 1})
    store.registrar("b", {"n": 2})
    store.registrar("c", {"n": 3})

    eventos = store.ler(limite=2)
    assert [e["tipo"] for e in eventos] == ["b", "c"]


def test_eventos_vazios(tmp_path: Path) -> None:

    store = EventStore(tmp_path / "eventos.jsonl")
    assert store.ler() == []