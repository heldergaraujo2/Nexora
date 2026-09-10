"""Registro central de ferramentas executaveis (ADR-008.."""
from __future__ import annotations

from typing import Any, Callable


class Ferramenta:
    """Ferramenta registrada com nome, descricao e executor."""

    def __init__(
        self,
        nome: str,
        descricao: str,
        executar: Callable[[dict[str, Any]], Any],
    ) -> None:
        self.nome = nome.strip()
        self.descricao = descricao.strip()
        self._executar = executar

    def executar(self, parametros: dict[str, Any]) -> Any:
        return self._executar(parametros)


class RegistryFerramentas:
    """Mapeia nomes de ferramentas a instancias."""

    def __init__(self) -> None:
        self._ferramentas: dict[str, Ferramenta] = {}

    def registrar(self, ferramenta: Ferramenta) -> None:
        self._ferramentas[ferramenta.nome] = ferramenta

    def obter(self, nome: str) -> Ferramenta:
        return self._ferramentas[nome.strip()]

    def executar(self, nome: str, parametros: dict[str, Any]) -> Any:
        return self.obter(nome).executar(parametros)

    def nomes(self) -> list[str]:
        return sorted(self._ferramentas)