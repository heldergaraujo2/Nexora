"""Roteamento determinístico entre providers e modelos."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from nexora.providers.manager import ProviderManager
from nexora.providers.modelos import PerfilCapacidadeModelo
from nexora.runtime.hardware import PerfilHardware
from nexora.runtime.modelos import avaliar_modelo


@dataclass(frozen=True)
class CandidatoRoteamento:
    provider: str
    modelo: str
    score: float
    adequado: bool
    motivos: tuple[str, ...] = ()


class RoteadorInteligente:
    """Escolhe provider/modelo sem executar a tarefa."""

    def __init__(self, manager: ProviderManager) -> None:
        self._manager = manager

    def selecionar(
        self,
        candidatos: list[dict[str, Any]],
        hardware: PerfilHardware,
        *,
        tarefa: str = "general",
        contexto_necessario: int = 0,
        exigir_tool_calling: bool = False,
        exigir_streaming: bool = False,
        exigir_provider_saudavel: bool = False,
    ) -> list[CandidatoRoteamento]:
        """Ordena candidatos por adequacao, capacidades e score deterministico.

        A funcao somente decide. Ela nao executa o provider nem a tarefa.
        Capacidades nao declaradas sao tratadas como ausentes.
        """
        avaliados: list[CandidatoRoteamento] = []
        for candidato in candidatos:
            provider = str(candidato.get("provider", "")).strip().lower()
            modelo = str(candidato.get("modelo", "")).strip()
            perfil = candidato.get("perfil")
            if not provider or not modelo or not isinstance(perfil, PerfilCapacidadeModelo):
                continue
            if provider not in self._manager.nomes():
                continue

            motivos: list[str] = []
            capacidades = self._manager.obter_capacidades(provider)
            adequado = True
            if exigir_tool_calling and not capacidades.tool_calling:
                adequado = False
                motivos.append("provider_sem_tool_calling")
            if exigir_streaming and not capacidades.streaming:
                adequado = False
                motivos.append("provider_sem_streaming")
            if contexto_necessario > capacidades.max_context_tokens > 0:
                adequado = False
                motivos.append("provider_contexto_insuficiente")
            if exigir_provider_saudavel and not self._manager.obter_healthcheck(provider)["saudavel"]:
                adequado = False
                motivos.append("provider_indisponivel")

            avaliacao = avaliar_modelo(
                modelo,
                perfil,
                hardware,
                tarefa=tarefa,
                contexto_necessario=contexto_necessario,
            )
            if not avaliacao.adequado:
                adequado = False
            motivos.extend(avaliacao.motivos)
            score = avaliacao.score if adequado else -100.0
            avaliados.append(CandidatoRoteamento(provider, modelo, score, adequado, tuple(motivos)))

        return sorted(avaliados, key=lambda item: (-item.adequado, -item.score, item.provider, item.modelo))
