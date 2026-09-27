import pytest
from nexora.integracoes.browser import AcaoBrowser, BrowserAdapter, BrowserBackendIndisponivel, ResultadoBrowser

def test_browser_adapter_fails_closed_without_backend():
    with pytest.raises(BrowserBackendIndisponivel): BrowserAdapter().executar(AcaoBrowser("navigate","https://example.com"))

def test_browser_adapter_delegates_to_explicit_backend():
    class B:
        nome="fake"
        def executar(self, acao): return ResultadoBrowser(True, acao.alvo)
    r=BrowserAdapter(B()).executar(AcaoBrowser("navigate","https://example.com"))
    assert r.sucesso and r.saida.endswith("example.com")
