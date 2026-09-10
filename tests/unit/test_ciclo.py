"""Testes do ciclo de execucao (core.."""
from nexora.core.ciclo import Executor, Verificador, executar_ciclo


def _executor_fake(tarefa: dict) -> str:
    return f"ok:{tarefa.get('descricao', '')}"


def _verificador_sempre_ok(contexto: dict) -> bool:
    return True


def _registrar(contexto: dict) -> None:
    assert contexto["tipo"] == "ciclo"


def test_ciclo_simples_conclui_com_sucesso():
    resultado = executar_ciclo(
        objetivo="Teste",
        planejador=_PlanejadorFalso(),
        executor=Executor(_executor_fake),
        verificador=Verificador(_verificador_sempre_ok),
        registrar=_registrar,
    )
    assert resultado.ok
    assert resultado.metricas["total_tarefas"] == 1
    assert resultado.metricas["concluidas"] == 1


class _PlanejadorFalso:
    """Planejador deterministico para testes."""

    def planejar(self, objetivo: str) -> list[dict]:
        return [{"id": "t1", "descricao": "tarefa 1"}]


def test_ciclo_com_falha_marca_falhas():
    def _falhar(tarefa: dict) -> str:
        raise RuntimeError("boom")

    resultado = executar_ciclo(
        objetivo="Quebra",
        planejador=_PlanejadorFalso(),
        executor=Executor(_falhar),
        verificador=Verificador(_verificador_sempre_ok),
        registrar=_registrar,
    )
    assert resultado.ok is False
    assert resultado.metricas["falhas"] == 1