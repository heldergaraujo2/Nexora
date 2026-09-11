"""Orquestrador da NEXORA com historico e comunicacao entre agentes."""
from __future__ import annotations

from datetime import datetime, timezone

from nexora.comunicacao import CommunicationBus
from nexora.core.ciclo import Executor as ExecutorCiclo, Verificador as VerificadorCiclo
from nexora.core.objetivo import Objetivo
from nexora.core.plano import Plano, Tarefa
from nexora.runtime.eventos import EventStore
from nexora.runtime.verificacao import texto_nao_vazio


class Orquestrador:
    """Recebe um objetivo, coordena tarefas e publica seu ciclo no barramento."""

    def __init__(self, rotador, provider, planejador=None, evento_store=None, historico=None, communication_bus=None, agent_id="orchestrator"):
        self.rotador = rotador
        self.provider = provider
        self.planejador = planejador or self._planejar
        self.eventos = evento_store
        self.historico = historico if historico is not None else []
        self.communication_bus = communication_bus
        self.agent_id = agent_id

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

    def _executar_tarefa(self, tarefa):
        descricao = tarefa.get("descricao", "")
        return self.provider.generate(descricao).text

    def _verificar(self, contexto):
        return texto_nao_vazio(contexto)

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
            plano.adicionar_tarefa(Tarefa(descricao=item.get("descricao", "")))
        self._registrar("plano", plano.para_dict())
        self._publicar("orquestracao.plano", {"objetivo_id": objetivo.id, "plano_id": plano.id, "tarefas": len(plano.tarefas)})

        executor = ExecutorCiclo(self._executar_tarefa)
        verificador = VerificadorCiclo(self._verificar)

        etapas = []
        ok_geral = True
        for tarefa in plano.tarefas:
            tarefa_dict = tarefa.para_dict()
            self._publicar("orquestracao.tarefa.inicio", {"objetivo_id": objetivo.id, "tarefa_id": tarefa_dict.get("id")})
            try:
                saida = executor.executar(tarefa_dict)
                ok = verificador.verificar(tarefa_dict, saida)
            except Exception as exc:
                saida = ""
                ok = False
                erro = str(exc)
            else:
                erro = None
            etapa = {"tarefa_id": tarefa_dict.get("id"), "ok": ok, "saida": saida, "erro": erro}
            etapas.append(etapa)
            self._publicar("orquestracao.tarefa.resultado", {"objetivo_id": objetivo.id, **etapa})
            if not ok:
                ok_geral = False

        objetivo.concluido_em = datetime.now(timezone.utc).isoformat()
        objetivo.sucesso = ok_geral
        objetivo.metricas = {"total": len(etapas), "ok": sum(1 for e in etapas if e["ok"]), "falhas": sum(1 for e in etapas if not e["ok"])}
        self._registrar("resultado", objetivo.para_dict())
        resultado = {"objetivo_id": objetivo.id, "texto": objetivo.texto, "sucesso": ok_geral,
                     "saida": etapas[-1]["saida"] if etapas else "", "etapas": etapas,
                     "metricas": objetivo.metricas, "historico": self.historico}
        self._publicar("orquestracao.resultado", {"objetivo_id": objetivo.id, "sucesso": ok_geral, "metricas": objetivo.metricas})
        return resultado
