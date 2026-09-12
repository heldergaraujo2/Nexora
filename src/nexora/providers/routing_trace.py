"""Ponte explícita entre decisão de roteamento e ExecutionTrace."""
from __future__ import annotations

from typing import Any

from nexora.providers.roteamento import CandidatoRoteamento
from nexora.runtime.trace import ExecutionTrace


def registrar_decisao_trace(trace: ExecutionTrace, candidatos: list[CandidatoRoteamento]) -> None:
    """Registra uma decisão já tomada no metadata do trace sem executar nada."""
    if not isinstance(trace, ExecutionTrace):
        raise TypeError("trace deve ser um ExecutionTrace")
    trace.metadata["routing_decision"] = {
        "selected": candidatos[0].para_dict() if candidatos else None,
        "candidates": [candidato.para_dict() for candidato in candidatos],
    }


def routing_metadata(candidatos: list[CandidatoRoteamento]) -> dict[str, Any]:
    """Serializa a decisão para integração com componentes de execução."""
    return {
        "selected": candidatos[0].para_dict() if candidatos else None,
        "candidates": [candidato.para_dict() for candidato in candidatos],
    }
