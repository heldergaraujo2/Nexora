"""Ponte explícita entre decisão de roteamento e ExecutionTrace."""
from __future__ import annotations

from typing import Any

from nexora.providers.roteamento import CandidatoRoteamento
from nexora.runtime.trace import ExecutionTrace


def _serializar(candidato: CandidatoRoteamento) -> dict[str, Any]:
    return {
        "provider": candidato.provider,
        "modelo": candidato.modelo,
        "score": candidato.score,
        "adequado": candidato.adequado,
        "motivos": list(candidato.motivos),
    }


def registrar_decisao_trace(trace: ExecutionTrace, candidatos: list[CandidatoRoteamento]) -> None:
    """Registra uma decisão já tomada no metadata do trace sem executar nada."""
    if not isinstance(trace, ExecutionTrace):
        raise TypeError("trace deve ser um ExecutionTrace")
    trace.metadata["routing_decision"] = routing_metadata(candidatos)


def routing_metadata(candidatos: list[CandidatoRoteamento]) -> dict[str, Any]:
    """Serializa a decisão para integração com componentes de execução."""
    return {
        "selected": _serializar(candidatos[0]) if candidatos else None,
        "candidates": [_serializar(candidato) for candidato in candidatos],
    }
