import pytest

from nexora.agentes import AgenteRegistro, RegistroAgentes


def test_registra_e_normaliza_capacidades() -> None:
    registro = RegistroAgentes()
    agente = registro.registrar(
        AgenteRegistro(
            id="pesquisa-1",
            nome="Pesquisador",
            capacidades=(" Pesquisa Mercado ", "web_pesquisa", "web_pesquisa"),
            prioridade=0.8,
        )
    )

    assert agente.capacidades == ("pesquisa_mercado", "web_pesquisa")
    assert registro.obter("pesquisa-1") is agente


def test_rejeita_agente_duplicado() -> None:
    registro = RegistroAgentes()
    agente = AgenteRegistro(id="a1", nome="Agente")
    registro.registrar(agente)

    with pytest.raises(ValueError, match="ja registrado"):
        registro.registrar(agente)


def test_descobre_por_capacidade_e_prioridade() -> None:
    registro = RegistroAgentes(
        [
            AgenteRegistro(id="baixo", nome="Baixo", capacidades=("pesquisa",), prioridade=0.4),
            AgenteRegistro(id="alto", nome="Alto", capacidades=("pesquisa",), prioridade=0.9),
            AgenteRegistro(id="outro", nome="Outro", capacidades=("codigo",), prioridade=1.0),
        ]
    )

    encontrados = registro.descobrir(" PESQUISA ")

    assert [item.id for item in encontrados] == ["alto", "baixo"]
    assert registro.melhor_para("pesquisa").id == "alto"


def test_agente_indisponivel_nao_e_selecionado() -> None:
    registro = RegistroAgentes(
        [AgenteRegistro(id="off", nome="Off", capacidades=("pesquisa",), disponivel=False)]
    )

    assert registro.descobrir("pesquisa") == []
    assert registro.descobrir("pesquisa", apenas_disponiveis=False)[0].id == "off"
    assert registro.melhor_para("pesquisa") is None
