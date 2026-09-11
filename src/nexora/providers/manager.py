"""ProviderManager: monitora chamadas, latencia e erros dos providers."""
from __future__ import annotations

import time
from typing import Any


class ProviderManager:
    """Envolve providers e registra metricas de uso."""

    def __init__(self) -> None:
        self._fabricas: dict[str, Any] = {}
        self._chamadas: int =  0
        self._erros: int =  0
        self._tempo_total: float =  0.0
        self._ultimas_falhas: dict[str, str] = {}

    def registrar(self, nome: str, fabrica: Any) -> None:
        self._fabricas[nome.strip().lower()] = fabrica

    def obter(self, nome: str) -> Any:
        chave = nome.strip().lower()
        fabrica = self._fabricas[chave]
        return fabrica() if callable(fabrica) else fabrica

    def executar(self, nome: str, prompt: str, **kwargs: Any):
        """Executa generate do provider registrando latencia e erros."""
        chave = nome.strip().lower()
        provider = self.obter(nome)
        inicio = time.monotonic()
        self._chamadas += 1
        try:
            resultado = provider.generate(prompt, **kwargs)
        except Exception as erro:
            self._erros += 1
            self._ultimas_falhas[chave] = str(erro)
            raise
        finally:
            self._tempo_total += time.monotonic() - inicio
        return resultado

    def estatisticas(self) -> dict[str, Any]:
        """Resumo das metricas de uso."""
        total = self._chamadas
        return {
            "chamadas": total,
            "erros": self._erros,
            "latencia_media": (self._tempo_total / total) if total else None,
            "ultimas_falhas": dict(self._ultimas_falhas),
        }

    def obter_healthcheck(self, nome: str) -> dict[str, Any]:
        """Healthcheck detalhado sem necessariamente instanciar o provider."""
        chave = nome.strip().lower()
        try:
            provider = self.obter(nome)
            saudavel = provider.saudavel()
            return {"saudavel": saudavel, "motivo": None, "ultima_falha": self._ultimas_falhas.get(chave, None)}
        except Exception as erro:
            self._ultimas_falhas[chave] = str(erro)
            return {"saudavel": False, "motivo": str(erro), "ultima_falha": str(erro)}

    def nomes(self) -> list[str]:
        return list(self._fabricas.keys())

    def saudaveis(self) -> list[str]:
        return [n for n in self.nomes() if self.obter_healthcheck(n)["saudavel"]]
