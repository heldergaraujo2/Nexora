from nexora.integracoes.mcp import MCPPrompt, MCPRegistry, MCPResource, MCPTool


def test_mcp_registry_contracts():
    r = MCPRegistry()
    r.registrar_tool(MCPTool("echo", "Echo", executar=lambda x: x["v"]))
    r.registrar_resource(MCPResource("nexora://memory/1", "memory"))
    r.registrar_prompt(MCPPrompt("research"))
    assert r.executar_tool("echo", {"v": 7}) == 7
    assert len(r.resources()) == 1 and len(r.prompts()) == 1
