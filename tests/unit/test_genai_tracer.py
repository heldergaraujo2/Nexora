from nexora.observabilidade.genai import TracerGenAI


def test_genai_span_lifecycle():
    t = TracerGenAI()
    s = t.iniciar("provider.generate", "llm", model="test")
    s.evento("tool.call", tool="echo")
    t.encerrar(s)
    assert s.fim is not None and s.duracao is not None
    assert s.eventos[0]["nome"] == "tool.call"
