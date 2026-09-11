"""Testes do Evolution Engine (Fase 10)."""
from __future__ import annotations

from pathlib import Path

from nexora.evolucao import Aprendizado, RegistroAprendizados, RecomendadorEvolucao


def test_registro_registra_aprendizado(tmp_path: Path) -> None:
    registro = RegistroAprendizados(tmp_path / "a.jsonl")
    aprendizado = Aprendizado(tarefa="t1", melhor_variante="vA", taxa_sucesso=1.0, total_execucoes=2)
    registro.registrar(aprendizado)
    itens = registro.listar()
    assert len(itens) == 1
    assert itens[0].tarefa == "t1"
    assert itens[0].melhor_variante == "vA"
import os
import subprocess
import sys


def test_registro_lista_na_ordem(tmp_path: Path) -> None:
    registro = RegistroAprendizados(tmp_path / "a.jsonl")
    for nome in ("a", "b", "c"):
        registro.registrar(Aprendizado(tarefa="t", melhor_variante=nome, taxa_sucesso=0.5, total_execucoes=1))
    assert [a.melhor_variante for a in registro.listar()] == ["a", "b", "c"]

def test_registro_resumir(tmp_path: Path) -> None:
    registro = RegistroAprendizados(tmp_path / "a.jsonl")
    registro.registrar(Aprendizado(tarefa="t", melhor_variante="vA", taxa_sucesso=1.0, total_execucoes=1))
    resumo = registro.resumir()
    assert resumo["total"] == 1
    assert resumo["por_variante"]["vA"]["taxa_media"] == 1.0

def test_evoluir_gera_e_recomenda(tmp_path: Path) -> None:
    registro = RegistroAprendizados(tmp_path / "a.jsonl")
    recomendador = RecomendadorEvolucao(registro)
    experimento = {
        "experimento": "exp1",
        "tarefa": "t1",
        "resultados": [
            {"indice": 1, "variante": "vA", "sucesso": True, "tentativas": 1, "saida": "ok"},
            {"indice": 2, "variante": "vB", "sucesso": False, "tentativas": 3, "saida": "x"},
        ],
    }
    aprendizado = recomendador.evoluir(experimento)
    assert aprendizado.melhor_variante == "vA"
    assert aprendizado.taxa_sucesso == 0.5
    reposto = recomendador.recomendar("t1")
    assert reposto is not None
    assert reposto.melhor_variante == "vA"
    assert recomendador.recomendar("nao_existe") is None

def test_cli_evoluir(tmp_path: Path) -> None:
    env = {**os.environ, "PYTHONPATH": str(Path.cwd() / "src")}
    resultado = subprocess.run(
        [sys.executable, "-m", "nexora", "evoluir", "recomendar", "--tarefa", "t1", "--arquivo", str(tmp_path / "a.jsonl")],
        capture_output=True,
        text=True,
        env=env,
        timeout=30,
    )
    assert resultado.returncode == 0
    assert "aprendizado" in resultado.stdout or resultado.stdout == ""
