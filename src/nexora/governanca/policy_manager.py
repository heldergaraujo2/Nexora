"""Lifecycle seguro para carregamento e substituicao de politicas da NEXORA."""
from __future__ import annotations

from pathlib import Path
from threading import RLock
from typing import Callable

from ..auditoria.registro import RegistroAuditoria
from .policy import PolicyEngine
from .policy_loader import carregar_policy_toml


class GerenciadorPolitica:
    """Mantem uma politica ativa e permite reload atomico apos validacao.

    A politica atual nunca e substituida por uma configuracao invalida. O lock
    protege a troca do objeto e a leitura da referencia ativa em processos com
    multiplas threads.
    """

    def __init__(
        self,
        policy: PolicyEngine,
        *,
        auditoria: RegistroAuditoria | None = None,
        loader: Callable[[Path], PolicyEngine] = carregar_policy_toml,
    ) -> None:
        self._validar_policy(policy)
        self._policy = policy
        self.auditoria = auditoria
        self.loader = loader
        self._lock = RLock()

    @staticmethod
    def _validar_policy(policy: PolicyEngine) -> None:
        if not isinstance(policy, PolicyEngine):
            raise TypeError("policy deve ser uma instancia de PolicyEngine")

    @property
    def policy(self) -> PolicyEngine:
        with self._lock:
            return self._policy

    @property
    def fingerprint(self) -> str:
        return self.policy.fingerprint

    def reload(self, caminho: Path) -> PolicyEngine:
        """Valida uma nova politica antes de troca-la atomica e audita o resultado."""
        caminho = Path(caminho)
        anterior = self.policy
        try:
            candidata = self.loader(caminho)
            self._validar_policy(candidata)
        except Exception as exc:
            self._auditar(
                "politica.reload.rejeitado",
                caminho,
                anterior,
                None,
                str(exc),
            )
            raise

        with self._lock:
            self._policy = candidata

        self._auditar(
            "politica.reload.aplicado",
            caminho,
            anterior,
            candidata,
            None,
        )
        return candidata

    def _auditar(
        self,
        evento: str,
        caminho: Path,
        anterior: PolicyEngine,
        candidata: PolicyEngine | None,
        erro: str | None,
    ) -> None:
        if self.auditoria is None:
            return
        self.auditoria.registrar(
            evento,
            entidade="politica",
            entidade_id=candidata.fingerprint if candidata is not None else anterior.fingerprint,
            dados={
                "origem": str(caminho),
                "fingerprint_anterior": anterior.fingerprint,
                "fingerprint_novo": candidata.fingerprint if candidata is not None else None,
                "versao_anterior": anterior.versao,
                "versao_nova": candidata.versao if candidata is not None else None,
                "erro": erro,
            },
        )


__all__ = ["GerenciadorPolitica"]
