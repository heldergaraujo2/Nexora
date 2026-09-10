"""Testes do registry de ferramentas."""
from nexora.tools.registry import Ferramenta, RegistryFerramentas


def test_registry_ferramentas_executa():
    def _soma(parametros: dict) -> int:
        return parametros["a"] + parametros["b"]

    repo = RegistryFerramentas()
    repo.registrar(Ferramenta(nome="soma", descricao="Soma dois numeros", executar=_soma))
    assert repo.obter("soma").descricao == "Soma dois numeros"
    assert repo.executar("soma", {"a": 2, "b": 3}) == 5

def test_registry_ferramentas_nomes_ordenados():
    repo = RegistryFerramentas()
    repo.registrar(Ferramenta(nome="zeta", descricao="", executar=lambda parametros: None))
    repo.registrar(Ferramenta(nome="alfa", descricao="", executar=lambda parametros: None))
    assert repo.nomes() == ["alfa", "zeta"]