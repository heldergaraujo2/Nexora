from nexora.comunicacao import CommunicationBus, DelegadorAgentes, EstadoDelegacao, ExecutorDelegacoes
from nexora.experiencia.registro import RegistroExperiencias


def test_executor_registra_experiencia_terminal_de_sucesso(tmp_path):
    bus = CommunicationBus()
    delegador = DelegadorAgentes(bus)
    experiencias = RegistroExperiencias(tmp_path / "experiencias.jsonl")
    executor = ExecutorDelegacoes(bus, delegador, experiencias=experiencias)

    executor.registrar("research-agent", lambda delegacao: {"ok": True})
    delegacao = delegador.delegar(
        solicitante="orchestrator",
        executor="research-agent",
        tarefa="pesquisar mercado",
    )

    registros = experiencias.listar()
    assert delegacao.estado is EstadoDelegacao.CONCLUIDA
    assert len(registros) == 1
    assert registros[0]["tipo_de_tarefa"] == "delegacao"
    assert registros[0]["sucesso"] is True
    assert registros[0]["metadados"]["delegacao_id"] == delegacao.id
    assert registros[0]["metadados"]["tentativas"] == 1


def test_executor_registra_apenas_resultado_terminal_apos_retry(tmp_path):
    bus = CommunicationBus()
    delegador = DelegadorAgentes(bus)
    experiencias = RegistroExperiencias(tmp_path / "experiencias.jsonl")
    executor = ExecutorDelegacoes(
        bus,
        delegador,
        max_tentativas=2,
        experiencias=experiencias,
    )
    chamadas = 0

    def handler(delegacao):
        nonlocal chamadas
        chamadas += 1
        if chamadas == 1:
            raise RuntimeError("falha transitoria")
        return {"ok": True}

    executor.registrar("research-agent", handler)
    delegacao = delegador.delegar(
        solicitante="orchestrator",
        executor="research-agent",
        tarefa="repetir pesquisa",
    )

    registros = experiencias.listar()
    assert delegacao.estado is EstadoDelegacao.CONCLUIDA
    assert delegacao.tentativas == 2
    assert len(registros) == 1
    assert registros[0]["sucesso"] is True
    assert registros[0]["metadados"]["tentativas"] == 2


def test_executor_registra_experiencia_terminal_de_falha(tmp_path):
    bus = CommunicationBus()
    delegador = DelegadorAgentes(bus)
    experiencias = RegistroExperiencias(tmp_path / "experiencias.jsonl")
    executor = ExecutorDelegacoes(bus, delegador, experiencias=experiencias)

    def handler(delegacao):
        raise RuntimeError("falha definitiva")

    executor.registrar("coding-agent", handler)
    delegacao = delegador.delegar(
        solicitante="orchestrator",
        executor="coding-agent",
        tarefa="executar codigo",
    )

    registros = experiencias.listar()
    assert delegacao.estado is EstadoDelegacao.FALHOU
    assert len(registros) == 1
    assert registros[0]["sucesso"] is False
    assert registros[0]["metadados"]["erro"] == "falha definitiva"
