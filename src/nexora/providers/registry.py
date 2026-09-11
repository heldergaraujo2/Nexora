"""Registro central de Providers de IA (ADR-003: desacoplar modelos e provedores.."""
from __future__ import annotations

from typing import Any


class ProviderDesconhecido(LookupError):
    """Erro lancado quando um provider nao esta registrado."""


class RegistryProviders:
    """Mapeia nomes de providers a suas fabricas."""

    def __init__(self) -> None:
        self._fabricas: dict[str, Any] = {}
        self._prioridades: dict[str, int] = {}

    def registrar(self, nome: str, fabrica: Any, prioridade: int =  0) -> None:
        self._fabricas[nome.strip().lower()] = fabrica
        self._prioridades[nome.strip().lower()] = prioridade

    def obter(self, nome: str) -> Any:
        nome_chave = nome.strip().lower()
        if nome_chave not in self._fabricas:
            raise ProviderDesconhecido(nome_chave)
        return self._fabricas[nome_chave]

    def disponiveis(self) -> list[str]:
        return sorted(self._fabricas)


    def prioridade(self, nome: str) -> int:
        return self._prioridades.get(nome.strip().lower(),  0)

    def listar_por_capacidade(self, tool_calling: bool | None = None, streaming: bool | None = None) -> list[str]:
        """Retorna nomes de providers que atendem as capacidades exigidas."""
        resultado = []
        for chave, fabrica in self._fabricas.items():
            if self.__provider_atende(fabrica, tool_calling=tool_calling, streaming=streaming):
                resultado.append(chave)
        return resultado

    @staticmethod
    def __provider_atende(fabrica, tool_calling, streaming) -> bool:
        try:
            instancia = fabrica() if callable(fabrica) else fabrica
            caps = getattr(instancia, "capabilities", None)
        except Exception:
            return False
        if caps is None:
            return True
        if tool_calling is not None and caps.tool_calling != tool_calling:
            return False
        if streaming is not None and caps.streaming != streaming:
            return False
        return True

    def nomes_por_prioridade(self) -> list[str]:
        """Nomes ordenados por prioridade crescente, desempatando por nome."""
        return sorted(self._fabricas, key=lambda chave: (self._prioridades.get(chave,  0), chave))

    def remover(self, nome: str) -> None:
        nome_chave = nome.strip().lower()
        self._fabricas.pop(nome_chave, None)