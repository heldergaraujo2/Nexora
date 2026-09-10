"""Testes do FakeProvider deterministico e auditavel."""
from nexora.providers.fake import FakeProvider


def test_fake_provider_gera_eco():
    provider = FakeProvider()
    resultado = provider.generate("ola")
    assert resultado.text == "[fake:ola]"


def test_fake_provider_usa_resposta_registrada():
    provider = FakeProvider()
    provider.registrar_resposta("pergunta", "resposta")
    assert provider.generate("pergunta").text == "resposta"


def test_fake_provider_audita_chamadas():
    provider = FakeProvider()
    provider.generate("a")
    provider.generate("b")
    assert len(provider.chamadas) == 2
    assert provider.chamadas[0]["prompt"] == "a"


def test_fake_provider_saudavel_e_fechar():
    provider = FakeProvider()
    assert provider.saudavel()is True
    provider.fechar()
    assert provider.chamadas == []
