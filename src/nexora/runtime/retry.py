"""Politica de retry tipado e seguro para o Runtime da NEXORA."""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class TipoRetry(str, Enum):
    PROVIDER = "provider"
    TRANSPORTE = "transporte"
    FERRAMENTA = "ferramenta"
    VERIFICACAO = "verificacao"
    CORRECAO = "correcao"
    RECUPERACAO = "recuperacao"
    WORKFLOW = "workflow"


@dataclass(frozen=True)
class RetryContexto:
    tipo: TipoRetry
    tentativa: int
    max_tentativas: int
    efeito_externo: bool = False
    idempotente: bool = False
    autorizado: bool = True
    precondicoes_ok: bool = True


@dataclass(frozen=True)
class RetryDecisao:
    permitido: bool
    motivo: str
    proxima_tentativa: int | None


class RetryPolicy:
    """Evita retry de efeitos externos sem as barreiras exigidas."""

    def __init__(self, *, max_tentativas: int = 3) -> None:
        if max_tentativas < 1:
            raise ValueError("max_tentativas deve ser >= 1")
        self.max_tentativas = max_tentativas

    def decidir(self, contexto: RetryContexto) -> RetryDecisao:
        if contexto.tentativa < 1:
            raise ValueError("tentativa deve ser >= 1")
        if contexto.tentativa >= min(self.max_tentativas, contexto.max_tentativas):
            return RetryDecisao(False, "limite de tentativas atingido", None)
        if not contexto.autorizado:
            return RetryDecisao(False, "retry nao autorizado", None)
        if not contexto.precondicoes_ok:
            return RetryDecisao(False, "precondicoes de retry nao satisfeitas", None)
        if contexto.efeito_externo and not contexto.idempotente:
            return RetryDecisao(False, "efeito externo nao idempotente", None)
        return RetryDecisao(True, "retry permitido", contexto.tentativa + 1)
