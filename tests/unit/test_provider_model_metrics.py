from nexora.providers.base import GenerationResult, ProviderCapability
from nexora.providers.manager import ProviderManager
from nexora.providers.pricing import PricingEntry, PricingRegistry


class ProviderFake:
    name = "groq"

    def __init__(self, modelo: str, prompt_tokens: int = 100, completion_tokens: int = 100) -> None:
        self.modelo = modelo
        self.capabilities = ProviderCapability()
        self.prompt_tokens = prompt_tokens
        self.completion_tokens = completion_tokens

    def generate(self, prompt: str, **kwargs):
        return GenerationResult(
            text=f"ok:{self.modelo}",
            usage={
                "prompt_tokens": self.prompt_tokens,
                "completion_tokens": self.completion_tokens,
                "total_tokens": self.prompt_tokens + self.completion_tokens,
            },
        )


def registry() -> PricingRegistry:
    return PricingRegistry([
        PricingEntry("groq", "model-a", "USD", 1.0, 1.0, "test", "2026-09-12", "test"),
        PricingEntry("groq", "model-b", "USD", 2.0, 2.0, "test", "2026-09-12", "test"),
    ])


def test_metricas_por_modelo_nao_misturam_modelos(tmp_path):
    manager = ProviderManager(tmp_path / "history.json", registry())
    manager.registrar("groq", lambda **kwargs: ProviderFake(kwargs.get("modelo", "model-a")))

    for _ in range(3):
        manager.executar_instancia("groq", ProviderFake("model-a"), "x")
    for _ in range(3):
        manager.executar_instancia("groq", ProviderFake("model-b"), "x")

    a = manager.estatisticas_modelo("groq", "model-a")
    b = manager.estatisticas_modelo("groq", "model-b")
    provider = manager.estatisticas_provider("groq")

    assert a["chamadas"] == 3
    assert b["chamadas"] == 3
    assert a["total_tokens"] == 600
    assert b["total_tokens"] == 600
    assert a["geracoes_com_custo"] == 3
    assert b["geracoes_com_custo"] == 3
    assert b["custo_total"] > a["custo_total"]
    assert provider["chamadas"] == 6
    assert provider["geracoes_com_custo"] == 6


def test_metricas_por_modelo_sao_persistidas_e_recarregadas(tmp_path):
    path = tmp_path / "history.json"
    manager = ProviderManager(path, registry())
    manager.registrar("groq", lambda **kwargs: ProviderFake(kwargs.get("modelo", "model-a")))
    for _ in range(3):
        manager.executar_instancia("groq", ProviderFake("model-a"), "x")

    recarregado = ProviderManager(path, registry())
    dados = recarregado.estatisticas_modelo("groq", "model-a")
    assert dados["chamadas"] == 3
    assert dados["total_tokens"] == 600
    assert dados["geracoes_com_custo"] == 3


def test_falha_e_contabilizada_no_modelo(tmp_path):
    class Falho(ProviderFake):
        def generate(self, prompt: str, **kwargs):
            raise RuntimeError("falha")

    manager = ProviderManager(tmp_path / "history.json", registry())
    manager.registrar("groq", lambda **kwargs: Falho(kwargs.get("modelo", "model-a")))
    try:
        manager.executar_instancia("groq", Falho("model-a"), "x")
    except RuntimeError:
        pass
    else:
        raise AssertionError("a falha deveria propagar")

    dados = manager.estatisticas_modelo("groq", "model-a")
    assert dados["chamadas"] == 1
    assert dados["sucessos"] == 0
    assert dados["erros"] == 1
