"""Testes do Objetivo (core.."""
from nexora.core.objetivo import Objetivo


def test_objetivo_cria_com_id_e_texto():
    objetivo = Objetivo("Comprar cafe")
    assert objetivo.texto == "Comprar cafe"
    assert objetivo.id


def test_objetivo_remove_espacos():
    assert Objetivo("  limpar , mesa  ").texto == "limpar , mesa"


def test_objetivo_para_dict_redondo():
    objetivo = Objetivo("Ler livro", objetivos_secundarios=["comprar"])
    dados = objetivo.para_dict()
    assert dados["texto"] == "Ler livro"
    assert dados["objetivos_secundarios"] == ["comprar"]
    assert dados["sucesso"] is None