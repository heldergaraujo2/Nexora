"""Testes do Orquestrador (Fase 3)."""
import json

from nexora.orquestracao.orquestrador import Orquestrador
from nexora.orquestracao.roteador import Roteador
from nexora.providers.fake import FakeProvider
from nexora.providers.registry import RegistryProviders
from nexora.runtime.eventos import EventStore


def _montar_orquestrador(tmp_path):
    reg = RegistryProviders()
    reg.registrar("fake", lambda: FakeProvider())
    rot = Roteador(reg)
    prov = FakeProvider()
    store = EventStore(tmp_path / "eventos.jsonl")
    return Orquestrador(rot, prov, evento_store=store)


def test_executar_objetivo_com_sucesso(tmp_path):
    res = _montar_orquestrador(tmp_path).executar("teste objetivo")
    assert res["sucesso"]
    assert res["metricas"]["total"] == 1
    assert res["etapas"][0]["ok"]


def test_executar_registra_historico(tmp_path):
    res = _montar_orquestrador(tmp_path).executar("teste historico")
    tipos = [e["tipo"] for e in res["historico"]]
    assert tipos == ["objetivo", "plano", "resultado"]


def test_executar_grava_eventos(tmp_path):
    orq = _montar_orquestrador(tmp_path)
    orq.executar("teste eventos")
    eventos = json.loads((tmp_path / "eventos.jsonl").read_text(encoding="utf-8").strip().splitlines()[-1])
    assert eventos["tipo"] == "resultado"
    assert eventos["dados"]["sucesso"]

