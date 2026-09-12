"""Integracao do Orchestrator com o ciclo canonico do AgentRuntime."""

from __future__ import annotations

from dataclasses import dataclass

from nexora.governanca.permissoes import GerenciadorPermissoes
from nexora.governanca.policy import EfeitoPolitica, PolicyEngine, RegraPolitica
from nexora.orquestracao.orquestrador import Orquestrador
from nexora.providers.base import GenerationResult
from nexora.runtime.checkpoint import CheckpointEngine
from nexora.tools.registry import Ferramenta, RegistryFerramentas


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


def test_orquestrador_execution_trace_recebe_contexto_real_da_tarefa_e_provider() -> None:
    provider = _SequenceProvider(["resultado valido"])
    provider.name = "provider-teste"
    orquestrador = Orquestrador(
        rotador=_Rotador(provider),
        provider=provider,
        planejador=lambda _: [{"id": "t1", "descricao": "gerar resultado"}],
    )

    resultado = orquestrador.executar("concluir tarefa")
    trace = resultado["etapas"][0]["trace"]

    assert trace["task_id"] == "t1"
    assert trace["provider"] == "provider-teste"
    assert trace["agent_id"] == "orchestrator:runtime"
    assert trace["metadata"]["objetivo_id"] == resultado["objetivo_id"]
    assert trace["metadata"]["executor"] == "orchestrator"
    assert trace["status"] == "success"
    assert trace["retry_count"] == 0


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


def test_orquestrador_ferramenta_passa_uma_vez_pela_governanca() -> None:
    chamadas = 0

    def executar_ferramenta(parametros: dict[str, object]) -> str:
        nonlocal chamadas
        chamadas += 1
        return f"ok:{parametros['valor']}"

    policy = PolicyEngine(
        regras=(
            RegraPolitica(
                id="allow-orchestrator-tool",
                efeito=EfeitoPolitica.ALLOW,
                solicitante="orchestrator",
                executor="ferramenta_teste",
                tarefa="executar",
            ),
        ),
        origem="integration-test",
    )
    permissoes = GerenciadorPermissoes(policy)
    checkpoint = CheckpointEngine()
    registry = RegistryFerramentas(permissoes=permissoes, checkpoint=checkpoint)
    registry.registrar(
        Ferramenta(
            nome="ferramenta_teste",
            descricao="Ferramenta de teste controlada",
            executar=executar_ferramenta,
        )
    )

    provider = _SequenceProvider(["provider-nao-deve-ser-chamado"])
    orquestrador = Orquestrador(
        rotador=_Rotador(provider),
        provider=provider,
        ferramentas=registry,
        planejador=lambda _: [
            {
                "id": "t1",
                "descricao": "executar ferramenta",
                "ferramenta": "ferramenta_teste",
                "parametros": {"valor": "42"},
            }
        ],
    )

    resultado = orquestrador.executar("usar ferramenta controlada")

    assert resultado["sucesso"] is True
    assert resultado["etapas"][0]["saida"] == "ok:42"
    assert resultado["etapas"][0]["tentativas"] == 1
    assert resultado["etapas"][0]["ferramenta"] == "ferramenta_teste"
    assert resultado["etapas"][0]["trace"]["task_id"] == "t1"
    assert resultado["etapas"][0]["trace"]["provider"] == ""
    assert resultado["etapas"][0]["trace"]["metadata"]["ferramenta"] == "ferramenta_teste"
    assert chamadas == 1
    assert provider.chamadas == 0
    assert len(checkpoint.listar()) == 1
    assert checkpoint.listar()[0].motivo == "antes_da_acao"
