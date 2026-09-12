from __future__ import annotations

from typing import Any

from nexora.agentes.pesquisa import ResearchAgent
from nexora.providers.base import GenerationResult


class BuscaIntegracao:
    def executar(self, nome: str, parametros: dict[str, Any] | None = None) -> list[dict[str, str]]:
        assert nome == "buscar"
        consulta = (parametros or {}).get("consulta", "")
        return [{
            "titulo": "Fonte de integracao",
            "url": "https://fonte.test/pesquisa",
            "trecho": "Evidencia observada para a consulta.",
            "consulta": consulta,
        }]


class ProviderIntegracao:
    def generate(self, prompt: str, **kwargs: Any) -> GenerationResult:
        return GenerationResult(
            text="Afirmacao verificavel baseada na fonte [fonte:1].",
            tool_calls=[],
        )


def test_research_agent_preserva_proveniencia_no_resultado_e_trace():
    agente = ResearchAgent(ProviderIntegracao(), BuscaIntegracao())

    resultado = agente.pesquisar("qual e a evidencia", quantidade=1)

    assert resultado.sucesso is True
    assert len(resultado.evidencias) == 1
    evidencia = resultado.evidencias[0]
    assert evidencia["claim"] == "Afirmacao verificavel baseada na fonte [fonte:1]."
    assert evidencia["evidence"]["url"] == "https://fonte.test/pesquisa"
    assert evidencia["evidence"]["confianca"] is None
    assert resultado.trace["metadata"]["research_evidence"] == resultado.evidencias
