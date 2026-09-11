import pytest

from nexora.auditoria import RegistroAuditoria
from nexora.comunicacao import CommunicationBus, DelegadorAgentes, EstadoDelegacao, ExecutorDelegacoes
from nexora.governanca import EfeitoPolitica, PolicyEngine, RegraPolitica


def test_policy_engine_allow_por_regra():
    policy = PolicyEngine(
        [RegraPolitica("allow-research", EfeitoPolitica.ALLOW, solicitante="orchestrator", executor="research-agent")]
    )

    decisao = policy.decidir(
        solicitante="orchestrator",
        executor="research-agent",
        tarefa="pesquisar",
    )

    assert decisao.efeito is EfeitoPolitica.ALLOW
    assert decisao.permitido is True
    assert decisao.regra_id == "allow-research"
    assert decisao.versao == 1
    assert decisao.origem is None


def test_policy_engine_deny_por_padrao():
    policy = PolicyEngine(
        [RegraPolitica("allow-research", EfeitoPolitica.ALLOW, executor="research-agent")]
    )

    decisao = policy.decidir(
        solicitante="unknown",
        executor="coding-agent",
        tarefa="executar",
    )

    assert decisao.efeito is EfeitoPolitica.DENY
    assert decisao.permitido is False
    assert decisao.regra_id is None


def test_policy_engine_preserva_versao_e_origem():
    policy = PolicyEngine(versao=3, origem="config/policy.toml")

    decisao = policy.decidir(
        solicitante="orchestrator",
        executor="research-agent",
        tarefa="pesquisar",
    )

    assert decisao.versao == 3
    assert decisao.origem == "config/policy.toml"
    assert decisao.regra_id is None


def test_policy_engine_rejeita_id_duplicado():
    with pytest.raises(ValueError, match="ids de regras devem ser unicos"):
        PolicyEngine(
            [
                RegraPolitica("mesma-regra", EfeitoPolitica.ALLOW),
                RegraPolitica("mesma-regra", EfeitoPolitica.DENY),
            ]
        )


def test_policy_engine_rejeita_id_vazio():
    with pytest.raises(ValueError, match="id deve ser texto nao vazio"):
        RegraPolitica("   ", EfeitoPolitica.ALLOW)


def test_executor_permite_execucao_e_audita_decisao(tmp_path):
    bus = CommunicationBus()
    delegador = DelegadorAgentes(bus)
    auditoria = RegistroAuditoria(tmp_path / "audit.jsonl")
    policy = PolicyEngine(
        [RegraPolitica("allow-research", EfeitoPolitica.ALLOW, solicitante="orchestrator", executor="research-agent")],
        versao=2,
        origem="config/policy.toml",
    )
    executor = ExecutorDelegacoes(bus, delegador, auditoria=auditoria, policy=policy)
    chamadas = []
    executor.registrar("research-agent", lambda delegacao: chamadas.append(delegacao.id) or {"ok": True})

    delegacao = delegador.delegar(
        solicitante="orchestrator",
        executor="research-agent",
        tarefa="pesquisar",
    )

    assert delegacao.estado is EstadoDelegacao.CONCLUIDA
    assert chamadas == [delegacao.id]
    eventos = auditoria.listar(entidade_id=delegacao.id)
    assert eventos[0]["evento"] == "politica.decisao"
    assert eventos[0]["dados"]["efeito"] == "allow"
    assert eventos[0]["dados"]["permitido"] is True
    assert eventos[0]["dados"]["regra_id"] == "allow-research"
    assert eventos[0]["dados"]["versao"] == 2
    assert eventos[0]["dados"]["origem"] == "config/policy.toml"
    assert [item["evento"] for item in eventos] == [
        "politica.decisao",
        "delegacao.aceita",
        "delegacao.concluida",
    ]


def test_executor_negar_execucao_e_audita_decisao(tmp_path):
    bus = CommunicationBus()
    delegador = DelegadorAgentes(bus)
    auditoria = RegistroAuditoria(tmp_path / "audit.jsonl")
    policy = PolicyEngine(
        [RegraPolitica("deny-coding", EfeitoPolitica.DENY, solicitante="orchestrator", executor="coding-agent")],
        versao=4,
        origem="governanca/policy.toml",
    )
    executor = ExecutorDelegacoes(bus, delegador, auditoria=auditoria, policy=policy)
    chamadas = []
    executor.registrar("coding-agent", lambda delegacao: chamadas.append(delegacao.id))

    delegacao = delegador.delegar(
        solicitante="orchestrator",
        executor="coding-agent",
        tarefa="executar codigo",
    )

    assert delegacao.estado is EstadoDelegacao.FALHOU
    assert chamadas == []
    assert "execucao negada pela politica" in delegacao.erro
    eventos = auditoria.listar(entidade_id=delegacao.id)
    assert eventos[0]["evento"] == "politica.decisao"
    assert eventos[0]["dados"]["efeito"] == "deny"
    assert eventos[0]["dados"]["permitido"] is False
    assert eventos[0]["dados"]["regra_id"] == "deny-coding"
    assert eventos[0]["dados"]["versao"] == 4
    assert eventos[0]["dados"]["origem"] == "governanca/policy.toml"
    assert [item["evento"] for item in eventos] == [
        "politica.decisao",
        "delegacao.falhou",
    ]
