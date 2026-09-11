from pathlib import Path

import pytest

from nexora.auditoria import RegistroAuditoria
from nexora.governanca import (
    EfeitoPolitica,
    GerenciadorPolitica,
    PolicyEngine,
    RegraPolitica,
)


def _policy(efeito: EfeitoPolitica, origem: str = "memory") -> PolicyEngine:
    return PolicyEngine(
        [RegraPolitica(id="rule", efeito=efeito, solicitante="agent", executor="tool", tarefa="run")],
        versao=2,
        origem=origem,
    )


def test_reload_troca_politica_somente_apos_validacao(tmp_path: Path) -> None:
    caminho = tmp_path / "policy.toml"
    caminho.write_text(
        """[policy]
version = 2
default = "deny"

[[policy.rules]]
id = "allow-run"
effect = "allow"
requester = "agent"
executor = "tool"
task = "run"
""",
        encoding="utf-8",
    )
    atual = _policy(EfeitoPolitica.DENY)
    manager = GerenciadorPolitica(atual)

    nova = manager.reload(caminho)

    assert manager.policy is nova
    assert manager.fingerprint == nova.fingerprint
    assert nova.decidir(solicitante="agent", executor="tool", tarefa="run").permitido


def test_reload_invalido_preserva_politica_anterior(tmp_path: Path) -> None:
    caminho = tmp_path / "policy.toml"
    caminho.write_text("[policy]\nversion = 1\n", encoding="utf-8")
    atual = _policy(EfeitoPolitica.ALLOW)
    manager = GerenciadorPolitica(atual)
    fingerprint_anterior = manager.fingerprint

    with pytest.raises(Exception):
        manager.reload(caminho)

    assert manager.fingerprint == fingerprint_anterior
    assert manager.policy is atual


def test_reload_audita_aplicacao_e_fingerprints(tmp_path: Path) -> None:
    caminho = tmp_path / "policy.toml"
    caminho.write_text('[policy]\nversion = 2\ndefault = "deny"\n', encoding="utf-8")
    auditoria = RegistroAuditoria(tmp_path / "audit.jsonl")
    atual = _policy(EfeitoPolitica.ALLOW)
    manager = GerenciadorPolitica(atual, auditoria=auditoria)

    nova = manager.reload(caminho)
    eventos = auditoria.listar(evento="politica.reload.aplicado")

    assert len(eventos) == 1
    assert eventos[0]["dados"]["fingerprint_anterior"] == atual.fingerprint
    assert eventos[0]["dados"]["fingerprint_novo"] == nova.fingerprint
    assert eventos[0]["dados"]["versao_nova"] == 2


def test_reload_rejeitado_audita_erro_e_preserva_estado(tmp_path: Path) -> None:
    caminho = tmp_path / "policy.toml"
    caminho.write_text('[policy]\nversion = 2\nunknown = "x"\n', encoding="utf-8")
    auditoria = RegistroAuditoria(tmp_path / "audit.jsonl")
    atual = _policy(EfeitoPolitica.ALLOW)
    manager = GerenciadorPolitica(atual, auditoria=auditoria)

    with pytest.raises(Exception):
        manager.reload(caminho)

    eventos = auditoria.listar(evento="politica.reload.rejeitado")
    assert len(eventos) == 1
    assert eventos[0]["dados"]["fingerprint_anterior"] == atual.fingerprint
    assert eventos[0]["dados"]["fingerprint_novo"] is None
    assert eventos[0]["dados"]["erro"]
    assert manager.policy is atual
