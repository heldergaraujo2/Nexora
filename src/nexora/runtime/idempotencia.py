"""Contrato minimo de idempotencia para efeitos externos.

Este modulo fornece apenas a barreira de identidade/duplicidade. Ele nao executa
ferramentas, nao habilita retries e nao tenta desfazer efeitos externos.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from enum import Enum
from threading import RLock
from typing import Any, Mapping


class StatusIdempotencia(str, Enum):
    """Estado observado de uma operacao identificada por chave."""

    IN_PROGRESS = "in_progress"
    SUCCEEDED = "succeeded"
    FAILED = "failed"


class ConflitoIdempotencia(ValueError):
    """Indica reutilizacao de uma chave para uma operacao diferente."""


@dataclass(frozen=True)
class RegistroIdempotencia:
    """Registro imutavel da identidade e estado de uma operacao."""

    chave: str
    fingerprint: str
    status: StatusIdempotencia
    resultado: Any = None


class StoreIdempotenciaMemoria:
    """Store concorrente minimo para impedir execucao duplicada no mesmo processo.

    A implementacao e deliberadamente local/in-memory. Persistencia duravel e
    coordenacao entre processos ficam para uma etapa posterior.
    """

    def __init__(self) -> None:
        self._registros: dict[str, RegistroIdempotencia] = {}
        self._lock = RLock()

    def reivindicar(self, chave: str, fingerprint: str) -> RegistroIdempotencia:
        """Registra a operacao ou devolve o registro existente.

        A primeira chamada cria ``IN_PROGRESS`` e autoriza o chamador a executar.
        Chamadas posteriores com a mesma identidade nunca criam uma nova execucao.
        Reutilizar a chave com outro fingerprint e erro de integridade.
        """
        self._validar(chave, fingerprint)
        with self._lock:
            atual = self._registros.get(chave)
            if atual is not None:
                if atual.fingerprint != fingerprint:
                    raise ConflitoIdempotencia(
                        f"chave de idempotencia ja associada a outra operacao: {chave}"
                    )
                return atual
            novo = RegistroIdempotencia(
                chave=chave,
                fingerprint=fingerprint,
                status=StatusIdempotencia.IN_PROGRESS,
            )
            self._registros[chave] = novo
            return novo

    def concluir(
        self,
        chave: str,
        fingerprint: str,
        *,
        sucesso: bool,
        resultado: Any = None,
    ) -> RegistroIdempotencia:
        """Fecha uma operacao ja reivindicada, sem alterar sua identidade."""
        self._validar(chave, fingerprint)
        with self._lock:
            atual = self._registros.get(chave)
            if atual is None:
                raise KeyError(f"operacao de idempotencia inexistente: {chave}")
            if atual.fingerprint != fingerprint:
                raise ConflitoIdempotencia(
                    f"chave de idempotencia associada a outro fingerprint: {chave}"
                )
            novo = RegistroIdempotencia(
                chave=chave,
                fingerprint=fingerprint,
                status=(
                    StatusIdempotencia.SUCCEEDED
                    if sucesso
                    else StatusIdempotencia.FAILED
                ),
                resultado=resultado,
            )
            self._registros[chave] = novo
            return novo

    def obter(self, chave: str) -> RegistroIdempotencia | None:
        """Retorna o registro atual, se existir."""
        with self._lock:
            return self._registros.get(chave)

    @staticmethod
    def _validar(chave: str, fingerprint: str) -> None:
        if not chave.strip():
            raise ValueError("chave de idempotencia deve ser uma string nao vazia")
        if not fingerprint.strip():
            raise ValueError("fingerprint deve ser uma string nao vazia")


def fingerprint_operacao(payload: Mapping[str, Any]) -> str:
    """Gera fingerprint deterministico de um payload serializavel em JSON."""
    canonico = json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(canonico).hexdigest()
