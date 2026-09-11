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


def test_registry_disponiveis_ordenados():
    repo = RegistryProviders()
    repo.registrar("zeta", lambda: 1)
    repo.registrar("alfa", lambda: 2)
    assert repo.disponiveis() == ["alfa", "zeta"]


def test_registry_registrar_substitui_mesmo_nome():
    repo = RegistryProviders()
    repo.registrar("groq", lambda: 1)
    repo.registrar("GROQ", lambda: 2)
    assert repo.obter("groq")() == 2


def test_registry_prioridade_padrao_eh_zero():
    repo = RegistryProviders()
    repo.registrar("fake", lambda: FakeProvider())
    assert repo.prioridade("fake") == 0


def test_registry_registrar_com_prioridade_e_ordena():
    repo = RegistryProviders()
    repo.registrar("zeta", lambda: "zeta", prioridade=10)
    repo.registrar("alfa", lambda: "alfa", prioridade=1)
    assert repo.nomes_por_prioridade() == ["alfa", "zeta"]


def test_registry_listar_por_capacidade_filtra():
    from nexora.providers.fake import FakeProvider
    repo = RegistryProviders()
    repo.registrar("fake", lambda: FakeProvider())
    repo.registrar("groq", lambda: "groq")
    assert "fake" in repo.listar_por_capacidade()
    assert "fake" in repo.listar_por_capacidade(tool_calling=True)
    assert "fake" not in repo.listar_por_capacidade(tool_calling=False)
