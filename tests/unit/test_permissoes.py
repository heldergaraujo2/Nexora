"""Testes da fronteira de permissao da NEXORA."""
from __future__ import annotations

from pathlib import Path

import pytest

from nexora.auditoria import RegistroAuditoria
from nexora.governanca import (
    EfeitoPolitica,
    GerenciadorPermissoes,
    PedidoPermissao,
    PermissaoNegada,
    PolicyEngine,
    RegraPolitica,
)


def test_permissao_allow() -> None:
    policy = PolicyEngine(
        [
            RegraPolitica(
                id="allow-build",
                efeito=EfeitoPolitica.ALLOW,
                solicitante="coding-agent",
                executor="terminal",
                tarefa="build",
            )
        ]
    )
    pedido = PedidoPermissao("coding-agent", "terminal", "build")

    decisao = GerenciadorPermissoes(policy).verificar(pedido)

    assert decisao.permitido is True
    assert decisao.regra_id == "allow-build"


def test_permissao_default_deny() -> None:
    policy = PolicyEngine()
    pedido = PedidoPermissao("coding-agent", "terminal", "shell")

    decisao = GerenciadorPermissoes(policy).verificar(pedido)

    assert decisao.permitido is False
    assert decisao.efeito is EfeitoPolitica.DENY


def test_permissao_exigir_interrompe_execucao() -> None:
    policy = PolicyEngine()
    pedido = PedidoPermissao("coding-agent", "terminal", "shell")

    with pytest.raises(PermissaoNegada):
        GerenciadorPermissoes(policy).exigir(pedido)


def test_permissao_audita_decisao(tmp_path: Path) -> None:
    auditoria = RegistroAuditoria(tmp_path / "auditoria.jsonl")
    policy = PolicyEngine(
        [
            RegraPolitica(
                id="allow-research",
                efeito=EfeitoPolitica.ALLOW,
                solicitante="orchestrator",
                executor="research-agent",
                tarefa="pesquisar",
            )
        ],
        versao=2,
        origem="policy.toml",
    )
    pedido = PedidoPermissao("orchestrator", "research-agent", "pesquisar", {"fonte": "web"})

    decisao = GerenciadorPermissoes(policy, auditoria=auditoria).verificar(pedido)
    eventos = auditoria.listar(evento="permissao.decisao")

    assert decisao.permitido is True
    assert len(eventos) == 1
    assert eventos[0].dados["regra_id"] == "allow-research"
    assert eventos[0].dados["versao"] == 2
    assert eventos[0].dados["fingerprint"] == policy.fingerprint
    assert eventos[0].dados["contexto"] == {"fonte": "web"}


def test_pedido_permissao_valida_campos() -> None:
    with pytest.raises(ValueError):
        PedidoPermissao("", "terminal", "shell")
    with pytest.raises(ValueError):
        PedidoPermissao("agent", "", "shell")
    with pytest.raises(ValueError):
        PedidoPermissao("agent", "terminal", "")
