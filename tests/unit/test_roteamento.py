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


class ProviderFalho(ProviderTeste):
    def generate(self, prompt: str, **kwargs):
        raise RuntimeError("falha de teste")


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


def test_manager_registra_historico_real_por_provider():
    manager = ProviderManager()
    manager.registrar("teste", ProviderTeste())
    for _ in range(3):
        manager.executar("teste", "ping")
    metricas = manager.estatisticas_provider("teste")
    assert metricas["chamadas"] == 3
    assert metricas["sucessos"] == 3
    assert metricas["erros"] == 0
    assert metricas["taxa_sucesso"] == 1.0
    assert metricas["taxa_erro"] == 0.0
    assert isinstance(metricas["latencia_media"], float)


def test_roteamento_usa_historico_de_sucesso_com_ajuste_limitado_e_explicavel():
    manager = ProviderManager()
    manager.registrar("alpha", ProviderTeste())
    manager.registrar("beta", ProviderTeste())
    for _ in range(3):
        manager.executar("alpha", "ping")

    candidatos = [
        {"provider": "beta", "modelo": "coder-7b", "perfil": perfil_modelo("coder-7b", contexto=32768, parametros="7B")},
        {"provider": "alpha", "modelo": "coder-7b", "perfil": perfil_modelo("coder-7b", contexto=32768, parametros="7B")},
    ]
    resultado = RoteadorInteligente(manager).selecionar(candidatos, hw(), tarefa="coding")
    assert resultado[0].provider == "alpha"
    assert "historico_alta_taxa_sucesso" in resultado[0].motivos
    assert resultado[0].score - resultado[1].score <= 1.5


def test_roteamento_penaliza_provider_com_alta_taxa_de_erro():
    manager = ProviderManager()
    manager.registrar("falho", ProviderFalho())
    manager.registrar("bom", ProviderTeste())
    for _ in range(3):
        try:
            manager.executar("falho", "ping")
        except RuntimeError:
            pass

    candidatos = [
        {"provider": "falho", "modelo": "coder-7b", "perfil": perfil_modelo("coder-7b", contexto=32768, parametros="7B")},
        {"provider": "bom", "modelo": "coder-7b", "perfil": perfil_modelo("coder-7b", contexto=32768, parametros="7B")},
    ]
    resultado = RoteadorInteligente(manager).selecionar(candidatos, hw(), tarefa="coding")
    assert resultado[0].provider == "bom"
    falho = next(item for item in resultado if item.provider == "falho")
    assert "historico_alta_taxa_erro" in falho.motivos


def test_roteamento_pode_desativar_uso_do_historico():
    manager = ProviderManager()
    manager.registrar("alpha", ProviderTeste())
    manager.registrar("beta", ProviderTeste())
    for _ in range(3):
        manager.executar("alpha", "ping")
    candidatos = [
        {"provider": "beta", "modelo": "coder-7b", "perfil": perfil_modelo("coder-7b", contexto=32768, parametros="7B")},
        {"provider": "alpha", "modelo": "coder-7b", "perfil": perfil_modelo("coder-7b", contexto=32768, parametros="7B")},
    ]
    resultado = RoteadorInteligente(manager).selecionar(candidatos, hw(), tarefa="coding", usar_historico=False)
    assert resultado[0].provider == "alpha"
    assert not any(item.motivos for item in resultado if item.provider == "alpha")
