"""ProviderManager: monitora chamadas, latencia, tokens e custo real."""
from __future__ import annotations

import json
import os
import time
from pathlib import Path
from typing import Any

from nexora.providers.base import GenerationResult, ProviderCapability
from nexora.providers.pricing import PRICING_REGISTRY, PricingRegistry


class ProviderManager:
    """Envolve providers e registra metricas globais, por provider e por modelo."""

    _SCHEMA_VERSION = 4

    def __init__(self, persistencia_path: str | Path | None = None, pricing_registry: PricingRegistry | None = None) -> None:
        self._fabricas: dict[str, Any] = {}
        self._chamadas: int = 0
        self._erros: int = 0
        self._tempo_total: float = 0.0
        self._ultimas_falhas: dict[str, str] = {}
        self._metricas_provider: dict[str, dict[str, Any]] = {}
        self._metricas_modelo: dict[str, dict[str, dict[str, Any]]] = {}
        self._pricing_registry = pricing_registry or PRICING_REGISTRY
        caminho_env = os.getenv("NEXORA_PROVIDER_HISTORY_PATH")
        caminho = persistencia_path if persistencia_path is not None else caminho_env
        self._persistencia_path = Path(caminho) if caminho else None
        self._carregar_historico()

    @staticmethod
    def _metricas_vazias() -> dict[str, Any]:
        return {"chamadas": 0, "sucessos": 0, "erros": 0, "tempo_total": 0.0, "prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0, "geracoes_com_tokens": 0, "custo_total": 0.0, "geracoes_com_custo": 0}

    def registrar(self, nome: str, fabrica: Any) -> None:
        chave = nome.strip().lower()
        self._fabricas[chave] = fabrica
        self._metricas_provider.setdefault(chave, self._metricas_vazias())
        self._metricas_modelo.setdefault(chave, {})

    def obter(self, nome: str) -> Any:
        chave = nome.strip().lower()
        fabrica = self._fabricas[chave]
        return fabrica() if callable(fabrica) else fabrica

    def obter_com_modelo(self, nome: str, modelo: str) -> Any:
        chave = nome.strip().lower()
        fabrica = self._fabricas[chave]
        if not callable(fabrica):
            raise TypeError(f"Provider {chave} nao possui factory configuravel por modelo")
        return fabrica(modelo=modelo)

    def executar(self, nome: str, prompt: str, **kwargs: Any):
        chave = nome.strip().lower()
        return self.executar_instancia(chave, self.obter(nome), prompt, **kwargs)

    def executar_instancia(self, nome: str, provider: Any, prompt: str, **kwargs: Any):
        """Executa uma instancia ja selecionada e registra metricas reais."""
        chave = nome.strip().lower()
        inicio = time.monotonic()
        self._chamadas += 1
        metricas = self._metricas_provider.setdefault(chave, self._metricas_vazias())
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
            self._registrar_usage(metricas, chave, provider, resultado, inicio)
            return resultado
        finally:
            decorrido = time.monotonic() - inicio
            self._tempo_total += decorrido
            metricas["tempo_total"] += decorrido
            modelo = self._modelo_provider(provider)
            if modelo:
                metricas_modelo = self._metricas_modelo.setdefault(chave, {}).setdefault(modelo, self._metricas_vazias())
                metricas_modelo["tempo_total"] += decorrido
                # chamadas/sucessos/erros sao atualizados no bloco principal para
                # preservar a semantica mesmo quando generate() levanta excecao.
                if metricas_modelo["chamadas"] == 0 or metricas_modelo["chamadas"] < metricas["chamadas"]:
                    metricas_modelo["chamadas"] += 1
                    if metricas.get("sucessos", 0) > 0 and metricas.get("erros", 0) == 0:
                        metricas_modelo["sucessos"] += 1
                    elif metricas.get("erros", 0) > 0:
                        # Corrigido abaixo por _registrar_modelo_resultado quando ha
                        # uma execucao real; este ramo existe apenas para falhas.
                        metricas_modelo["erros"] += 1
            self._salvar_historico()

    def _registrar_usage(self, metricas: dict[str, Any], provider_name: str, provider: Any, resultado: Any, inicio: float) -> None:
        modelo = self._modelo_provider(provider)
        metricas_modelo = None
        if modelo:
            metricas_modelo = self._metricas_modelo.setdefault(provider_name, {}).setdefault(modelo, self._metricas_vazias())
            # O bloco finally garante a contagem base; aqui marcamos sucesso.
            metricas_modelo["sucessos"] += 1
        if not isinstance(resultado, GenerationResult) or not isinstance(resultado.usage, dict):
            return
        valores: dict[str, int] = {}
        for chave in ("prompt_tokens", "completion_tokens", "total_tokens"):
            valor = resultado.usage.get(chave)
            if isinstance(valor, int) and valor >= 0:
                valores[chave] = valor
        if not valores:
            return
        metricas["prompt_tokens"] += valores.get("prompt_tokens", 0)
        metricas["completion_tokens"] += valores.get("completion_tokens", 0)
        metricas["total_tokens"] += valores.get("total_tokens", 0)
        metricas["geracoes_com_tokens"] += 1
        if metricas_modelo is not None:
            metricas_modelo["prompt_tokens"] += valores.get("prompt_tokens", 0)
            metricas_modelo["completion_tokens"] += valores.get("completion_tokens", 0)
            metricas_modelo["total_tokens"] += valores.get("total_tokens", 0)
            metricas_modelo["geracoes_com_tokens"] += 1

        prompt_tokens = valores.get("prompt_tokens")
        completion_tokens = valores.get("completion_tokens")
        if prompt_tokens is not None and completion_tokens is not None and modelo:
            custo = self._pricing_registry.calculate(provider_name, modelo, prompt_tokens=prompt_tokens, completion_tokens=completion_tokens)
            if custo is not None:
                metricas["custo_total"] += custo
                metricas["geracoes_com_custo"] += 1
                if metricas_modelo is not None:
                    metricas_modelo["custo_total"] += custo
                    metricas_modelo["geracoes_com_custo"] += 1

    @staticmethod
    def _modelo_provider(provider: Any) -> str:
        for atributo in ("modelo", "model", "_modelo"):
            valor = getattr(provider, atributo, "")
            if isinstance(valor, str) and valor.strip():
                return valor.strip()
        return ""

    def calcular_custo(self, provider: Any, resultado: Any) -> float | None:
        """Calcula custo somente com uso medido e preco publicado."""
        if not isinstance(resultado, GenerationResult) or not isinstance(resultado.usage, dict):
            return None
        prompt_tokens = resultado.usage.get("prompt_tokens")
        completion_tokens = resultado.usage.get("completion_tokens")
        provider_name = getattr(provider, "name", "")
        modelo = self._modelo_provider(provider)
        if not isinstance(provider_name, str) or not modelo:
            return None
        if not isinstance(prompt_tokens, int) or prompt_tokens < 0:
            return None
        if not isinstance(completion_tokens, int) or completion_tokens < 0:
            return None
        return self._pricing_registry.calculate(provider_name, modelo, prompt_tokens=prompt_tokens, completion_tokens=completion_tokens)

    def _carregar_historico(self) -> None:
        if self._persistencia_path is None or not self._persistencia_path.exists():
            return
        try:
            dados = json.loads(self._persistencia_path.read_text(encoding="utf-8"))
        except (OSError, ValueError, json.JSONDecodeError):
            return
        if not isinstance(dados, dict) or dados.get("schema_version") not in {1, 2, 3, self._SCHEMA_VERSION}:
            return
        metricas = dados.get("providers")
        falhas = dados.get("ultimas_falhas")
        if not isinstance(metricas, dict) or not isinstance(falhas, dict):
            return
        for nome, valores in metricas.items():
            if not isinstance(nome, str) or not isinstance(valores, dict):
                continue
            try:
                campos = {campo: int(valores.get(campo, 0)) for campo in ("chamadas", "sucessos", "erros", "prompt_tokens", "completion_tokens", "total_tokens", "geracoes_com_tokens", "geracoes_com_custo")}
                tempo_total = float(valores.get("tempo_total", 0.0))
                custo_total = float(valores.get("custo_total", 0.0))
            except (TypeError, ValueError):
                continue
            if min(*campos.values(), tempo_total, custo_total) < 0:
                continue
            chave = nome.strip().lower()
            self._metricas_provider[chave] = {**campos, "tempo_total": tempo_total, "custo_total": custo_total}
            self._chamadas += campos["chamadas"]
            self._erros += campos["erros"]
            self._tempo_total += tempo_total
        modelos = dados.get("models", {})
        if isinstance(modelos, dict):
            for provider, por_modelo in modelos.items():
                if not isinstance(provider, str) or not isinstance(por_modelo, dict):
                    continue
                destino = self._metricas_modelo.setdefault(provider.strip().lower(), {})
                for modelo, valores in por_modelo.items():
                    metricas_modelo = self._validar_metricas(valores)
                    if metricas_modelo is not None:
                        destino[str(modelo)] = metricas_modelo
        self._ultimas_falhas = {nome: valor for nome, valor in falhas.items() if isinstance(nome, str) and isinstance(valor, str)}

    @classmethod
    def _validar_metricas(cls, valores: Any) -> dict[str, Any] | None:
        if not isinstance(valores, dict):
            return None
        try:
            campos = {campo: int(valores.get(campo, 0)) for campo in ("chamadas", "sucessos", "erros", "prompt_tokens", "completion_tokens", "total_tokens", "geracoes_com_tokens", "geracoes_com_custo")}
            tempo_total = float(valores.get("tempo_total", 0.0))
            custo_total = float(valores.get("custo_total", 0.0))
        except (TypeError, ValueError):
            return None
        if min(*campos.values(), tempo_total, custo_total) < 0:
            return None
        return {**campos, "tempo_total": tempo_total, "custo_total": custo_total}

    def _salvar_historico(self) -> None:
        if self._persistencia_path is None:
            return
        destino = self._persistencia_path
        payload = {"schema_version": self._SCHEMA_VERSION, "providers": self._metricas_provider, "models": self._metricas_modelo, "ultimas_falhas": self._ultimas_falhas}
        try:
            destino.parent.mkdir(parents=True, exist_ok=True)
            temporario = destino.with_name(f".{destino.name}.tmp")
            temporario.write_text(json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")), encoding="utf-8")
            os.replace(temporario, destino)
        except OSError:
            return

    def estatisticas(self) -> dict[str, Any]:
        total = self._chamadas
        return {"chamadas": total, "erros": self._erros, "latencia_media": (self._tempo_total / total) if total else None, "ultimas_falhas": dict(self._ultimas_falhas)}

    @staticmethod
    def _estatisticas_metricas(metricas: dict[str, Any], ultima_falha: str | None = None) -> dict[str, Any]:
        total = int(metricas["chamadas"])
        sucessos = int(metricas["sucessos"])
        erros = int(metricas["erros"])
        return {"chamadas": total, "sucessos": sucessos, "erros": erros, "latencia_media": (float(metricas["tempo_total"]) / total) if total else None, "taxa_sucesso": (sucessos / total) if total else None, "taxa_erro": (erros / total) if total else None, "ultima_falha": ultima_falha, "prompt_tokens": int(metricas.get("prompt_tokens", 0)), "completion_tokens": int(metricas.get("completion_tokens", 0)), "total_tokens": int(metricas.get("total_tokens", 0)), "geracoes_com_tokens": int(metricas.get("geracoes_com_tokens", 0)), "custo_total": float(metricas.get("custo_total", 0.0)), "geracoes_com_custo": int(metricas.get("geracoes_com_custo", 0))}

    def estatisticas_provider(self, nome: str) -> dict[str, Any]:
        chave = nome.strip().lower()
        metricas = self._metricas_provider.get(chave, self._metricas_vazias())
        return self._estatisticas_metricas(metricas, self._ultimas_falhas.get(chave))

    def estatisticas_modelo(self, provider: str, modelo: str) -> dict[str, Any]:
        """Retorna metricas medidas especificamente para provider + modelo."""
        provedor = provider.strip().lower()
        nome_modelo = modelo.strip()
        metricas = self._metricas_modelo.get(provedor, {}).get(nome_modelo)
        if metricas is None:
            return self._estatisticas_metricas(self._metricas_vazias())
        return self._estatisticas_metricas(metricas, self._ultimas_falhas.get(provedor))

    def estatisticas_modelos(self, provider: str | None = None) -> dict[str, dict[str, dict[str, Any]]]:
        """Retorna historico por modelo, opcionalmente limitado a um provider."""
        if provider is None:
            provedores = self._metricas_modelo
        else:
            chave = provider.strip().lower()
            provedores = {chave: self._metricas_modelo.get(chave, {})}
        return {p: {m: self._estatisticas_metricas(v, self._ultimas_falhas.get(p)) for m, v in modelos.items()} for p, modelos in provedores.items()}

    def estatisticas_providers(self) -> dict[str, dict[str, Any]]:
        return {nome: self.estatisticas_provider(nome) for nome in self.nomes()}

    def obter_healthcheck(self, nome: str) -> dict[str, Any]:
        chave = nome.strip().lower()
        try:
            provider = self.obter(nome)
            saudavel = provider.saudavel()
            return {"saudavel": saudavel, "motivo": None, "ultima_falha": self._ultimas_falhas.get(chave)}
        except Exception as erro:
            self._ultimas_falhas[chave] = str(erro)
            self._salvar_historico()
            return {"saudavel": False, "motivo": str(erro), "ultima_falha": str(erro)}

    def obter_capacidades(self, nome: str) -> ProviderCapability:
        provider = self.obter(nome)
        capacidades = getattr(provider, "capabilities", None)
        return capacidades if isinstance(capacidades, ProviderCapability) else ProviderCapability()

    def nomes(self) -> list[str]:
        return list(self._fabricas.keys())

    def saudaveis(self) -> list[str]:
        return [n for n in self.nomes() if self.obter_healthcheck(n)["saudavel"]]
