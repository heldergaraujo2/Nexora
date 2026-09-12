"""Detecção portátil e somente-leitura dos recursos básicos do host."""
from __future__ import annotations

import os
import platform
import shutil
from dataclasses import dataclass


@dataclass(frozen=True)
class PerfilHardware:
    sistema: str
    arquitetura: str
    cpu_nucleos: int
    ram_bytes: int
    gpu_nome: str = ""
    vram_bytes: int = 0


class DetectorHardware:
    """Coleta informações disponíveis sem instalar software ou alterar o host."""

    def detectar(self) -> PerfilHardware:
        return PerfilHardware(
            sistema=platform.system(),
            arquitetura=platform.machine(),
            cpu_nucleos=max(1, os.cpu_count() or 1),
            ram_bytes=self._ram_bytes(),
        )

    @staticmethod
    def _ram_bytes() -> int:
        try:
            import psutil  # type: ignore
            return int(psutil.virtual_memory().total)
        except ImportError:
            return 0


def classificar_hardware(perfil: PerfilHardware) -> str:
    """Classificação conservadora para decisões futuras de instalação/modelo."""
    ram_gb = perfil.ram_bytes / (1024 ** 3) if perfil.ram_bytes else 0
    if perfil.vram_bytes >= 8 * (1024 ** 3) or ram_gb >= 32:
        return "high"
    if perfil.vram_bytes >= 4 * (1024 ** 3) or ram_gb >= 16:
        return "medium"
    return "basic"
