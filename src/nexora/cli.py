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
from nexora.seguranca.registro import Acao, RegistroPolitica
from nexora.memoria.registro import ItemMemoria, RegistroMemorias
from nexora.recursos.registro import Recurso, RegistroRecursos
from nexora.economia.registro import CustoExecucao, RegistroCustos


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



def _economia_comando(acao, arquivo, provider=None, tokens_entrada=None, tokens_saida=None):
    registro = RegistroCustos(Path(arquivo))
    if acao == "registrar":
        custo = CustoExecucao(provider=provider or "desconhecido", tokens_entrada=int(tokens_entrada or 0), tokens_saida=int(tokens_saida or 0))
        registro.registrar(custo)
        print("custo registrado")
    else:
        resumo = registro.resumir()
        print("total={} tokens={}".format(resumo["total_execucoes"], resumo["total_tokens"]))
        for nome, dados in resumo["por_provider"].items():
            print("  {}: execucoes={} tokens={}".format(nome, dados["execucoes"], dados["tokens_total"]))

def _seguranca_comando(acao, arquivo, nome=None, permitir=False):
    registro = RegistroPolitica(Path(arquivo))
    if acao == "definir":
        registro.definir(nome=nome, permitida=bool(permitir))
        print("politica definida")
    elif acao == "avaliar":
        permitida = registro.avaliar(nome)
        print("permitida={}".format(permitida))
    else:
        resumo = registro.resumir()
        print("seguranca_resumo={}".format(resumo))

def _memoria_comando(acao, arquivo, chave=None, conteudo=None):
    registro = RegistroMemorias(Path(arquivo))
    if acao == "lembrar":
        registro.lembrar(chave=chave, conteudo=conteudo)
        print("memoria registrada")
    elif acao == "buscar":
        valor = registro.buscar(chave=chave)
        print("valor={}".format(valor))
    else:
        resumo = registro.resumir()
        print("resumo={}".format(resumo))

def _recursos_comando(acao, arquivo, tipo=None, quantidade=None, executor=None):
    registro = RegistroRecursos(Path(arquivo))
    if acao == "registrar":
        registro.registrar(tipo=tipo, quantidade=float(quantidade), executor=executor)
        print("recurso registrado")
    else:
        resumo = registro.resumir()
        print("recursos_resumo={}".format(resumo))

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
    p_eco = sub.add_parser("economia", help="registra custos e resumo por provider")
    p_eco_sub = p_eco.add_subparsers(dest="acao", required=True)
    p_registrar = p_eco_sub.add_parser("registrar", help="registra um custo de execucao")
    p_registrar.add_argument("--provider", default="fake", help="alias do provider")
    p_registrar.add_argument("--tokens-entrada", dest="tokens_entrada", type=int, default=0, help="tokens de entrada")
    p_registrar.add_argument("--tokens-saida", dest="tokens_saida", type=int, default=0, help="tokens de saida")
    p_registrar.add_argument("--arquivo", required=True, help="caminho do arquivo de custos")
    p_resumir_eco = p_eco_sub.add_parser("resumir", help="resumo por provider")
    p_resumir_eco.add_argument("--arquivo", required=True, help="caminho do arquivo de custos")
    p_seg = sub.add_parser("seguranca", help="politica de permissao de acoes")
    p_seg_sub = p_seg.add_subparsers(dest="acao", required=True)
    p_def_seg = p_seg_sub.add_parser("definir", help="define a politica de uma acao")
    p_def_seg.add_argument("--acao", dest="acao_nome", required=True, help="nome da acao")
    p_def_seg.add_argument("--permitir", action="store_true", help="permite a acao")
    p_def_seg.add_argument("--arquivo", required=True, help="caminho do arquivo de politica")
    p_aval_seg = p_seg_sub.add_parser("avaliar", help="avalia se uma acao esta permitida")
    p_aval_seg.add_argument("--acao", dest="acao_nome", required=True, help="nome da acao")
    p_aval_seg.add_argument("--arquivo", required=True, help="caminho do arquivo de politica")
    p_res_seg = p_seg_sub.add_parser("resumir", help="resumo por escopo")
    p_res_seg.add_argument("--arquivo", required=True, help="caminho do arquivo de politica")
    p_mem = sub.add_parser("memoria", help="memoria persistente da plataforma")
    p_mem_sub = p_mem.add_subparsers(dest="acao", required=True)
    p_lembrar = p_mem_sub.add_parser("lembrar", help="registra uma memoria")
    p_lembrar.add_argument("--chave", required=True, help="chave da memoria")
    p_lembrar.add_argument("--conteudo", required=True, help="corpo da memoria")
    p_lembrar.add_argument("--arquivo", required=True, help="caminho do arquivo de memoria")
    p_buscar = p_mem_sub.add_parser("buscar", help="busca uma memoria por chave")
    p_buscar.add_argument("--chave", required=True, help="chave da memoria")
    p_buscar.add_argument("--arquivo", required=True, help="caminho do arquivo de memoria")
    p_res_mem = p_mem_sub.add_parser("resumir", help="resumo por escopo")
    p_res_mem.add_argument("--arquivo", required=True, help="caminho do arquivo de memoria")
    p_rec = sub.add_parser("recursos", help="consumo de recursos por executor")
    p_rec_sub = p_rec.add_subparsers(dest="acao", required=True)
    p_reg_rec = p_rec_sub.add_parser("registrar", help="registra consumo de recurso")
    p_reg_rec.add_argument("--tipo", required=True, help="tipo do recurso")
    p_reg_rec.add_argument("--quantidade", required=True, help="quantidade consumida")
    p_reg_rec.add_argument("--executor", required=True, help="executor do recurso")
    p_reg_rec.add_argument("--arquivo", required=True, help="caminho do arquivo de recursos")
    p_res_rec = p_rec_sub.add_parser("resumir", help="resumo por tipo")
    p_res_rec.add_argument("--arquivo", required=True, help="caminho do arquivo de recursos")

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
    elif args.comando == "economia":
        _economia_comando(args.acao, args.arquivo, provider=getattr(args, "provider", None), tokens_entrada=getattr(args, "tokens_entrada", None), tokens_saida=getattr(args, "tokens_saida", None))
    elif args.comando == "seguranca":
        _seguranca_comando(args.acao, args.arquivo, nome=getattr(args, "acao_nome", None), permitir=getattr(args, "permitir", False))
    elif args.comando == "memoria":
        _memoria_comando(args.acao, args.arquivo, chave=getattr(args, "chave", None), conteudo=getattr(args, "conteudo", None))
    elif args.comando == "recursos":
        _recursos_comando(args.acao, args.arquivo, tipo=getattr(args, "tipo", None), quantidade=getattr(args, "quantidade", None), executor=getattr(args, "executor", None))
    elif args.comando == "agente":
        if args.subcomando == "pesquisar":
            _pesquisar_comando(args.pergunta, quantidade=args.quantidade, alias=args.provider)
        if args.subcomando == "codar":
            _codar_comando(args.tarefa, linguagem=args.linguagem, alias=args.provider)


if __name__ == "__main__":
    main()

