"""Contratos MCP-like para interoperabilidade de ferramentas da NEXORA.

O modulo mantem um nucleo pequeno e agnostico. Transporte, autenticação e servidor
MCP real devem ser implementados por adaptadores, não pelo Tool Registry.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable


@dataclass(frozen=True)
class MCPTool:
    nome: str
    descricao: str
    input_schema: dict[str, Any] = field(default_factory=dict)
    executar: Callable[[dict[str, Any]], Any] | None = None


@dataclass(frozen=True)
class MCPResource:
    uri: str
    nome: str
    descricao: str = ""


@dataclass(frozen=True)
class MCPPrompt:
    nome: str
    descricao: str = ""
    argumentos: tuple[str, ...] = ()


class MCPRegistry:
    """Registro local de capacidades interoperáveis, sem execução automática."""

    def __init__(self) -> None:
        self._tools: dict[str, MCPTool] = {}
        self._resources: dict[str, MCPResource] = {}
        self._prompts: dict[str, MCPPrompt] = {}

    def registrar_tool(self, tool: MCPTool) -> None:
        if not tool.nome.strip():
            raise ValueError("tool MCP exige nome")
        self._tools[tool.nome] = tool

    def registrar_resource(self, resource: MCPResource) -> None:
        if not resource.uri.strip():
            raise ValueError("resource MCP exige URI")
        self._resources[resource.uri] = resource

    def registrar_prompt(self, prompt: MCPPrompt) -> None:
        if not prompt.nome.strip():
            raise ValueError("prompt MCP exige nome")
        self._prompts[prompt.nome] = prompt

    def tools(self) -> list[MCPTool]:
        return sorted(self._tools.values(), key=lambda x: x.nome)

    def resources(self) -> list[MCPResource]:
        return sorted(self._resources.values(), key=lambda x: x.uri)

    def prompts(self) -> list[MCPPrompt]:
        return sorted(self._prompts.values(), key=lambda x: x.nome)

    def executar_tool(self, nome: str, argumentos: dict[str, Any]) -> Any:
        tool = self._tools[nome]
        if tool.executar is None:
            raise RuntimeError("tool MCP sem executor local")
        return tool.executar(argumentos)
