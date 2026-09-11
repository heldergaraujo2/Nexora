from nexora.auditoria import RegistroAuditoria
from nexora.comunicacao import CommunicationBus, DelegadorAgentes, EstadoDelegacao, ExecutorDelegacoes
from nexora.experiencia import RegistroExperiencias


def test_registro_auditoria_persiste_e_filtra(tmp_path):
    registro = RegistroAuditoria(tmp_path / "audit.jsonl")

    primeiro = registro.registrar(
        "delegacao.aceita",
        entidade="delegacao",
        entidade_id="abc",
        dados={"executor": "research-agent"},
    )
    registro.registrar(
        "delegacao.concluida",
        entidade="delegacao",
        entidade_id="abc",
        dados={"tentativas": 1},
    )

    assert primeiro["evento"] == "delegacao.aceita"
    assert len(registro.listar(entidade_id="abc")) == 2
    assert len(registro.listar(evento="delegacao.concluida")) == 1
    assert registro.listar(limite=1)[0]["evento"] == "delegacao.concluida"


def test_executor_audita_ciclo_terminal_e_experiencia(tmp_path):
    bus = CommunicationBus()
    delegador = DelegadorAgentes(bus)
    auditoria = RegistroAuditoria(tmp_path / "audit.jsonl")
    experiencias = RegistroExperiencias(tmp_path / "experiencias.jsonl")
    executor = ExecutorDelegacoes(
        bus,
        delegador,
        experiencias=experiencias,
        auditoria=auditoria,
    )
    executor.registrar("research-agent", lambda delegacao: {"ok": True})

    delegacao = delegador.delegar(
        solicitante="orchestrator",
        executor="research-agent",
        tarefa="pesquisar",
    )

    eventos = auditoria.listar(entidade_id=delegacao.id)
    assert [item["evento"] for item in eventos] == [
        "delegacao.aceita",
        "delegacao.concluida",
    ]
    assert experiencias.listar(tipo_de_tarefa="delegacao")[0]["sucesso"] is True
    assert delegacao.estado is EstadoDelegacao.CONCLUIDA


def test_executor_audita_falha_definitiva_sem_experiencia_intermediaria(tmp_path):
    bus = CommunicationBus()
    delegador = DelegadorAgentes(bus)
    auditoria = RegistroAuditoria(tmp_path / "audit.jsonl")
    experiencias = RegistroExperiencias(tmp_path / "experiencias.jsonl")
    executor = ExecutorDelegacoes(
        bus,
        delegador,
        max_tentativas=2,
        experiencias=experiencias,
        auditoria=auditoria,
    )
    executor.registrar("coding-agent", lambda delegacao: (_ for _ in ()).throw(RuntimeError("falhou")))

    delegacao = delegador.delegar(
        solicitante="orchestrator",
        executor="coding-agent",
        tarefa="executar",
    )

    eventos = auditoria.listar(entidade_id=delegacao.id)
    assert [item["evento"] for item in eventos] == [
        "delegacao.aceita",
        "delegacao.falhou",
    ]
    experiencia = experiencias.listar(tipo_de_tarefa="delegacao")[0]
    assert experiencia["sucesso"] is False
    assert experiencia["metadados"]["tentativas"] == 2
