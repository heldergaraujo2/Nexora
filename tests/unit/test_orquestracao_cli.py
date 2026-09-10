"""Testes da CLI (Fase 3)."""
import os
import subprocess
import sys
from pathlib import Path


def test_cli_info():
    raiz = Path(__file__).resolve().parents[2]
    env = {**os.environ, "PYTHONPATH": str(raiz / "src")}
    resultado = subprocess.run(
        [sys.executable, "-m", "nexora", "info"],
        capture_output=True,
        text=True,
        env=env,
        timeout=30,
    )
    assert resultado.returncode == 0
    assert "NEXORA" in resultado.stdout