"""Barramento deterministico de mensagens entre agentes da NEXORA.

O barramento apenas transporta e registra mensagens. Ele nao executa ferramentas,
nao chama providers e nao produz efeitos externos por conta propria.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable
import uuid


class EstadoMensagem(str, Enum):
    """Estado de entrega observado pelo barramento."""

    PENDENTE = "pendente"
    ENTREGUE = "entregue"
    LIDA = "lida"


@dataclass(frozen=True)
class MensagemAgente:
    """Envelope imutavel para comunicacao entre agentes."""

    remetente: str
    destinatario: str
    tipo: str
    payload: dict[str, Any] = field(default_factory=dict)
    correlacao_id: str | None = None
    resposta_a: str | None = None
    id: str = field(default_factory=lambda: uuid.uuid4().hex)

    def __post_init__(self) -> None:
        for nome, valor in (
            ("remetente", self.remetente),
            ("destinatario", self.destinatario),
            ("tipo", self.tipo),
        ):
            if not isinstance(valor, str) or not valor.strip():
                raise ValueError(f"{nome} deve ser uma string nao vazia")
        if not isinstance(self.payload, dict):
            raise TypeError("payload deve ser um dicionario")

    def para_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "remetente": self.remetente,
            "destinatario": self.destinatario,
            "tipo": self.tipo,
            "payload": dict(self.payload),
            "correlacao_id": self.correlacao_id,
            "resposta_a": self.resposta_a,
        }


class CommunicationBus:
    """Barramento em memoria com envio, assinatura e consulta deterministica."""

    def __init__(self) -> None:
        self._mensagens: dict[str, MensagemAgente] = {}
        self._estados: dict[str, EstadoMensagem] = {}
        self._assinantes: dict[str, list[Callable[[MensagemAgente], None]]] = {}

    def enviar(self, mensagem: MensagemAgente) -> str:
        """Publica uma mensagem e notifica assinantes do destinatario e de '*'."""
        if mensagem.id in self._mensagens:
            raise ValueError(f"mensagem ja registrada: {mensagem.id}")
        self._mensagens[mensagem.id] = mensagem
        self._estados[mensagem.id] = EstadoMensagem.PENDENTE
        self._notificar(mensagem.destinatario, mensagem)
        self._notificar("*", mensagem)
        return mensagem.id

    def publicar(
        self,
        *,
        remetente: str,
        destinatario: str,
        tipo: str,
        payload: dict[str, Any] | None = None,
        correlacao_id: str | None = None,
        resposta_a: str | None = None,
    ) -> MensagemAgente:
        """Cria e envia uma mensagem, retornando o envelope criado."""
        mensagem = MensagemAgente(
            remetente=remetente,
            destinatario=destinatario,
            tipo=tipo,
            payload={} if payload is None else payload,
            correlacao_id=correlacao_id,
            resposta_a=resposta_a,
        )
        self.enviar(mensagem)
        return mensagem

    def assinar(
        self,
        destinatario: str,
        callback: Callable[[MensagemAgente], None],
    ) -> None:
        """Registra callback para um agente ou para todos usando '*'."""
        if not destinatario.strip():
            raise ValueError("destinatario deve ser uma string nao vazia")
        self._assinantes.setdefault(destinatario, []).append(callback)

    def obter(self, mensagem_id: str) -> MensagemAgente | None:
        return self._mensagens.get(mensagem_id)

    def estado(self, mensagem_id: str) -> EstadoMensagem | None:
        return self._estados.get(mensagem_id)

    def marcar_lida(self, mensagem_id: str) -> None:
        if mensagem_id not in self._mensagens:
            raise KeyError(mensagem_id)
        self._estados[mensagem_id] = EstadoMensagem.LIDA

    def listar(
        self,
        *,
        destinatario: str | None = None,
        remetente: str | None = None,
        tipo: str | None = None,
        correlacao_id: str | None = None,
    ) -> list[MensagemAgente]:
        """Lista mensagens mantendo a ordem de publicacao."""
        mensagens = list(self._mensagens.values())
        if destinatario is not None:
            mensagens = [m for m in mensagens if m.destinatario == destinatario]
        if remetente is not None:
            mensagens = [m for m in mensagens if m.remetente == remetente]
        if tipo is not None:
            mensagens = [m for m in mensagens if m.tipo == tipo]
        if correlacao_id is not None:
            mensagens = [m for m in mensagens if m.correlacao_id == correlacao_id]
        return mensagens

    def _notificar(self, canal: str, mensagem: MensagemAgente) -> None:
        callbacks = self._assinantes.get(canal, ())
        if callbacks:
            self._estados[mensagem.id] = EstadoMensagem.ENTREGUE
        for callback in callbacks:
            callback(mensagem)
