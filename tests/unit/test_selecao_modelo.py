from nexora.providers.modelos import perfil_modelo
from nexora.runtime.hardware import PerfilHardware
from nexora.runtime.selecao_modelo import selecionar_modelos


def hw(ram_gb=16):
    return PerfilHardware("Windows", "AMD64", 8, ram_gb * 1024**3)


def test_selecao_prioriza_modelo_adequado_para_tarefa():
    modelos = [
        ("general-7b", perfil_modelo("general-7b", contexto=32768, parametros="7B")),
        ("qwen2.5-coder:7b", perfil_modelo("qwen2.5-coder:7b", contexto=32768, parametros="7B")),
    ]
    candidatos = selecionar_modelos(modelos, hw(), tarefa="coding", contexto_necessario=16000)
    assert [c.nome for c in candidatos] == ["qwen2.5-coder:7b", "general-7b"]


def test_selecao_remove_modelo_inadequado():
    modelos = [
        ("coder-32b", perfil_modelo("coder-32b", contexto=32768, parametros="32B")),
        ("coder-7b", perfil_modelo("coder-7b", contexto=32768, parametros="7B")),
    ]
    candidatos = selecionar_modelos(modelos, hw(), tarefa="coding")
    assert [c.nome for c in candidatos] == ["coder-7b"]


def test_selecao_respeita_limite_e_ordem_de_desempate():
    modelos = [
        ("a-7b", perfil_modelo("a-7b", contexto=32768, parametros="7B")),
        ("b-7b", perfil_modelo("b-7b", contexto=32768, parametros="7B")),
        ("c-7b", perfil_modelo("c-7b", contexto=32768, parametros="7B")),
    ]
    candidatos = selecionar_modelos(modelos, hw(), limite=2)
    assert [c.nome for c in candidatos] == ["a-7b", "b-7b"]


def test_selecao_com_limite_zero_nao_retorna_candidatos():
    modelos = [("coder-7b", perfil_modelo("coder-7b", parametros="7B"))]
    assert selecionar_modelos(modelos, hw(), limite=0) == []
