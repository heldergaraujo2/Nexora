"""Testes do registry de ferramentas."""
from __future__ import annotations

import pytest

from nexora.auditoria.registro import RegistroAuditoria
from nexora.governanca.policy import EfeitoPolitica, PolicyEngine, RegraPolitica
from nexora.governanca.permissoes import GerenciadorPermissoes, PermissaoNegada
from nexora.runtime.checkpoint import CheckpointEngine
from nexora.runtime.ferramenta import ResultadoFerramenta
from nexora.runtime.verificacao import Verificacao, sem_erros, texto_nao_vazio
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


def test_registry_checkpoint_apos_allow_e_antes_da_execucao():
    ordem: list[str] = []
    checkpoint = CheckpointEngine()
    policy = PolicyEngine(
        [RegraPolitica(id="allow", efeito=EfeitoPolitica.ALLOW, solicitante="agente", executor="soma", tarefa="executar")],
    )
    permissoes = GerenciadorPermissoes(policy)
    repo = RegistryFerramentas(permissoes=permissoes, checkpoint=checkpoint)
    repo.registrar(
        Ferramenta(
            nome="soma",
            descricao="",
            executar=lambda parametros: ordem.append("tool") or 5,
        )
    )

    assert repo.executar("soma", {}, solicitante="agente", execucao_id="exec-1") == 5
    assert ordem == ["tool"]
    checkpoints = checkpoint.listar(execucao_id="exec-1")
    assert len(checkpoints) == 1
    assert checkpoints[0].estado == {
        "tipo": "ferramenta",
        "ferramenta": "soma",
        "solicitante": "agente",
        "contexto": {},
    }


def test_registry_policy_deny_nao_cria_checkpoint_nem_executa():
    executou: list[bool] = []
    checkpoint = CheckpointEngine()
    policy = PolicyEngine([])
    permissoes = GerenciadorPermissoes(policy)
    repo = RegistryFerramentas(permissoes=permissoes, checkpoint=checkpoint)
    repo.registrar(
        Ferramenta(
            nome="soma",
            descricao="",
            executar=lambda parametros: executou.append(True),
        )
    )

    try:
        repo.executar("soma", {}, solicitante="agente", execucao_id="exec-1")
    except PermissaoNegada:
        pass
    else:
        raise AssertionError("politica deny deveria impedir a ferramenta")

    assert executou == []
    assert checkpoint.listar(execucao_id="exec-1") == []


def test_registry_checkpoint_falhando_impede_execucao():
    executou: list[bool] = []

    class CheckpointQueFalha:
        def criar(self, *args, **kwargs):
            raise RuntimeError("checkpoint indisponivel")

    repo = RegistryFerramentas(checkpoint=CheckpointQueFalha())  # type: ignore[arg-type]
    repo.registrar(
        Ferramenta(
            nome="soma",
            descricao="",
            executar=lambda parametros: executou.append(True),
        )
    )

    try:
        repo.executar("soma", {})
    except RuntimeError as exc:
        assert str(exc) == "checkpoint indisponivel"
    else:
        raise AssertionError("falha do checkpoint deveria impedir a ferramenta")

    assert executou == []


def test_registry_observa_e_verifica_resultado_com_sucesso():
    observacoes: list[dict] = []
    verificador = Verificacao([texto_nao_vazio, sem_erros])

    def observar(contexto: dict) -> object:
        observacoes.append(contexto)
        from nexora.runtime.observacao import Observacao

        return Observacao(
            etapa_id=contexto["etapa_id"],
            ok=True,
            saida=contexto["saida"],
            metadados={"origem": "teste"},
        )

    repo = RegistryFerramentas(observador=observar, verificador=verificador)
    repo.registrar(Ferramenta(nome="eco", descricao="", executar=lambda parametros: "ok"))

    resultado = repo.executar("eco", {}, execucao_id="exec-observado")

    assert isinstance(resultado, ResultadoFerramenta)
    assert resultado.ferramenta == "eco"
    assert resultado.execucao_id == "exec-observado"
    assert resultado.resultado == "ok"
    assert resultado.observacao.ok is True
    assert resultado.verificado is True
    assert resultado.sucesso is True
    assert observacoes[0]["resultado"] == "ok"


def test_registry_verificacao_reprova_sem_impedir_execucao():
    verificador = Verificacao([texto_nao_vazio])
    repo = RegistryFerramentas(verificador=verificador)
    repo.registrar(Ferramenta(nome="vazio", descricao="", executar=lambda parametros: "   "))

    resultado = repo.executar("vazio", {}, execucao_id="exec-verificacao")

    assert isinstance(resultado, ResultadoFerramenta)
    assert resultado.resultado == "   "
    assert resultado.observacao.ok is True
    assert resultado.verificado is False
    assert resultado.sucesso is False


def test_registry_audita_resultado_apos_execucao(tmp_path):
    auditoria = RegistroAuditoria(tmp_path / "auditoria.jsonl")
    repo = RegistryFerramentas(auditoria=auditoria)
    repo.registrar(Ferramenta(nome="eco", descricao="", executar=lambda parametros: "ok"))

    assert repo.executar("eco", {}, solicitante="agente", execucao_id="exec-audit") == "ok"

    eventos = auditoria.listar(entidade_id="exec-audit")
    assert len(eventos) == 1
    assert eventos[0]["evento"] == "ferramenta.resultado"
    assert eventos[0]["dados"] == {
        "ferramenta": "eco",
        "solicitante": "agente",
        "sucesso": True,
        "observado": False,
        "verificado": None,
    }


def test_registry_audita_resultado_verificado(tmp_path):
    auditoria = RegistroAuditoria(tmp_path / "auditoria.jsonl")
    repo = RegistryFerramentas(
        auditoria=auditoria,
        verificador=Verificacao([texto_nao_vazio]),
    )
    repo.registrar(Ferramenta(nome="eco", descricao="", executar=lambda parametros: "ok"))

    resultado = repo.executar("eco", {}, execucao_id="exec-audit-verificado")

    assert resultado.sucesso is True
    evento = auditoria.listar(entidade_id="exec-audit-verificado")[0]
    assert evento["dados"]["observado"] is True
    assert evento["dados"]["observacao_ok"] is True
    assert evento["dados"]["verificado"] is True
    assert evento["dados"]["sucesso"] is True


def test_registry_audita_falha_da_ferramenta_e_propaga_excecao(tmp_path):
    auditoria = RegistroAuditoria(tmp_path / "auditoria.jsonl")
    repo = RegistryFerramentas(auditoria=auditoria)
    repo.registrar(
        Ferramenta(
            nome="falha",
            descricao="",
            executar=lambda parametros: (_ for _ in ()).throw(RuntimeError("boom")),
        )
    )

    with pytest.raises(RuntimeError, match="boom"):
        repo.executar("falha", {}, execucao_id="exec-falha")

    evento = auditoria.listar(entidade_id="exec-falha")[0]
    assert evento["evento"] == "ferramenta.falhou"
    assert evento["dados"]["erro_tipo"] == "RuntimeError"
    assert evento["dados"]["erro"] == "boom"
