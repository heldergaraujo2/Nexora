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
        self._chamadas = self._erros = 0
        self._tempo_total = 0.0
        self._ultimas_falhas: dict[str, str] = {}
        self._metricas_provider: dict[str, dict[str, Any]] = {}
        self._metricas_modelo: dict[str, dict[str, dict[str, Any]]] = {}
        self._pricing_registry = pricing_registry or PRICING_REGISTRY
        caminho = persistencia_path if persistencia_path is not None else os.getenv("NEXORA_PROVIDER_HISTORY_PATH")
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
        fabrica = self._fabricas[nome.strip().lower()]
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
        modelo = self._modelo_provider(provider)
        inicio = time.monotonic()
        self._chamadas += 1
        metricas = self._metricas_provider.setdefault(chave, self._metricas_vazias())
        metricas["chamadas"] += 1
        modelo_metricas = None
        if modelo:
            modelo_metricas = self._metricas_modelo.setdefault(chave, {}).setdefault(modelo, self._metricas_vazias())
            modelo_metricas["chamadas"] += 1
        try:
            resultado = provider.generate(prompt, **kwargs)
        except Exception as erro:
            self._erros += 1
            metricas["erros"] += 1
            self._ultimas_falhas[chave] = str(erro)
            if modelo_metricas is not None:
                modelo_metricas["erros"] += 1
            raise
        else:
            metricas["sucessos"] += 1
            if modelo_metricas is not None:
                modelo_metricas["sucessos"] += 1
            self._registrar_usage(metricas, modelo_metricas, chave, provider, resultado)
            return resultado
        finally:
            decorrido = time.monotonic() - inicio
            self._tempo_total += decorrido
            metricas["tempo_total"] += decorrido
            if modelo_metricas is not None:
                modelo_metricas["tempo_total"] += decorrido
            self._salvar_historico()

    def _registrar_usage(self, metricas: dict[str, Any], modelo_metricas: dict[str, Any] | None, provider_name: str, provider: Any, resultado: Any) -> None:
        if not isinstance(resultado, GenerationResult) or not isinstance(resultado.usage, dict):
            return
        valores: dict[str, int] = {}
        for chave in ("prompt_tokens", "completion_tokens", "total_tokens"):
            valor = resultado.usage.get(chave)
            if isinstance(valor, int) and valor >= 0:
                valores[chave] = valor
        if not valores:
            return
        for alvo in (metricas, modelo_metricas):
            if alvo is not None:
                alvo["prompt_tokens"] += valores.get("prompt_tokens", 0)
                alvo["completion_tokens"] += valores.get("completion_tokens", 0)
                alvo["total_tokens"] += valores.get("total_tokens", 0)
                alvo["geracoes_com_tokens"] += 1
        prompt_tokens = valores.get("prompt_tokens")
        completion_tokens = valores.get("completion_tokens")
        modelo = self._modelo_provider(provider)
        if prompt_tokens is not None and completion_tokens is not None and modelo:
            custo = self._pricing_registry.calculate(provider_name, modelo, prompt_tokens=prompt_tokens, completion_tokens=completion_tokens)
            if custo is not None:
                for alvo in (metricas, modelo_metricas):
                    if alvo is not None:
                        alvo["custo_total"] += custo
                        alvo["geracoes_com_custo"] += 1

    @staticmethod
    def _modelo_provider(provider: Any) -> str:
        for atributo in ("modelo", "model", "_modelo"):
            valor = getattr(provider, atributo, "")
            if isinstance(valor, str) and valor.strip():
                return valor.strip()
        return ""

    def calcular_custo(self, provider: Any, resultado: Any) -> float | None:
        if not isinstance(resultado, GenerationResult) or not isinstance(resultado.usage, dict):
            return None
        prompt_tokens = resultado.usage.get("prompt_tokens")
        completion_tokens = resultado.usage.get("completion_tokens")
        provider_name = getattr(provider, "name", "")
        modelo = self._modelo_provider(provider)
        if not isinstance(provider_name, str) or not modelo or not isinstance(prompt_tokens, int) or prompt_tokens < 0 or not isinstance(completion_tokens, int) or completion_tokens < 0:
            return None
        return self._pricing_registry.calculate(provider_name, modelo, prompt_tokens=prompt_tokens, completion_tokens=completion_tokens)

    @classmethod
    def _validar_metricas(cls, valores: Any) -> dict[str, Any] | None:
        if not isinstance(valores, dict):
            return None
        try:
            campos = {c: int(valores.get(c, 0)) for c in ("chamadas", "sucessos", "erros", "prompt_tokens", "completion_tokens", "total_tokens", "geracoes_com_tokens", "geracoes_com_custo")}
            tempo_total = float(valores.get("tempo_total", 0.0))
            custo_total = float(valores.get("custo_total", 0.0))
        except (TypeError, ValueError):
            return None
        if min(*campos.values(), tempo_total, custo_total) < 0:
            return None
        return {**campos, "tempo_total": tempo_total, "custo_total": custo_total}

    def _carregar_historico(self) -> None:
        if self._persistencia_path is None or not self._persistencia_path.exists():
            return
        try:
            dados = json.loads(self._persistencia_path.read_text(encoding="utf-8"))
        except (OSError, ValueError, json.JSONDecodeError):
            return
        if not isinstance(dados, dict) or dados.get("schema_version") not in {1, 2, 3, self._SCHEMA_VERSION}:
            return
        providers = dados.get("providers")
        falhas = dados.get("ultimas_falhas")
        if not isinstance(providers, dict) or not isinstance(falhas, dict):
            return
        for nome, valores in providers.items():
            metricas = self._validar_metricas(valores)
            if metricas is None or not isinstance(nome, str):
                continue
            chave = nome.strip().lower()
            self._metricas_provider[chave] = metricas
            self._chamadas += metricas["chamadas"]
            self._erros += metricas["erros"]
            self._tempo_total += metricas["tempo_total"]
        modelos = dados.get("models", {})
        if isinstance(modelos, dict):
            for provider, por_modelo in modelos.items():
                if not isinstance(provider, str) or not isinstance(por_modelo, dict):
                    continue
                destino = self._metricas_modelo.setdefault(provider.strip().lower(), {})
                for modelo, valores in por_modelo.items():
                    metricas = self._validar_metricas(valores)
                    if metricas is not None:
                        destino[str(modelo)] = metricas
        self._ultimas_falhas = {n: v for n, v in falhas.items() if isinstance(n, str) and isinstance(v, str)}

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

    @staticmethod
    def _estatisticas_metricas(metricas: dict[str, Any], ultima_falha: str | None = None) -> dict[str, Any]:
        total, sucessos, erros = int(metricas["chamadas"]), int(metricas["sucessos"]), int(metricas["erros"])
        return {"chamadas": total, "sucessos": sucessos, "erros": erros, "latencia_media": (float(metricas["tempo_total"]) / total) if total else None, "taxa_sucesso": (sucessos / total) if total else None, "taxa_erro": (erros / total) if total else None, "ultima_falha": ultima_falha, "prompt_tokens": int(metricas.get("prompt_tokens", 0)), "completion_tokens": int(metricas.get("completion_tokens", 0)), "total_tokens": int(metricas.get("total_tokens", 0)), "geracoes_com_tokens": int(metricas.get("geracoes_com_tokens", 0)), "custo_total": float(metricas.get("custo_total", 0.0)), "geracoes_com_custo": int(metricas.get("geracoes_com_custo", 0))}

    def estatisticas(self) -> dict[str, Any]:
        return {"chamadas": self._chamadas, "erros": self._erros, "latencia_media": (self._tempo_total / self._chamadas) if self._chamadas else None, "ultimas_falhas": dict(self._ultimas_falhas)}

    def estatisticas_provider(self, nome: str) -> dict[str, Any]:
        chave = nome.strip().lower()
        return self._estatisticas_metricas(self._metricas_provider.get(chave, self._metricas_vazias()), self._ultimas_falhas.get(chave))

    def estatisticas_modelo(self, provider: str, modelo: str) -> dict[str, Any]:
        """Retorna somente o historico real de um par provider/modelo."""
        provedor, nome_modelo = provider.strip().lower(), modelo.strip()
        metricas = self._metricas_modelo.get(provedor, {}).get(nome_modelo, self._metricas_vazias())
        return self._estatisticas_metricas(metricas, self._ultimas_falhas.get(provedor))

    def estatisticas_modelos(self, provider: str | None = None) -> dict[str, dict[str, dict[str, Any]]]:
        provedores = self._metricas_modelo if provider is None else {provider.strip().lower(): self._metricas_modelo.get(provider.strip().lower(), {})}
        return {p: {m: self._estatisticas_metricas(v, self._ultimas_falhas.get(p)) for m, v in modelos.items()} for p, modelos in provedores.items()}

    def estatisticas_providers(self) -> dict[str, dict[str, Any]]:
        return {nome: self.estatisticas_provider(nome) for nome in self.nomes()}

    def obter_healthcheck(self, nome: str) -> dict[str, Any]:
        chave = nome.strip().lower()
        try:
            saudavel = self.obter(nome).saudavel()
            return {"saudavel": saudavel, "motivo": None, "ultima_falha": self._ultimas_falhas.get(chave)}
        except Exception as erro:
            self._ultimas_falhas[chave] = str(erro)
            self._salvar_historico()
            return {"saudavel": False, "motivo": str(erro), "ultima_falha": str(erro)}

    def obter_capacidades(self, nome: str) -> ProviderCapability:
        capacidades = getattr(self.obter(nome), "capabilities", None)
        return capacidades if isinstance(capacidades, ProviderCapability) else ProviderCapability()

    def nomes(self) -> list[str]:
        return list(self._fabricas.keys())

    def saudaveis(self) -> list[str]:
        return [n for n in self.nomes() if self.obter_healthcheck(n)["saudavel"]]
