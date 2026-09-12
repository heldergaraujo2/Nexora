from __future__ import annotations

from nexora.providers.roteamento import CandidatoRoteamento
from nexora.providers.routing_trace import registrar_decisao_trace, routing_metadata
from nexora.runtime.trace import ExecutionTrace


def test_decisao_de_roteamento_entra_no_execution_trace_sem_executar_provider():
    candidatos = [
        CandidatoRoteamento(
            provider="ollama",
            modelo="qwen-coder-7b",
            score=13.5,
            adequado=True,
            motivos=("hardware_adequado", "historico_alta_taxa_sucesso"),
        ),
        CandidatoRoteamento(
            provider="groq",
            modelo="general-7b",
            score=8.0,
            adequado=True,
            motivos=("modelo_general",),
        ),
    ]
    trace = ExecutionTrace(agent_id="orchestrator:runtime", task_id="t1")

    registrar_decisao_trace(trace, candidatos)

    routing = trace.metadata["routing_decision"]
    assert routing["selected"]["provider"] == "ollama"
    assert routing["selected"]["modelo"] == "qwen-coder-7b"
    assert routing["selected"]["adequado"] is True
    assert routing["candidates"][1]["provider"] == "groq"
    assert routing["candidates"][0]["motivos"] == ["hardware_adequado", "historico_alta_taxa_sucesso"]


def test_routing_metadata_vazio_nao_inventa_decisao():
    assert routing_metadata([]) == {"selected": None, "candidates": []}
