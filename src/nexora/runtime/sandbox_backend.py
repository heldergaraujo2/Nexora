"""Abstracao de backend de sandbox para a NEXORA.

A interface permite trocar subprocesso local por Docker/OpenSandbox no futuro
sem acoplar o Runtime a um produto externo.
"""
from __future__ import annotations

from dataclasses import dataclass
import subprocess
from typing import Protocol, Sequence


@dataclass(frozen=True)
class ResultadoSandbox:
    retorno: int
    saida: str
    erro: str
    backend: str


class SandboxBackend(Protocol):
    nome: str

    def executar(self, comando: Sequence[str], *, timeout: float = 30.0) -> ResultadoSandbox:
        ...


class SubprocessSandboxBackend:
    nome = "subprocess-local"

    def __init__(self, permitidos: Sequence[str] = ()) -> None:
        self._permitidos = {p.strip() for p in permitidos if p.strip()}

    def permitir(self, comando: str) -> None:
        if comando.strip():
            self._permitidos.add(comando.strip())

    def executar(self, comando: Sequence[str], *, timeout: float = 30.0) -> ResultadoSandbox:
        partes = list(comando)
        if not partes or partes[0] not in self._permitidos:
            raise PermissionError(f"comando nao permitido: {partes[0] if partes else ''}")
        try:
            r = subprocess.run(partes, capture_output=True, text=True, timeout=timeout)
            return ResultadoSandbox(r.returncode, r.stdout, r.stderr, self.nome)
        except subprocess.TimeoutExpired:
            return ResultadoSandbox(-1, "", "timeout", self.nome)
        except FileNotFoundError:
            return ResultadoSandbox(127, "", "comando inexistente", self.nome)


class BackendNaoDisponivel(RuntimeError):
    pass


class DockerSandboxBackend:
    """Adapter opcional: falha fechado quando Docker nao esta configurado."""

    nome = "docker"

    def __init__(self, imagem: str = "python:3.12-slim") -> None:
        if not imagem.strip():
            raise ValueError("imagem deve ser nao vazia")
        self.imagem = imagem

    def executar(self, comando: Sequence[str], *, timeout: float = 30.0) -> ResultadoSandbox:
        raise BackendNaoDisponivel(
            "DockerSandboxBackend e apenas contrato de integracao; configure um executor Docker explicitamente"
        )
