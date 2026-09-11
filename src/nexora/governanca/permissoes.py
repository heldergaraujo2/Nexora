"""Fronteira explicita de permissao para ferramentas e recursos da NEXORA."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from ..auditoria.registro import RegistroAuditoria
from .policy import DecisaoPolitica, PolicyEngine


class PermissaoNegada(PermissionError):
    """Erro levantado quando uma acao nao e autorizada pela politica."""


@dataclass(frozen=True)
class PedidoPermissao:
    """Pedido de permissao antes da execucao de uma acao."""

    solicitante: str
    recurso: str
    acao: str
    contexto: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.solicitante.strip():
            raise ValueError("solicitante deve ser uma string nao vazia")
        if not self.recurso.strip():
            raise ValueError("recurso deve ser uma string nao vazia")
        if not self.acao.strip():
            raise ValueError("acao deve ser uma string nao vazia")


class GerenciadorPermissoes:
    """Aplica a PolicyEngine como fronteira de permissao sem executar a acao."""

    def __init__(
        self,
        policy: PolicyEngine,
        *,
        auditoria: RegistroAuditoria | None = None,
    ) -> None:
        self.policy = policy
        self.auditoria = auditoria

    def verificar(self, pedido: PedidoPermissao) -> DecisaoPolitica:
        """Avalia e audita o pedido; nunca executa o recurso."""
        decisao = self.policy.decidir(
            solicitante=pedido.solicitante,
            executor=pedido.recurso,
            tarefa=pedido.acao,
        )
        if self.auditoria is not None:
            self.auditoria.registrar(
                "permissao.decisao",
                entidade="permissao",
                entidade_id=f"{pedido.solicitante}:{pedido.recurso}:{pedido.acao}",
                dados={
                    "solicitante": pedido.solicitante,
                    "recurso": pedido.recurso,
                    "acao": pedido.acao,
                    "efeito": decisao.efeito.value,
                    "permitido": decisao.permitido,
                    "motivo": decisao.motivo,
                    "regra_id": decisao.regra_id,
                    "versao": decisao.versao,
                    "origem": decisao.origem,
                    "fingerprint": decisao.fingerprint,
                    "contexto": dict(pedido.contexto),
                },
            )
        return decisao

    def exigir(self, pedido: PedidoPermissao) -> DecisaoPolitica:
        """Avalia o pedido e interrompe o fluxo quando a politica negar."""
        decisao = self.verificar(pedido)
        if not decisao.permitido:
            raise PermissaoNegada(decisao.motivo)
        return decisao


__all__ = ["GerenciadorPermissoes", "PedidoPermissao", "PermissaoNegada"]
