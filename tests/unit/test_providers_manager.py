"""Testes do ProviderManager."""
import json
import pytest
from nexora.providers.base import GenerationResult, Provider, ProviderCapability, ProviderError
from nexora.providers.manager import ProviderManager
from nexora.providers.pricing import PricingEntry, PricingRegistry

class ProviderSaudavel(Provider):
    def __init__(self):
        super().__init__(name="saudavel", capabilities=ProviderCapability()); self.chamadas = 0
    def generate(self, prompt, **kwargs):
        self.chamadas += 1; return GenerationResult(text="ok")
    def saudavel(self): return True

class ProviderComTokens(Provider):
    def __init__(self): super().__init__(name="tokens", capabilities=ProviderCapability())
    def generate(self, prompt, **kwargs): return GenerationResult(text="ok", usage={"prompt_tokens": 7, "completion_tokens": 5, "total_tokens": 12})
    def saudavel(self): return True

class ProviderPriced(Provider):
    def __init__(self):
        self._modelo = "modelo-teste"; super().__init__(name="priced", capabilities=ProviderCapability())
    @property
    def modelo(self): return self._modelo
    def generate(self, prompt, **kwargs): return GenerationResult(text="ok", usage={"prompt_tokens": 1_000_000, "completion_tokens": 2_000_000, "total_tokens": 3_000_000})
    def saudavel(self): return True

class ProviderDoente(Provider):
    def __init__(self): super().__init__(name="doente", capabilities=ProviderCapability())
    def generate(self, prompt, **kwargs): raise ProviderError("fora do ar")
    def saudavel(self): return False

def test_manager_estatisticas_contam_chamadas_e_erros():
    manager = ProviderManager(); manager.registrar("saudavel", ProviderSaudavel); manager.registrar("doente", ProviderDoente)
    assert manager.executar("saudavel", "oi").text == "ok"
    with pytest.raises(ProviderError): manager.executar("doente", "oi")
    stats = manager.estatisticas(); assert stats["chamadas"] == 2; assert stats["erros"] == 1; assert "doente" in stats["ultimas_falhas"]

def test_manager_executar_instancia_registra_sem_criar_outra_instancia():
    manager = ProviderManager(); manager.registrar("saudavel", ProviderSaudavel); provider = ProviderSaudavel()
    assert manager.executar_instancia("saudavel", provider, "oi").text == "ok"; assert provider.chamadas == 1; assert manager.estatisticas_provider("saudavel")["chamadas"] == 1; assert manager.obter("saudavel").chamadas == 0

def test_manager_registra_tokens_somente_quando_provider_fornece_telemetria():
    manager = ProviderManager(); manager.registrar("tokens", ProviderComTokens); manager.registrar("saudavel", ProviderSaudavel); manager.executar("tokens", "oi"); manager.executar("saudavel", "oi")
    a, b = manager.estatisticas_provider("tokens"), manager.estatisticas_provider("saudavel")
    assert a["prompt_tokens"] == 7; assert a["completion_tokens"] == 5; assert a["total_tokens"] == 12; assert a["geracoes_com_tokens"] == 1; assert b["total_tokens"] == 0; assert b["geracoes_com_tokens"] == 0

def test_manager_calcula_custo_somente_com_preco_e_tokens_reais():
    pricing = PricingRegistry([PricingEntry("priced", "modelo-teste", "USD", 0.15, 0.60, "teste-v1", "2026-09-12", "https://example.invalid")]); manager = ProviderManager(pricing_registry=pricing); manager.registrar("priced", ProviderPriced); resultado = manager.executar("priced", "oi")
    assert manager.calcular_custo(ProviderPriced(), resultado) == pytest.approx(1.35); stats = manager.estatisticas_provider("priced"); assert stats["custo_total"] == pytest.approx(1.35); assert stats["geracoes_com_custo"] == 1

