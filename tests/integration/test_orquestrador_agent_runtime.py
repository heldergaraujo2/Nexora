"""Integracao do Orchestrator com o ciclo canonico do AgentRuntime."""

from __future__ import annotations

from dataclasses import dataclass

from nexora.governanca.permissoes import GerenciadorPermissoes
from nexora.governanca.policy import EfeitoPolitica, PolicyEngine, RegraPolitica
from nexora.orquestracao.orquestrador import Orquestrador
from nexora.providers.base import GenerationResult, Provider, ProviderCapability
from nexora.providers.manager import ProviderManager
from nexora.providers.modelos import PerfilCapacidadeModelo
from nexora.providers.roteamento import RoteadorInteligente
from nexora.runtime.checkpoint import CheckpointEngine
from nexora.runtime.hardware import PerfilHardware
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


class _RoutedProvider(Provider):
    def __init__(self, modelo: str) -> None:
        super().__init__("routed-provider", ProviderCapability(max_context_tokens=32768))
        self.modelo = modelo
        self.chamadas = 0

    def generate(self, _prompt: str, **_kwargs) -> GenerationResult:
        self.chamadas += 1
        return GenerationResult(text=f"resultado:{self.modelo}", tool_calls=[])


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


def test_orquestrador_rota_provider_e_modelo_realmente_e_registra_decisao_no_trace() -> None:
    manager = ProviderManager()
    instancias: list[_RoutedProvider] = []

    def factory(*, modelo: str = "default") -> _RoutedProvider:
        provider = _RoutedProvider(modelo)
        instancias.append(provider)
        return provider

    manager.registrar("routed-provider", factory)
    roteador = RoteadorInteligente(manager)
    hardware = PerfilHardware(
        sistema="Windows",
        arquitetura="AMD64",
        cpu_nucleos=6,
        ram_bytes=16 * 1024**3,
    )
    candidatos = [
        {
            "provider": "routed-provider",
            "modelo": "general-7b",
            "perfil": PerfilCapacidadeModelo(
                categoria="general",
                tamanho_parametros_b=7.0,
                contexto=32768,
            ),
        },
        {
            "provider": "routed-provider",
            "modelo": "coder-7b",
            "perfil": PerfilCapacidadeModelo(
                categoria="coding",
                tamanho_parametros_b=7.0,
                contexto=32768,
                adequado_coding=True,
            ),
        },
    ]
    fallback = _SequenceProvider(["nao deve ser usado"])
    orquestrador = Orquestrador(
        rotador=_Rotador(fallback),
        provider=fallback,
        provider_manager=manager,
        roteador_inteligente=roteador,
        candidatos_roteamento=candidatos,
        hardware=hardware,
        planejador=lambda _: [{"id": "t1", "descricao": "escrever codigo"}],
    )

    resultado = orquestrador.executar("escrever codigo")
    trace = resultado["etapas"][0]["trace"]

    assert resultado["sucesso"] is True
    assert resultado["etapas"][0]["saida"] == "resultado:coder-7b"
    assert fallback.chamadas == 0
    assert len(instancias) == 3  # capability probe + instancia selecionada; healthcheck usa a selecionada
    assert instancias[0].modelo == "default"
    assert all(instancia.modelo == "coder-7b" for instancia in instancias[1:])
    assert trace["provider"] == "routed-provider"
    assert trace["model"] == "coder-7b"
    assert trace["metadata"]["routing_decision"]["selected"]["modelo"] == "coder-7b"
    assert trace["metadata"]["routing_decision"]["selected"]["provider"] == "routed-provider"