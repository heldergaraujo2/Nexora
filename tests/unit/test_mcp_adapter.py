from nexora.integracoes.mcp import MCPRegistry, MCPTool
from nexora.integracoes.mcp_adapter import MCPToolAdapter
from nexora.tools.registry import RegistryFerramentas


def test_mcp_import_stays_inside_registry_boundary():
    m=MCPRegistry(); m.registrar_tool(MCPTool("echo","echo",executar=lambda p:p["v"]))
    registry=RegistryFerramentas()
    MCPToolAdapter(registry,m).importar_tool("echo")
    assert registry.executar("echo", {"v": 3}) == 3
