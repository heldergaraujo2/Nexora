"""Orquestrador da NEXORA com historico e comunicacao entre agentes."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from nexora.comunicacao import CommunicationBus
from nexora.core.objetivo import Objetivo
from nexora.core.plano import Plano, Tarefa
from nexora.runtime.agente import AgenteRuntime, ResultadoAgente
from nexora.runtime.analise import AnalisadorFalhas
from nexora.runtime.correcao import Corrector
from nexora.runtime.eventos import EventStore
from nexora.runtime.trace import ExecutionTrace
from nexora.runtime.verificacao import texto_nao_vazio
from nexora.tools.registry import RegistryFerramentas


class Orquestrador:
    """Coordena objetivos e tarefas; o AgenteRuntime possui o ciclo de execucao."""

    def __init__(
        self,
        rotador,
        provider,
        planejador=None,
        evento_store=None,
        historico=None,
        communication_bus=None,
        agent_id="orchestrator",
        ferramentas: RegistryFerramentas | None = None,
        max_tentativas: int = 3,
    ):
        self.rotador = rotador
        self.provider = provider
        self.planejador = planejador or self._planejar
        self.eventos = evento_store
        self.historico = historico if historico is not None else []
        self.communication_bus = communication_bus
        self.agent_id = agent_id
        self.ferramentas = ferramentas
        self.max_tentativas = max_tentativas

    @staticmethod
    def _planejar(objetivo):
        return [{"id": "t1", "descricao": "Executar objetivo"}]

    def _registrar(self, tipo, dados):
        registro = {"tipo": tipo, "dados": dados}
        self.historico.append(registro)
        if self.eventos is not None:
            self.eventos.registrar(tipo, dados)

    def _publicar(self, tipo, payload):
        if self.communication_bus is not None:
            self.communication_bus.publicar(
                remetente=self.agent_id,
                destinatario="*",
                tipo=tipo,
                payload=payload,
            )

    def _executar_tarefa(self, tarefa, provider):
        descricao = tarefa.get("descricao", "")
        ferramenta = tarefa.get("ferramenta")
        if ferramenta is not None:
            if self.ferramentas is None:
                raise RuntimeError("Registry de ferramentas nao configurado")
            resultado = self.ferramentas.executar(
                ferramenta,
                tarefa.get("parametros", {}),
                solicitante=self.agent_id,
                contexto={
                    "objetivo_id": tarefa.get("objetivo_id"),
                    "tarefa_id": tarefa.get("id"),
                    "descricao": descricao,
                },
                execucao_id=tarefa.get("execucao_id"),
            )
            if hasattr(resultado, "resultado"):
                return resultado.resultado
            return resultado
        return provider.generate(descricao).text

    @staticmethod
    def _verificar(saida):
        return texto_nao_vazio({"saida": saida})

    @staticmethod
    def _analisar(observacao):
        return AnalisadorFalhas().analisar(observacao)

    def _executar_runtime(self, tarefa_dict, provider):
        def executar(_prompt):
            return self._executar_tarefa(tarefa_dict, provider)

        def verificar(saida):
            return self._verificar(saida)

        corrector = Corrector(executar=executar, registrar=self._registrar)
        # Retentativas de ferramentas/efeitos externos sao deliberadamente desabilitadas
        # nesta primeira integracao; providers sem efeitos externos podem usar recovery.
        tentativas = 1 if tarefa_dict.get("ferramenta") is not None else self.max_tentativas
        provider_name = getattr(provider, "name", "")
        trace = ExecutionTrace(
            agent_id=f"{self.agent_id}:runtime",
            task_id=str(tarefa_dict.get("id") or ""),
            provider=provider_name if isinstance(provider_name, str) else "",
            metadata={
                "objetivo_id": tarefa_dict.get("objetivo_id"),
                "executor": self.agent_id,
                "ferramenta": tarefa_dict.get("ferramenta") or "",
            },
        )
        runtime = AgenteRuntime(
            executar=executar,
            verificar=verificar,
            analisar=self._analisar,
            corregir=corrector.corregir,
            registrar=self._registrar,
            max_tentativas=tentativas,
            communication_bus=self.communication_bus,
            agent_id=f"{self.agent_id}:runtime",
            trace=trace,
        )
        return runtime.executar(tarefa_dict.get("descricao", ""))

    def executar(self, objetivo_texto, alias=None):
        objetivo = Objetivo(objetivo_texto)
        self._registrar("objetivo", objetivo.para_dict())
        self._publicar("orquestracao.inicio", {"objetivo_id": objetivo.id, "objetivo": objetivo.texto})

        provider = self.rotador.obter_provider(objetivo_texto, alias=alias)
        if not provider.saudavel():
            self._publicar("orquestracao.erro", {"objetivo_id": objetivo.id, "motivo": "Provider indisponivel"})
            raise RuntimeError("Provider indisponivel")

        plano_dict = self.planejador(objetivo_texto)
        plano = Plano(objetivo_id=objetivo.id)
        for item in plano_dict:
            plano.adicionar_tarefa(
                Tarefa(
                    descricao=item.get("descricao", ""),
                    ferramenta=item.get("ferramenta"),
                    parametros=item.get("parametros", {}),
                    depende_de=item.get("depende_de", []),
                )
            )
        self._registrar("plano", plano.para_dict())
        self._publicar("orquestracao.plano", {"objetivo_id": objetivo.id, "plano_id": plano.id, "tarefas": len(plano.tarefas)})

        etapas = []
        ok_geral = True
        for tarefa in plano.tarefas:
            tarefa_dict = tarefa.para_dict()
            tarefa_dict["objetivo_id"] = objetivo.id
            self._publicar("orquestracao.tarefa.inicio", {"objetivo_id": objetivo.id, "tarefa_id": tarefa_dict.get("id")})
            resultado_runtime: ResultadoAgente = self._executar_runtime(tarefa_dict, provider)
            etapa: dict[str, Any] = {
                "tarefa_id": tarefa_dict.get("id"),
                "ok": resultado_runtime.sucesso,
                "saida": resultado_runtime.saida_final,
                "erro": resultado_runtime.etapas[-1].get("erro") if resultado_runtime.etapas else None,
                "tentativas": resultado_runtime.tentativas,
                "historico_runtime": resultado_runtime.historico,
                "trace": resultado_runtime.trace,
            }
            if tarefa_dict.get("ferramenta") is not None:
                etapa["ferramenta"] = tarefa_dict["ferramenta"]
                etapa["parametros"] = tarefa_dict.get("parametros", {})
            etapas.append(etapa)
            self._publicar("orquestracao.tarefa.resultado", {"objetivo_id": objetivo.id, **etapa})
            if not resultado_runtime.sucesso:
                ok_geral = False

        objetivo.concluido_em = datetime.now(timezone.utc).isoformat()
        objetivo.sucesso = ok_geral
        objetivo.metricas = {"total": len(etapas), "ok": sum(1 for e in etapas if e["ok"]), "falhas": sum(1 for e in etapas if not e["ok"])}
        self._registrar("resultado", objetivo.para_dict())
        resultado = {
            "objetivo_id": objetivo.id,
            "texto": objetivo.texto,
            "sucesso": ok_geral,
            "saida": etapas[-1]["saida"] if etapas else "",
            "etapas": etapas,
            "metricas": objetivo.metricas,
            "historico": self.historico,
        }
        self._publicar("orquestracao.resultado", {"objetivo_id": objetivo.id, "sucesso": ok_geral, "metricas": objetivo.metricas})
        return resultado