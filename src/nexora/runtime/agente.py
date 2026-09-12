"""Runtime do agente generalista com comunicacao entre agentes."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable

from nexora.comunicacao import CommunicationBus
from nexora.runtime.avaliacao import AvaliadorResultado, ResultadoAvaliacao
from nexora.runtime.observacao import Observacao
from nexora.runtime.trace import ExecutionTrace


@dataclass
class ResultadoAgente:
    objetivo: str
    sucesso: bool
    saida_final: str = ""
    tentativas: int = 0
    etapas: list[dict[str, Any]] = field(default_factory=list)
    metricas: dict[str, Any] = field(default_factory=dict)
    historico: list[dict[str, Any]] = field(default_factory=list)
    avaliacao: dict[str, Any] = field(default_factory=dict)
    trace: dict[str, Any] = field(default_factory=dict)
    evidencias: list[dict[str, Any]] = field(default_factory=list)


class AgenteRuntime:
    """Executa um agente e pode publicar seu ciclo no barramento de comunicacao."""

    def __init__(self, executar: Callable[[str], str], verificar: Callable[[str], bool], analisar: Callable[[Any], Any], corregir: Callable[[str, Any], str], *, registrar: Callable[[str, dict[str, Any]], None] | None = None, max_tentativas: int = 3, communication_bus: CommunicationBus | None = None, agent_id: str = "agent", trace: ExecutionTrace | None = None, avaliador: AvaliadorResultado | None = None) -> None:
        if max_tentativas < 1:
            raise ValueError("max_tentativas deve ser >= 1")
        if not agent_id.strip():
            raise ValueError("agent_id deve ser uma string nao vazia")
        self._executar = executar
        self._verificar = verificar
        self._analisar = analisar
        self._corregir = corregir
        self._registrar = registrar
        self._max_tentativas = max_tentativas
        self._communication_bus = communication_bus
        self._agent_id = agent_id
        self._trace = trace
        self._avaliador = avaliador

    def _publicar(self, tipo: str, payload: dict[str, Any], *, destinatario: str = "*") -> None:
        if self._communication_bus is not None:
            self._communication_bus.publicar(remetente=self._agent_id, destinatario=destinatario, tipo=tipo, payload=payload)

    def executar(self, objetivo: str) -> ResultadoAgente:
        trace = self._trace or ExecutionTrace(agent_id=self._agent_id)
        historico: list[dict[str, Any]] = []
        saida = ""
        tentativas = 0
        ultimo_erro = None
        ok = False
        self._publicar("agente.inicio", {"objetivo": objetivo, "execution_id": trace.execution_id, "trace_id": trace.trace_id})
        while tentativas < self._max_tentativas:
            tentativas += 1
            if tentativas > 1:
                trace.incrementar_retry()
            erro_execucao: str | None = None
            try:
                saida = self._executar(objetivo)
            except Exception as exc:
                saida = ""
                erro_execucao = str(exc)
            if erro_execucao is not None:
                ok = False
                ultimo_erro = erro_execucao
            else:
                try:
                    ok = self._verificar(saida)
                except Exception as exc:
                    ok = False
                    ultimo_erro = str(exc)
                    erro_execucao = str(exc)
            observacao = Observacao(etapa_id=f"{self._agent_id}:{tentativas}", ok=ok, saida=saida, erro=erro_execucao, metadados={"tentativa": tentativas, "execution_id": trace.execution_id, "trace_id": trace.trace_id})
            observacao_dict = {"tentativa": tentativas, "saida": observacao.saida, "erro": observacao.erro, "ok": observacao.ok, "etapa_id": observacao.etapa_id}
            historico.append(observacao_dict)
            if not ok:
                if self._registrar is not None:
                    self._registrar("observacao", observacao_dict)
                self._publicar("agente.observacao", observacao_dict)
                falha = self._analisar(observacao)
                falha_dict = falha.para_dict() if hasattr(falha, "para_dict") else {"plano": str(falha)}
                if self._registrar is not None:
                    self._registrar("falha", falha_dict)
                self._publicar("agente.falha", {"tentativa": tentativas, **falha_dict})
                ultimo_erro = falha.motivo if hasattr(falha, "motivo") and falha.motivo else ultimo_erro
                if falha.plano in {"abort", "troca_provider"}:
                    break
                if falha.plano == "ajuste_prompt":
                    saida = self._corregir(objetivo, falha)
                    try:
                        ok = self._verificar(saida)
                        reteste_erro = None
                    except Exception as exc:
                        ok = False
                        reteste_erro = str(exc)
                    reteste = {"tentativa": tentativas, "ok": ok, "saida": saida, "erro": reteste_erro}
                    historico.append(reteste)
                    if self._registrar is not None:
                        self._registrar("reteste", reteste)
                    self._publicar("agente.reteste", reteste)
                if ok:
                    break
                continue
            break

        avaliacao: ResultadoAvaliacao | None = None
        if self._avaliador is not None:
            avaliacao = self._avaliador.avaliar(objetivo, saida)
            trace.metadata["evaluation"] = avaliacao.para_dict()
            if self._registrar is not None:
                self._registrar("avaliacao", avaliacao.para_dict())
            self._publicar("agente.avaliacao", {"objetivo": objetivo, "sucesso": avaliacao.sucesso, "score": avaliacao.score, "execution_id": trace.execution_id, "trace_id": trace.trace_id})

        trace.finalizar(status="success" if ok else "failed", failure_type="" if ok else (ultimo_erro or "verification_failed"))
        metricas = {"tentativas": tentativas, "max_tentativas": self._max_tentativas}
        if avaliacao is not None:
            metricas["evaluation_score"] = avaliacao.score
            metricas["evaluation_success"] = avaliacao.sucesso
        resultado = ResultadoAgente(objetivo=objetivo, sucesso=ok, saida_final=saida, tentativas=tentativas, etapas=[{"tentativa": tentativas, "ok": ok, "saida": saida, "erro": ultimo_erro}], metricas=metricas, historico=historico, avaliacao=avaliacao.para_dict() if avaliacao is not None else {}, trace=trace.para_dict())
        self._publicar("agente.resultado", {"objetivo": objetivo, "sucesso": ok, "tentativas": tentativas, "saida": saida, "execution_id": trace.execution_id, "trace_id": trace.trace_id, "status": trace.status})
        return resultado
