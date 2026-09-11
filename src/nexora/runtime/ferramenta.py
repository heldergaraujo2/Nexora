"""Contrato de resultado observado para execucao de ferramentas."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from nexora.runtime.observacao import Observacao


@dataclass(frozen=True)
class ResultadoFerramenta:
    """Resultado estruturado de uma ferramenta apos observacao e verificacao."""

    ferramenta: str
    execucao_id: str
    resultado: Any
    observacao: Observacao
    verificado: bool | None = None

    @property
    def sucesso(self) -> bool:
        """Indica se a ferramenta terminou sem erro e, quando verificada, foi aprovada."""
        return self.observacao.ok and self.verificado is not False
