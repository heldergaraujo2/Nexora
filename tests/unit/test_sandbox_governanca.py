from __future__ import annotations

from unittest.mock import patch

import pytest

from nexora.auditoria.registro import RegistroAuditoria
from nexora.governanca.permissoes import GerenciadorPermissoes, PermissaoNegada
from nexora.governanca.policy import EfeitoPolitica, PolicyEngine, RegraPolitica
from nexora.runtime.sandbox import AcaoNegada, Sandbox


def _permissoes(efeito: EfeitoPolitica, auditoria: RegistroAuditoria | None = None) -> GerenciadorPermissoes:
    policy = PolicyEngine([
        RegraPolitica("sandbox", efeito, solicitante="agente", executor="sandbox", tarefa="echo"),
    ])
    return GerenciadorPermissoes(policy, auditoria=auditoria)


def test_sandbox_sem_politica_preserva_compatibilidade() -> None:
    sandbox = Sandbox(["echo"])
    with patch("nexora.runtime.sandbox.subprocess.run") as executar:
        executar.return_value.returncode = 0
        executar.return_value.stdout = "ok"
        executar.return_value.stderr = ""
        assert sandbox.executar("echo ola")["retorno"] == 0
        executar.assert_called_once()


def test_sandbox_com_policy_allow_executa() -> None:
    sandbox = Sandbox(["echo"], permissoes=_permissoes(EfeitoPolitica.ALLOW), solicitante="agente")
    with patch("nexora.runtime.sandbox.subprocess.run") as executar:
        executar.return_value.returncode = 0
        executar.return_value.stdout = "ok"
        executar.return_value.stderr = ""
        sandbox.executar("echo ola")
        executar.assert_called_once_with(["echo", "ola"], capture_output=True, text=True, timeout=30)


def test_sandbox_com_policy_deny_nao_executa() -> None:
    sandbox = Sandbox(["echo"], permissoes=_permissoes(EfeitoPolitica.DENY), solicitante="agente")
    with patch("nexora.runtime.sandbox.subprocess.run") as executar:
        with pytest.raises(PermissaoNegada):
            sandbox.executar("echo segredo")
        executar.assert_not_called()


def test_sandbox_allowlist_continua_negando_antes_da_policy() -> None:
    sandbox = Sandbox([], permissoes=_permissoes(EfeitoPolitica.ALLOW), solicitante="agente")
    with patch("nexora.runtime.sandbox.subprocess.run") as executar:
        with pytest.raises(AcaoNegada):
            sandbox.executar("echo ola")
        executar.assert_not_called()


def test_sandbox_policy_deny_audita_decisao() -> None:
    auditoria = RegistroAuditoria()
    sandbox = Sandbox(["echo"], permissoes=_permissoes(EfeitoPolitica.DENY, auditoria), solicitante="agente")
    with pytest.raises(PermissaoNegada):
        sandbox.executar("echo segredo")
    eventos = auditoria.listar(evento="permissao.decisao")
    assert len(eventos) == 1
    assert eventos[0]["dados"]["permitido"] is False
    assert eventos[0]["dados"]["recurso"] == "sandbox"
