from nexora.runtime.agente import AgenteRuntime
from nexora.runtime.analise import AnalisadorFalhas
from nexora.runtime.correcao import Corrector


def _verificar(s: str) -> bool:
    return len(s.strip()) > 0


def _analisar(obs):
    return AnalisadorFalhas().analisar(obs)


def test_ciclo_sucesso_na_primeira_tentativa():
    chamadas = []

    def exec(p: str) -> str:
        chamadas.append(p)
        return "saida ok"

    corr = Corrector(executar=exec)
    r = AgenteRuntime(executar=exec, verificar=_verificar, analisar=_analisar, corregir=corr.corregir, max_tentativas=3).executar("objetivo")
    assert r.sucesso is True


    assert r.tentativas == 1

def test_ciclo_corrige_saida_vazia():
    valores = ["", "saida corrigida"]
    chamadas = []

    def exec(p: str) -> str:
        chamadas.append(p)
        return valores.pop(0)

    corr = Corrector(executar=exec)
    r = AgenteRuntime(executar=exec, verificar=_verificar, analisar=_analisar, corregir=corr.corregir, max_tentativas=3).executar("objetivo")
    assert r.sucesso is True


    assert r.tentativas == 2


    assert len(chamadas) == 2

def test_ciclo_respeita_limite_de_tentativas():
    chamadas = []

    def exec(p: str) -> str:
        chamadas.append(p)
        return ""

    corr = Corrector(executar=exec)
    r = AgenteRuntime(executar=exec, verificar=_verificar, analisar=_analisar, corregir=corr.corregir, max_tentativas=2).executar("objetivo")
    assert r.sucesso is False


    assert r.tentativas == 2
