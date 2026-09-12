"""Provider local Ollama para a arquitetura model-agnostica da NEXORA."""
from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from typing import Any

from nexora.providers.base import (
    GenerationResult,
    Provider,
    ProviderCapability,
    ProviderIndisponivel,
)


class ProviderOllama(Provider):
    """Cliente Ollama via HTTP stdlib, sem dependencias externas."""

    URL_PADRAO = "http://localhost:11434"
    MODELO_PADRAO = "qwen2.5-coder:7b-instruct-q4_K_M"

    def __init__(self, url: str | None = None, modelo: str | None = None, timeout: int = 120) -> None:
        base_url = url or os.environ.get("NEXORA_OLLAMA_URL") or self.URL_PADRAO
        self._url = base_url.rstrip("/")
        self._modelo = modelo or os.environ.get("NEXORA_OLLAMA_MODEL") or self.MODELO_PADRAO
        self._timeout = timeout
        super().__init__("ollama", ProviderCapability(tool_calling=False, streaming=False, max_context_tokens=32768))

    @property
    def modelo(self) -> str:
        return self._modelo

    @property
    def url(self) -> str:
        return self._url

    def generate(self, prompt: str, **kwargs: Any) -> GenerationResult:
        payload: dict[str, Any] = {
            "model": self._modelo,
            "messages": [{"role": "user", "content": prompt}],
            "stream": False,
        }
        if "temperature" in kwargs:
            payload["options"] = {"temperature": kwargs["temperature"]}
        if kwargs.get("system"):
            payload["messages"].insert(0, {"role": "system", "content": kwargs["system"]})
        dados = self._post("/api/chat", payload)
        mensagem = dados.get("message") or {}
        return GenerationResult(text=mensagem.get("content") or "", tool_calls=mensagem.get("tool_calls", []), raw=dados)

    def listar_modelos(self) -> dict[str, Any]:
        """Lista modelos instalados sem executar inferencia."""
        return self._get("/api/tags")

    def saudavel(self) -> bool:
        try:
            self.listar_modelos()
            return True
        except ProviderIndisponivel:
            return False

    def _post(self, caminho: str, payload: dict[str, Any]) -> dict[str, Any]:
        corpo = json.dumps(payload).encode("utf-8")
        pedido = urllib.request.Request(f"{self._url}{caminho}", data=corpo, headers={"Content-Type": "application/json"}, method="POST")
        try:
            with urllib.request.urlopen(pedido, timeout=self._timeout) as resp:
                return json.loads(resp.read().decode("utf-8") or "{}")
        except urllib.error.HTTPError as exc:
            raise ProviderIndisponivel(f"Ollama HTTP {exc.code}") from exc
        except (urllib.error.URLError, TimeoutError, OSError, json.JSONDecodeError) as exc:
            raise ProviderIndisponivel(f"Ollama indisponivel: {exc}") from exc

    def _get(self, caminho: str) -> dict[str, Any]:
        pedido = urllib.request.Request(f"{self._url}{caminho}", method="GET")
        try:
            with urllib.request.urlopen(pedido, timeout=self._timeout) as resp:
                return json.loads(resp.read().decode("utf-8") or "{}")
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError, OSError, json.JSONDecodeError) as exc:
            raise ProviderIndisponivel(f"Ollama indisponivel: {exc}") from exc

    def fechar(self) -> None:
        pass
