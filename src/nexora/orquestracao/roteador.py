"""Roteamento de Provider por objetivo, alias e default (ADR-003)."""
from __future__ import annotations

import os

from nexora.providers.registry import RegistryProviders


class Roteador:
    """Seleciona o provider recomendado para um objetivo."""

    REGRAS = [
        (("groq", "ia", "llm", "chat", "escreva", "crie"), "groq"),
        (("teste", "test", "fake", "echo"), "fake"),
    ]

    def __init__(self, registry: RegistryProviders, default: str | None = None, manager: object | None = None) -> None:
        self.registry = registry
        self._default = default or os.environ.get("NEXORA_PROVIDER_PADRAO") or "fake"
        self._manager = manager

    def recomendar(self, objetivo: str) -> str:
        texto = objetivo.strip().lower()
        for palavras, provider in self.REGRAS:
            if any(p in texto for p in palavras):
                return provider
        return self._default

    def obter_provider(self, objetivo: str, alias: str | None = None):
        nome = self.recomendar(objetivo) if alias is None else alias
        if self._manager is None:
            return self.registry.obter(nome)()
        candidatos = self._manager.saudaveis()
        if nome in candidatos:
            candidatos.remove(nome)
            candidatos.insert(0, nome)
        for nome_cand in candidatos:
            return self._manager.obter(nome_cand)
        raise RuntimeError("nenhum provider saudavel disponivel")
