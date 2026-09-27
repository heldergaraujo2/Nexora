"""Memoria hibrida local-first inspirada em retrieval lexical, vetorial e grafico.

Implementacao original da NEXORA: nao depende de banco externo nem de modelo de embeddings.
Os adaptadores opcionais permitem conectar embeddings/grafo reais sem mudar o contrato.
"""
from __future__ import annotations

from dataclasses import dataclass, field
import math
import re
import time
from typing import Callable, Iterable, Sequence


@dataclass(frozen=True)
class Memoria:
    id: str
    texto: str
    tipo: str = "episodica"
    metadados: dict[str, object] = field(default_factory=dict)
    criado_em: float = field(default_factory=time.time)
    ultima_ativacao: float | None = None


@dataclass(frozen=True)
class ResultadoMemoria:
    memoria: Memoria
    score: float
    sinais: dict[str, float]


def _tokens(texto: str) -> list[str]:
    return re.findall(r"[\wÀ-ÿ]+", texto.lower())


class MemoriaHibrida:
    """Combina ranking lexical, semantico opcional, grafo opcional e RRF."""

    def __init__(
        self,
        *,
        semantic_search: Callable[[str, int], Sequence[tuple[str, float]]] | None = None,
        graph_search: Callable[[str, int], Sequence[tuple[str, float]]] | None = None,
        decay_half_life: float | None = 86400.0 * 30,
    ) -> None:
        if decay_half_life is not None and decay_half_life <= 0:
            raise ValueError("decay_half_life deve ser > 0")
        self._items: dict[str, Memoria] = {}
        self._semantic = semantic_search
        self._graph = graph_search
        self._half_life = decay_half_life

    def adicionar(self, memoria: Memoria) -> None:
        if not memoria.id.strip() or not memoria.texto.strip():
            raise ValueError("memoria exige id e texto nao vazios")
        self._items[memoria.id] = memoria

    def listar(self) -> list[Memoria]:
        return list(self._items.values())

    def _lexical(self, consulta: str, limite: int) -> list[tuple[str, float]]:
        q = set(_tokens(consulta))
        if not q:
            return []
        documentos = {mid: set(_tokens(m.texto)) for mid, m in self._items.items()}
        n = len(documentos)
        df = {t: sum(t in d for d in documentos.values()) for t in q}
        scores: list[tuple[str, float]] = []
        for mid, doc in documentos.items():
            if not doc:
                continue
            score = 0.0
            for token in q:
                if token in doc:
                    idf = math.log((n + 1) / (df[token] + 1)) + 1.0
                    score += idf
            if score:
                scores.append((mid, score))
        return sorted(scores, key=lambda x: (-x[1], x[0]))[:limite]

    @staticmethod
    def _rrf(rankings: Iterable[Sequence[tuple[str, float]]], k: int = 60) -> dict[str, float]:
        fused: dict[str, float] = {}
        for ranking in rankings:
            for rank, (mid, _score) in enumerate(ranking, start=1):
                fused[mid] = fused.get(mid, 0.0) + 1.0 / (k + rank)
        return fused

    def buscar(self, consulta: str, *, limite: int = 10) -> list[ResultadoMemoria]:
        if limite < 1:
            raise ValueError("limite deve ser >= 1")
        lexical = self._lexical(consulta, max(limite * 3, 10))
        semantic = list(self._semantic(consulta, max(limite * 3, 10))) if self._semantic else []
        graph = list(self._graph(consulta, max(limite * 3, 10))) if self._graph else []
        fused = self._rrf([lexical, semantic, graph])
        agora = time.time()
        resultados: list[ResultadoMemoria] = []
        for mid, base in fused.items():
            memoria = self._items.get(mid)
            if memoria is None:
                continue
            decay = 1.0
            if self._half_life and memoria.ultima_ativacao:
                idade = max(0.0, agora - memoria.ultima_ativacao)
                decay = 0.5 ** (idade / self._half_life)
            score = base * decay
            resultados.append(ResultadoMemoria(memoria, score, {
                "rrf": base,
                "decay": decay,
                "lexical": dict(lexical).get(mid, 0.0),
                "semantic": dict(semantic).get(mid, 0.0),
                "graph": dict(graph).get(mid, 0.0),
            }))
        resultados.sort(key=lambda r: (-r.score, r.memoria.id))
        return resultados[:limite]
