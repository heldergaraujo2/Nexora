from __future__ import annotations

from nexora.runtime.agente import AgenteRuntime
from nexora.runtime.analise import AnalisadorFalhas
from nexora.runtime.correcao import Corrector


def test_runtime_retorna_trace_correlacionavel() -> None:
    chamadas = 0

    def executar(_objetivo: str) -> str:
        nonlocal chamadas
        chamadas += 1
        return "ok" if chamadas > 1 else ""

    runtime = AgenteRuntime(
        executar=executar,
        verificar=lambda saida: bool(saida.strip()),
        analisar=lambda observacao: AnalisadorFalhas().analisar(observacao),
        corregir=Corrector(executar=executar).corregir,
        max_tentativas=2,
        agent_id="agent-test",
    )

    resultado = runtime.executar("objetivo")

    assert resultado.sucesso is True
    assert resultado.trace["agent_id"] == "agent-test"
    assert resultado.trace["execution_id"]
    assert resultado.trace["trace_id"]
    assert resultado.trace["status"] == "success"
    assert resultado.trace["retry_count"] == 1
    assert resultado.trace["finished_at"] is not None
