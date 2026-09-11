"""Teste integrado do caminho orquestrador -> ferramenta -> governanca."""
from __future__ import annotations

from nexora.auditoria.registro import RegistroAuditoria
from nexora.governanca.permissoes import GerenciadorPermissoes
from nexora.governanca.policy import EfeitoPolitica, PolicyEngine, RegraPolitica
from nexora.providers.fake import FakeProvider
from nexora.runtime.checkpoint import CheckpointEngine
from nexora.runtime.verificacao import Verificacao, texto_nao_vazio
from nexora.orquestracao.orquestrador import Orquestrador
from nexora.tools.registry import Ferramenta, RegistryFerramentas


class _Rotador:
    def __init__(self, provider):
        self.provider = provider

    def obter_provider(self, objetivo, alias=None):
        return self.provider


def test_orquestrador_percorre_fluxo_completo_de_ferramenta(tmp_path):
    auditoria = RegistroAuditoria(tmp_path / "auditoria.jsonl")
    checkpoint = CheckpointEngine(auditoria=auditoria)
    policy = PolicyEngine(
        [
            RegraPolitica(
                id="allow-orchestrator-echo",
                efeito=EfeitoPolitica.ALLOW,
                solicitante="orchestrator",
                executor="echo",
                tarefa="executar",
            )
        ],
        origin="integration-test",
    )
    permissoes = GerenciadorPermissoes(policy, auditoria=auditoria)
    ferramentas = RegistryFerramentas(
        permissoes=permissoes,
        checkpoint=checkpoint,
        verificador=Verificacao([texto_nao_vazio]),
        auditoria=auditoria,
    )
    executado: list[dict] = []
    ferramentas.registrar(
        Ferramenta(
            nome="echo",
            descricao="Retorna o valor recebido",
            executar=lambda parametros: executado.append(parametros) or parametros["valor"],
        )
    )

    provider = FakeProvider({"objetivo de teste": "fallback"})
    orquestrador = Orquestrador(
        _Rotador(provider),
        provider,
        planejador=lambda objetivo: [
            {"id": "t1", "descricao": "usar ferramenta", "ferramenta": "echo", "parametros": {"valor": "resultado"}}
        ],
        ferramentas=ferramentas,
    )

    resultado = orquestrador.executar("objetivo de teste")

    assert resultado["sucesso"] is True
    assert resultado["metricas"] == {"total": 1, "ok": 1, "falhas": 0}
    assert resultado["etapas"][0]["ferramenta"] == "echo"
    assert resultado["etapas"][0]["saida"] == "resultado"
    assert executado == [{"valor": "resultado"}]
    assert provider.chamadas == []

    tarefa_id = resultado["etapas"][0]["tarefa_id"]
    checkpoints = checkpoint.listar()
    assert len(checkpoints) == 1
    assert checkpoints[0].estado["ferramenta"] == "echo"
    assert checkpoints[0].estado["contexto"]["tarefa_id"] == tarefa_id

    eventos = auditoria.listar()
    tipos = [evento["evento"] for evento in eventos]
    assert "permissao.decisao" in tipos
    assert "ferramenta.resultado" in tipos
    permissao = next(evento for evento in eventos if evento["evento"] == "permissao.decisao")
    assert permissao["dados"]["permitido"] is True
    assert permissao["dados"]["fingerprint"] == policy.fingerprint
    ferramenta = next(evento for evento in eventos if evento["evento"] == "ferramenta.resultado")
    assert ferramenta["dados"]["sucesso"] is True
    assert ferramenta["dados"]["verificado"] is True
