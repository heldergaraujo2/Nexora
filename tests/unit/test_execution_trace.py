from __future__ import annotations

from nexora.runtime.trace import ExecutionTrace


def test_execution_trace_serializa_contexto_canonico() -> None:
    trace = ExecutionTrace(
        agent_id="orchestrator:runtime",
        task_id="task-1",
        provider="groq",
        model="modelo-teste",
        tokens=128,
        latency_ms=42.5,
        cost=0.001,
        policy_version="v2",
        policy_fingerprint="abc123",
        checkpoint_id="checkpoint-1",
    )

    assert trace.execution_id
    assert trace.trace_id
    assert trace.span_id
    assert trace.retry_count == 0
    assert trace.para_dict()["provider"] == "groq"
    assert trace.para_dict()["checkpoint_id"] == "checkpoint-1"


def test_execution_trace_controla_retry_e_finalizacao() -> None:
    trace = ExecutionTrace()

    assert trace.incrementar_retry() == 1
    assert trace.incrementar_retry() == 2

    trace.finalizar(status="failed", failure_type="provider_error")

    assert trace.status == "failed"
    assert trace.failure_type == "provider_error"
    assert trace.finished_at is not None


def test_execution_trace_rejeita_status_vazio() -> None:
    trace = ExecutionTrace()

    try:
        trace.finalizar(status="   ")
    except ValueError as exc:
        assert str(exc) == "status deve ser uma string nao vazia"
    else:
        raise AssertionError("status vazio deveria ser rejeitado")
