import pytest
from nexora.runtime.sandbox_backend import BackendNaoDisponivel, DockerSandboxBackend, SubprocessSandboxBackend


def test_local_backend_allowlist():
    b = SubprocessSandboxBackend(["python"])
    r = b.executar(["python", "-c", "print('ok')"])
    assert r.retorno == 0 and r.saida.strip() == "ok"


def test_docker_adapter_fails_closed():
    with pytest.raises(BackendNaoDisponivel):
        DockerSandboxBackend().executar(["python", "-c", "print(1)"])
