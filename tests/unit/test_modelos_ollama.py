from __future__ import annotations

from nexora.providers.modelos import DescobridorModelosOllama, ModeloLocal, perfil_modelo


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
    )
    modelos = DescobridorModelosOllama(provider).listar()
    assert modelos == [
        ModeloLocal("qwen2.5-coder:7b", 4700000000, "qwen2", "7.6B", 32768),
        ModeloLocal("modelo-sem-detalhes"),
    ]
    assert DescobridorModelosOllama(provider).nomes() == ["qwen2.5-coder:7b", "modelo-sem-detalhes"]


def test_perfil_identifica_modelo_de_codigo_sem_fixar_modelo():
    assert perfil_modelo("qwen2.5-coder:7b") == {"nome": "qwen2.5-coder:7b", "categoria": "coding"}
    assert perfil_modelo("llama3:8b") == {"nome": "llama3:8b", "categoria": "general"}
