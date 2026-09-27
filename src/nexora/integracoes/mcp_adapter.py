"""Adaptador seguro entre MCP-like contracts e o Tool Registry governado da NEXORA."""
from __future__ import annotations

from typing import Any

from nexora.integracoes.mcp import MCPRegistry, MCPTool
from nexora.tools.registry import Ferramenta, RegistryFerramentas


class MCPToolAdapter:
    """Importa capacidades MCP para o Registry; a execução continua governada pelo Registry."""

    def __init__(self, registry: RegistryFerramentas, mcp: MCPRegistry) -> None:
        self.registry = registry
        self.mcp = mcp

    def importar_tool(self, nome: str, *, descricao: str | None = None) -> Ferramenta:
        tool = next((item for item in self.mcp.tools() if item.nome == nome), None)
        if tool is None:
            raise KeyError(nome)
        if tool.executar is None:
            raise ValueError(f"tool MCP sem executor local: {nome}")

        ferramenta = Ferramenta(
            nome=tool.nome,
            descricao=descricao or tool.descricao,
            executar=tool.executar,
        )
        self.registry.registrar(ferramenta)
        return ferramenta
