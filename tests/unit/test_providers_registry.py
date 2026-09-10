"""Testes do registry de providers."""
import pytest

from nexora.providers.registry import ProviderDesconhecido, RegistryProviders


def test_registry_registra_e_obtem():
    repo = RegistryProviders()
    repo.registrar("groq", lambda: "groq")
    assert repo.obter("GROQ")() == "groq"


def test_registry_obter_desconhecido_levanta():
    repo = RegistryProviders()
    with pytest.raises(ProviderDesconhecido):
        repo.obter("nao-existe")


def test_registry_remover():
    repo = RegistryProviders()
    repo.registrar("a", lambda: 1)
    repo.remover("A")
    assert repo.disponiveis() == []