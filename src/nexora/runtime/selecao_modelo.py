"""Seleção determinística de modelos locais adequados ao hardware."""
from __future__ import annotations

from dataclasses import dataclass

from nexora.providers.modelos import PerfilCapacidadeModelo
from nexora.runtime.hardware import PerfilHardware
from nexora.runtime.modelos import AvaliacaoModelo, avaliar_modelo


@dataclass(frozen=True)
class CandidatoModelo:
    nome: str
    avaliacao: AvaliacaoModelo


def selecionar_modelos(
    modelos: list[tuple[str, PerfilCapacidadeModelo]],
    hardware: PerfilHardware,
    *,
    tarefa: str = "general",
    contexto_necessario: int = 0,
    limite: int = 3,
) -> list[CandidatoModelo]:
    """Ordena candidatos adequados por score, preservando ordem como desempate."""
    if limite <= 0:
        return []

    candidatos = [
        CandidatoModelo(
            nome=nome,
            avaliacao=avaliar_modelo(
                nome,
                perfil,
                hardware,
                tarefa=tarefa,
                contexto_necessario=contexto_necessario,
            ),
        )
        for nome, perfil in modelos
    ]
    adequados = [candidato for candidato in candidatos if candidato.avaliacao.adequado]
    adequados.sort(key=lambda candidato: candidato.avaliacao.score, reverse=True)
    return adequados[:limite]
