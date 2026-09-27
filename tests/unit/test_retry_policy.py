from nexora.runtime.retry import RetryContexto, RetryPolicy, TipoRetry


def test_retry_externo_nao_idempotente_e_negado():
    d = RetryPolicy().decidir(RetryContexto(TipoRetry.FERRAMENTA, 1, 3, efeito_externo=True))
    assert not d.permitido
    assert "idempotente" in d.motivo


def test_retry_idempotente_e_permitido():
    d = RetryPolicy().decidir(RetryContexto(TipoRetry.FERRAMENTA, 1, 3, efeito_externo=True, idempotente=True))
    assert d.permitido and d.proxima_tentativa == 2
