"""Testes do sandbox de execucao controlada."""
import pytest

from nexora.runtime.sandbox import AcaoNegada, Sandbox


def test_sandbox_executa_comando_permitido():
    caixa = Sandbox(permitidos=["echo"])
    resultado=caixa.executar("echo ola")
    assert resultado["retorno"] == 0


def test_sandbox_nega_comando_fora_da_allowlist():
    caixa = Sandbox(permitidos=["ls"])
    with pytest.raises(AcaoNegada):
        caixa.executar("rm -rf /")


def test_sandbox_permitir_adiciona_comando():
    caixa = Sandbox()
    caixa.permitir("pwd")
    resultado=caixa.executar("pwd")
    assert resultado["saida"].strip() == "/workspace/project"