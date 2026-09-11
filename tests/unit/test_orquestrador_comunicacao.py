from nexora.comunicacao import CommunicationBus, EstadoMensagem
from nexora.orquestracao.orquestrador import Orquestrador


class Provider:
    def saudavel(self):
        return True

    def generate(self, texto):
        return type("Resposta", (), {"text": f"resultado: {texto}"})()


class Router:
    def obter_provider(self, objetivo, alias=None):
        return Provider()


def test_orquestrador_publica_ciclo_no_bus():
    bus = CommunicationBus()
    orquestrador = Orquestrador(
        Router(),
        Provider(),
        communication_bus=bus,
    )

    resultado = orquestrador.executar("teste de comunicacao")

    assert resultado["sucesso"] is True
    mensagens = bus.listar(remetente="orchestrator")
    assert [m.tipo for m in mensagens] == [
        "orquestracao.inicio",
        "orquestracao.plano",
        "orquestracao.tarefa.inicio",
        "orquestracao.tarefa.resultado",
        "orquestracao.resultado",
    ]
    assert all(bus.estado(m.id) == EstadoMensagem.ENTREGUE for m in mensagens)
