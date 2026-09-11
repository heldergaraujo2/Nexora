"""Testes do Roteador de Provider (Fase 3)."""
from nexora.orquestracao.roteador import Roteador
from nexora.providers.fake import FakeProvider
from nexora.providers.registry import RegistryProviders

def _registry_com_fake():
    reg = RegistryProviders()
    reg.registrar("fake", lambda: FakeProvider())
    return reg


def test_recomendar_groq_para_objetivo_de_ia():
    reg = _registry_com_fake()
    rot = Roteador(reg)
    assert rot.recomendar("crie um texto de ia") == "groq"


def test_recomendar_fake_para_teste():
    reg = _registry_com_fake()
    rot = Roteador(reg)
    assert rot.recomendar("teste rapido") == "fake"


def test_default_usado_quando_sem_palavra_chave():
    reg = _registry_com_fake()
    rot = Roteador(reg)
    assert rot.recomendar("qualquer coisa neutra") == "fake"


def test_obter_provider_com_alias():
    reg = _registry_com_fake()
    rot = Roteador(reg)
    prov = rot.obter_provider("qualquer", alias="fake")
    assert isinstance(prov, FakeProvider)


def test_fallback_quando_recomendado_insaludavel():
    from nexora.providers.manager import ProviderManager

    class Insaludavel(FakeProvider):
        def saudavel(self):
            return False

    reg = RegistryProviders()
    mgr = ProviderManager()
    mgr.registrar("fake", FakeProvider)
    mgr.registrar("groq", Insaludavel)

    rot = Roteador(reg, manager=mgr)
    prov = rot.obter_provider("crie um texto")
    assert isinstance(prov, FakeProvider)

def test_fallback_todos_insaludaveis_levanta_erro():
    from nexora.providers.manager import ProviderManager
    import pytest

    class Insaludavel(FakeProvider):
        def saudavel(self):
            return False

    reg = RegistryProviders()
    mgr = ProviderManager()
    mgr.registrar("groq", Insaludavel)

    rot = Roteador(reg, manager=mgr)
    with pytest.raises(RuntimeError):
        rot.obter_provider("crie um texto")
