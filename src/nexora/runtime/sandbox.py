"""Sandbox de execucao controlada (ADR-005: acoes auditadas, permitidas por allowlist.."""
from __future__ import annotations

import shlex
import subprocess
from typing import Any, Sequence


class AcaoNegada(PermissionError):
    """Erro lancado quando uma acao fora da allowlist e tentada."""


class Sandbox:
    """Executa comandos de forma restrita por allowlist."""

    def __init__(self, permitidos: Sequence[str] = ()) -> None:
        self._permitidos = set(permitidos)

    def permitir(self, comando: str) -> None:
        self._permitidos.add(comando.strip())


    def executar(self, comando: str) -> dict[str, Any]:
        base = shlex.split(comando)[0] if comando.strip() else ""
        if base not in self._permitidos:

            raise AcaoNegada(f"Comando nao permitido: {base}")
        try:
            resultado = subprocess.run(
                shlex.split(comando),
                capture_output=True,
                text=True,
                timeout=30,
            )
            return {
                "retorno": resultado.returncode,
                "saida": resultado.stdout,
                "erro": resultado.stderr,
            }
        except subprocess.TimeoutExpired:
            return {"retorno": -1, "saida": "", "erro": "timeout"}
        except FileNotFoundError:
            return {"retorno": 127, "saida": "", "erro": "comando inexistente"}