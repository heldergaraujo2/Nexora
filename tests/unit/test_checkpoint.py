from __future__ import annotations

from nexora.auditoria import RegistroAuditoria
from nexora.runtime.checkpoint import CheckpointEngine


def test_cria_checkpoint_e_isola_estado() -> None:
    engine = CheckpointEngine()
    estado = {"etapa": "planejar", "dados": {"tentativa": 1}}

    checkpoint = engine.criar("exec-1", estado)
    estado["dados"]["tentativa"] = 99

    assert checkpoint.execucao_id == "exec-1"
    assert checkpoint.motivo == "antes_da_acao"
    assert checkpoint.estado["dados"]["tentativa"] == 1


def test_recuperar_retorna_copia_sem_mutar_checkpoint() -> None:
    engine = CheckpointEngine()
    checkpoint = engine.criar("exec-1", {"contador": 1})

    recuperado = engine.recuperar(checkpoint.id)
    recuperado["contador"] = 2

    assert engine.obter(checkpoint.id).estado["contador"] == 1


def test_listar_filtra_por_execucao() -> None:
    engine = CheckpointEngine()
    primeiro = engine.criar("exec-1", {"n": 1})
    segundo = engine.criar("exec-2", {"n": 2})

    encontrados = engine.listar(execucao_id="exec-1")

    assert [item.id for item in encontrados] == [primeiro.id]
    assert encontrados[0].estado == {"n": 1}
    assert segundo.id not in {item.id for item in encontrados}


def test_checkpoint_audita_criacao_e_recuperacao(tmp_path) -> None:
    auditoria = RegistroAuditoria(tmp_path / "audit.jsonl")
    engine = CheckpointEngine(auditoria=auditoria)
    checkpoint = engine.criar("exec-1", {"estado": "seguro"}, motivo="antes_tool")

    assert engine.recuperar(checkpoint.id) == {"estado": "seguro"}

    registros = auditoria.listar(entidade="checkpoint", entidade_id=checkpoint.id)
    assert [item["evento"] for item in registros] == [
        "checkpoint.criado",
        "checkpoint.recuperado",
    ]
    assert registros[0]["dados"]["execucao_id"] == "exec-1"


def test_rejeita_identificadores_e_estado_invalidos() -> None:
    engine = CheckpointEngine()

    for execucao_id in ("", "   "):
        try:
            engine.criar(execucao_id, {})
        except ValueError:
            pass
        else:
            raise AssertionError("execucao_id vazio deveria falhar")

    try:
        engine.criar("exec-1", [])  # type: ignore[arg-type]
    except TypeError:
        pass
    else:
        raise AssertionError("estado nao-dict deveria falhar")

    try:
        engine.obter("inexistente")
    except KeyError:
        pass
    else:
        raise AssertionError("checkpoint inexistente deveria falhar")
