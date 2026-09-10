"""Interface base tipada de Provider."""
from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, AsyncIterator

class ProviderError(Exception):
    """Erro padronizado do provider."""

class ProviderIndisponivel(ProviderError):
    """Provider nao respondeu ou esta fora do ar."""

class ProviderSemCredencial(ProviderError):
    """Credencial de acesso ausente ou invalida."""

class ProviderCapability:
    """Capacidades declaradas do provider."""
    def __init__(self, *, tool_calling: bool = False, streaming: bool = False, max_context_tokens: int = 0) -> None:
        self.tool_calling = tool_calling
        self.streaming = streaming
        self.max_context_tokens = max_context_tokens

@dataclass
class GenerationResult:
    """Resposta completa de uma geracao."""
    text: str
    tool_calls: list[dict[str, Any]] = field(default_factory=list)
    raw: Any = None

@dataclass
class StreamChunk:
    """Fragmento de uma resposta em streaming."""
    delta: str = ""
    done: bool = False
    tool_calls: list[dict[str, Any]] = field(default_factory=list)

class Provider(ABC):
    """Contrato minimo que todo provider deve cumprir (ADR-006)."""
    def __init__(self, name: str, capabilities: ProviderCapability) -> None:
        self.name = name
        self.capabilities = capabilities

    @abstractmethod
    def generate(self, prompt: str, **kwargs: Any) -> GenerationResult:
        """Gera uma resposta completa."""

    def stream(self, prompt: str, **kwargs: Any) -> AsyncIterator[StreamChunk]:
        raise NotImplementedError("stream opcional")
        yield StreamChunk()  # pragma: no cover

    def saudavel(self) -> bool:
        """Verifica se o provider esta disponivel."""
        try:
            self.generate("[saudavel]")
            return True
        except ProviderError:
            return False

    def fechar(self) -> None:
        """Libera recursos do provider (no-op por padrao)."""
