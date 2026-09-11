"""Runtime do agente generalista: OBJECTIVE->PLAN->EXECUTE->OBSERVE->VERIFY->ANALYZE->CORRECT->RETEST."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable


@dataclass
class ResultadoAgente:

    objetivo: str
    sucesso: bool
    saida_final: str = ""
    tentativas: int = 0
    etapas: list[dict[str, Any]] = field(default_factory=list)
    metricas: dict[str, Any] = field(default_factory=dict)
    historico: list[dict[str, Any]] = field(default_factory=list)


class AgenteRuntime:

    def __init__(
        self,
        executar: Callable[[str], str],
        verificar: Callable[[str], bool],
        analisar: Callable[[Any], Any],
        corregir: Callable[[str, Any], str],
        *,
        registrar: Callable[[str, dict[str, Any]], None] | None = None,
        max_tentativas: int = 3,
    ) -> None:

        self._executar = executar
        self._verificar = verificar
        self._analisar = analisar
        self._corregir = corregir
        self._registrar = registrar
        self._max_tentativas = max_tentativas


    def executar(self, objetivo: str) -> ResultadoAgente:



        historico: list[dict[str, Any]] = []
        saida = ""
        tentativas = 0
        ultimo_erro = None
        ok = False

        while tentativas < self._max_tentativas:

            tentativas += 1
            saida = self._executar(objetivo)
            observacao = {"tentativa": tentativas, "saida": saida, "erro": None}
            ok = self._verificar(saida)

            if not ok:

                if self._registrar is not None:
                    self._registrar("observacao", observacao)
                falha = self._analisar(observacao)
                if self._registrar is not None:
                    self._registrar("falha", falha.para_dict() if hasattr(falha, "para_dict") else {"plano": str(falha)})
                ultimo_erro = falha.motivo if hasattr(falha, "motivo") else str(falha)
                if falha.plano == "abort":


                    break
                if falha.plano == "troca_provider":


                    break
                if falha.plano == "ajuste_prompt":
                    saida = self._corregir(objetivo, falha)
                    ok = self._verificar(saida)
                    if self._registrar is not None:
                        self._registrar("reteste", {"tentativa": tentativas, "ok": ok, "saida": saida})
                if ok:
                    break
                continue

            else:

                break


        return ResultadoAgente(
            objetivo=objetivo,
            sucesso=ok,
            saida_final=saida,
            tentativas=tentativas,
            etapas=[{"tentativa": tentativas, "ok": ok, "saida": saida, "erro": ultimo_erro}],
            metricas={"tentativas": tentativas, "max_tentativas": self._max_tentativas},
            historico=historico,
        )
