"""Politica minima de autorizacao para execucao de tarefas."""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Iterable


class EfeitoPolitica(str, Enum):
    ALLOW = "allow"
    DENY = "deny"


@dataclass(frozen=True)
class RegraPolitica:
    efeito: EfeitoPolitica
    solicitante: str | None = None
    executor: str | None = None
    tarefa: str | None = None

    def corresponde(self, *, solicitante: str, executor: str, tarefa: str) -> bool:
        return (
            (self.solicitante is None or self.solicitante == solicitante)
            and (self.executor is None or self.executor == executor)
            and (self.tarefa is None or self.tarefa == tarefa)
        )


@dataclass(frozen=True)
class DecisaoPolitica:
    efeito: EfeitoPolitica
    motivo: str
    regra: RegraPolitica | None = None
    versao: int = 1
    origem: str | None = None

    @property
    def permitido(self) -> bool:
        return self.efeito is EfeitoPolitica.ALLOW


class PolicyEngine:
    """Avalia regras ordenadas de autorizacao sem executar tarefas.

    A primeira regra que corresponder vence. Quando nenhuma regra corresponde,
    aplica-se o efeito padrao, que por seguranca e DENY.
    """

    def __init__(
        self,
        regras: Iterable[RegraPolitica] = (),
        *,
        padrao: EfeitoPolitica = EfeitoPolitica.DENY,
        versao: int = 1,
        origem: str | None = None,
    ) -> None:
        if isinstance(versao, bool) or not isinstance(versao, int) or versao < 1:
            raise ValueError("versao deve ser um inteiro maior ou igual a 1")
        if origem is not None and (not isinstance(origem, str) or not origem.strip()):
            raise ValueError("origem deve ser texto nao vazio quando informada")
        self.regras = tuple(regras)
        self.padrao = EfeitoPolitica(padrao)
        self.versao = versao
        self.origem = origem

    def decidir(self, *, solicitante: str, executor: str, tarefa: str) -> DecisaoPolitica:
        if not solicitante.strip() or not executor.strip() or not tarefa.strip():
            raise ValueError("solicitante, executor e tarefa sao obrigatorios")
        for regra in self.regras:
            if regra.corresponde(solicitante=solicitante, executor=executor, tarefa=tarefa):
                return DecisaoPolitica(
                    regra.efeito,
                    "regra correspondente",
                    regra,
                    self.versao,
                    self.origem,
                )
        return DecisaoPolitica(
            self.padrao,
            "nenhuma regra correspondente",
            None,
            self.versao,
            self.origem,
        )

    def autorizar(self, delegacao: Any) -> DecisaoPolitica:
        return self.decidir(
            solicitante=delegacao.solicitante,
            executor=delegacao.executor,
            tarefa=delegacao.tarefa,
        )


__all__ = ["DecisaoPolitica", "EfeitoPolitica", "PolicyEngine", "RegraPolitica"]
