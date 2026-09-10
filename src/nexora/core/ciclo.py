"""Ciclo de execucao do agente (ADR-010: planejar, executar, verificar, registrar.."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Protocol


@dataclass
class ResultadoCiclo:
    """Resultado de uma execucao unica do ciclo agente."""

    objetivo_id: str
    plano_id: str | None = None
    tarefa_id: str | None = None
    ok: bool = False
    saida: str = ""
    erro: str | None = None
    etapas: list[dict[str, Any]] = field(default_factory=list)
    metricas: dict[str, Any] = field(default_factory=dict)


class Planejador(Protocol):
    def planejar(self, objetivo: str) -> list[dict[str, str]]: ...


class Executor:
    """Executa tarefas de forma controlada por um provider."""

    def __init__(self, executar_tarefa: Callable[[dict[str, Any], str]]) -> None:
        self._executar_tarefa = executar_tarefa

    def executar(self, tarefa: dict[str, Any]) -> str:
        return self._executar_tarefa(tarefa)


class Verificador:
    """Valida resultados de execucao."""

    def __init__(self, criterio: Callable[[dict[str, Any], bool]]) -> None:
        self._criterio = criterio

    def verificar(self, tarefa: dict[str, Any], saida: str) -> bool:
        return self._criterio({"tarefa": tarefa, "saida": saida})


def executar_ciclo(
    *,
    objetivo: str,
    planejador: Planejador,
    executor: Executor,
    verificador: Verificador,
    registrar: Callable[[dict[str, Any], None]],
    max_tarefas: int = 10,
) -> ResultadoCiclo:
    """Executa o ciclo completo e retorna o resultado consolidado."""

    plano = planejador.planejar(objetivo)
    etapas: list[dict[str, Any]] = []
    metricas: dict[str, Any] = {}

    metricas["total_tarefas"] = len(plano)
    metricas["concluidas"] = 0
    metricas["falhas"] = 0
    metricas["etapas_executadas"] = len(etapas)

    for tarefa_dict in plano[:max_tarefas]:
        tarefa_id = tarefa_dict.get("id", "desconhecida")
        try:
            saida = executor.executar(tarefa_dict)
            ok = verificador.verificar(tarefa_dict, saida)
        except Exception as exc:
            saida = ""
            ok = False
            erro = str(exc)
        else:
            erro = None
        etapas.append(
            {
                "tarefa_id": tarefa_id,
                "ok": ok,
                "saida": saida,
                "erro": erro,
            }
        )
        if ok:
            metricas["concluidas"] +=  1
        else:
            metricas["falhas"] += 1
    metricas["etapas_executadas"] = len(etapas)

    registrar(
        {
            "tipo": "ciclo",
            "objetivo": objetivo,
            "plano": plano,
            "etapas": etapas,
            "metricas": metricas,
        }
    )
    return ResultadoCiclo(
        objetivo_id=objetivo,
        plano_id=None,
        ok=metricas["falhas"] == 0,
        saida=str(metricas),
        etapas=etapas,
        metricas=metricas,
    )