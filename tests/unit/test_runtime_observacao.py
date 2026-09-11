from nexora.runtime.observacao import Observacao


def test_observacao_captura_saida():
    obs = Observacao(etapa_id="t1", ok=True, saida="ola", metadados={"fonte": "fake"})
    assert obs.etapa_id == "t1"
    assert obs.ok is True
    assert obs.saida == "ola"
    assert obs.carimbo


def test_observacao_captura_erro():
    obs = Observacao(etapa_id="t2", ok=False, saida="", erro="timeout")
    assert obs.erro == "timeout"
    assert obs.ok is False
