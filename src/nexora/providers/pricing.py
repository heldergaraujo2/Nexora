"""Precificacao versionada para telemetria de custo da NEXORA.

Somente precos publicados por uma fonte autoritativa e identificados por
modelo sao aceitos. Ausencia de preco significa custo desconhecido (None),
nunca estimativa.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Iterable


@dataclass(frozen=True)
class PricingEntry:
    provider: str
    model: str
    currency: str
    input_per_million: float
    output_per_million: float
    version: str
    effective_date: str
    source: str

    def __post_init__(self) -> None:
        if not self.provider.strip() or not self.model.strip():
            raise ValueError("provider e model sao obrigatorios")
        if self.currency != "USD":
            raise ValueError("somente USD e suportado nesta versao")
        if self.input_per_million < 0 or self.output_per_million < 0:
            raise ValueError("precos nao podem ser negativos")
        date.fromisoformat(self.effective_date)
        if not self.version.strip() or not self.source.strip():
            raise ValueError("version e source sao obrigatorios")


class PricingRegistry:
    """Registro deterministico de precos publicados por provider/modelo."""

    def __init__(self, entries: Iterable[PricingEntry] = ()) -> None:
        self._entries: dict[tuple[str, str], PricingEntry] = {}
        for entry in entries:
            self.register(entry)

    def register(self, entry: PricingEntry) -> None:
        key = (entry.provider.strip().lower(), entry.model.strip())
        if key in self._entries:
            raise ValueError(f"preco ja registrado para {key[0]}/{key[1]}")
        self._entries[key] = entry

    def get(self, provider: str, model: str) -> PricingEntry | None:
        return self._entries.get((provider.strip().lower(), model.strip()))

    def calculate(self, provider: str, model: str, *, prompt_tokens: int, completion_tokens: int) -> float | None:
        if not isinstance(prompt_tokens, int) or prompt_tokens < 0:
            raise ValueError("prompt_tokens deve ser inteiro nao negativo")
        if not isinstance(completion_tokens, int) or completion_tokens < 0:
            raise ValueError("completion_tokens deve ser inteiro nao negativo")
        entry = self.get(provider, model)
        if entry is None:
            return None
        return ((prompt_tokens / 1_000_000) * entry.input_per_million) + ((completion_tokens / 1_000_000) * entry.output_per_million)

    def as_dict(self) -> dict[tuple[str, str], dict[str, object]]:
        return {
            key: {
                "currency": entry.currency,
                "input_per_million": entry.input_per_million,
                "output_per_million": entry.output_per_million,
                "version": entry.version,
                "effective_date": entry.effective_date,
                "source": entry.source,
            }
            for key, entry in self._entries.items()
        }


# Snapshot oficial usado pela NEXORA no momento da implementacao.
# Modelos Groq com preco publico por token. Modelos com "Contact Sales"
# permanecem deliberadamente ausentes e resultam em cost=None.
PRICING_REGISTRY = PricingRegistry(
    [
        PricingEntry(
            provider="groq",
            model="openai/gpt-oss-120b",
            currency="USD",
            input_per_million=0.15,
            output_per_million=0.60,
            version="groq-models-2026-09-12",
            effective_date="2026-09-12",
            source="https://console.groq.com/docs/models",
        ),
        PricingEntry(
            provider="groq",
            model="openai/gpt-oss-20b",
            currency="USD",
            input_per_million=0.075,
            output_per_million=0.30,
            version="groq-models-2026-09-12",
            effective_date="2026-09-12",
            source="https://console.groq.com/docs/models",
        ),
    ]
)
