"""Orquestrador da NEXORA com historico e comunicacao entre agentes."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from nexora.comunicacao import CommunicationBus
from nexora.core.objetivo import Objetivo
from nexora.core.plano import Plano, Tarefa
from nexora.providers.manager import ProviderManager
from nexora.providers.roteamento import CandidatoRoteamento, RoteadorInteligente
from nexora.providers.routing_trace import registrar_decisao_trace
from nexora.runtime.agente import AgenteRuntime, ResultadoAgente
from nexora.runtime.analise import AnalisadorFalhas
from nexora.runtime.correcao import Corrector
from nexora.runtime.eventos import EventStore
from nexora.runtime.hardware import PerfilHardware
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
        provider_manager: ProviderManager | None = None,
        roteador_inteligente: RoteadorInteligente | None = None,
        candidatos_roteamento: list[dict[str, Any]] | None = None,
        hardware: PerfilHardware | None = None,
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
        self.provider_manager = provider_manager
        self.roteador_inteligente = roteador_inteligente
        self.candidatos_roteamento = candidatos_roteamento
        self.hardware = hardware

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
            argumentos = {
                "ferramenta": ferramenta,
                "parametros": tarefa.get("parametros", {}),
                "solicitante": self.agent_id,
                "contexto": {
                    "objetivo_id": tarefa.get("objetivo_id"),
                    "tarefa_id": tarefa.get("id"),
                    "descricao": descricao,
                },
            }
            idempotencia_chave = tarefa.get("idempotencia_chave")
            if idempotencia_chave is None and self.ferramentas.idempotencia_habilitada:
                idempotencia_chave = f"{tarefa.get('objetivo_id', '')}:{tarefa.get('id', '')}:{ferramenta}"
            resultado = self.ferramentas.executar(
                ferramenta,
                argumentos["parametros"],
                solicitante=argumentos["solicitante"],
                contexto=argumentos["contexto"],
                execucao_id=tarefa.get("execucao_id"),
                idempotencia_chave=idempotencia_chave,
            )
            if hasattr(resultado, "resultado"):
                return resultado.resultado
            return resultado
        provider_name = getattr(provider, "name", "")
        if (
            self.provider_manager is not None
            and isinstance(provider_name, str)
            and provider_name.strip().lower() in self.provider_manager.nomes()
        ):
            return self.provider_manager.executar_instancia(provider_name, provider, descricao).text
        return provider.generate(descricao).text

    @staticmethod
    def _verificar(saida):
        return texto_nao_vazio({"saida": saida})

    @staticmethod
    def _analisar(observacao):
        return AnalisadorFalhas().analisar(observacao)

    def _executar_runtime(
        self,
        tarefa_dict,
        provider,
        *,
        routing_candidates: list[CandidatoRoteamento] | None = None,
    ):
        def executar(_prompt):
            return self._executar_tarefa(tarefa_dict, provider)

        def verificar(saida):
            return self._verificar(saida)

        corrector = Corrector(executar=executar, registrar=self._registrar)
        # Retentativas de ferramentas/efeitos externos sao deliberadamente desabilitadas
        # nesta primeira integracao; providers sem efeitos externos podem usar recovery.
        tentativas = 1 if tarefa_dict.get("ferramenta") is not None else self.max_tentativas
        provider_name = getattr(provider, "name", "")
        model_name = getattr(provider, "modelo", "")
        trace = ExecutionTrace(
            agent_id=f"{self.agent_id}:runtime",
            task_id=str(tarefa_dict.get("id") or ""),
            provider=provider_name if isinstance(provider_name, str) else "",
            model=model_name if isinstance(model_name, str) else "",
            metadata={
                "objetivo_id": tarefa_dict.get("objetivo_id"),
                "executor": self.agent_id,
                "ferramenta": tarefa_dict.get("ferramenta") or "",
            },
        )
        if routing_candidates is not None:
            registrar_decisao_trace(trace, routing_candidates)
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

    def _selecionar_provider(self, objetivo_texto: str, alias=None):
        """Seleciona provider/modelo pelo router inteligente quando configurado.

        O caminho legado continua intacto quando o router inteligente nao possui
        contexto suficiente. Quando uma decisao inteligente e usada, o provider
        e instanciado com o modelo selecionado, sem fallback silencioso.
        """
        if (
            self.roteador_inteligente is None
            or self.provider_manager is None
            or self.hardware is None
            or not self.candidatos_roteamento
        ):
            return self.rotador.obter_provider(objetivo_texto, alias=alias), None

        candidatos = self.roteador_inteligente.selecionar(
            self.candidatos_roteamento,
            self.hardware,
            tarefa="coding" if "cod" in objetivo_texto.lower() else "general",
        )
        adequados = [candidato for candidato in candidatos if candidato.adequado]
        if not adequados:
            raise RuntimeError("Nenhum provider/modelo adequado pelo roteador inteligente")
        selecionado = adequados[0]
        provider = self.provider_manager.obter_com_modelo(selecionado.provider, selecionado.modelo)
        return provider, candidatos

    def executar(self, objetivo_texto, alias=None):
        objetivo = Objetivo(objetivo_texto)
        self._registrar("objetivo", objetivo.para_dict())
        self._publicar("orquestracao.inicio", {"objetivo_id": objetivo.id, "objetivo": objetivo.texto})

        provider, routing_candidates = self._selecionar_provider(objetivo_texto, alias=alias)
        if not provider.saudavel():
            self._publicar("orquestracao.erro", {"objetivo_id": objetivo.id, "motivo": "Provider indisponivel"})
            raise RuntimeError("Provider indisponivel")

        plano_dict = self.planejador(objetivo_texto)
        plano = Plano(objetivo_id=objetivo.id)
        for item in plano_dict:
            plano.adicionar_tarefa(
                Tarefa(
                    descricao=item.get("descricao", ""),
                    id=item.get("id"),
                    ferramenta=item.get("ferramenta"),
                    parametros=item.get("parametros", {}),
                    depende_de=item.get("depende_de", []),
                    idempotencia_chave=item.get("idempotencia_chave"),
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
            resultado_runtime: ResultadoAgente = self._executar_runtime(
                tarefa_dict,
                provider,
                routing_candidates=routing_candidates,
            )
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
                if tarefa_dict.get("idempotencia_chave") is not None:
                    etapa["idempotencia_chave"] = tarefa_dict["idempotencia_chave"]
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
