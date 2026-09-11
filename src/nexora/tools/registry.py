"""Registro central de ferramentas executaveis (ADR-008)."""
from __future__ import annotations

from typing import Any, Callable
from uuid import uuid4

from nexora.governanca.permissoes import GerenciadorPermissoes, PedidoPermissao
from nexora.runtime.checkpoint import CheckpointEngine
from nexora.runtime.ferramenta import ResultadoFerramenta
from nexora.runtime.observacao import Observacao
from nexora.runtime.verificacao import Verificacao


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
    """Mapeia ferramentas e aplica permissao, checkpoint e observacao/verificacao opcionais."""

    def __init__(
        self,
        permissoes: GerenciadorPermissoes | None = None,
        checkpoint: CheckpointEngine | None = None,
        *,
        observador: Callable[[dict[str, Any]], Observacao] | None = None,
        verificador: Verificacao | None = None,
    ) -> None:
        self._ferramentas: dict[str, Ferramenta] = {}
        self._permissoes = permissoes
        self._checkpoint = checkpoint
        self._observador = observador
        self._verificador = verificador

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
        identificador = (execucao_id or uuid4().hex).strip()

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

        resultado = ferramenta.executar(parametros)

        if self._observador is None and self._verificador is None:
            return resultado

        dados_observacao = {
            "etapa_id": identificador,
            "ferramenta": ferramenta.nome,
            "resultado": resultado,
            "saida": resultado if isinstance(resultado, str) else repr(resultado),
            "erro": None,
            "contexto": contexto_seguro,
        }
        observacao = (
            self._observador(dados_observacao)
            if self._observador is not None
            else Observacao(
                etapa_id=identificador,
                ok=True,
                saida=dados_observacao["saida"],
                metadados={
                    "ferramenta": ferramenta.nome,
                    "contexto": contexto_seguro,
                },
            )
        )

        verificado = None
        if self._verificador is not None:
            contexto_verificacao = {
                **dados_observacao,
                "observacao": observacao,
            }
            verificado = self._verificador.verificar(contexto_verificacao)

        return ResultadoFerramenta(
            ferramenta=ferramenta.nome,
            execucao_id=identificador,
            resultado=resultado,
            observacao=observacao,
            verificado=verificado,
        )

    def nomes(self) -> list[str]:
        return sorted(self._ferramentas)
