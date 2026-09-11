"""Delegacao de tarefas entre agentes usando o Communication Bus."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any
import uuid

from ..agentes.registro import RegistroAgentes
from .bus import CommunicationBus


class EstadoDelegacao(str, Enum):
    SOLICITADA = "solicitada"
    ACEITA = "aceita"
    CONCLUIDA = "concluida"
    FALHOU = "falhou"
    CANCELADA = "cancelada"


@dataclass
class Delegacao:
    solicitante: str
    executor: str
    tarefa: str
    prioridade: float = 0.5
    contexto: dict[str, Any] = field(default_factory=dict)
    id: str = field(default_factory=lambda: uuid.uuid4().hex)
    estado: EstadoDelegacao = EstadoDelegacao.SOLICITADA
    resultado: Any = None
    erro: str | None = None
    mensagem_id: str | None = None

    def __post_init__(self) -> None:
        if not self.solicitante.strip() or not self.executor.strip():
            raise ValueError("solicitante e executor sao obrigatorios")
        if not self.tarefa.strip():
            raise ValueError("tarefa deve ser uma string nao vazia")
        if not 0 <= self.prioridade <= 1:
            raise ValueError("prioridade deve estar entre 0 e 1")

    def para_dict(self) -> dict[str, Any]:
        return {"id": self.id, "solicitante": self.solicitante, "executor": self.executor,
                "tarefa": self.tarefa, "prioridade": self.prioridade, "contexto": dict(self.contexto),
                "estado": self.estado.value, "resultado": self.resultado, "erro": self.erro,
                "mensagem_id": self.mensagem_id}


class DelegadorAgentes:
    """Coordena o contrato de delegacao sem executar a tarefa delegada."""

    def __init__(self, bus: CommunicationBus, registro: RegistroAgentes | None = None) -> None:
        self.bus = bus
        self.registro = registro
        self._delegacoes: dict[str, Delegacao] = {}

    def delegar(self, *, solicitante: str, executor: str, tarefa: str,
                prioridade: float = 0.5, contexto: dict[str, Any] | None = None) -> Delegacao:
        delegacao = Delegacao(solicitante=solicitante, executor=executor, tarefa=tarefa,
                              prioridade=prioridade, contexto={} if contexto is None else contexto)
        mensagem = self.bus.publicar(remetente=solicitante, destinatario=executor,
                                     tipo="delegacao.solicitada", payload=delegacao.para_dict(),
                                     correlacao_id=delegacao.id)
        delegacao.mensagem_id = mensagem.id
        self._delegacoes[delegacao.id] = delegacao
        return delegacao

    def delegar_por_capacidade(self, *, solicitante: str, capacidade: str, tarefa: str,
                               prioridade: float = 0.5,
                               contexto: dict[str, Any] | None = None) -> Delegacao:
        """Seleciona automaticamente o agente disponivel mais bem classificado."""
        if self.registro is None:
            raise RuntimeError("registro de agentes nao configurado")
        agente = self.registro.melhor_para(capacidade)
        if agente is None:
            raise LookupError(f"nenhum agente disponivel para a capacidade: {capacidade}")
        contexto_final = {} if contexto is None else dict(contexto)
        contexto_final.setdefault("capacidade_solicitada", capacidade)
        return self.delegar(
            solicitante=solicitante,
            executor=agente.id,
            tarefa=tarefa,
            prioridade=prioridade,
            contexto=contexto_final,
        )

    def atualizar(self, delegacao_id: str, *, estado: EstadoDelegacao,
                  resultado: Any = None, erro: str | None = None) -> Delegacao:
        delegacao = self._delegacoes.get(delegacao_id)
        if delegacao is None:
            raise KeyError(delegacao_id)
        delegacao.estado = estado
        delegacao.resultado = resultado
        delegacao.erro = erro
        tipo = "delegacao.resultado" if estado in {EstadoDelegacao.CONCLUIDA, EstadoDelegacao.FALHOU, EstadoDelegacao.CANCELADA} else "delegacao.estado"
        self.bus.publicar(remetente=delegacao.executor, destinatario=delegacao.solicitante,
                          tipo=tipo, payload=delegacao.para_dict(), correlacao_id=delegacao.id,
                          resposta_a=delegacao.mensagem_id)
        return delegacao

    def obter(self, delegacao_id: str) -> Delegacao | None:
        return self._delegacoes.get(delegacao_id)

    def listar(self, *, solicitante: str | None = None,
               executor: str | None = None) -> list[Delegacao]:
        itens = list(self._delegacoes.values())
        if solicitante is not None:
            itens = [item for item in itens if item.solicitante == solicitante]
        if executor is not None:
            itens = [item for item in itens if item.executor == executor]
        return itens
