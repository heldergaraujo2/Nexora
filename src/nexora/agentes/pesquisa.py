"""Research Agent da NEXORA: planeja consultas, busca via ferramentas e sintetiza com fontes."""
from __future__ import annotations

from typing import Any, Callable

from nexora.runtime.agente import AgenteRuntime
from nexora.runtime.analise import AnalisadorFalhas
from nexora.runtime.correcao import Corrector
from nexora.runtime.verificacao import texto_nao_vazio


class ResearchAgent:
    """Agente de pesquisa: deriva consultas, executa buscas e sintetiza resposta verificada."""

    def __init__(
        self,
        provider: Any,
        ferramentas: Any,
        *,
        registrar: Callable = None,
        max_tentativas: int =3,
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
        palavras = [p for p in base.split() if len(p) >4]
        for p in palavras[:max(0, quantidade -1)]:
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

    def _analisar(self, observacao: dict) -> Any:
        if self._ultimo_erro:
            observacao["erro"] = self._ultimo_erro
        return AnalisadorFalhas().analisar(observacao)

    def pesquisar(self, pergunta: str, *, quantidade: int =3) -> Any:
        consultas = self._planejar_consultas(pergunta, quantidade)
        fontes = self._coletar_fontes(consultas)
        prompt = self._montar_prompt(pergunta, fontes)
        return self._runtime.executar(prompt)

