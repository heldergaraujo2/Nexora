"""Provider fake deterministico para testes (ADR-006)."""
from nexora.providers.base import GenerationResult, Provider, ProviderCapability

class FakeProvider(Provider):
    """Provider deterministico que ecoa o prompt ou devolve texto fixo."""
    def __init__(self, respostas=None) -> None:
        super().__init__("fake", ProviderCapability(tool_calling=True, streaming=False))
        self.respostas = respostas if respostas is not None else {}

    def generate(self, prompt, **kwargs) -> GenerationResult:
        texto = self.respostas.get(prompt, f"[fake:{prompt}]")
        return GenerationResult(text=texto, tool_calls=[])



    def registrar_resposta(self, prompt, resposta) -> None:
        self.respostas[prompt] = resposta