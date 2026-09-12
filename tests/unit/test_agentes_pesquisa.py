"""Testes do Research Agent (Fase 7)."""
from __future__ import annotations

import hashlib
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

from nexora.agentes.pesquisa import EvidenciaPesquisa, ResearchAgent
from nexora.providers.base import GenerationResult


class FakeBusca:
    """Fake de RegistryFerramentas para testes do ResearchAgent."""
    def __init__(self, resultados: list = None) -> None:
        self.resultados = list(resultados) if resultados else []
        self.consultas = []

    def executar(self, nome: str, parametros: dict = None) -> list:
        assert nome == "buscar"
        consulta = (parametros or {}).get("consulta", "")
        self.consultas.append(consulta)
        if self.resultados:
            return self.resultados.pop(0)
        return []


class FakePesquisa:
    """Provider deterministico para testes do ResearchAgent."""
    def __init__(self, respostas: list[str]) -> None:
        self.respostas = list(respostas)
        self.chamadas = []

    def generate(self, prompt: str, **kwargs: Any) -> GenerationResult:
        self.chamadas.append(prompt)
        texto = self.respostas.pop(0) if self.respostas else ""
        return GenerationResult(text=texto, tool_calls=[])


def _fonte(texto: str, url: str = "https://exemplo.dev") -> list:
    return [{"titulo": texto, "url": url, "trecho": texto}]


def test_planeja_consultas_quantidade():
    ag = ResearchAgent(FakePesquisa([]), FakeBusca())
    consultas = ag._planejar_consultas("o que e uma arquitetura de agentes", quantidade=2)
    assert len(consultas) == 2
    assert consultas[0] == "o que e uma arquitetura de agentes"
    assert "arquitetura" in consultas[1]


def test_executa_busca_via_ferramentas():
    buscas = FakeBusca([_fonte("a"), _fonte("b")])
    ag = ResearchAgent(FakePesquisa([]), buscas)
    consultas = ag._planejar_consultas("o que e a nexora", quantidade=2)
    fontes = ag._coletar_fontes(consultas)
    assert len(fontes) == 2
    assert fontes[0]["consulta"] == consultas[0]
    assert len(buscas.consultas) == 2


def test_pesquisar_sintetiza_com_citacoes():
    prov = FakePesquisa(["Resposta com fonte [fonte:1]"])
    buscas = FakeBusca([_fonte("a")])
    ag = ResearchAgent(prov, buscas)
    r = ag.pesquisar("o que e a nexora", quantidade=1)
    assert r.sucesso is True
    assert r.tentativas == 1
    assert "[fonte:1]" in r.saida_final


def test_pesquisar_produz_claim_evidencia_proveniencia_e_adequacao():
    prov = FakePesquisa(["NEXORA possui pesquisa estruturada [fonte:1]."])
    buscas = FakeBusca([_fonte("NEXORA possui pesquisa estruturada e fontes verificáveis.", "https://fonte.dev/ref")])
    ag = ResearchAgent(prov, buscas)

    r = ag.pesquisar("o que e a nexora", quantidade=1)

    assert len(r.evidencias) == 1
    claim = r.evidencias[0]
    assert claim["claim"] == "NEXORA possui pesquisa estruturada [fonte:1]."
    assert claim["evidence"]["source_id"] == 1
    assert claim["evidence"]["titulo"] == "NEXORA possui pesquisa estruturada e fontes verificáveis."
    assert claim["evidence"]["url"] == "https://fonte.dev/ref"
    assert claim["evidence"]["trecho"] == "NEXORA possui pesquisa estruturada e fontes verificáveis."
    assert claim["evidence"]["consulta"] == "o que e a nexora"
    assert claim["evidence"]["confianca"] is None
    assert len(claim["evidence"]["source_ref"]) == 64
    assert claim["adequacao"]["status"] == "SUSTENTADA"
    assert claim["adequacao"]["cobertura"] >= 0.6
    assert r.metricas["evidencias"] == 1
    assert r.metricas["evidencias_sustentadas"] == 1
    assert r.trace["metadata"]["research_evidence"] == r.evidencias


def test_pesquisar_fonte_existente_mas_nao_sustenta_claim():
    prov = FakePesquisa(["NEXORA possui pesquisa estruturada [fonte:1]."])
    buscas = FakeBusca([_fonte("A fonte descreve exclusivamente preços e faturamento.")])
    ag = ResearchAgent(prov, buscas)

    r = ag.pesquisar("o que e a nexora", quantidade=1)

    assert r.evidencias[0]["adequacao"]["status"] == "INSUFICIENTE"
    assert r.metricas["evidencias_insuficientes"] == 1
    assert r.evidencias[0]["evidence"]["confianca"] is None


def test_pesquisar_multiplas_fontes_avalia_cada_claim():
    prov = FakePesquisa(["NEXORA possui pesquisa estruturada [fonte:1]. O sistema trata preços [fonte:2]."])
    buscas = FakeBusca([
        [{"titulo": "Pesquisa estruturada da NEXORA", "url": "https://a.dev", "trecho": "NEXORA possui pesquisa estruturada."}],
        [{"titulo": "Preços", "url": "https://b.dev", "trecho": "O sistema trata preços e faturamento."}],
    ])
    ag = ResearchAgent(prov, buscas)

    r = ag.pesquisar("o que e a nexora", quantidade=2)

    assert len(r.evidencias) == 2
    assert [e["adequacao"]["status"] for e in r.evidencias] == ["SUSTENTADA", "SUSTENTADA"]
    assert r.metricas["evidencias_sustentadas"] == 2


def test_source_ref_e_deterministico_e_independente_do_indice():
    primeira = EvidenciaPesquisa(source_id=1, titulo="t", url="u", trecho="x", consulta="q")
    segunda = EvidenciaPesquisa(source_id=99, titulo="t", url="u", trecho="x", consulta="q")
    esperado = hashlib.sha256("t\x1fu\x1fx\x1fq".encode("utf-8")).hexdigest()
    assert primeira.source_ref == esperado
    assert segunda.source_ref == esperado


def test_pesquisar_ignora_citacao_para_fonte_inexistente():
    prov = FakePesquisa(["Resposta com fonte [fonte:99]."])
    buscas = FakeBusca([_fonte("a")])
    ag = ResearchAgent(prov, buscas)

    r = ag.pesquisar("o que e a nexora", quantidade=1)

    assert r.sucesso is True
    assert r.evidencias == []
    assert r.metricas["evidencias"] == 0


def test_pesquisar_respeita_limite():
    prov = FakePesquisa(["resposta sem citacao"])
    ag = ResearchAgent(prov, FakeBusca(), max_tentativas=2)
    r = ag.pesquisar("o que e a nexora", quantidade=1)
    assert r.sucesso is False
    assert r.tentativas == 2
    assert r.evidencias == []


def test_cli_agente_pesquisar():
    env = {**os.environ, "PYTHONPATH": str(Path.cwd() / "src")}
    resultado = subprocess.run(
        [sys.executable, "-m", "nexora", "agente", "pesquisar", "o que e a nexora", "--provider", "fake"],
        capture_output=True,
        text=True,
        env=env,
        timeout=30,
    )
    assert resultado.returncode == 0
    assert "sucesso=True" in resultado.stdout
