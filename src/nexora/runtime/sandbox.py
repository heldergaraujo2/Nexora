"""Sandbox de execucao controlada (ADR-005)."""
from __future__ import annotations

import shlex
import subprocess
from typing import Any, Sequence

from ..governanca.permissoes import GerenciadorPermissoes, PedidoPermissao


class AcaoNegada(PermissionError):
    """Erro lancado quando uma acao fora da allowlist e tentada."""


class Sandbox:
    """Executa comandos por allowlist e, opcionalmente, por politica."""

    def __init__(self, permitidos: Sequence[str] = (), *, permissoes: GerenciadorPermissoes | None = None, solicitante: str = "sandbox") -> None:
        if not solicitante.strip():
            raise ValueError("solicitante deve ser uma string nao vazia")
        self._permitidos = set(permitidos)
        self._permissoes = permissoes
        self._solicitante = solicitante.strip()

    def permitir(self, comando: str) -> None:
        self._permitidos.add(comando.strip())

    def executar(self, comando: str, *, solicitante: str | None = None) -> dict[str, Any]:
        partes = shlex.split(comando)
        base = partes[0] if partes else ""
        if base not in self._permitidos:
            raise AcaoNegada(f"Comando nao permitido: {base}")

        if self._permissoes is not None:
            self._permissoes.exigir(PedidoPermissao(
                solicitante=(solicitante or self._solicitante).strip(),
                recurso="sandbox",
                acao=base,
                contexto={"comando_base": base},
            ))

        try:
            resultado = subprocess.run(partes, capture_output=True, text=True, timeout=30)
            return {"retorno": resultado.returncode, "saida": resultado.stdout, "erro": resultado.stderr}
        except subprocess.TimeoutExpired:
            return {"retorno": -1, "saida": "", "erro": "timeout"}
        except FileNotFoundError:
            return {"retorno": 127, "saida": "", "erro": "comando inexistente"}
