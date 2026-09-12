"""Roteamento determinístico entre providers e modelos."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any
from nexora.providers.manager import ProviderManager
from nexora.providers.modelos import PerfilCapacidadeModelo
from nexora.runtime.hardware import PerfilHardware
from nexora.runtime.modelos import avaliar_modelo


@dataclass(frozen=True)
class CandidatoRoteamento:
    provider: str
    modelo: str
    score: float
    adequado: bool
    motivos: tuple[str, ...] = ()


class RoteadorInteligente:
    """Escolhe provider/modelo sem executar a tarefa."""
    def __init__(self, manager: ProviderManager) -> None:
        self._manager = manager

    def _ajuste_historico(self, provider: str) -> tuple[float, list[str]]:
        historico = self._manager.estatisticas_provider(provider)
        chamadas = int(historico["chamadas"])
        if chamadas < 3:
            return 0.0, []
        ajuste, motivos = 0.0, []
        taxa_erro, taxa_sucesso, latencia = historico["taxa_erro"], historico["taxa_sucesso"], historico["latencia_media"]
        if isinstance(taxa_sucesso, float) and taxa_sucesso >= 0.90:
            ajuste += 1.0; motivos.append("historico_alta_taxa_sucesso")
        elif isinstance(taxa_erro, float) and taxa_erro >= 0.50:
            ajuste -= 2.0; motivos.append("historico_alta_taxa_erro")
        if isinstance(latencia, float):
            todas = [d["latencia_media"] for d in self._manager.estatisticas_providers().values() if isinstance(d["latencia_media"], float)]
            media_global = (sum(todas) / len(todas)) if todas else None
            if isinstance(media_global, float) and latencia < media_global:
                ajuste += 0.5; motivos.append("historico_baixa_latencia")
            elif isinstance(media_global, float) and latencia > media_global:
                ajuste -= 0.5; motivos.append("historico_alta_latencia")
        return ajuste, motivos

    def _custo_historico_por_milhao(self, provider: str) -> float | None:
        historico = self._manager.estatisticas_provider(provider)
        geracoes, tokens, custo = int(historico.get("geracoes_com_custo", 0)), int(historico.get("total_tokens", 0)), float(historico.get("custo_total", 0.0))
        if geracoes < 3 or tokens <= 0 or custo < 0:
            return None
        return (custo / tokens) * 1_000_000

    def _custo_historico_modelo_por_milhao(self, provider: str, modelo: str) -> float | None:
        """Custo real por milhao para o par exato provider/modelo.

        Nao mistura modelos. Menos de tres geracoes precificadas nao influencia.
        """
        historico = self._manager.estatisticas_modelo(provider, modelo)
        geracoes, tokens, custo = int(historico.get("geracoes_com_custo", 0)), int(historico.get("total_tokens", 0)), float(historico.get("custo_total", 0.0))
        if geracoes < 3 or tokens <= 0 or custo < 0:
            return None
        return (custo / tokens) * 1_000_000

    def _ajuste_custo_historico(self, provider: str, provedores_candidatos: list[str]) -> tuple[float, list[str]]:
        """Mantem o ajuste agregado por provider para compatibilidade."""
        custo = self._custo_historico_por_milhao(provider)
        if custo is None:
            return 0.0, []
        custos = [v for nome in provedores_candidatos if (v := self._custo_historico_por_milhao(nome)) is not None]
        if len(custos) < 2:
            return 0.0, []
        media = sum(custos) / len(custos)
        if media <= 0:
            return 0.0, []
        rel = (custo - media) / media
        if rel <= -0.10:
            return 0.75, ["historico_custo_real_mais_baixo"]
        if rel >= 0.10:
            return -0.75, ["historico_custo_real_mais_alto"]
        return 0.0, []

    def _ajuste_custo_modelo(self, provider: str, modelo: str, candidatos: list[tuple[str, str]]) -> tuple[float, list[str]]:
        custo = self._custo_historico_modelo_por_milhao(provider, modelo)
        if custo is None:
            return 0.0, []
        custos = [v for p, m in candidatos if (v := self._custo_historico_modelo_por_milhao(p, m)) is not None]
        if len(custos) < 2:
            return 0.0, []
        media = sum(custos) / len(custos)
        if media <= 0:
            return 0.0, []
        rel = (custo - media) / media
        if rel <= -0.10:
            return 0.75, ["historico_custo_modelo_real_mais_baixo"]
        if rel >= 0.10:
            return -0.75, ["historico_custo_modelo_real_mais_alto"]
        return 0.0, []

    def selecionar(self, candidatos: list[dict[str, Any]], hardware: PerfilHardware, *, tarefa: str = "general", contexto_necessario: int = 0, exigir_tool_calling: bool = False, exigir_streaming: bool = False, exigir_provider_saudavel: bool = False, usar_historico: bool = True, considerar_custo: bool = True) -> list[CandidatoRoteamento]:
        """Ordena candidatos por adequacao, capacidades e historico medido."""
        avaliados: list[CandidatoRoteamento] = []
        pares = [(str(c.get("provider", "")).strip().lower(), str(c.get("modelo", "")).strip()) for c in candidatos if str(c.get("provider", "")).strip() and str(c.get("modelo", "")).strip()]
        for candidato in candidatos:
            provider = str(candidato.get("provider", "")).strip().lower()
            modelo = str(candidato.get("modelo", "")).strip()
            perfil = candidato.get("perfil")
            if not provider or not modelo or not isinstance(perfil, PerfilCapacidadeModelo) or provider not in self._manager.nomes():
                continue
            motivos: list[str] = []
            capacidades = self._manager.obter_capacidades(provider)
            adequado = True
            if exigir_tool_calling and not capacidades.tool_calling:
                adequado = False; motivos.append("provider_sem_tool_calling")
            if exigir_streaming and not capacidades.streaming:
                adequado = False; motivos.append("provider_sem_streaming")
            if contexto_necessario > capacidades.max_context_tokens > 0:
                adequado = False; motivos.append("provider_contexto_insuficiente")
            if exigir_provider_saudavel and not self._manager.obter_healthcheck(provider)["saudavel"]:
                adequado = False; motivos.append("provider_indisponivel")
            avaliacao = avaliar_modelo(modelo, perfil, hardware, tarefa=tarefa, contexto_necessario=contexto_necessario)
            if not avaliacao.adequado:
                adequado = False
            motivos.extend(avaliacao.motivos)
            score = avaliacao.score if adequado else -100.0
            if adequado and usar_historico:
                ajuste, motivos_historico = self._ajuste_historico(provider)
                score += ajuste; motivos.extend(motivos_historico)
                if considerar_custo:
                    ajuste_custo, motivos_custo = self._ajuste_custo_modelo(provider, modelo, pares)
                    score += ajuste_custo; motivos.extend(motivos_custo)
            avaliados.append(CandidatoRoteamento(provider, modelo, score, adequado, tuple(motivos)))
        return sorted(avaliados, key=lambda item: (-item.adequado, -item.score, item.provider, item.modelo))
