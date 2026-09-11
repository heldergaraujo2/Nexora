"""Carregamento declarativo de politicas a partir de TOML."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from nexora.config.loaders import ConfiguracaoInvalida, carregar_toml
from nexora.governanca.policy import EfeitoPolitica, PolicyEngine, RegraPolitica


def carregar_policy_toml(caminho: Path) -> PolicyEngine:
    """Carrega um PolicyEngine a partir de um documento TOML versionado.

    Schema minimo:

        [policy]
        version = 1
        default = "deny"

        [[policy.rules]]
        effect = "allow"
        requester = "orchestrator"
        executor = "research-agent"
        task = "pesquisar"

    Apenas dados declarativos sao interpretados; nenhuma expressao ou codigo
    presente no arquivo e executado.
    """
    dados = carregar_toml(caminho)
    policy = dados.get("policy")
    if not isinstance(policy, dict):
        raise ConfiguracaoInvalida("seção [policy] obrigatoria")

    version = policy.get("version")
    if version != 1:
        raise ConfiguracaoInvalida("policy.version deve ser 1")

    default = policy.get("default", EfeitoPolitica.DENY.value)
    try:
        padrao = EfeitoPolitica(default)
    except (TypeError, ValueError) as exc:
        raise ConfiguracaoInvalida("policy.default deve ser 'allow' ou 'deny'") from exc

    regras_raw = policy.get("rules", [])
    if not isinstance(regras_raw, list):
        raise ConfiguracaoInvalida("policy.rules deve ser uma lista")

    regras: list[RegraPolitica] = []
    for indice, item in enumerate(regras_raw):
        if not isinstance(item, dict):
            raise ConfiguracaoInvalida(f"policy.rules[{indice}] deve ser uma tabela")
        desconhecidos = set(item) - {"effect", "requester", "executor", "task"}
        if desconhecidos:
            nomes = ", ".join(sorted(desconhecidos))
            raise ConfiguracaoInvalida(f"policy.rules[{indice}] possui campos desconhecidos: {nomes}")
        try:
            efeito = EfeitoPolitica(item["effect"])
        except (KeyError, TypeError, ValueError) as exc:
            raise ConfiguracaoInvalida(
                f"policy.rules[{indice}].effect deve ser 'allow' ou 'deny'"
            ) from exc

        campos = {"solicitante": "requester", "executor": "executor", "tarefa": "task"}
        valores: dict[str, Any] = {}
        for destino, origem in campos.items():
            valor = item.get(origem)
            if valor is not None and (not isinstance(valor, str) or not valor.strip()):
                raise ConfiguracaoInvalida(
                    f"policy.rules[{indice}].{origem} deve ser texto nao vazio"
                )
            valores[destino] = valor

        regras.append(RegraPolitica(efeito=efeito, **valores))

    return PolicyEngine(regras, padrao=padrao)


__all__ = ["carregar_policy_toml"]
