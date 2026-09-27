from nexora.agentes.pesquisa_guardrails import GuardiaoPesquisa, OrcamentoPesquisa


def test_public_destination_blocks_private_addresses():
    g = GuardiaoPesquisa()
    assert not g.destino_publico("http://127.0.0.1:8000/x")
    assert not g.destino_publico("http://localhost/x")
    assert g.destino_publico("https://example.com/x")


def test_source_budget_limits_domains_and_count():
    g = GuardiaoPesquisa(OrcamentoPesquisa(max_consultas=2, max_fontes=2, max_dominios=1))
    fontes = [
        {"url": "https://a.example/1"},
        {"url": "https://b.example/2"},
        {"url": "https://a.example/3"},
    ]
    out = g.filtrar_fontes(fontes)
    assert len(out) == 2
    assert {x["url"].split("/")[2] for x in out} == {"a.example"}
