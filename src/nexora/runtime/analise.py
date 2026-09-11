"""Classifica falhas de execucao para decidir retry/replan/abort."""
from __future__ import annotations

from typing import Any


class FalhaAnalisada:


    def __init__(self, tipo: str, retentavel: bool, plano: str, motivo: str = "") -> None:

        self.tipo = tipo
        self.retentavel = retentavel
        self.plano = plano
        self.motivo = motivo

    def para_dict(self) -> dict[str, Any]:

        return {"tipo": self.tipo, "retentavel": self.retentavel, "plano": self.plano, "motivo": self.motivo}



class AnalisadorFalhas:




    def analisar(self, observacao: Any) -> FalhaAnalisada:





        erro = None if observacao is None else getattr(observacao, "erro", None)

        texto = str(erro or "").lower()
        marcadores = ("timeout", "temporario", "sobrecarregado", "429", "500")
        retentavel = any(m in texto for m in marcadores) if texto else True

        tipo = "retentavel" if retentavel else "irreversivel"
        plano = "retry" if retentavel else "abort"
        return FalhaAnalisada(tipo=tipo, retentavel=retentavel, plano=plano, motivo=str(erro or ""))
