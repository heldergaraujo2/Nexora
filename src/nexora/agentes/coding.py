"""Coding Agent da NEXORA: gera e corrige codigo usando o runtime generalista."""
from __future__ import annotations

from typing import Any, Callable

from nexora.runtime.agente import AgenteRuntime
from nexora.runtime.analise import AnalisadorFalhas
from nexora.runtime.correcao import Corrector
from nexora.runtime.verificacao import texto_nao_vazio

_MARCADORES_PYTHON = ("def ", "import ", "class ", "from ", "@")


class CodingAgent:
    """Agente especializado em codigo: monta prompt, executa via runtime e verifica sintaxe."""

    def __init__(
        self,
        provider: Any,
        *,
        registrar: Callable[[str, dict[str, Any]], None] | None = None,
        max_tentativas: int =  3,
    ) -> None:
        self._provider = provider
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

    def _executar(self, prompt: str) -> str:
        res = self._provider.generate(prompt)
        return res.text

    def _parecer_python(self, texto: str) -> bool:
        t = texto.lstrip()
        return any(t.startswith(m) for m in _MARCADORES_PYTHON)

    def _verificar(self, saida: str) -> bool:
        self._ultimo_erro = None
        if not texto_nao_vazio({"saida": saida}):
            self._ultimo_erro = "Saida vazia"
            return False
        if self._parecer_python(saida):
            try:
                compile(saida, "<codigo>", "exec")
            except (SyntaxError, ValueError) as exc:
                self._ultimo_erro = str(exc)
                return False
        return True

    def _analisar(self, observacao: dict[str, Any]) -> Any:
        if self._ultimo_erro:
            observacao["erro"] = self._ultimo_erro
        return AnalisadorFalhas().analisar(observacao)

    def codar(self, tarefa: str, *, linguagem: str = "python") -> Any:
        prompt = f"Voce e um engenheiro de software especialista em {linguagem}.\nEscreva codigo para: {tarefa}\nResponda apenas com o codigo, sem explicacoes."
        return self._runtime.executar(prompt)

