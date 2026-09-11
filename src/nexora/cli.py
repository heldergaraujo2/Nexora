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
from nexora.experimentacao.experimento import ExecutorExperimentos, Experimento
from nexora.evolucao.registro import Aprendizado, RecomendadorEvolucao, RegistroAprendizados


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
    sys.exit(0 if res.sucesso else 1)


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


def _experimento_comando(nome, tarefa, variantes, alias):
    reg = _montar_registry()
    rot = Roteador(reg)
    prov = rot.obter_provider(tarefa, alias=alias)
    exp = Experimento(nome=nome, tarefa=tarefa)
    for variante in variantes:
        exp.adicionar_variante(variante)
    executor = ExecutorExperimentos(prov)
    res = executor.executar(exp)
    print(f"experimento={res["experimento"]} variantes={res["total_variantes"]} sucessos={res["sucessos"]}")
    for r in res["resultados"]:
        print(f"  {r["indice"]}: sucesso={r["sucesso"]} tentativas={r["tentativas"]}")
    sys.exit(0 if res["sucessos"] == res["total_variantes"] else 1)


def _evoluir_comando(acao, arquivo, tarefa=None):
    registro = RegistroAprendizados(Path(arquivo))
    if acao == "aprender":
        aprendizado = Aprendizado(tarefa=tarefa, melhor_variante="manual", taxa_sucesso=1.0, total_execucoes=1)
        registro.registrar(aprendizado)
        print(f"aprendizado registrado para: {tarefa}")
    else:
        recom = RecomendadorEvolucao(registro)
        melhor = recom.recomendar(tarefa) if tarefa else None
        if melhor:
            print(f"recomendado={melhor.melhor_variante} taxa={melhor.taxa_sucesso:.2f}")
        else:
            print("nenhum aprendizado encontrado")


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

    p_expm = sub.add_parser("experimento", help="define e roda experimentos de abordagem")
    p_expm_sub = p_expm.add_subparsers(dest="acao", required=True)
    p_rodar = p_expm_sub.add_parser("rodar", help="roda um experimento com variantes")
    p_rodar.add_argument("--nome", required=True, help="nome do experimento")
    p_rodar.add_argument("--tarefa", required=True, help="tarefa em linguagem natural")
    p_rodar.add_argument("--variante", dest="variantes", action="append", required=True, help="variante de abordagem (repetivel)")
    p_rodar.add_argument("--provider", dest="provider", default=None, help="alias do provider")

    p_evol = sub.add_parser("evoluir", help="registra aprendizados e recomenda evolucao")
    p_evol_sub = p_evol.add_subparsers(dest="acao", required=True)
    p_aprender = p_evol_sub.add_parser("aprender", help="registra um aprendizado")
    p_aprender.add_argument("--tarefa", required=True, help="tarefa do aprendizado")
    p_aprender.add_argument("--arquivo", required=True, help="caminho do arquivo de aprendizados")
    p_recomendar = p_evol_sub.add_parser("recomendar", help="recomenda melhor abordagem para uma tarefa")
    p_recomendar.add_argument("--tarefa", required=True, help="tarefa a recomendar")
    p_recomendar.add_argument("--arquivo", required=True, help="caminho do arquivo de aprendizados")

    args = parser.parse_args()
    if args.comando == "info":
        print(f"NEXORA {__about__.__version__} — plataforma de agentes de IA model-agnostica")
    elif args.comando == "executar":
        _executar_comando(args.objetivo, alias=args.provider)
    elif args.comando == "experiencia":
        _experiencia_comando(args.acao, arquivo=args.arquivo)
    elif args.comando == "experimento":
        _experimento_comando(args.nome, args.tarefa, args.variantes, alias=args.provider)
    elif args.comando == "evoluir":
        _evoluir_comando(args.acao, args.arquivo, tarefa=args.tarefa)
    elif args.comando == "agente":
        if args.subcomando == "pesquisar":
            _pesquisar_comando(args.pergunta, quantidade=args.quantidade, alias=args.provider)
        if args.subcomando == "codar":
            _codar_comando(args.tarefa, linguagem=args.linguagem, alias=args.provider)


if __name__ == "__main__":
    main()

