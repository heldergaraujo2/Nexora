"""Registro central de ferramentas executaveis (ADR-008)."""
from __future__ import annotations

from typing import Any, Callable
from uuid import uuid4

from nexora.governanca.permissoes import GerenciadorPermissoes, PedidoPermissao
from nexora.runtime.checkpoint import CheckpointEngine


class Ferramenta:
    """Ferramenta registrada com nome, descricao e executor."""

    def __init__(
        self,
        nome: str,
        descricao: str,
        executar: Callable[[dict[str, Any]], Any],
    ) -> None:
        self.nome = nome.strip()
        self.descricao = descricao.strip()
        self._executar = executar

    def executar(self, parametros: dict[str, Any]) -> Any:
        return self._executar(parametros)


class RegistryFerramentas:
    """Mapeia ferramentas e aplica permissao e checkpoint antes da execucao."""

    def __init__(
        self,
        permissoes: GerenciadorPermissoes | None = None,
        checkpoint: CheckpointEngine | None = None,
    ) -> None:
        self._ferramentas: dict[str, Ferramenta] = {}
        self._permissoes = permissoes
        self._checkpoint = checkpoint

    def registrar(self, ferramenta: Ferramenta) -> None:
        self._ferramentas[ferramenta.nome] = ferramenta

    def obter(self, nome: str) -> Ferramenta:
        return self._ferramentas[nome.strip()]

    def executar(
        self,
        nome: str,
        parametros: dict[str, Any],
        *,
        solicitante: str = "sistema",
        contexto: dict[str, Any] | None = None,
        execucao_id: str | None = None,
    ) -> Any:
        ferramenta = self.obter(nome)
        contexto_seguro = dict(contexto or {})

        if self._permissoes is not None:
            self._permissoes.exigir(
                PedidoPermissao(
                    solicitante=solicitante,
                    recurso=ferramenta.nome,
                    acao="executar",
                    contexto=contexto_seguro,
                )
            )

        if self._checkpoint is not None:
            identificador = (execucao_id or uuid4().hex).strip()
            self._checkpoint.criar(
                identificador,
                {
                    "tipo": "ferramenta",
                    "ferramenta": ferramenta.nome,
                    "solicitante": solicitante,
                    "contexto": contexto_seguro,
                },
                motivo="antes_da_acao",
            )

        return ferramenta.executar(parametros)

    def nomes(self) -> list[str]:
        return sorted(self._ferramentas)