def test_manager_nao_estima_custo_sem_preco():
    manager = ProviderManager(); manager.registrar("tokens", ProviderComTokens); resultado = manager.executar("tokens", "oi"); assert manager.calcular_custo(ProviderComTokens(), resultado) is None; assert manager.estatisticas_provider("tokens")["custo_total"] == 0.0; assert manager.estatisticas_provider("tokens")["geracoes_com_custo"] == 0

def test_manager_persiste_e_recarrega_tokens_medidos(tmp_path):
    caminho = tmp_path / "provider-history.json"; primeiro = ProviderManager(persistencia_path=caminho); primeiro.registrar("tokens", ProviderComTokens); primeiro.executar("tokens", "oi"); segundo = ProviderManager(persistencia_path=caminho); segundo.registrar("tokens", ProviderComTokens); stats = segundo.estatisticas_provider("tokens")
    assert stats["total_tokens"] == 12; assert stats["prompt_tokens"] == 7; assert stats["completion_tokens"] == 5; assert stats["geracoes_com_tokens"] == 1

def test_manager_healthcheck_reporta_estado():
    manager = ProviderManager(); manager.registrar("saudavel", ProviderSaudavel); assert manager.obter_healthcheck("saudavel")["saudavel"] is True; assert manager.obter_healthcheck("nao-existe")["saudavel"] is False

def test_manager_persiste_e_recarrega_historico(tmp_path):
    caminho = tmp_path / "provider-history.json"; primeiro = ProviderManager(persistencia_path=caminho); primeiro.registrar("saudavel", ProviderSaudavel); assert primeiro.executar("saudavel", "oi").text == "ok"; segundo = ProviderManager(persistencia_path=caminho); segundo.registrar("saudavel", ProviderSaudavel); stats = segundo.estatisticas_provider("saudavel")
    assert stats["chamadas"] == 1; assert stats["sucessos"] == 1; assert stats["erros"] == 0; assert stats["latencia_media"] is not None

def test_manager_persistencia_registra_falha_e_sobrevive_a_novo_processo(tmp_path):
    caminho = tmp_path / "provider-history.json"; primeiro = ProviderManager(persistencia_path=caminho); primeiro.registrar("doente", ProviderDoente)
    with pytest.raises(ProviderError): primeiro.executar("doente", "oi")
    segundo = ProviderManager(persistencia_path=caminho); segundo.registrar("doente", ProviderDoente); stats = segundo.estatisticas_provider("doente")
    assert stats["chamadas"] == 1; assert stats["erros"] == 1; assert stats["ultima_falha"] == "fora do ar"

def test_manager_persistencia_tem_schema_e_escrita_atomica(tmp_path):
    caminho = tmp_path / "provider-history.json"; manager = ProviderManager(persistencia_path=caminho); manager.registrar("saudavel", ProviderSaudavel); manager.executar("saudavel", "oi"); dados = json.loads(caminho.read_text(encoding="utf-8"))
    assert dados["schema_version"] == 4; assert dados["providers"]["saudavel"]["chamadas"] == 1; assert "models" in dados; assert not caminho.with_name(".provider-history.json.tmp").exists()

def test_manager_persistencia_ignora_arquivo_invalido(tmp_path):
    caminho = tmp_path / "provider-history.json"; caminho.write_text("{invalido", encoding="utf-8"); manager = ProviderManager(persistencia_path=caminho); manager.registrar("saudavel", ProviderSaudavel); assert manager.estatisticas_provider("saudavel")["chamadas"] == 0

def test_manager_persistencia_pode_ser_configurada_por_variavel_de_ambiente(tmp_path, monkeypatch):
    caminho = tmp_path / "env-history.json"; monkeypatch.setenv("NEXORA_PROVIDER_HISTORY_PATH", str(caminho)); manager = ProviderManager(); manager.registrar("saudavel", ProviderSaudavel); manager.executar("saudavel", "oi"); assert caminho.exists(); dados = json.loads(caminho.read_text(encoding="utf-8")); assert dados["providers"]["saudavel"]["sucessos"] == 1
