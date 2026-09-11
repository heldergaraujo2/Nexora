from nexora.runtime.correcao import Corrector





class FalhaStub:


    def __init__(self, plano, motivo=""):
        self.plano = plano

        self.motivo = motivo



def test_corrector_rerun_executa_novamamente():
    chamadas = []
    def exec(p: str) -> str:
        chamadas.append(p)
        return "resultado"

    c = Corrector(executar=exec)


    saida = c.corregir("prompt", FalhaStub("rerun"))
    assert saida == "resultado"

    assert len(chamadas) == 1

def test_corrector_ajuste_prompt_prefixa():
    chamadas = []
    def exec(p: str) -> str:
        chamadas.append(p)
        return "ok"

    c = Corrector(executar=exec)

    c.corregir("prompt", FalhaStub("ajuste_prompt"))
    assert chamadas[0].startswith("Tente novamente")

def test_corrector_registra_evento():
    eventos = []
    def exec(p: str) -> str:
        return "ok"

    c = Corrector(executar=exec, registrar=lambda tipo, dados: eventos.append((tipo, dados)))

    c.corregir("prompt", FalhaStub("rerun", "timeout"))
    assert eventos[0][0] == "correcao"
    assert eventos[0][1]["motivo"] == "timeout"
