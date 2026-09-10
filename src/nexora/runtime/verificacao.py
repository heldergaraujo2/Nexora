"""Verificacao de resultados e saidas (ADR-012: agente verifica o propio trabalho.."""
from __future__ import annotations

from typing import Any, Callable


class Verificacao:
    """Aplica criterios verificaveis a saida de uma execucao."""

    def __init__(self, criterios: list[Callable[[dict[str, Any]], bool]] | None = None) -> None:
        self._criterios = criterios if criterios is not None else []


    def adicionar(self, criterio: Callable[[dict[str, Any]], bool]) -> None:
        self._criterios.append(criterio)


    def verificar(self, contexto: dict[str, Any]) -> bool:
        return all(criterio(contexto) for criterio in self._criterios)


def texto_nao_vazio(contexto: dict[str, Any]) -> bool:
    """Criterio que falha quando a saida e vazia ou somente espacos."""

    saida = contexto.get("saida", "")
    return isinstance(saida, str) and bool(saida.strip())


def sem_erros(contexto: dict[str, Any]) -> bool:
    """Criterio que falha quando ha um erro registrado no contexto."""

    return contexto.get("erro") is None