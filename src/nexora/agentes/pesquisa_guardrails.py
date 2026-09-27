"""Guardrails de pesquisa: orçamento, diversidade e bloqueio conservador de destinos locais."""
from __future__ import annotations

from dataclasses import dataclass
import ipaddress
from urllib.parse import urlparse


@dataclass(frozen=True)
class OrcamentoPesquisa:
    max_consultas: int = 5
    max_fontes: int = 20
    max_dominios: int = 10

    def __post_init__(self) -> None:
        if min(self.max_consultas, self.max_fontes, self.max_dominios) < 1:
            raise ValueError("limites de pesquisa devem ser >= 1")


class GuardiaoPesquisa:
    """Aplica limites determinísticos antes de fontes entrarem no contexto do agente."""

    def __init__(self, orcamento: OrcamentoPesquisa | None = None) -> None:
        self.orcamento = orcamento or OrcamentoPesquisa()

    @staticmethod
    def destino_publico(url: str) -> bool:
        try:
            parsed = urlparse(url)
            host = parsed.hostname
            if parsed.scheme not in {"http", "https"} or not host:
                return False
            if host in {"localhost", "localhost.localdomain"}:
                return False
            try:
                endereco = ipaddress.ip_address(host)
            except ValueError:
                return True
            return not (endereco.is_private or endereco.is_loopback or endereco.is_link_local or endereco.is_reserved)
        except ValueError:
            return False

    def filtrar_fontes(self, fontes: list[dict]) -> list[dict]:
        aceitas: list[dict] = []
        dominios: set[str] = set()
        for fonte in fontes:
            url = str(fonte.get("url", ""))
            if not self.destino_publico(url):
                continue
            host = urlparse(url).hostname or ""
            if host not in dominios and len(dominios) >= self.orcamento.max_dominios:
                continue
            dominios.add(host)
            aceitas.append(dict(fonte))
            if len(aceitas) >= self.orcamento.max_fontes:
                break
        return aceitas
