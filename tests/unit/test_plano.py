"""Testes do Plano (core.."""
from nexora.core.plano import Plano, Tarefa


def test_tarefa_cria_com_status_pendente():
    tarefa = Tarefa("Listar arquivos")
    assert tarefa.status == "pendente"
    assert tarefa.parametros == {}


def test_tarefa_para_dict():
    tarefa = Tarefa("Executar", ferramenta="bash")
    dados=tarefa.para_dict()
    assert dados["ferramenta"] == "bash"


def test_tarefa_preserva_chave_de_idempotencia():
    tarefa = Tarefa("Executar efeito", ferramenta="efeito", idempotencia_chave="op-123")
    assert tarefa.idempotencia_chave == "op-123"
    assert tarefa.para_dict()["idempotencia_chave"] == "op-123"


def test_plano_adiciona_e_lista_pendentes():
    plano = Plano(objetivo_id="obj-1")
    plano.adicionar_tarefa(Tarefa("a"))
    plano.adicionar_tarefa(Tarefa("b"))
    pendentes=plano.pendentes()
    assert len(pendentes) == 2
    assert plano.status == "planejado"