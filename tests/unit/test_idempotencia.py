from __future__ import annotations

import threading

import pytest

from nexora.runtime.idempotencia import (
    ConflitoIdempotencia,
    StatusIdempotencia,
    StoreIdempotenciaMemoria,
    fingerprint_operacao,
)


def test_primeira_reivindicacao_cria_operacao_em_andamento() -> None:
    store = StoreIdempotenciaMemoria()

    registro = store.reivindicar("op-1", "fp-1")

    assert registro.status is StatusIdempotencia.IN_PROGRESS
    assert registro.chave == "op-1"
    assert registro.fingerprint == "fp-1"


def test_mesma_chave_e_fingerprint_nao_criam_segunda_execucao() -> None:
    store = StoreIdempotenciaMemoria()

    primeiro = store.reivindicar("op-1", "fp-1")
    segundo = store.reivindicar("op-1", "fp-1")

    assert segundo == primeiro
    assert store.obter("op-1") == primeiro


def test_mesma_chave_com_fingerprint_diferente_e_rejeitada() -> None:
    store = StoreIdempotenciaMemoria()
    store.reivindicar("op-1", "fp-1")

    with pytest.raises(ConflitoIdempotencia):
        store.reivindicar("op-1", "fp-2")


def test_conclusao_preserva_identidade_e_retorna_resultado() -> None:
    store = StoreIdempotenciaMemoria()
    store.reivindicar("op-1", "fp-1")

    registro = store.concluir("op-1", "fp-1", sucesso=True, resultado={"id": 42})

    assert registro.status is StatusIdempotencia.SUCCEEDED
    assert registro.resultado == {"id": 42}
    assert store.obter("op-1") == registro


def test_operacao_falha_nao_e_reexecutada_automaticamente() -> None:
    store = StoreIdempotenciaMemoria()
    store.reivindicar("op-1", "fp-1")
    store.concluir("op-1", "fp-1", sucesso=False, resultado="erro")

    registro = store.reivindicar("op-1", "fp-1")

    assert registro.status is StatusIdempotencia.FAILED
    assert registro.resultado == "erro"


def test_fingerprint_e_deterministico_independente_da_ordem_das_chaves() -> None:
    primeiro = fingerprint_operacao({"acao": "pagar", "valor": 10})
    segundo = fingerprint_operacao({"valor": 10, "acao": "pagar"})

    assert primeiro == segundo
    assert len(primeiro) == 64


def test_chave_e_fingerprint_vazios_sao_rejeitados() -> None:
    store = StoreIdempotenciaMemoria()

    with pytest.raises(ValueError):
        store.reivindicar("", "fp-1")
    with pytest.raises(ValueError):
        store.reivindicar("op-1", "")


def test_reivindicacao_concorrente_cria_um_unico_registro() -> None:
    store = StoreIdempotenciaMemoria()
    resultados = []
    barreira = threading.Barrier(8)

    def trabalhador() -> None:
        barreira.wait()
        resultados.append(store.reivindicar("op-concorrente", "fp-1"))

    threads = [threading.Thread(target=trabalhador) for _ in range(8)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    assert len(resultados) == 8
    assert all(registro == resultados[0] for registro in resultados)
    assert store.obter("op-concorrente") == resultados[0]
