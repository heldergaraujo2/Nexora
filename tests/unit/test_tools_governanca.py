"""Testes da integracao entre ferramentas e governanca."""
from __future__ import annotations

from nexora.governanca import EfeitoPolitica, GerenciadorPermissoes, PolicyEngine, RegraPolitica, PermissaoNegada
from nexora.tools.registry import Ferramenta, RegistryFerramentas


def test_registry_sem_policy_preserva_execucao_existente() -> None:
    chamadas: list[dict[str, object]] = []
    registry = RegistryFerramentas()
    registry.registrar(Ferramenta("echo", "teste", lambda parametros: chamadas.append(parametros) or "ok"))

    resultado = registry.executar("echo", {"valor": 1})

    assert resultado == "ok"
    assert chamadas == [{"valor": 1}]


def test_registry_allow_executa_ferramenta() -> None:
    chamadas: list[dict[str, object]] = []
    policy = PolicyEngine(
        [
            RegraPolitica(
                id="allow-echo",
                efeito=EfeitoPolitica.ALLOW,
                solicitante="agent",
                executor="echo",
                tarefa="executar",
            )
        ]
    )
    registry = RegistryFerramentas(GerenciadorPermissoes(policy))
    registry.registrar(Ferramenta("echo", "teste", lambda parametros: chamadas.append(parametros) or "ok"))

    resultado = registry.executar("echo", {"valor": 2}, solicitante="agent")

    assert resultado == "ok"
    assert chamadas == [{"valor": 2}]


def test_registry_deny_nao_invoca_executor() -> None:
    chamadas: list[dict[str, object]] = []
    registry = RegistryFerramentas(GerenciadorPermissoes(PolicyEngine()))
    registry.registrar(Ferramenta("terminal", "teste", lambda parametros: chamadas.append(parametros) or "nao deveria"))

    try:
        registry.executar("terminal", {"comando": "whoami"}, solicitante="agent")
    except PermissaoNegada:
        pass
    else:
        raise AssertionError("A execucao deveria ser negada pela policy")

    assert chamadas == []
