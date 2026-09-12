"""Research Agent da NEXORA: planeja consultas, busca via ferramentas e sintetiza com fontes."""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Callable

from nexora.runtime.agente import AgenteRuntime
from nexora.runtime.analise import AnalisadorFalhas
from nexora.runtime.correcao import Corrector
from nexora.runtime.observacao import Observacao
from nexora.runtime.verificacao import texto_nao_vazio


@dataclass(frozen=True)
class EvidenciaPesquisa:
    """Evidência estruturada preservando a proveniência da fonte observada."""

    source_id: int
    titulo: str = ""
    url: str = ""
    trecho: str = ""
    consulta: str = ""
    confianca: float | None = None

    def para_dict(self) -> dict[str, Any]:
        return {
            "source_id": self.source_id,
            "titulo": self.titulo,
            "url": self.url,
            "trecho": self.trecho,
            "consulta": self.consulta,
            "confianca": self.confianca,
        }


@dataclass(frozen=True)
class AfirmacaoPesquisa:
    """Claim explicitamente ligado a uma evidência citada na resposta."""

    claim: str
    evidencia: EvidenciaPesquisa

    def para_dict(self) -> dict[str, Any]:
        return {"claim": self.claim, "evidence": self.evidencia.para_dict()}


class ResearchAgent:
    """Agente de pesquisa: deriva consultas, executa buscas e sintetiza resposta verificada."""

    def __init__(
        self,
        provider: Any,
        ferramentas: Any,
        *,
        registrar: Callable = None,
        max_tentativas: int = 3,
    ) -> None:
        self._provider = provider
        self._ferramentas = ferramentas
        self._registrar = registrar
        self._ultimo_erro = None
        self._corrector = Corrector(executar=self._executar, registrar=registrar)
        self._runtime = AgenteRuntime(
            executar=self._executar,
            verificar=self._verificar,
            analisar=self._analisar,
            corregir=self._corrector.corregir,
            registrar=registrar,
            max_tentativas=max_tentativas,
        )

    def _planejar_consultas(self, pergunta: str, quantidade: int) -> list:
        base = pergunta.strip().rstrip("。").rstrip("?").strip()
        consultas = [base]
        palavras = [p for p in base.split() if len(p) > 4]
        for p in palavras[:max(0, quantidade - 1)]:
            consultas.append(f"{p} definicao contexto aplicacao")
        return consultas[:quantidade]

    def _executar_busca(self, consulta: str) -> list:
        resultado = self._ferramentas.executar("buscar", {"consulta": consulta})
        if isinstance(resultado, list):
            return resultado
        return []

    def _coletar_fontes(self, consultas: list) -> list:
        fontes = []
        for consulta in consultas:
            itens = self._executar_busca(consulta)
            for item in itens:
                item = dict(item)
                item["consulta"] = consulta
                fontes.append(item)
        return fontes

    def _montar_prompt(self, pergunta: str, fontes: list) -> str:
        linhas = []
        for i, f in enumerate(fontes):
            titulo = f.get("titulo", "")
            url = f.get("url", "")
            trecho = f.get("trecho", "")
            linhas.append(f"Fonte {i+1}: {titulo} — {url} — {trecho}")
        base = "Voce e um pesquisador rigoroso. Responda a pergunta usando APENAS as fontes abaixo."
        corpo = "\n".join(linhas)
        return base + "\n" + corpo + "\nPergunta: " + pergunta + "\nTermine citando as fontes como [fonte:1]."

    @staticmethod
    def _frase_citada(saida: str, inicio: int, fim: int) -> str:
        """Extrai somente o claim local associado a uma citação, sem inferir semântica."""
        inicio_frase = max(saida.rfind(".", 0, inicio), saida.rfind("\n", 0, inicio)) + 1
        fim_frase = saida.find(".", fim)
        if fim_frase < 0:
            fim_frase = len(saida)
        return saida[inicio_frase:fim_frase + (1 if fim_frase < len(saida) else 0)].strip()

    def _estruturar_evidencias(self, saida: str, fontes: list) -> list[dict[str, Any]]:
        """Liga claims citados a fontes reais; não inventa confiança ausente."""
        afirmacoes: list[dict[str, Any]] = []
        for match in re.finditer(r"\[fonte:(\d+)\]", saida):
            indice = int(match.group(1))
            if indice < 1 or indice > len(fontes):
                continue
            fonte = fontes[indice - 1]
            evidencia = EvidenciaPesquisa(
                source_id=indice,
                titulo=str(fonte.get("titulo", "")),
                url=str(fonte.get("url", "")),
                trecho=str(fonte.get("trecho", "")),
                consulta=str(fonte.get("consulta", "")),
                confianca=None,
            )
            claim = self._frase_citada(saida, match.start(), match.end())
            if claim:
                afirmacoes.append(AfirmacaoPesquisa(claim=claim, evidencia=evidencia).para_dict())
        return afirmacoes

    def _executar(self, prompt: str) -> str:
        res = self._provider.generate(prompt)
        return res.text

    def _verificar(self, saida: str) -> bool:
        self._ultimo_erro = None
        if not texto_nao_vazio({"saida": saida}):
            self._ultimo_erro = "Saida vazia"
            return False
        if "[fonte:" not in saida:
            self._ultimo_erro = "Resposta sem citacao de fonte"
            return False
        return True

    def _analisar(self, observacao: Observacao) -> Any:
        if self._ultimo_erro:
            observacao.erro = self._ultimo_erro
        falha = AnalisadorFalhas().analisar(observacao)
        if not falha.retentavel:
            falha.retentavel = True
            falha.plano = "retry"
            falha.tipo = "retentavel"
        return falha

    def pesquisar(self, pergunta: str, *, quantidade: int = 3) -> Any:
        consultas = self._planejar_consultas(pergunta, quantidade)
        fontes = self._coletar_fontes(consultas)
        prompt = self._montar_prompt(pergunta, fontes)
        resultado = self._runtime.executar(prompt)
        evidencias = self._estruturar_evidencias(resultado.saida_final, fontes)
        resultado.evidencias = evidencias
        resultado.metricas["evidencias"] = len(evidencias)
        resultado.trace.setdefault("metadata", {})["research_evidence"] = evidencias
        if self._registrar is not None:
            self._registrar("evidencias_pesquisa", {"quantidade": len(evidencias), "evidencias": evidencias})
        return resultado
