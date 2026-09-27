"""Loop econômico explícito da NEXORA, sem executar transações financeiras automaticamente."""
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum


class EstadoEconomico(str, Enum):
    DESCOBERTA="descoberta"; PROTOTIPO="prototipo"; VALIDACAO="validacao"; LANCAMENTO="lancamento"; MEDICAO="medicao"; MELHORIA="melhoria"; RECEITA="receita"; REINVESTIMENTO="reinvestimento"


@dataclass(frozen=True)
class EventoEconomico:
    oportunidade_id: str
    estado: EstadoEconomico
    dados: dict[str, object]


class CicloEconomico:
    """Máquina de estados auditável; efeitos financeiros reais exigem adaptador/autorização externos."""
    ORDEM=(EstadoEconomico.DESCOBERTA,EstadoEconomico.PROTOTIPO,EstadoEconomico.VALIDACAO,EstadoEconomico.LANCAMENTO,EstadoEconomico.MEDICAO,EstadoEconomico.MELHORIA,EstadoEconomico.RECEITA,EstadoEconomico.REINVESTIMENTO)
    def __init__(self,oportunidade_id:str)->None:
        if not oportunidade_id.strip(): raise ValueError("oportunidade_id obrigatório")
        self.oportunidade_id=oportunidade_id; self.estado=EstadoEconomico.DESCOBERTA; self.eventos:list[EventoEconomico]=[]
    def avancar(self, estado:EstadoEconomico, **dados:object)->EventoEconomico:
        if estado not in self.ORDEM: raise ValueError("estado inválido")
        atual=self.ORDEM.index(self.estado); novo=self.ORDEM.index(estado)
        if novo != atual+1: raise ValueError(f"transição inválida: {self.estado.value} -> {estado.value}")
        self.estado=estado; evento=EventoEconomico(self.oportunidade_id,estado,dict(dados)); self.eventos.append(evento); return evento
