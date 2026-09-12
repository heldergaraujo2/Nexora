"""Descoberta e perfis de modelos locais, sem acoplamento a um modelo único."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from nexora.providers.ollama import ProviderOllama


@dataclass(frozen=True)
class ModeloLocal:
    nome: str
    tamanho_bytes: int = 0
    familia: str = ""
    parametros: str = ""
    contexto: int = 0


class DescobridorModelosOllama:
    """Converte ``/api/tags`` em um contrato simples de modelos locais."""

    def __init__(self, provider: ProviderOllama) -> None:
        self._provider = provider

    def listar(self) -> list[ModeloLocal]:
        dados = self._provider.listar_modelos()
        modelos: list[ModeloLocal] = []
        for item in dados.get("models", []):
            if not isinstance(item, dict) or not item.get("name"):
                continue
            detalhes = item.get("details") or {}
            modelos.append(
                ModeloLocal(
                    nome=str(item["name"]),
                    tamanho_bytes=int(item.get("size") or 0),
                    familia=str(detalhes.get("family") or ""),
                    parametros=str(detalhes.get("parameter_size") or ""),
                    contexto=int(item.get("context_length") or 0),
                )
            )
        return modelos

    def nomes(self) -> list[str]:
        return [modelo.nome for modelo in self.listar()]


def perfil_modelo(nome: str) -> dict[str, Any]:
    """Retorna metadados de capacidade sem afirmar desempenho de hardware."""
    nome_normalizado = nome.lower()
    if "coder" in nome_normalizado:
        categoria = "coding"
    else:
        categoria = "general"
    return {"nome": nome, "categoria": categoria}
