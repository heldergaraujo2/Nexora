"""Avaliação determinística de adequação de modelos ao hardware local."""
from __future__ import annotations

from dataclasses import dataclass

from nexora.providers.modelos import PerfilCapacidadeModelo, pontuar_modelo
from nexora.runtime.hardware import PerfilHardware


@dataclass(frozen=True)
class AvaliacaoModelo:
    nome: str
    score: float
    adequado: bool
    motivos: tuple[str, ...] = ()


def estimar_memoria_modelo_bytes(parametros_b: float) -> int:
    """Estimativa conservadora simples para pesos em torno de 1 byte/parâmetro."""
    if parametros_b <= 0:
        return 0
    return int(parametros_b * 1_000_000_000)


def avaliar_modelo(
    nome: str,
    perfil: PerfilCapacidadeModelo,
    hardware: PerfilHardware,
    *,
    tarefa: str = "general",
    contexto_necessario: int = 0,
) -> AvaliacaoModelo:
    motivos: list[str] = []
    score = pontuar_modelo(perfil, tarefa=tarefa, contexto_necessario=contexto_necessario)
    ram_disponivel = hardware.ram_bytes
    memoria_estimada = estimar_memoria_modelo_bytes(perfil.tamanho_parametros_b)

    if contexto_necessario > 0 and perfil.contexto < contexto_necessario:
        motivos.append("contexto_insuficiente")
    if memoria_estimada and ram_disponivel and memoria_estimada > ram_disponivel:
        motivos.append("modelo_maior_que_ram")
    if not hardware.cpu_nucleos:
        motivos.append("cpu_indisponivel")

    adequado = not motivos
    if not adequado:
        score -= 100.0

    return AvaliacaoModelo(nome=nome, score=score, adequado=adequado, motivos=tuple(motivos))
