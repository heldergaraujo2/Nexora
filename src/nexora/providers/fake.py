"""Provider fake deterministico para testes (ADR-006.."""
from __future__ import annotations

from typing import Any

from nexora.providers.base import GenerationResult, Provider, ProviderCapability


class FakeProvider(Provider):
    """Provider deterministico que ecoa o prompt ou devolve texto fixo."""

    def __init__(self, respostas: dict[str, str] | None = None) -> None:
        super().__init__("fake", ProviderCapability(tool_calling=True, streaming=False))
        self.respostas = dict(respostas or {})
        self.chamadas: list[dict[str, Any]] = []

    def generate(self, prompt: str, **kwargs: Any) -> GenerationResult:
        self.chamadas.append({"prompt": prompt, "kwargs": kwargs})
        texto = self.respostas.get(prompt, f"[fake:{prompt}]")
        return GenerationResult(text=texto, tool_calls=[])

    def registrar_resposta(self, prompt: str, resposta: str) -> None:
        self.respostas[prompt] = resposta

    def saudavel(self) -> bool:
        return True

    def fechar(self) -> None:
        self.chamadas.clear()