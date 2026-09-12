"""ProviderManager: monitora chamadas, latencia, erros e capacidades."""
from __future__ import annotations

import time
from typing import Any

from nexora.providers.base import ProviderCapability


class ProviderManager:
    """Envolve providers e registra metricas de uso globais e por provider."""

    def __init__(self) -> None:
        self._fabricas: dict[str, Any] = {}
        self._chamadas: int = 0
        self._erros: int = 0
        self._tempo_total: float = 0.0
        self._ultimas_falhas: dict[str, str] = {}
        self._metricas_provider: dict[str, dict[str, Any]] = {}

    def registrar(self, nome: str, fabrica: Any) -> None:
        chave = nome.strip().lower()
        self._fabricas[chave] = fabrica
        self._metricas_provider.setdefault(
            chave,
            {"chamadas": 0, "sucessos": 0, "erros": 0, "tempo_total": 0.0},
        )

    def obter(self, nome: str) -> Any:
        chave = nome.strip().lower()
        fabrica = self._fabricas[chave]
        return fabrica() if callable(fabrica) else fabrica

    def executar(self, nome: str, prompt: str, **kwargs: Any):
        """Executa generate registrando latencia, sucesso e erro do provider."""
        chave = nome.strip().lower()
        provider = self.obter(nome)
        inicio = time.monotonic()
        self._chamadas += 1
        metricas = self._metricas_provider.setdefault(
            chave,
            {"chamadas": 0, "sucessos": 0, "erros": 0, "tempo_total": 0.0},
        )
        metricas["chamadas"] += 1
        try:
            resultado = provider.generate(prompt, **kwargs)
        except Exception as erro:
            self._erros += 1
            metricas["erros"] += 1
            self._ultimas_falhas[chave] = str(erro)
            raise
        else:
            metricas["sucessos"] += 1
            return resultado
        finally:
            decorrido = time.monotonic() - inicio
            self._tempo_total += decorrido
            metricas["tempo_total"] += decorrido

    def estatisticas(self) -> dict[str, Any]:
        """Resumo das metricas de uso globais."""
        total = self._chamadas
        return {
            "chamadas": total,
            "erros": self._erros,
            "latencia_media": (self._tempo_total / total) if total else None,
            "ultimas_falhas": dict(self._ultimas_falhas),
        }

    def estatisticas_provider(self, nome: str) -> dict[str, Any]:
        """Retorna apenas metricas medidas do provider solicitado.

        Os valores sao historicos do processo atual; nenhuma estimativa e criada.
        """
        chave = nome.strip().lower()
        metricas = self._metricas_provider.get(chave)
        if metricas is None:
            return {
                "chamadas": 0,
                "sucessos": 0,
                "erros": 0,
                "latencia_media": None,
                "taxa_sucesso": None,
                "taxa_erro": None,
                "ultima_falha": self._ultimas_falhas.get(chave),
            }
        total = int(metricas["chamadas"])
        sucessos = int(metricas["sucessos"])
        erros = int(metricas["erros"])
        return {
            "chamadas": total,
            "sucessos": sucessos,
            "erros": erros,
            "latencia_media": (float(metricas["tempo_total"]) / total) if total else None,
            "taxa_sucesso": (sucessos / total) if total else None,
            "taxa_erro": (erros / total) if total else None,
            "ultima_falha": self._ultimas_falhas.get(chave),
        }

    def estatisticas_providers(self) -> dict[str, dict[str, Any]]:
        """Retorna metricas medidas de todos os providers registrados."""
        return {nome: self.estatisticas_provider(nome) for nome in self.nomes()}

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

    def obter_capacidades(self, nome: str) -> ProviderCapability:
        """Retorna capacidades declaradas, sem inventar suporte ausente."""
        provider = self.obter(nome)
        capacidades = getattr(provider, "capabilities", None)
        if isinstance(capacidades, ProviderCapability):
            return capacidades
        return ProviderCapability()

    def nomes(self) -> list[str]:
        return list(self._fabricas.keys())

    def saudaveis(self) -> list[str]:
        return [n for n in self.nomes() if self.obter_healthcheck(n)["saudavel"]]
