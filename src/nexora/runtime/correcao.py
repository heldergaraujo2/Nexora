"""Aplica acoes corretivas (rerun, troca de provider,) registrando eventos."""
from __future__ import annotations

from typing import Any, Callable


class Corrector:


    def __init__(
        self,
        executar: Callable[[str], str],
        *,
        registrar: Callable[[str, dict[str, Any]], None] | None = None,
    ) -> None:

        self._executar = executar
        self._registrar = registrar


    def corregir(self, prompt: str, falha: Any) -> str:

        acao = falha.plano
        if self._registrar is not None:


            self._registrar("correcao", {"acao": acao, "motivo": falha.motivo})
        if acao in ("retry", "rerun"):


            return self._executar(prompt)
        if acao == "troca_provider":


            return self._executar(prompt)
        if acao == "ajuste_prompt":


            return self._executar(f"Tente novamente: {prompt}")
        return self._executar(prompt)
