"""Testes do registro e calculo de precificacao."""

import pytest

from nexora.providers.pricing import PricingEntry, PricingRegistry


def test_pricing_calcula_custo_por_tokens():
    registry = PricingRegistry([
        PricingEntry(
            provider="groq",
            model="modelo-teste",
            currency="USD",
            input_per_million=0.15,
            output_per_million=0.60,
            version="teste-v1",
            effective_date="2026-09-12",
            source="https://example.invalid/pricing",
        )
    ])
    assert registry.calculate("groq", "modelo-teste", prompt_tokens=1_000_000, completion_tokens=2_000_000) == pytest.approx(1.35)


def test_pricing_desconhecido_retorna_none():
    registry = PricingRegistry()
    assert registry.calculate("groq", "sem-preco", prompt_tokens=10, completion_tokens=20) is None


def test_pricing_rejeita_preco_duplicado():
    entry = PricingEntry("groq", "modelo", "USD", 1.0, 2.0, "v1", "2026-09-12", "https://example.invalid")
    registry = PricingRegistry([entry])
    with pytest.raises(ValueError):
        registry.register(entry)


def test_pricing_rejeita_tokens_invalidos():
    registry = PricingRegistry()
    with pytest.raises(ValueError):
        registry.calculate("groq", "x", prompt_tokens=-1, completion_tokens=0)
