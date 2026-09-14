"""Reconciliação determinística e conservadora de múltiplas evidências.

Esta camada NÃO determina a verdade de uma afirmação. Ela apenas compara sinais
lexicais auditáveis entre evidências que já passaram pela verificação de adequação.
"""

from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Any, Iterable


class StatusReconciliacao:
    CORROBORADA = "CORROBORADA"
    CONFLITANTE = "CONFLITANTE"
    NAO_CORROBORADA = "NAO_CORROBORADA"
    INDETERMINADA = "INDETERMINADA"


@dataclass(frozen=True)
class ResultadoReconciliacao:
    """Resultado auditável da comparação de evidências."""

    status: str
    evidencias_consideradas: int
    fontes_independentes: int
    pares_conflitantes: tuple[tuple[str, str], ...] = ()
    motivos: tuple[str, ...] = ()
    confianca: float | None = None

    def para_dict(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "evidencias_consideradas": self.evidencias_consideradas,
            "fontes_independentes": self.fontes_independentes,
            "pares_conflitantes": [list(par) for par in self.pares_conflitantes],
            "motivos": list(self.motivos),
            "confianca": self.confianca,
        }


@dataclass(frozen=True)
class _Sinal:
    ref: str
    termos: frozenset[str]
    positivo: bool | None


class ReconciliadorEvidencias:
    """Reconcilia evidências adequadas sem inferir verdade semântica.

    Por padrão exige duas referências independentes para declarar corroboração.
    A independência é tratada conservadoramente: ``source_ref`` duplicado não
    conta duas vezes e referências idênticas são consideradas a mesma fonte.
    """

    _STOPWORDS = frozenset(
        "a o e de do da dos das em no na nos nas um uma por para com sem que se".split()
    )
    _NEGACOES = frozenset(
        "nao não nunca nenhum nenhuma jamais inexiste inexistente impossível".split()
    )

    def __init__(self, *, min_termos: int = 2) -> None:
        if min_termos < 1:
            raise ValueError("min_termos deve ser >= 1")
        self.min_termos = min_termos

    @classmethod
    def _tokens(cls, texto: str) -> frozenset[str]:
        palavras = re.findall(r"[\wÀ-ÿ]+", texto.casefold())
        return frozenset(
            palavra
            for palavra in palavras
            if len(palavra) > 1 and palavra not in cls._STOPWORDS
        )

    @classmethod
    def _polaridade(cls, texto: str) -> bool | None:
        tokens = cls._tokens(texto)
        return False if tokens & cls._NEGACOES else None

    @staticmethod
    def _campo(evidencia: Any, nome: str, padrao: Any = "") -> Any:
        if isinstance(evidencia, dict):
            return evidencia.get(nome, padrao)
        return getattr(evidencia, nome, padrao)

    def _adequada(self, evidencia: Any) -> bool:
        adequacao = self._campo(evidencia, "adequacao", None)
        if isinstance(adequacao, dict):
            status = adequacao.get("status")
        else:
            status = getattr(adequacao, "status", adequacao)
        return status == "SUSTENTADA"

    def _sinal(self, evidencia: Any) -> _Sinal:
        ref = str(self._campo(evidencia, "source_ref", "") or "")
        trecho = str(self._campo(evidencia, "trecho", "") or "")
        # O título é proveniência/metadado, não evidência do claim.
        return _Sinal(
            ref or f"anonimo:{id(evidencia)}",
            self._tokens(trecho),
            self._polaridade(trecho),
        )

    def reconciliar(self, claim: str, evidencias: Iterable[Any]) -> ResultadoReconciliacao:
        if not isinstance(claim, str) or not claim.strip():
            raise ValueError("claim deve ser texto não vazio")

        claim_terms = self._tokens(claim)
        sinais: list[_Sinal] = []
        refs: set[str] = set()
        for evidencia in evidencias:
            if not self._adequada(evidencia):
                continue
            sinal = self._sinal(evidencia)
            if sinal.ref in refs:
                continue
            refs.add(sinal.ref)
            if len(sinal.termos & claim_terms) >= self.min_termos:
                sinais.append(sinal)

        if not sinais:
            return ResultadoReconciliacao(
                StatusReconciliacao.NAO_CORROBORADA,
                0,
                0,
                motivos=("nenhuma_evidencia_adequada_com_cobertura_minima",),
            )

        conflitos: list[tuple[str, str]] = []
        for indice, esquerda in enumerate(sinais):
            for direita in sinais[indice + 1 :]:
                cobertura = len((esquerda.termos & direita.termos) & claim_terms)
                if cobertura < self.min_termos:
                    continue
                if esquerda.positivo is False and direita.positivo is not False:
                    conflitos.append((esquerda.ref, direita.ref))
                elif direita.positivo is False and esquerda.positivo is not False:
                    conflitos.append((esquerda.ref, direita.ref))

        if conflitos:
            return ResultadoReconciliacao(
                StatusReconciliacao.CONFLITANTE,
                len(sinais),
                len({s.ref for s in sinais}),
                tuple(conflitos),
                ("sinais_de_polaridade_incompatíveis",),
            )

        if len(sinais) >= 2:
            return ResultadoReconciliacao(
                StatusReconciliacao.CORROBORADA,
                len(sinais),
                len({s.ref for s in sinais}),
                motivos=("duas_ou_mais_fontes_independentes_com_suporte_lexical",),
            )

        return ResultadoReconciliacao(
            StatusReconciliacao.NAO_CORROBORADA,
            len(sinais),
            len({s.ref for s in sinais}),
            motivos=("apenas_uma_fonte_independente_com_suporte",),
        )
