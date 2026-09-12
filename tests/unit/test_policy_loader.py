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
version = 2
default = "deny"

[[policy.rules]]
id = "allow-research"
effect = "allow"
requester = "orchestrator"
executor = "research-agent"
task = "pesquisar"

[[policy.rules]]
id = "deny-research"
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
    assert allow.regra_id == "allow-research"
    assert deny.efeito is EfeitoPolitica.DENY
    assert deny.regra_id == "deny-research"
    assert policy.versao == 2


def test_carregar_policy_toml_exige_versao_2(tmp_path):
    caminho = tmp_path / "policy.toml"
    caminho.write_text('[policy]\nversion = 1\n', encoding="utf-8")

    with pytest.raises(ConfiguracaoInvalida, match="policy.version"):
        carregar_policy_toml(caminho)


def test_carregar_policy_toml_rejeita_versao_boolean(tmp_path):
    caminho = tmp_path / "policy.toml"
    caminho.write_text('[policy]\nversion = true\n', encoding="utf-8")

    with pytest.raises(ConfiguracaoInvalida, match="policy.version"):
        carregar_policy_toml(caminho)


def test_carregar_policy_toml_rejeita_campo_desconhecido_no_policy(tmp_path):
    caminho = tmp_path / "policy.toml"
    caminho.write_text(
        """[policy]
version = 2
unknown = "valor"
""",
        encoding="utf-8",
    )

    with pytest.raises(ConfiguracaoInvalida, match=r"\[policy\].*campos desconhecidos"):
        carregar_policy_toml(caminho)


def test_carregar_policy_toml_rejeita_campo_desconhecido(tmp_path):
    caminho = tmp_path / "policy.toml"
    caminho.write_text(
        """[policy]
version = 2

[[policy.rules]]
id = "allow-research"
effect = "allow"
requester = "orchestrator"
unknown = "valor"
""",
        encoding="utf-8",
    )

    with pytest.raises(ConfiguracaoInvalida, match="campos desconhecidos"):
        carregar_policy_toml(caminho)


def test_carregar_policy_toml_rejeita_id_ausente(tmp_path):
    caminho = tmp_path / "policy.toml"
    caminho.write_text(
        """[policy]
version = 2

[[policy.rules]]
effect = "allow"
executor = "research-agent"
""",
        encoding="utf-8",
    )

    with pytest.raises(ConfiguracaoInvalida, match=r"\.id"):
        carregar_policy_toml(caminho)


def test_carregar_policy_toml_rejeita_id_duplicado(tmp_path):
    caminho = tmp_path / "policy.toml"
    caminho.write_text(
        """[policy]
version = 2

[[policy.rules]]
id = "duplicada"
effect = "allow"

[[policy.rules]]
id = "duplicada"
effect = "deny"
""",
        encoding="utf-8",
    )

    with pytest.raises(ConfiguracaoInvalida, match="ids de regras devem ser unicos"):
        carregar_policy_toml(caminho)


def test_carregar_policy_toml_rejeita_efeito_invalido(tmp_path):
    caminho = tmp_path / "policy.toml"
    caminho.write_text(
        """[policy]
version = 2

[[policy.rules]]
id = "invalid-effect"
effect = "execute"
""",
        encoding="utf-8",
    )

    with pytest.raises(ConfiguracaoInvalida, match="effect"):
        carregar_policy_toml(caminho)


def test_carregar_policy_toml_rejeita_toml_invalido(tmp_path):
    caminho = tmp_path / "policy.toml"
    caminho.write_text('[policy\nversion = 2\n', encoding="utf-8")

    with pytest.raises(ConfiguracaoInvalida, match="TOML invalido"):
        carregar_policy_toml(caminho)
