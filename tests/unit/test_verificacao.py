"""Testes da verificacao de saidas."""
from nexora.runtime.verificacao import Verificacao, sem_erros, texto_nao_vazio


def test_verificacao_aplica_todos_os_criterios():
    verif = Verificacao(criterios=[texto_nao_vazio, sem_erros])
    assert verif.verificar({"saida": "ola", "erro": None})
    assert not verif.verificar({"saida": "", "erro": None})


def test_verificacao_adicionar_criterio():
    verif = Verificacao()
    verif.adicionar(texto_nao_vazio)
    assert verif.verificar({"saida": "x"})


def test_sem_erros_detecta_erro():
    assert sem_erros({"erro": None})
    assert not sem_erros({"erro": "falhou"})