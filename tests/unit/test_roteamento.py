from nexora.providers.manager import ProviderManager
from nexora.providers.modelos import perfil_modelo
from nexora.providers.roteamento import RoteadorInteligente
from nexora.runtime.hardware import PerfilHardware


def hw():
    return PerfilHardware("Windows", "AMD64", 8, 16 * 1024**3)


def test_roteamento_prioriza_candidato_adequado_e_score():
    manager = ProviderManager()
    manager.registrar("ollama", object())
    manager.registrar("groq", object())
    candidatos = [
        {"provider": "groq", "modelo": "general-7b", "perfil": perfil_modelo("general-7b", contexto=32768, parametros="7B")},
        {"provider": "ollama", "modelo": "qwen-coder-7b", "perfil": perfil_modelo("qwen-coder-7b", contexto=32768, parametros="7B")},
    ]
    resultado = RoteadorInteligente(manager).selecionar(candidatos, hw(), tarefa="coding", contexto_necessario=16000)
    assert resultado[0].provider == "ollama"
    assert resultado[0].modelo == "qwen-coder-7b"


def test_roteamento_ignora_provider_nao_registrado_e_candidato_invalido():
    manager = ProviderManager()
    manager.registrar("ollama", object())
    candidatos = [
        {"provider": "desconhecido", "modelo": "x", "perfil": perfil_modelo("x")},
        {"provider": "ollama", "modelo": "", "perfil": perfil_modelo("x")},
    ]
    assert RoteadorInteligente(manager).selecionar(candidatos, hw()) == []
