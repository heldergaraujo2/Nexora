"""Historico persistente de qualidade por tipo de tarefa e provider/modelo."""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from nexora.runtime.avaliacao import ResultadoAvaliacao


class HistoricoAvaliacao:
    """Persiste somente qualidade observada; nunca estima qualidade ausente."""

    _SCHEMA_VERSION = 1

    def __init__(self, persistencia_path: str | Path | None = None) -> None:
        caminho = persistencia_path if persistencia_path is not None else os.getenv("NEXORA_EVALUATION_HISTORY_PATH")
        self._persistencia_path = Path(caminho) if caminho else None
        self._metricas: dict[str, dict[str, dict[str, dict[str, Any]]]] = {}
        self._carregar()

    @staticmethod
    def _vazio() -> dict[str, Any]:
        return {"avaliacoes": 0, "sucessos": 0, "score_total": 0.0}

    def registrar(self, provider: str, modelo: str, tipo_tarefa: str, avaliacao: ResultadoAvaliacao | dict[str, Any]) -> None:
        p = provider.strip().lower()
        m = modelo.strip()
        t = tipo_tarefa.strip().lower()
        if not p or not m or not t:
            raise ValueError("provider, modelo e tipo_tarefa sao obrigatorios")
        dados = avaliacao.para_dict() if isinstance(avaliacao, ResultadoAvaliacao) else avaliacao
        if not isinstance(dados, dict):
            raise TypeError("avaliacao deve ser ResultadoAvaliacao ou dict")
        score = dados.get("score")
        sucesso = dados.get("sucesso")
        if not isinstance(score, (int, float)) or isinstance(score, bool) or not 0.0 <= float(score) <= 1.0:
            raise ValueError("score da avaliacao deve estar entre 0 e 1")
        if not isinstance(sucesso, bool):
            raise ValueError("sucesso da avaliacao deve ser booleano")
        metricas = self._metricas.setdefault(p, {}).setdefault(m, {}).setdefault(t, self._vazio())
        metricas["avaliacoes"] += 1
        metricas["sucessos"] += int(sucesso)
        metricas["score_total"] += float(score)
        self._salvar()

    def estatisticas(self, provider: str, modelo: str, tipo_tarefa: str) -> dict[str, Any]:
        p = provider.strip().lower()
        m = modelo.strip()
        t = tipo_tarefa.strip().lower()
        metricas = self._metricas.get(p, {}).get(m, {}).get(t, self._vazio())
        total = int(metricas["avaliacoes"])
        return {
            "avaliacoes": total,
            "sucessos": int(metricas["sucessos"]),
            "score_medio": float(metricas["score_total"]) / total if total else None,
            "taxa_sucesso": int(metricas["sucessos"]) / total if total else None,
        }

    def estatisticas_todas(self) -> dict[str, dict[str, dict[str, dict[str, Any]]]]:
        return {
            provider: {
                modelo: {tipo: self._estatisticas_metricas(metricas) for tipo, metricas in tipos.items()}
                for modelo, tipos in modelos.items()
            }
            for provider, modelos in self._metricas.items()
        }

    @staticmethod
    def _estatisticas_metricas(metricas: dict[str, Any]) -> dict[str, Any]:
        total = int(metricas["avaliacoes"])
        return {
            "avaliacoes": total,
            "sucessos": int(metricas["sucessos"]),
            "score_medio": float(metricas["score_total"]) / total if total else None,
            "taxa_sucesso": int(metricas["sucessos"]) / total if total else None,
        }

    @classmethod
    def _validar_metricas(cls, valores: Any) -> dict[str, Any] | None:
        if not isinstance(valores, dict):
            return None
        try:
            avaliacoes = int(valores.get("avaliacoes", 0))
            sucessos = int(valores.get("sucessos", 0))
            score_total = float(valores.get("score_total", 0.0))
        except (TypeError, ValueError):
            return None
        if avaliacoes < 0 or sucessos < 0 or sucessos > avaliacoes or score_total < 0 or score_total > avaliacoes:
            return None
        return {"avaliacoes": avaliacoes, "sucessos": sucessos, "score_total": score_total}

    def _carregar(self) -> None:
        if self._persistencia_path is None or not self._persistencia_path.exists():
            return
        try:
            dados = json.loads(self._persistencia_path.read_text(encoding="utf-8"))
        except (OSError, ValueError, json.JSONDecodeError):
            return
        if not isinstance(dados, dict) or dados.get("schema_version") != self._SCHEMA_VERSION:
            return
        metricas = dados.get("metrics")
        if not isinstance(metricas, dict):
            return
        for provider, modelos in metricas.items():
            if not isinstance(provider, str) or not isinstance(modelos, dict):
                continue
            destino_modelos = self._metricas.setdefault(provider.strip().lower(), {})
            for modelo, tipos in modelos.items():
                if not isinstance(modelo, str) or not isinstance(tipos, dict):
                    continue
                destino_tipos = destino_modelos.setdefault(modelo, {})
                for tipo, valores in tipos.items():
                    if not isinstance(tipo, str):
                        continue
                    validado = self._validar_metricas(valores)
                    if validado is not None:
                        destino_tipos[tipo.strip().lower()] = validado

    def _salvar(self) -> None:
        if self._persistencia_path is None:
            return
        destino = self._persistencia_path
        payload = {"schema_version": self._SCHEMA_VERSION, "metrics": self._metricas}
        try:
            destino.parent.mkdir(parents=True, exist_ok=True)
            temporario = destino.with_name(f".{destino.name}.tmp")
            temporario.write_text(json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")), encoding="utf-8")
            os.replace(temporario, destino)
        except OSError:
            return
