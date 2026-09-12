"""Descoberta e perfis de capacidade de modelos locais."""
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


@dataclass(frozen=True)
class PerfilCapacidadeModelo:
    """Capacidade declarada/estimada do modelo, sem prometer benchmark."""

    categoria: str = "general"
    tamanho_parametros_b: float = 0.0
    contexto: int = 0
    adequado_coding: bool = False


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
            modelos.append(ModeloLocal(
                nome=str(item["name"]),
                tamanho_bytes=int(item.get("size") or 0),
                familia=str(detalhes.get("family") or ""),
                parametros=str(detalhes.get("parameter_size") or ""),
                contexto=int(item.get("context_length") or 0),
            ))
        return modelos

    def nomes(self) -> list[str]:
        return [modelo.nome for modelo in self.listar()]


def perfil_modelo(nome: str, *, contexto: int = 0, parametros: str = "") -> PerfilCapacidadeModelo:
    """Deriva somente capacidades observáveis do nome/metadados do modelo."""
    normalizado = nome.lower()
    coding = "coder" in normalizado or "code" in normalizado
    valor = 0.0
    texto = parametros.strip().upper().replace("B", "")
    try:
        valor = float(texto)
    except ValueError:
        pass
    return PerfilCapacidadeModelo(
        categoria="coding" if coding else "general",
        tamanho_parametros_b=valor,
        contexto=max(0, int(contexto)),
        adequado_coding=coding,
    )


def pontuar_modelo(
    perfil: PerfilCapacidadeModelo,
    *,
    tarefa: str = "general",
    contexto_necessario: int = 0,
    limite_parametros_b: float | None = None,
) -> float:
    """Pontuação determinística para seleção futura; não é benchmark de qualidade."""
    score = 0.0
    if tarefa == "coding" and perfil.adequado_coding:
        score += 10.0
    if tarefa != "coding" and perfil.categoria == "general":
        score += 5.0
    if contexto_necessario > 0 and perfil.contexto >= contexto_necessario:
        score += 3.0
    if limite_parametros_b is not None and perfil.tamanho_parametros_b > limite_parametros_b:
        score -= 100.0
    else:
        score += min(perfil.tamanho_parametros_b, 32.0) * 0.1
    return score
