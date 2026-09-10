"""Orquestrador da NEXORA: objetivo em linguagem natural a resultado verificado."""
from __future__ import annotations

from datetime import datetime, timezone

from nexora.core.objetivo import Objetivo
from nexora.core.plano import Plano, Tarefa
from nexora.core.ciclo import Executor as ExecutorCiclo, Verificador as VerificadorCiclo
from nexora.orquestracao.roteador import Roteador
from nexora.runtime.eventos import EventStore
from nexora.runtime.verificacao import texto_nao_vazio


class Orquestrador:

    """Recebe um objetivo e executa o ciclo completo com historico."""

    def __init__(self, rotador, provider, planejador=None, evento_store=None, historico=None):
        self.rotador = rotador
        self.provider = provider
        self.planejador = planejador or self._planejar
        self.eventos = evento_store
        self.historico = historico if historico is not None else []

    @staticmethod
    def _planejar(objetivo):
        return [{"id": "t1", "descricao": "Executar objetivo"}]

    def _registrar(self, tipo, dados):
        registro = {"tipo": tipo, "dados": dados}
        self.historico.append(registro)
        if self.eventos is not None:
            self.eventos.registrar(tipo, dados)

    def _executar_tarefa(self, tarefa):
        descricao = tarefa.get("descricao", "")
        return self.provider.generate(descricao).text

    def _verificar(self, contexto):
        return texto_nao_vazio(contexto)

    def executar(self, objetivo_texto, alias=None):
        objetivo = Objetivo(objetivo_texto)
        self._registrar("objetivo", objetivo.para_dict())

        provider = self.rotador.obter_provider(objetivo_texto, alias=alias)
        if not provider.saudavel():
            raise RuntimeError("Provider indisponivel")

        plano_dict = self.planejador(objetivo_texto)
        plano = Plano(objetivo_id=objetivo.id)
        for item in plano_dict:
     
            plano.adicionar_tarefa(Tarefa(descricao=item.get("descricao", "")))
        self._registrar("plano", plano.para_dict())

        executor = ExecutorCiclo(self._executar_tarefa)
        verificador = VerificadorCiclo(self._verificar)

        etapas = []
        ok_geral = True
        for tarefa in plano.tarefas:
            tarefa_dict = tarefa.para_dict()
            try:
                saida = executor.executar(tarefa_dict)
                ok = verificador.verificar(tarefa_dict, saida)
            except Exception as exc:
                saida = ""
                ok = False
                erro = str(exc)
            else:
                erro = None
            etapas.append({"tarefa_id": tarefa_dict.get("id"), "ok": ok, "saida": saida, "erro": erro})
            if not ok:
                ok_geral = False

        objetivo.concluido_em = datetime.now(timezone.utc).isoformat()
        objetivo.sucesso = ok_geral
        objetivo.metricas = {"total": len(etapas), "ok": sum(1 for e in etapas if e["ok"]), "falhas": sum(1 for e in etapas if not e["ok"])}
        self._registrar("resultado", objetivo.para_dict())

        return {"objetivo_id": objetivo.id, "texto": objetivo.texto, "sucesso": ok_geral,
                "saida": etapas[-1]["saida"] if etapas else "", "etapas": etapas,
                "metricas": objetivo.metricas, "historico": self.historico}