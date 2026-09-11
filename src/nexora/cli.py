"""CLI primaria da NEXORA."""
import argparse
import sys
from pathlib import Path

from nexora import __about__
from nexora.agentes.coding import CodingAgent
from nexora.agentes.pesquisa import ResearchAgent
from nexora.orquestracao.orquestrador import Orquestrador
from nexora.orquestracao.roteador import Roteador
from nexora.providers.fake import FakeProvider
from nexora.providers.groq import ProviderGroq
from nexora.providers.registry import RegistryProviders
from nexora.tools.registry import Ferramenta, RegistryFerramentas
from nexora.experiencia.registro import RegistroExperiencias


def _montar_registry():
    reg = RegistryProviders()
    reg.registrar("fake", lambda: FakeProvider())
    reg.registrar("groq", lambda: ProviderGroq())
    return reg


def _buscar_fake(parametros):
    return [{"titulo": "Nexora", "url": "https://nexora.dev", "trecho": "plataforma de agentes de IA"}]


def _executar_comando(objetivo_texto, alias=None):
    reg = _montar_registry()
    rot = Roteador(reg)
    prov = rot.obter_provider(objetivo_texto, alias=alias)
    orq = Orquestrador(rot, prov)
    res = orq.executar(objetivo_texto, alias=alias)
    print(f"sucesso={res["sucesso"]} etapas={res["metricas"]["total"]}")
    sys.exit(0 if res["sucesso"] else 1)


def _codar_comando(tarefa, linguagem, alias):
    reg = _montar_registry()
    rot = Roteador(reg)
    prov = rot.obter_provider(tarefa, alias=alias)
    ag = CodingAgent(prov)
    res = ag.codar(tarefa, linguagem=linguagem)
    print(f"sucesso={res.sucesso} tentativas={res.tentativas}")
    print(res.saida_final)
    sys.exit(0 if res.sucesso else 1)


def _pesquisar_comando(pergunta, quantidade, alias):
    reg = _montar_registry()
    rot = Roteador(reg)
    prov = rot.obter_provider(pergunta, alias=alias)
    ferramentas = RegistryFerramentas()
    ferramentas.registrar(Ferramenta("buscar", "busca fake", _buscar_fake))
    ag = ResearchAgent(prov, ferramentas)
    res = ag.pesquisar(pergunta, quantidade=quantidade)
    print(f"sucesso={res.sucesso} tentativas={res.tentativas}")
    print(res.saida_final)
    sys.exit(0 if res.sucesso else  1)


def _experiencia_comando(acao, arquivo):
    caminho = Path(arquivo)
    reg = RegistroExperiencias(caminho)
    if acao == "resumir":
        resumo = reg.resumir()
        print(f"total={resumo["geral"]["total"]} sucesso={resumo["geral"]["sucesso"]} falhas={resumo["geral"]["falhas"]}")
        for tipo, dados in resumo["tipos"].items():
            print(f"{tipo}: total={dados["total"]} sucesso={dados["sucesso"]} falhas={dados["falhas"]} taxa={dados["taxa_sucesso"]:.2f}")
    else:
        for r in reg.listar():
            print(f"{r["carimbo"]} {r["tipo_de_tarefa"]} sucesso={r["sucesso"]}")


def main() -> None:
    parser = argparse.ArgumentParser(prog="nexora", description="NEXORA plataforma de agentes de IA")
    parser.add_argument("--version", action="version", version=__about__.__version__)
    sub = parser.add_subparsers(dest="comando")
    sub.add_parser("info", help="informacoes da plataforma")

    p_exec = sub.add_parser("executar", help="executa um objetivo em linguagem natural")
    p_exec.add_argument("objetivo", help="objetivo em linguagem natural")
    p_exec.add_argument("--provider", dest="provider", default=None, help="alias do provider")

    p_agente = sub.add_parser("agente", help="agentes especializados da NEXORA")
    sub_ag = p_agente.add_subparsers(dest="subcomando", required=True)
    p_codar = sub_ag.add_parser("codar", help="gera codigo a partir de uma tarefa em linguagem natural")
    p_codar.add_argument("tarefa", help="tarefa de codigo em linguagem natural")
    p_codar.add_argument("--linguagem", default="python", help="linguagem alvo")
    p_codar.add_argument("--provider", dest="provider", default=None, help="alias do provider")
    p_pesquisar = sub_ag.add_parser("pesquisar", help="pesquisa um topico e sintetiza resposta com fontes")
    p_pesquisar.add_argument("pergunta", help="pergunta ou topico em linguagem natural")
    p_pesquisar.add_argument("--fontes", dest="quantidade", type=int, default=3, help="quantidade de consultas/fontes")
    p_pesquisar.add_argument("--provider", dest="provider", default=None, help="alias do provider")

    p_exp = sub.add_parser("experiencia", help="registro e resumo de experiencias")
    p_exp_sub = p_exp.add_subparsers(dest="acao", required=True)
    p_resumir = p_exp_sub.add_parser("resumir", help="resumo por tipo de tarefa")
    p_resumir.add_argument("--arquivo", required=True, help="caminho do arquivo de experiencias")
    p_listar = p_exp_sub.add_parser("listar", help="lista experiencias")
    p_listar.add_argument("--arquivo", required=True, help="caminho do arquivo de experiencias")

    args = parser.parse_args()
    if args.comando == "info":
        print(f"NEXORA {__about__.__version__} — plataforma de agentes de IA model-agnostica")
    elif args.comando == "executar":
        _executar_comando(args.objetivo, alias=args.provider)
    elif args.comando == "experiencia":
        _experiencia_comando(args.acao, arquivo=args.arquivo)
    elif args.comando == "agente":
        if args.subcomando == "pesquisar":
            _pesquisar_comando(args.pergunta, quantidade=args.quantidade, alias=args.provider)
        if args.subcomando == "codar":
            _codar_comando(args.tarefa, linguagem=args.linguagem, alias=args.provider)


if __name__ == "__main__":
    main()

