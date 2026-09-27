from nexora.observabilidade.genai import TracerGenAI
from nexora.runtime.agente import AgenteRuntime
from nexora.runtime.analise import AnalisadorFalhas
from nexora.runtime.correcao import Corrector


def test_runtime_emits_attempt_span():
    tracer = TracerGenAI()
    runtime = AgenteRuntime(
        executar=lambda p: "ok",
        verificar=lambda s: True,
        analisar=AnalisadorFalhas().analisar,
        corregir=Corrector(lambda p: "ok").corregir,
        tracer=tracer,
    )
    result = runtime.executar("teste")
    assert result.sucesso
    assert len(tracer.spans()) == 1
    assert tracer.spans()[0].atributos["success"] is True
