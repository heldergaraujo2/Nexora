from nexora.runtime.analise import AnalisadorFalhas



class ObservacaoStub:


    def __init__(self, erro=None):
        self.erro = erro


def test_falha_retentavel_classifica_retry():
    obs = ObservacaoStub(erro="timeout")
    falha = AnalisadorFalhas().analisar(obs)
    assert falha.retentavel is True

    assert falha.plano == "retry"

def test_falha_comum_classifica_abort():
    obs = ObservacaoStub(erro="erro grave")
    falha = AnalisadorFalhas().analisar(obs)
    assert falha.retentavel is False

def test_falha_sem_erro_classifica_retry():
    obs = ObservacaoStub(erro=None)
    falha = AnalisadorFalhas().analisar(obs)
    assert falha.retentavel
