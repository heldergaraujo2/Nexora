"""Integracao do Orquestrator com o ciclo canonico do AgentRuntime."""

from __future__ import annotations

from dataclasses import dataclass

from nexora.orquestracao.orquestrador import Orquestrador
from nexora.providers.base import GenerationResult


class _SequenceProvider:
    def __init__(self, respostas: list[str]) -> None:
        self._respostas = list(respostas)
        self.chamadas = 0

    def saudavel(self) -> bool:
        return True

    def generate(self, _prompt: str) -> GenerationResult:
        self.chamadas += 1
        resposta = self._respostas[min(self.chamadas - 1, len(self._respostas) - 1)]
        return GenerationResult(text=resposta, tool_calls=[])


@dataclass
class _Rotador:
    provider: object

    def obter_provider(self, _objetivo: str, alias=None):
        return self.provider


def test_orquestrador_delega_ciclo_de_provider_ao_runtime() -> None:
    provider = _SequenceProvider(["", "resultado valido"])
    orquestrador = Orquestrador(
        rotador=_Rotador(provider),
        provider=provider,
        planejador=lambda _: [{"id": "t1", "descricao": "gerar resultado"}],
    )

    resultado = orquestrador.executar("concluir tarefa")

    assert resultado["sucesso"] is True
    assert resultado["etapas"][0]["tentativas"] == 2
    assert resultado["etapas"][0]["saida"] == "resultado valido"
    assert provider.chamadas == 2
    assert any(
        evento["tipo"] == "observacao"
        for evento in orquestrador.historico
    )


def test_orquestrador_nao_deixa_excecao_de_provider_escapar() -> None:
    class _ProviderQueFalha:
        def saudavel(self) -> bool:
            return True

        def generate(self, _prompt: str) -> GenerationResult:
            raise RuntimeError("falha permanente")

    provider = _ProviderQueFalha()
    orquestrador = Orquestrador(
        rotador=_Rotador(provider),
        provider=provider,
        planejador=lambda _: [{"id": "t1", "descricao": "executar"}],
        max_tentativas=3,
    )

    resultado = orquestrador.executar("objetivo")

    assert resultado["sucesso"] is False
    assert resultado["etapas"][0]["tentativas"] == 1
    assert resultado["etapas"][0]["erro"] == "falha permanente"
