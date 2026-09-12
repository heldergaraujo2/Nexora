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
    ) -> list[CandidatoRoteamento]:
        avaliados: list[CandidatoRoteamento] = []
        for candidato in candidatos:
            provider = str(candidato.get("provider", "")).strip().lower()
            modelo = str(candidato.get("modelo", "")).strip()
            perfil = candidato.get("perfil")
            if not provider or not modelo or not isinstance(perfil, PerfilCapacidadeModelo):
                continue
            if provider not in self._manager.nomes():
                continue
            avaliacao = avaliar_modelo(
                modelo,
                perfil,
                hardware,
                tarefa=tarefa,
                contexto_necessario=contexto_necessario,
            )
            avaliados.append(CandidatoRoteamento(provider, modelo, avaliacao.score, avaliacao.adequado, avaliacao.motivos))
        return sorted(avaliados, key=lambda item: (-item.adequado, -item.score, item.provider, item.modelo))
