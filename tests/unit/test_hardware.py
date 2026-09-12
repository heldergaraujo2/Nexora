from __future__ import annotations

from nexora.runtime.hardware import DetectorHardware, PerfilHardware, classificar_hardware


def test_detector_hardware_retorna_perfil_basico():
    perfil = DetectorHardware().detectar()
    assert perfil.sistema
    assert perfil.arquitetura
    assert perfil.cpu_nucleos >= 1
    assert perfil.gpu_nome == ""
    assert perfil.vram_bytes == 0


def test_classificacao_high_por_vram():
    perfil = PerfilHardware("Windows", "AMD64", 6, 16 * 1024**3, "GPU", 8 * 1024**3)
    assert classificar_hardware(perfil) == "high"


def test_classificacao_medium_por_ram():
    perfil = PerfilHardware("Linux", "x86_64", 4, 16 * 1024**3)
    assert classificar_hardware(perfil) == "medium"


def test_classificacao_basic_sem_recursos_suficientes():
    perfil = PerfilHardware("Linux", "x86_64", 2, 8 * 1024**3)
    assert classificar_hardware(perfil) == "basic"
