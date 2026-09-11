import pytest

from nexora.config.loaders import ConfiguracaoInvalida, carregar_toml
from nexora.governanca import EfeitoPolitica
from nexora.governanca.policy_loader import carregar_policy_toml


def test_carregar_toml_valido(tmp_path):
    caminho = tmp_path / "nexora.toml"
    caminho.write_text('[app]\nname = "Nexora"\n', encoding="utf-8")

    dados = carregar_toml(caminho)

    assert dados == {"app": {"name": "Nexora"}}


def test_carregar_policy_toml_allow_e_deny(tmp_path):
    caminho = tmp_path / "policy.toml"
    caminho.write_text(
        """[policy]
version = 1
default = "deny"

[[policy.rules]]
effect = "allow"
requester = "orchestrator"
executor = "research-agent"
task = "pesquisar"

[[policy.rules]]
effect = "deny"
executor = "research-agent"
""",
        encoding="utf-8",
    )

    policy = carregar_policy_toml(caminho)

    allow = policy.decidir(
        solicitante="orchestrator",
        executor="research-agent",
        tarefa="pesquisar",
    )
    deny = policy.decidir(
        solicitante="unknown",
        executor="research-agent",
        tarefa="outra",
    )

    assert allow.efeito is EfeitoPolitica.ALLOW
    assert deny.efeito is EfeitoPolitica.DENY


def test_carregar_policy_toml_exige_versao_1(tmp_path):
    caminho = tmp_path / "policy.toml"
    caminho.write_text('[policy]\nversion = 2\n', encoding="utf-8")

    with pytest.raises(ConfiguracaoInvalida, match="policy.version"):
        carregar_policy_toml(caminho)


def test_carregar_policy_toml_rejeita_campo_desconhecido(tmp_path):
    caminho = tmp_path / "policy.toml"
    caminho.write_text(
        """[policy]
version = 1

[[policy.rules]]
effect = "allow"
requester = "orchestrator"
unknown = "valor"
""",
        encoding="utf-8",
    )

    with pytest.raises(ConfiguracaoInvalida, match="campos desconhecidos"):
        carregar_policy_toml(caminho)


def test_carregar_policy_toml_rejeita_efeito_invalido(tmp_path):
    caminho = tmp_path / "policy.toml"
    caminho.write_text(
        """[policy]
version = 1

[[policy.rules]]
effect = "execute"
""",
        encoding="utf-8",
    )

    with pytest.raises(ConfiguracaoInvalida, match="effect"):
        carregar_policy_toml(caminho)


def test_carregar_policy_toml_rejeita_toml_invalido(tmp_path):
    caminho = tmp_path / "policy.toml"
    caminho.write_text('[policy\nversion = 1\n', encoding="utf-8")

    with pytest.raises(ConfiguracaoInvalida, match="TOML invalido"):
        carregar_policy_toml(caminho)
