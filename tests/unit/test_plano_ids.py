from nexora.core.plano import Tarefa


def test_tarefa_preserva_id_fornecido_pelo_planejador() -> None:
    tarefa = Tarefa("gerar resultado", id="t1")

    assert tarefa.id == "t1"
    assert tarefa.para_dict()["id"] == "t1"


def test_tarefa_gera_id_quando_planejador_nao_fornece_id() -> None:
    tarefa = Tarefa("gerar resultado")

    assert tarefa.id
    assert len(tarefa.id) == 32
