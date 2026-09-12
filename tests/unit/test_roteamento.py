from nexora.providers.base import GenerationResult, Provider, ProviderCapability
from nexora.providers.manager import ProviderManager
from nexora.providers.modelos import perfil_modelo
from nexora.providers.roteamento import RoteadorInteligente
from nexora.runtime.hardware import PerfilHardware


def hw():
    return PerfilHardware("Windows", "AMD64", 8, 16 * 1024**3)


class ProviderTeste(Provider):
    def __init__(self, *, tool_calling=False, streaming=False, contexto=32768):
        super().__init__(
            "teste",
            ProviderCapability(
                tool_calling=tool_calling,
                streaming=streaming,
                max_context_tokens=contexto,
            ),
        )

    def generate(self, prompt: str, **kwargs):
        return GenerationResult(text=prompt)

    def saudavel(self):
        return True


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


def test_roteamento_respeita_tool_calling_declarado_pelo_provider():
    manager = ProviderManager()
    manager.registrar("sem-tool", ProviderTeste())
    manager.registrar("com-tool", ProviderTeste(tool_calling=True))
    candidatos = [
        {"provider": "sem-tool", "modelo": "coder-7b", "perfil": perfil_modelo("coder-7b", contexto=32768, parametros="7B")},
        {"provider": "com-tool", "modelo": "coder-7b", "perfil": perfil_modelo("coder-7b", contexto=32768, parametros="7B")},
    ]
    resultado = RoteadorInteligente(manager).selecionar(candidatos, hw(), tarefa="coding", exigir_tool_calling=True)
    assert resultado[0].provider == "com-tool"
    assert resultado[0].adequado is True
    assert "provider_sem_tool_calling" in resultado[1].motivos


def test_roteamento_rejeita_contexto_acima_do_limite_do_provider():
    manager = ProviderManager()
    manager.registrar("curto", ProviderTeste(contexto=8192))
    candidatos = [
        {"provider": "curto", "modelo": "coder-7b", "perfil": perfil_modelo("coder-7b", contexto=32768, parametros="7B")},
    ]
    resultado = RoteadorInteligente(manager).selecionar(candidatos, hw(), tarefa="coding", contexto_necessario=16000)
    assert resultado[0].adequado is False
    assert "provider_contexto_insuficiente" in resultado[0].motivos
