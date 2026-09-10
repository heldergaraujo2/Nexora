"""Testes dos carregadores de configuracao.."""
import json

import pytest

from nexora.config.loaders import ConfiguracaoInvalida, carregar_ambiente, carregar_json


def test_carregar_json_le_objeto(tmp_path):
    caminho = tmp_path / "config.json"
    caminho.write_text(json.dumps({"modo": "teste"}), encoding="utf-8")
    assert carregar_json(caminho)["modo"] == "teste"


def test_carregar_json_invalido_levanta(tmp_path):
    caminho=tmp_path / "ruim.json"
    caminho.write_text("{quebrado", encoding="utf-8")
    with pytest.raises(ConfiguracaoInvalida):
        carregar_json(caminho)


def test_carregar_ambiente_respeita_prefixo(monkeypatch):
    monkeypatch.setenv("NEXORA_MODO", "seguro")
    monkeypatch.setenv("OUTRA_VARIAVEL", "1")
    dados=carregar_ambiente()
    assert dados == {"modo": "seguro"}