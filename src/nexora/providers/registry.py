"""Registro central de Providers de IA (ADR-003: desacoplar modelos e provedores.."""
from __future__ import annotations

from typing import Any


class ProviderDesconhecido(LookupError):
    """Erro lancado quando um provider nao esta registrado."""


class RegistryProviders:
    """Mapeia nomes de providers a suas fabricas."""

    def __init__(self) -> None:
        self._fabricas: dict[str, Any] = {}

    def registrar(self, nome: str, fabrica: Any) -> None:
        self._fabricas[nome.strip().lower()] = fabrica

    def obter(self, nome: str) -> Any:
        nome_chave = nome.strip().lower()
        if nome_chave not in self._fabricas:
            raise ProviderDesconhecido(nome_chave)
        return self._fabricas[nome_chave]

    def disponiveis(self) -> list[str]:
        return sorted(self._fabricas)


    def remover(self, nome: str) -> None:
        nome_chave = nome.strip().lower()
        self._fabricas.pop(nome_chave, None)