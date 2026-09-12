"""ProviderManager: monitora chamadas, latencia, erros e capacidades."""
from __future__ import annotations

import json
import os
import time
from pathlib import Path
from typing import Any

from nexora.providers.base import ProviderCapability


class ProviderManager:
    """Envolve providers e registra metricas globais e por provider.

    A persistencia do historico e opcional. Quando configurada, usa um JSON
    versionado e escrita atomica para sobreviver a reinicializacoes sem tornar
    o manager dependente de banco de dados.
    """

    _SCHEMA_VERSION = 1

    def __init__(self, persistencia_path: str | Path | None = None) -> None:
        self._fabricas: dict[str, Any] = {}
        self._chamadas: int = 0
        self._erros: int = 0
        self._tempo_total: float = 0.0
        self._ultimas_falhas: dict[str, str] = {}
        self._metricas_provider: dict[str, dict[str, Any]] = {}
        caminho_env = os.getenv("NEXORA_PROVIDER_HISTORY_PATH")
        caminho = persistencia_path if persistencia_path is not None else caminho_env
        self._persistencia_path = Path(caminho) if caminho else None
        self._carregar_historico()

    def registrar(self, nome: str, fabrica: Any) -> None:
        chave = nome.strip().lower()
        self._fabricas[chave] = fabrica
        self._metricas_provider.setdefault(
            chave,
            {"chamadas": 0, "sucessos": 0, "erros": 0, "tempo_total": 0.0},
        )

    def obter(self, nome: str) -> Any:
        chave = nome.strip().lower()
        fabrica = self._fabricas[chave]
        return fabrica() if callable(fabrica) else fabrica

    def obter_com_modelo(self, nome: str, modelo: str) -> Any:
        """Cria uma instancia explicitamente configurada para o modelo selecionado.

        O factory registrado precisa declarar suporte ao argumento ``modelo``.
        Nao ha fallback silencioso para outro modelo, pois isso falsificaria a
        decisao de roteamento registrada no trace.
        """
        chave = nome.strip().lower()
        fabrica = self._fabricas[chave]
        if not callable(fabrica):
            raise TypeError(f"Provider {chave} nao possui factory configuravel por modelo")
        return fabrica(modelo=modelo)

    def executar(self, nome: str, prompt: str, **kwargs: Any):
        """Executa o provider registrado, delegando a metrica para a instancia."""
        chave = nome.strip().lower()
        provider = self.obter(nome)
        return self.executar_instancia(chave, provider, prompt, **kwargs)

    def executar_instancia(self, nome: str, provider: Any, prompt: str, **kwargs: Any):
        """Executa uma instancia ja selecionada e registra as metricas reais.

        Este caminho permite ao Orquestrador executar exatamente a instancia
        escolhida pelo roteador (inclusive um modelo explicito) sem criar uma
        segunda chamada apenas para contabilizacao.
        """
        chave = nome.strip().lower()
        inicio = time.monotonic()
        self._chamadas += 1
        metricas = self._metricas_provider.setdefault(
            chave,
            {"chamadas": 0, "sucessos": 0, "erros": 0, "tempo_total": 0.0},
        )
        metricas["chamadas"] += 1
        try:
            resultado = provider.generate(prompt, **kwargs)
        except Exception as erro:
            self._erros += 1
            metricas["erros"] += 1
            self._ultimas_falhas[chave] = str(erro)
            raise
        else:
            metricas["sucessos"] += 1
            return resultado
        finally:
            decorrido = time.monotonic() - inicio
            self._tempo_total += decorrido
            metricas["tempo_total"] += decorrido
            self._salvar_historico()

    def _carregar_historico(self) -> None:
        if self._persistencia_path is None or not self._persistencia_path.exists():
            return
        try:
            dados = json.loads(self._persistencia_path.read_text(encoding="utf-8"))
        except (OSError, ValueError, json.JSONDecodeError):
            return
        if not isinstance(dados, dict) or dados.get("schema_version") != self._SCHEMA_VERSION:
            return
        metricas = dados.get("providers")
        falhas = dados.get("ultimas_falhas")
        if not isinstance(metricas, dict) or not isinstance(falhas, dict):
            return
        for nome, valores in metricas.items():
            if not isinstance(nome, str) or not isinstance(valores, dict):
                continue
            try:
                chamadas = int(valores["chamadas"])
                sucessos = int(valores["sucessos"])
                erros = int(valores["erros"])
                tempo_total = float(valores["tempo_total"])
            except (KeyError, TypeError, ValueError):
                continue
            if min(chamadas, sucessos, erros, tempo_total) < 0:
                continue
            self._metricas_provider[nome] = {
                "chamadas": chamadas,
                "sucessos": sucessos,
                "erros": erros,
                "tempo_total": tempo_total,
            }
            self._chamadas += chamadas
            self._erros += erros
            self._tempo_total += tempo_total
        self._ultimas_falhas = {
            nome: valor for nome, valor in falhas.items() if isinstance(nome, str) and isinstance(valor, str)
        }

    def _salvar_historico(self) -> None:
        if self._persistencia_path is None:
            return
        destino = self._persistencia_path
        payload = {
            "schema_version": self._SCHEMA_VERSION,
            "providers": self._metricas_provider,
            "ultimas_falhas": self._ultimas_falhas,
        }
        try:
            destino.parent.mkdir(parents=True, exist_ok=True)
            temporario = destino.with_name(f".{destino.name}.tmp")
            temporario.write_text(
                json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")),
                encoding="utf-8",
            )
            os.replace(temporario, destino)
        except OSError:
            return

    def estatisticas(self) -> dict[str, Any]:
        """Resumo das metricas de uso globais."""
        total = self._chamadas
        return {
            "chamadas": total,
            "erros": self._erros,
            "latencia_media": (self._tempo_total / total) if total else None,
            "ultimas_falhas": dict(self._ultimas_falhas),
        }

    def estatisticas_provider(self, nome: str) -> dict[str, Any]:
        """Retorna apenas metricas medidas do provider solicitado.

        Os valores sao historicos do processo atual ou de uma persistencia
        previamente carregada; nenhuma estimativa e criada.
        """
        chave = nome.strip().lower()
        metricas = self._metricas_provider.get(chave)
        if metricas is None:
            return {
                "chamadas": 0,
                "sucessos": 0,
                "erros": 0,
                "latencia_media": None,
                "taxa_sucesso": None,
                "taxa_erro": None,
                "ultima_falha": self._ultimas_falhas.get(chave),
            }
        total = int(metricas["chamadas"])
        sucessos = int(metricas["sucessos"])
        erros = int(metricas["erros"])
        return {
            "chamadas": total,
            "sucessos": sucessos,
            "erros": erros,
            "latencia_media": (float(metricas["tempo_total"]) / total) if total else None,
            "taxa_sucesso": (sucessos / total) if total else None,
            "taxa_erro": (erros / total) if total else None,
            "ultima_falha": self._ultimas_falhas.get(chave),
        }

    def estatisticas_providers(self) -> dict[str, dict[str, Any]]:
        """Retorna metricas medidas de todos os providers registrados."""
        return {nome: self.estatisticas_provider(nome) for nome in self.nomes()}

    def obter_healthcheck(self, nome: str) -> dict[str, Any]:
        """Healthcheck detalhado sem necessariamente instanciar o provider."""
        chave = nome.strip().lower()
        try:
            provider = self.obter(nome)
            saudavel = provider.saudavel()
            return {"saudavel": saudavel, "motivo": None, "ultima_falha": self._ultimas_falhas.get(chave, None)}
        except Exception as erro:
            self._ultimas_falhas[chave] = str(erro)
            self._salvar_historico()
            return {"saudavel": False, "motivo": str(erro), "ultima_falha": str(erro)}

    def obter_capacidades(self, nome: str) -> ProviderCapability:
        """Retorna capacidades declaradas, sem inventar suporte ausente."""
        provider = self.obter(nome)
        capacidades = getattr(provider, "capabilities", None)
        if isinstance(capacidades, ProviderCapability):
            return capacidades
        return ProviderCapability()

    def nomes(self) -> list[str]:
        return list(self._fabricas.keys())

    def saudaveis(self) -> list[str]:
        return [n for n in self.nomes() if self.obter_healthcheck(n)["saudavel"]]
