from nexora.providers.modelos import perfil_modelo
from nexora.runtime.hardware import PerfilHardware
from nexora.runtime.modelos import avaliar_modelo, estimar_memoria_modelo_bytes


def hardware(ram_gb=16, cpu=8):
    return PerfilHardware("Windows", "AMD64", cpu, ram_gb * 1024**3)


def test_estimativa_memoria_e_deterministica():
    assert estimar_memoria_modelo_bytes(7.0) == 7_000_000_000
    assert estimar_memoria_modelo_bytes(0) == 0


def test_modelo_adequado_quando_contexto_e_memoria_cabem():
    perfil = perfil_modelo("qwen2.5-coder:7b", contexto=32768, parametros="7B")
    resultado = avaliar_modelo("qwen2.5-coder:7b", perfil, hardware(), tarefa="coding", contexto_necessario=16000)
    assert resultado.adequado is True
    assert resultado.score > 0
    assert resultado.motivos == ()


def test_modelo_inadequado_quando_contexto_nao_suporta_tarefa():
    perfil = perfil_modelo("coder-small", contexto=4096, parametros="3B")
    resultado = avaliar_modelo("coder-small", perfil, hardware(), tarefa="coding", contexto_necessario=8192)
    assert resultado.adequado is False
    assert "contexto_insuficiente" in resultado.motivos


def test_modelo_inadequado_quando_estimativa_excede_ram():
    perfil = perfil_modelo("coder-large", contexto=32768, parametros="32B")
    resultado = avaliar_modelo("coder-large", perfil, hardware(ram_gb=16), tarefa="coding")
    assert resultado.adequado is False
    assert "modelo_maior_que_ram" in resultado.motivos
