"""Knowledge Graph temporal deterministico para o World Model da NEXORA."""
from __future__ import annotations

from dataclasses import dataclass, field
import time
from typing import Iterable


@dataclass(frozen=True)
class Entidade:
    id: str
    tipo: str
    atributos: dict[str, object] = field(default_factory=dict)


@dataclass(frozen=True)
class FatoTemporal:
    id: str
    sujeito: str
    relacao: str
    objeto: str
    valido_desde: float
    valido_ate: float | None = None
    fonte: str | None = None
    metadados: dict[str, object] = field(default_factory=dict)

    def ativo_em(self, instante: float) -> bool:
        return self.valido_desde <= instante and (self.valido_ate is None or instante < self.valido_ate)


class GrafoTemporal:
    """Grafo append-friendly com validade temporal explícita."""

    def __init__(self) -> None:
        self._entidades: dict[str, Entidade] = {}
        self._fatos: dict[str, FatoTemporal] = {}

    def registrar_entidade(self, entidade: Entidade) -> None:
        if not entidade.id.strip() or not entidade.tipo.strip():
            raise ValueError("entidade exige id e tipo")
        self._entidades[entidade.id] = entidade

    def registrar_fato(self, fato: FatoTemporal) -> None:
        if not fato.id.strip() or not fato.sujeito.strip() or not fato.relacao.strip() or not fato.objeto.strip():
            raise ValueError("fato exige identificadores e relacao")
        if fato.valido_ate is not None and fato.valido_ate < fato.valido_desde:
            raise ValueError("valido_ate nao pode ser anterior a valido_desde")
        self._fatos[fato.id] = fato

    def encerrar_fato(self, fato_id: str, instante: float | None = None) -> FatoTemporal:
        atual = self._fatos[fato_id]
        fim = time.time() if instante is None else instante
        if fim < atual.valido_desde:
            raise ValueError("instante de encerramento invalido")
        novo = FatoTemporal(atual.id, atual.sujeito, atual.relacao, atual.objeto, atual.valido_desde, fim, atual.fonte, dict(atual.metadados))
        self._fatos[fato_id] = novo
        return novo

    def consultar(
        self,
        *,
        sujeito: str | None = None,
        relacao: str | None = None,
        objeto: str | None = None,
        em: float | None = None,
    ) -> list[FatoTemporal]:
        instante = time.time() if em is None else em
        fatos: Iterable[FatoTemporal] = self._fatos.values()
        fatos = (
            f for f in fatos
            if (sujeito is None or f.sujeito == sujeito)
            and (relacao is None or f.relacao == relacao)
            and (objeto is None or f.objeto == objeto)
            and f.ativo_em(instante)
        )
        return sorted(fatos, key=lambda f: (f.valido_desde, f.id), reverse=True)

    def entidades(self) -> list[Entidade]:
        return sorted(self._entidades.values(), key=lambda e: e.id)

    def fatos(self) -> list[FatoTemporal]:
        return sorted(self._fatos.values(), key=lambda f: f.id)
