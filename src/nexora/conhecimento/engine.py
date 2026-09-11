"""Conhecimento estruturado e rastreavel para a NEXORA."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable
import uuid


@dataclass(frozen=True)
class Conhecimento:
    """Unidade de conhecimento com origem, evidencias e confianca."""

    conteudo: str
    fonte: str
    confianca: float = 0.5
    escopo: str = "global"
    tags: tuple[str, ...] = ()
    evidencias: tuple[str, ...] = ()
    validado: bool = False
    id: str = field(default_factory=lambda: uuid.uuid4().hex)

    def __post_init__(self) -> None:
        if not self.conteudo.strip():
            raise ValueError("conteudo nao pode ser vazio")
        if not self.fonte.strip():
            raise ValueError("fonte nao pode ser vazia")
        if not 0.0 <= self.confianca <= 1.0:
            raise ValueError("confianca deve estar entre 0 e 1")

    def para_dict(self) -> dict[str, object]:
        return {
            "id": self.id,
            "conteudo": self.conteudo,
            "fonte": self.fonte,
            "confianca": self.confianca,
            "escopo": self.escopo,
            "tags": list(self.tags),
            "evidencias": list(self.evidencias),
            "validado": self.validado,
        }


class KnowledgeEngine:
    """Repositorio deterministico em memoria para conhecimento verificavel.

    A busca atual e lexical (texto/tags), deliberadamente sem alegar capacidades
    semanticas ou vetoriais. Backends persistentes e retrieval semantico podem
    ser adicionados posteriormente sem alterar o contrato basico.
    """

    def __init__(self) -> None:
        self._itens: dict[str, Conhecimento] = {}

    def adicionar(
        self,
        conteudo: str,
        *,
        fonte: str,
        confianca: float = 0.5,
        escopo: str = "global",
        tags: Iterable[str] = (),
        evidencias: Iterable[str] = (),
        validado: bool = False,
    ) -> Conhecimento:
        item = Conhecimento(
            conteudo=conteudo.strip(),
            fonte=fonte.strip(),
            confianca=confianca,
            escopo=escopo.strip() or "global",
            tags=tuple(tag.strip() for tag in tags if isinstance(tag, str) and tag.strip()),
            evidencias=tuple(
                evidencia.strip()
                for evidencia in evidencias
                if isinstance(evidencia, str) and evidencia.strip()
            ),
            validado=validado,
        )
        self._itens[item.id] = item
        return item

    def obter(self, conhecimento_id: str) -> Conhecimento | None:
        return self._itens.get(conhecimento_id)

    def listar(self, *, escopo: str | None = None) -> list[Conhecimento]:
        itens = list(self._itens.values())
        if escopo is not None:
            itens = [item for item in itens if item.escopo == escopo]
        return sorted(itens, key=lambda item: (-item.confianca, item.id))

    def buscar(self, termo: str, *, escopo: str | None = None, limite: int = 10) -> list[Conhecimento]:
        """Retorna conhecimento por correspondencia lexical, priorizando confianca."""
        termo_limpo = termo.strip().lower()
        if not termo_limpo:
            raise ValueError("termo nao pode ser vazio")
        if limite < 0:
            raise ValueError("limite deve ser >= 0")

        candidatos = []
        for item in self.listar(escopo=escopo):
            alvo = " ".join((item.conteudo, item.fonte, *item.tags)).lower()
            if termo_limpo in alvo:
                candidatos.append(item)
        return candidatos[:limite]

    def validar(self, conhecimento_id: str) -> Conhecimento:
        """Marca uma unidade existente como validada, preservando imutabilidade externa."""
        item = self._itens.get(conhecimento_id)
        if item is None:
            raise KeyError(conhecimento_id)
        atualizado = Conhecimento(
            conteudo=item.conteudo,
            fonte=item.fonte,
            confianca=item.confianca,
            escopo=item.escopo,
            tags=item.tags,
            evidencias=item.evidencias,
            validado=True,
            id=item.id,
        )
        self._itens[conhecimento_id] = atualizado
        return atualizado
