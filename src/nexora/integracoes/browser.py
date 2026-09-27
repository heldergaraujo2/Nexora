"""Contrato de Browser/Computer capability para adapters como browser-use."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Protocol


@dataclass(frozen=True)
class AcaoBrowser:
    tipo: str
    alvo: str = ""
    valor: str = ""
    metadados: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ResultadoBrowser:
    sucesso: bool
    saida: Any
    erro: str | None = None


class BrowserBackend(Protocol):
    nome: str
    def executar(self, acao: AcaoBrowser) -> ResultadoBrowser: ...


class BrowserBackendIndisponivel(RuntimeError):
    pass


class BrowserAdapter:
    """Adapter agnóstico; o backend real deve ser injetado explicitamente."""

    def __init__(self, backend: BrowserBackend | None = None) -> None:
        self._backend = backend

    @property
    def disponivel(self) -> bool:
        return self._backend is not None

    def executar(self, acao: AcaoBrowser) -> ResultadoBrowser:
        if self._backend is None:
            raise BrowserBackendIndisponivel("nenhum backend de browser configurado")
        return self._backend.executar(acao)
