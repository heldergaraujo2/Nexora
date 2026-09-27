"""Telemetria GenAI independente de SDK externo, alinhada a conceitos OpenTelemetry."""
from __future__ import annotations

from dataclasses import dataclass, field
import time
from typing import Any


@dataclass
class SpanGenAI:
    nome: str
    tipo: str
    inicio: float = field(default_factory=time.time)
    fim: float | None = None
    atributos: dict[str, Any] = field(default_factory=dict)
    eventos: list[dict[str, Any]] = field(default_factory=list)
    erro: str | None = None

    @property
    def duracao(self) -> float | None:
        return None if self.fim is None else max(0.0, self.fim - self.inicio)

    def evento(self, nome: str, **atributos: Any) -> None:
        self.eventos.append({"nome": nome, "timestamp": time.time(), "atributos": dict(atributos)})

    def encerrar(self, *, erro: Exception | str | None = None) -> None:
        self.fim = time.time()
        self.erro = None if erro is None else str(erro)


class TracerGenAI:
    """Tracer in-memory que pode receber exporter posteriormente."""

    def __init__(self, exporter: Any | None = None) -> None:
        self._spans: list[SpanGenAI] = []
        self._exporter = exporter

    def iniciar(self, nome: str, tipo: str, **atributos: Any) -> SpanGenAI:
        span = SpanGenAI(nome=nome, tipo=tipo, atributos=dict(atributos))
        self._spans.append(span)
        return span

    def encerrar(self, span: SpanGenAI, *, erro: Exception | str | None = None) -> SpanGenAI:
        span.encerrar(erro=erro)
        if self._exporter is not None:
            self._exporter.exportar(span)
        return span

    def spans(self) -> list[SpanGenAI]:
        return list(self._spans)

    def limpar(self) -> None:
        self._spans.clear()
