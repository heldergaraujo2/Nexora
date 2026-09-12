"""Registro central de ferramentas executaveis (ADR-008)."""
from __future__ import annotations

from typing import Any, Callable
from uuid import uuid4

from nexora.auditoria.registro import RegistroAuditoria
from nexora.governanca.permissoes import GerenciadorPermissoes, PedidoPermissao
from nexora.runtime.checkpoint import CheckpointEngine
from nexora.runtime.ferramenta import ResultadoFerramenta
from nexora.runtime.idempotencia import (
    StatusIdempotencia,
    StoreIdempotenciaMemoria,
    fingerprint_operacao,
)
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
    """Mapeia ferramentas e aplica governanca, idempotencia e observacao/verificacao."""

    def __init__(
        self,
        permissoes: GerenciadorPermissoes | None = None,
        checkpoint: CheckpointEngine | None = None,
        *,
        observador: Callable[[dict[str, Any]], Observacao] | None = None,
        verificador: Verificacao | None = None,
        auditoria: RegistroAuditoria | None = None,
        idempotencia: StoreIdempotenciaMemoria | None = None,
    ) -> None:
        self._ferramentas: dict[str, Ferramenta] = {}
        self._permissoes = permissoes
        self._checkpoint = checkpoint
        self._observador = observador
        self._verificador = verificador
        self._auditoria = auditoria
        self._idempotencia = idempotencia

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
        idempotencia_chave: str | None = None,
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

        idempotencia_fingerprint: str | None = None
        if idempotencia_chave is not None:
            if self._idempotencia is None:
                raise RuntimeError(
                    "idempotencia_chave exige um StoreIdempotenciaMemoria configurado"
                )
            idempotencia_fingerprint = fingerprint_operacao(
                {
                    "ferramenta": ferramenta.nome,
                    "parametros": parametros,
                    "solicitante": solicitante,
                    "contexto": contexto_seguro,
                }
            )
            registro, primeira_execucao = self._idempotencia.reivindicar_com_status(
                idempotencia_chave,
                idempotencia_fingerprint,
            )
            if not primeira_execucao:
                if self._auditoria is not None:
                    self._auditoria.registrar(
                        "ferramenta.idempotencia_reutilizada",
                        entidade="ferramenta",
                        entidade_id=identificador,
                        dados={
                            "ferramenta": ferramenta.nome,
                            "chave": idempotencia_chave,
                            "status": registro.status.value,
                        },
                    )
                if registro.status == StatusIdempotencia.SUCCEEDED:
                    return registro.resultado
                if registro.status == StatusIdempotencia.IN_PROGRESS:
                    raise RuntimeError(
                        f"operacao de idempotencia em andamento: {idempotencia_chave}"
                    )
                raise RuntimeError(
                    f"operacao de idempotencia falhou anteriormente; retry explicito necessario: {idempotencia_chave}"
                )

        try:
            resultado = ferramenta.executar(parametros)
        except Exception as exc:
            if self._idempotencia is not None and idempotencia_chave is not None:
                self._idempotencia.concluir(
                    idempotencia_chave,
                    idempotencia_fingerprint or "",
                    sucesso=False,
                    resultado=None,
                )
            if self._auditoria is not None:
                self._auditoria.registrar(
                    "ferramenta.falhou",
                    entidade="ferramenta",
                    entidade_id=identificador,
                    dados={
                        "ferramenta": ferramenta.nome,
                        "solicitante": solicitante,
                        "erro_tipo": type(exc).__name__,
                        "erro": str(exc),
                    },
                )
            raise

        if self._idempotencia is not None and idempotencia_chave is not None:
            self._idempotencia.concluir(
                idempotencia_chave,
                idempotencia_fingerprint or "",
                sucesso=True,
                resultado=resultado,
            )

        if self._observador is None and self._verificador is None:
            if self._auditoria is not None:
                self._auditoria.registrar(
                    "ferramenta.resultado",
                    entidade="ferramenta",
                    entidade_id=identificador,
                    dados={
                        "ferramenta": ferramenta.nome,
                        "solicitante": solicitante,
                        "sucesso": True,
                        "observado": False,
                        "verificado": None,
                    },
                )
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

        resultado_estruturado = ResultadoFerramenta(
            ferramenta=ferramenta.nome,
            execucao_id=identificador,
            resultado=resultado,
            observacao=observacao,
            verificado=verificado,
        )

        if self._auditoria is not None:
            self._auditoria.registrar(
                "ferramenta.resultado",
                entidade="ferramenta",
                entidade_id=identificador,
                dados={
                    "ferramenta": ferramenta.nome,
                    "solicitante": solicitante,
                    "sucesso": resultado_estruturado.sucesso,
                    "observado": True,
                    "observacao_ok": observacao.ok,
                    "verificado": verificado,
                },
            )

        return resultado_estruturado

    def nomes(self) -> list[str]:
        return sorted(self._ferramentas)
