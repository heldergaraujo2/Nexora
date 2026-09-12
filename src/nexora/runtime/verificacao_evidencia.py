"""Verificação determinística e auditável da adequação de evidências de pesquisa.

Este módulo NÃO prova a verdade de uma afirmação. Ele apenas mede sinais
lexicais observáveis entre uma afirmação e o trecho da fonte citado.
"""
from __future__ import annotations

import re
from dataclasses import dataclass


_STOPWORDS = frozenset(
    "a ao aos as com da das de do dos e em entre essa esse estas estes foi for ha isso na nas no nos o os para por que se sem sua suas um uma umas uns".split()
)


@dataclass(frozen=True)
class AdequacaoEvidencia:
    """Resultado auditável de adequação, sem alegar prova semântica."""

    status: str
    cobertura: float
    termos_relevantes: tuple[str, ...] = ()
    termos_encontrados: tuple[str, ...] = ()
    motivo: str = ""

    def para_dict(self) -> dict[str, object]:
        return {
            "status": self.status,
            "cobertura": self.cobertura,
            "termos_relevantes": list(self.termos_relevantes),
            "termos_encontrados": list(self.termos_encontrados),
            "motivo": self.motivo,
        }


def _termos(texto: str) -> list[str]:
    tokens = re.findall(r"[\wÀ-ÿ]+", texto.casefold())
    return [token for token in tokens if len(token) >= 4 and token not in _STOPWORDS]


def verificar_adequacao(claim: str, trecho: str, *, limiar_sustentacao: float = 0.6) -> AdequacaoEvidencia:
    """Calcula cobertura lexical do claim pelo trecho citado.

    ``SUSTENTADA`` significa somente que o trecho contém uma proporção suficiente
    dos termos relevantes do claim. Não significa que a fonte seja verdadeira,
    atual ou semanticamente suficiente.
    """
    if not isinstance(claim, str) or not claim.strip():
        raise ValueError("claim deve ser texto não vazio")
    if not isinstance(trecho, str):
        raise TypeError("trecho deve ser texto")
    if not 0 < limiar_sustentacao <= 1:
        raise ValueError("limiar_sustentacao deve estar entre 0 e 1")

    relevantes = tuple(dict.fromkeys(_termos(claim)))
    disponiveis = set(_termos(trecho))
    encontrados = tuple(termo for termo in relevantes if termo in disponiveis)

    if not relevantes:
        return AdequacaoEvidencia("INDETERMINADA", 0.0, motivo="claim_sem_termos_relevantes")
    if not trecho.strip():
        return AdequacaoEvidencia("INDETERMINADA", 0.0, relevantes, encontrados, "trecho_vazio")

    cobertura = len(encontrados) / len(relevantes)
    if cobertura >= limiar_sustentacao:
        status = "SUSTENTADA"
        motivo = "cobertura_lexical_suficiente"
    elif cobertura == 0:
        status = "INSUFICIENTE"
        motivo = "nenhuma_sobreposicao_lexical"
    else:
        status = "INSUFICIENTE"
        motivo = "cobertura_lexical_insuficiente"
    return AdequacaoEvidencia(status, cobertura, relevantes, encontrados, motivo)
