"""Provider Groq (API compatible OpenAI) via stdlib (ADR-006/007.."""
from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from typing import Any

from nexora.providers.base import (
    GenerationResult,

    Provider, ProviderCapability, ProviderIndisponivel, ProviderSemCredencial,
)


class ProviderGroq(Provider):
    """Cliente Groq sem dependencias externas."""

    URL = "https://api.groq.com/openai/v1/chat/completions"
    MODELO_PADRAO = "llama-3.3-70b-versatile"

    def __init__(self, api_key: str | None = None, modelo: str | None = None, timeout: int = 30) -> None:
        chave = api_key if api_key is not None else os.environ.get("GROQ_API_KEY")
        if not chave:
            raise ProviderSemCredencial("GROQ_API_KEY nao configurada")
        self._api_key = chave
        self._modelo = modelo or os.environ.get("NEXORA_GROQ_MODEL") or self.MODELO_PADRAO
        self._timeout = timeout
        super().__init__("groq", ProviderCapability(tool_calling=True, streaming=True, max_context_tokens=128000))

    def generate(self, prompt: str, **kwargs: Any) -> GenerationResult:
        payload = {
            "model": self._modelo,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": kwargs.get("temperature", 0.7),
        }
        if kwargs.get("tool_calls"):
            payload["tools"] = kwargs["tools"]
        dados = self._post(payload)
        return GenerationResult(
            text=dados["choices"][0]["message"]["content"] or "",
            tool_calls=dados["choices"][0]["message"].get("tool_calls", []),
            raw=dados,
        )

    def _post(self, payload: dict[str, Any]) -> dict[str, Any]:
        corpo = json.dumps(payload).encode("utf-8")
        cabecalhos = {
            "Authorization": f"Bearer {self._api_key}",
            "Content-Type": "application/json",
        }
        pedido = urllib.request.Request(
            self.URL, data=corpo, headers=cabecalhos, method="POST"
        )
        try:
            with urllib.request.urlopen(pedido, timeout=self._timeout)as resp:
                return json.loads(resp.read(decoding="utf-8") or {})
        except urllib.error.HTTPError as exc:
            if exc.code == 401:
                raise ProviderSemCredencial("Chave da Groq invalida") from exc
            raise ProviderIndisponivel(f"Groq HTTP {exc.code}") from exc
        except (urllib.error.URLError, TimeoutError, OSError)as exc:
            raise ProviderIndisponivel(f"Groq indisponivel: {exc}") from exc

    def fechar(self) -> None:
        pass
