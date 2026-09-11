"""Carregadores de configuracao (JSON, TOML e variaveis de ambiente)."""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any


class ConfiguracaoInvalida(ValueError):
    """Erro lancado quando o arquivo de configuracao e invalido."""


def carregar_json(caminho: Path) -> dict[str, Any]:
    """Le um arquivo JSON de configuracao e valida que seja um objeto."""

    if not caminho.exists():
        raise FileNotFoundError(f"Configuracao nao encontrada: {caminho}")
    try:
        dados = json.loads(caminho.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise ConfiguracaoInvalida(f"JSON invalido em {caminho}: {exc}") from exc
    if not isinstance(dados, dict):
        raise ConfiguracaoInvalida(f"Raiz do config deve ser objeto: {caminho}")
    return dados


def carregar_toml(caminho: Path) -> dict[str, Any]:
    """Le um arquivo TOML e valida que a raiz seja uma tabela.

    TOML e suportado pela biblioteca padrao a partir do Python 3.11.
    """
    if not caminho.exists():
        raise FileNotFoundError(f"Configuracao nao encontrada: {caminho}")
    try:
        import tomllib
    except ModuleNotFoundError as exc:
        raise ConfiguracaoInvalida(
            "carregar_toml requer Python 3.11 ou superior"
        ) from exc

    try:
        dados = tomllib.loads(caminho.read_text(encoding="utf-8"))
    except (tomllib.TOMLDecodeError, UnicodeDecodeError) as exc:
        raise ConfiguracaoInvalida(f"TOML invalido em {caminho}: {exc}") from exc
    if not isinstance(dados, dict):
        raise ConfiguracaoInvalida(f"Raiz do config deve ser tabela: {caminho}")
    return dados


def carregar_ambiente(prefixo: str = "NEXORA_") -> dict[str, Any]:
    """Le variaveis de ambiente com prefixo como secoes do config."""

    resultado: dict[str, Any] = {}
    for chave, valor in os.environ.items():
        if chave.startswith(prefixo):
            nome = chave[len(prefixo):].lower().replace("_", ".")
            resultado[nome] = valor
    return resultado
