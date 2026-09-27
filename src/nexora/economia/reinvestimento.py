"""Gate de reinvestimento econômico da NEXORA."""
from __future__ import annotations
from dataclasses import dataclass


@dataclass(frozen=True)
class PedidoReinvestimento:
    oportunidade_id: str
    valor: float
    beneficio_esperado: float
    risco: float
    autorizado_humano: bool = False


@dataclass(frozen=True)
class DecisaoReinvestimento:
    permitido: bool
    motivo: str


class GateReinvestimento:
    """Não movimenta recursos; apenas decide se um adaptador financeiro pode prosseguir."""

    def __init__(self, *, risco_maximo: float = 0.25, multiplicador_minimo: float = 1.0) -> None:
        if risco_maximo < 0 or multiplicador_minimo < 0:
            raise ValueError("limites inválidos")
        self.risco_maximo = risco_maximo
        self.multiplicador_minimo = multiplicador_minimo

    def decidir(self, pedido: PedidoReinvestimento) -> DecisaoReinvestimento:
        if pedido.valor <= 0:
            return DecisaoReinvestimento(False, "valor deve ser positivo")
        if pedido.risco > self.risco_maximo:
            return DecisaoReinvestimento(False, "risco acima do limite")
        if pedido.beneficio_esperado < pedido.valor * self.multiplicador_minimo:
            return DecisaoReinvestimento(False, "beneficio esperado abaixo do limite")
        if not pedido.autorizado_humano:
            return DecisaoReinvestimento(False, "efeito financeiro exige autorizacao humana")
        return DecisaoReinvestimento(True, "reinvestimento autorizado pelo gate")
