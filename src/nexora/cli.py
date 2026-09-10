"""CLI primaria da NEXORA."""
import argparse
import sys

from nexora import __about__
from nexora.orquestracao.orquestrador import Orquestrador
from nexora.orquestracao.roteador import Roteador
from nexora.providers.fake import FakeProvider
from nexora.providers.groq import ProviderGroq
from nexora.providers.registry import RegistryProviders


def _montar_registry():
    reg = RegistryProviders()
    reg.registrar("fake", lambda: FakeProvider())
    reg.registrar("groq", lambda: ProviderGroq())
    return reg


def _executar_comando(objetivo_texto, alias=None):
    reg = _montar_registry()
    rot = Roteador(reg)
    prov = rot.obter_provider(objetivo_texto, alias=alias)
    orq = Orquestrador(rot, prov)
    res = orq.executar(objetivo_texto, alias=alias)
    print(f"sucesso={res['sucesso']} etapas={res['metricas']['total']}")
    sys.exit(0 if res['sucesso'] else 1)


def main() -> None:
    parser = argparse.ArgumentParser(prog="nexora", description="NEXORA plataforma de agentes de IA")
    parser.add_argument("--version", action="version", version=__about__.__version__)
    sub = parser.add_subparsers(dest="comando")
    sub.add_parser("info", help="informacoes da plataforma")
    p_exec = sub.add_parser("executar", help="executa um objetivo em linguagem natural")
    p_exec.add_argument("objetivo", help="objetivo em linguagem natural")
    p_exec.add_argument("--provider", dest="provider", default=None, help="alias do provider")
    args = parser.parse_args()
    if args.comando == "info":
        print(f"NEXORA {__about__.__version__} — plataforma de agentes de IA model-agnostica")
    elif args.comando == "executar":
        _executar_comando(args.objetivo, alias=args.provider)


if __name__ == "__main__":
    main()