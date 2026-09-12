from __future__ import annotations

from nexora.providers.modelos import DescobridorModelosOllama, ModeloLocal, perfil_modelo, pontuar_modelo


class ProviderFake:
    def __init__(self, dados):
        self.dados = dados

    def listar_modelos(self):
        return self.dados


def test_descobridor_normaliza_modelos_ollama():
    provider = ProviderFake({
        "models": [{
            "name": "qwen2.5-coder:7b",
            "size": 4700000000,
            "details": {"family": "qwen2", "parameter_size": "7.6B"},
            "context_length": 32768,
        }, {"name": "modelo-sem-detalhes"}, "invalido"]
    })
    modelos = DescobridorModelosOllama(provider).listar()
    assert modelos == [
        ModeloLocal("qwen2.5-coder:7b", 4700000000, "qwen2", "7.6B", 32768),
        ModeloLocal("modelo-sem-detalhes"),
    ]


def test_perfil_modelo_deriva_capacidades_observaveis():
    perfil = perfil_modelo("qwen2.5-coder:7b", contexto=32768, parametros="7.6B")
    assert perfil.categoria == "coding"
    assert perfil.tamanho_parametros_b == 7.6
    assert perfil.contexto == 32768
    assert perfil.adequado_coding is True


def test_pontuacao_favorece_coding_e_respeita_limite():
    perfil = perfil_modelo("qwen2.5-coder:7b", contexto=32768, parametros="7.6B")
    assert pontuar_modelo(perfil, tarefa="coding", contexto_necessario=16000, limite_parametros_b=8) > 10
    assert pontuar_modelo(perfil, tarefa="coding", limite_parametros_b=4) < 0
