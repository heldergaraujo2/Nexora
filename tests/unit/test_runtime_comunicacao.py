from nexora.comunicacao import CommunicationBus, EstadoMensagem
from nexora.runtime.agente import AgenteRuntime


class Falha:
    plano = "ajuste_prompt"
    motivo = "saida vazia"

    def para_dict(self):
        return {"plano": self.plano, "motivo": self.motivo}


def test_runtime_publica_ciclo_no_bus():
    bus = CommunicationBus()
    runtime = AgenteRuntime(
        executar=lambda objetivo: f"ok: {objetivo}",
        verificar=lambda saida: bool(saida),
        analisar=lambda observacao: Falha(),
        corregir=lambda objetivo, falha: objetivo,
        communication_bus=bus,
        agent_id="coding-agent",
    )

    resultado = runtime.executar("criar componente")

    assert resultado.sucesso is True
    mensagens = bus.listar(remetente="coding-agent")
    assert [m.tipo for m in mensagens] == ["agente.inicio", "agente.resultado"]
    assert all(bus.estado(m.id) == EstadoMensagem.PENDENTE for m in mensagens)


def test_runtime_sem_bus_continua_compativel():
    runtime = AgenteRuntime(
        executar=lambda objetivo: objetivo,
        verificar=lambda saida: True,
        analisar=lambda observacao: Falha(),
        corregir=lambda objetivo, falha: objetivo,
    )

    resultado = runtime.executar("teste")

    assert resultado.sucesso is True
