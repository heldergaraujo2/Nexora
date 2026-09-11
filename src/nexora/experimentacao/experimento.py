"""Experimentation Engine: variantes de abordagem para uma mesma tarefa (Fase 9)."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class Experimento:
    """Definicao de um experimento com variantes de abordagem."""

    nome: str
    tarefa: str
    variantes: list[str] = field(default_factory=list)

    def adicionar_variante(self, descricao: str) -> None:
        """Adiciona uma variante de abordagem ao experimento."""
        self.variantes.append(descricao)


class ExecutorExperimentos:
    """Executa variantes via provider e registra metricas deterministicas."""

    def __init__(self, provider, *, max_tentativas: int = 1) -> None:
        self.provider = provider
        self.max_tentativas = max_tentativas

    def executar(self, experimento: Experimento) -> dict[str, Any]:
        """Executa cada variante e retorna comparacao deterministico."""
        resultados = []
        for indice, variante in enumerate(experimento.variantes, start=1):
            prompt = self._montar_prompt(experimento.tarefa, variante)
            saida = ""
            tentativas = 0
            sucesso = False
            for _ in range(self.max_tentativas):
                tentativas += 1
                try:
                    resultado = self.provider.generate(prompt)
                    saida = resultado.text
                    sucesso = self._verificar(saida)
                    if sucesso:
                        break
                except Exception:
                    sucesso = False
                    break
            resultados.append({
                "indice": indice,
                "variante": variante,
                "sucesso": sucesso,
                "tentativas": tentativas,
                "saida": saida,
            })
        return {
            "experimento": experimento.nome,
            "tarefa": experimento.tarefa,
            "total_variantes": len(resultados),
            "sucessos": sum(1 for r in resultados if r["sucesso"]),
            "resultados": resultados,
        }

    def _montar_prompt(self, tarefa: str, variante: str) -> str:
        """Monta o prompt para uma variante de abordagem."""
        return f"Tarefa: {tarefa}\nAbordagem: {variante}\nResponda de forma objetiva."

    def _verificar(self, saida: str) -> bool:
        """Verifica se a saida e valida (nao vazia)."""
        return bool(saida and saida.strip())

