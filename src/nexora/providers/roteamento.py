"""Roteamento determinístico entre providers e modelos."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from nexora.providers.manager import ProviderManager
from nexora.providers.modelos import PerfilCapacidadeModelo
from nexora.runtime.hardware import PerfilHardware
from nexora.runtime.historico_avaliacao import HistoricoAvaliacao
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

    def __init__(self, manager: ProviderManager, historico_avaliacao: HistoricoAvaliacao | None = None, min_amostra_qualidade: int = 5) -> None:
        if min_amostra_qualidade < 1:
            raise ValueError("min_amostra_qualidade deve ser >= 1")
        self._manager = manager
        self._historico_avaliacao = historico_avaliacao
        self._min_amostra_qualidade = min_amostra_qualidade

    def definir_historico_avaliacao(self, historico: HistoricoAvaliacao | None, *, min_amostra: int | None = None) -> None:
        """Conecta o historico de qualidade sem alterar a politica de execucao."""
        if min_amostra is not None and min_amostra < 1:
            raise ValueError("min_amostra deve ser >= 1")
        self._historico_avaliacao = historico
        if min_amostra is not None:
            self._min_amostra_qualidade = min_amostra

    @staticmethod
    def _ajuste_historico_metricas(historico: dict[str, Any], comparaveis: list[dict[str, Any]]) -> tuple[float, list[str]]:
        chamadas = int(historico.get("chamadas", 0))
        if chamadas < 3:
            return 0.0, []
        ajuste, motivos = 0.0, []
        taxa_erro = historico.get("taxa_erro")
        taxa_sucesso = historico.get("taxa_sucesso")
        latencia = historico.get("latencia_media")
        if isinstance(taxa_sucesso, float) and taxa_sucesso >= 0.90:
            ajuste += 1.0
            motivos.append("historico_alta_taxa_sucesso")
        elif isinstance(taxa_erro, float) and taxa_erro >= 0.50:
            ajuste -= 2.0
            motivos.append("historico_alta_taxa_erro")
        latencias = [d.get("latencia_media") for d in comparaveis if isinstance(d.get("latencia_media"), float)]
        if isinstance(latencia, float) and latencias:
            media_global = sum(latencias) / len(latencias)
            if latencia < media_global:
                ajuste += 0.5
                motivos.append("historico_baixa_latencia")
            elif latencia > media_global:
                ajuste -= 0.5
                motivos.append("historico_alta_latencia")
        return ajuste, motivos

    def _ajuste_historico(self, provider: str) -> tuple[float, list[str]]:
        historico = self._manager.estatisticas_provider(provider)
        comparaveis = list(self._manager.estatisticas_providers().values())
        return self._ajuste_historico_metricas(historico, comparaveis)

    def _ajuste_historico_modelo(self, provider: str, modelo: str, candidatos: list[tuple[str, str]]) -> tuple[float, list[str]]:
        """Usa confiabilidade/latencia do par exato provider/modelo quando ha amostra suficiente."""
        historico = self._manager.estatisticas_modelo(provider, modelo)
        if int(historico.get("chamadas", 0)) < 3:
            return 0.0, []
        comparaveis = [self._manager.estatisticas_modelo(p, m) for p, m in candidatos]
        return self._ajuste_historico_metricas(historico, comparaveis)

    def _ajuste_qualidade_tarefa(self, provider: str, modelo: str, tipo_tarefa: str, candidatos: list[tuple[str, str]]) -> tuple[float, list[str]]:
        """Aplica qualidade observada somente com amostra suficiente e peso conservador."""
        if self._historico_avaliacao is None:
            return 0.0, []
        historico = self._historico_avaliacao.qualidade_para_roteamento(provider, modelo, tipo_tarefa, min_amostra=self._min_amostra_qualidade)
        if not historico["amostra_suficiente"]:
            return 0.0, []
        score = historico["score_medio"]
        peso_amostra = float(historico.get("peso_amostra", 0.0))
        pares_com_amostra = []
        for candidato_provider, candidato_modelo in candidatos:
            dados = self._historico_avaliacao.qualidade_para_roteamento(candidato_provider, candidato_modelo, tipo_tarefa, min_amostra=self._min_amostra_qualidade)
            if dados["amostra_suficiente"]:
                pares_com_amostra.append(float(dados["score_medio"]))
        if len(pares_com_amostra) < 2:
            return 0.0, []
        media = sum(pares_com_amostra) / len(pares_com_amostra)
        diferenca = float(score) - media
        if abs(diferenca) < 0.05:
            return 0.0, []
        ajuste = max(-1.0, min(1.0, diferenca * 2.0 * peso_amostra))
        if ajuste > 0:
            return ajuste, ["qualidade_tarefa_historica_acima_media"]
        return ajuste, ["qualidade_tarefa_historica_abaixo_media"]

    def _custo_historico_por_milhao(self, provider: str) -> float | None:
        historico = self._manager.estatisticas_provider(provider)
        geracoes, tokens, custo = int(historico["geracoes_com_custo"]), int(historico["total_tokens"]), float(historico["custo_total"])
        if geracoes < 3 or tokens <= 0 or custo < 0:
            return None
        return (custo / tokens) * 1_000_000

    def _custo_historico_modelo_por_milhao(self, provider: str, modelo: str) -> float | None:
        """Custo real por milhao para o par exato provider/modelo."""
        historico = self._manager.estatisticas_modelo(provider, modelo)
        geracoes, tokens, custo = int(historico.get("geracoes_com_custo", 0)), int(historico.get("total_tokens", 0)), float(historico.get("custo_total", 0.0))
        if geracoes < 3 or tokens <= 0 or custo < 0:
            return None
        return (custo / tokens) * 1_000_000

    def _ajuste_custo_historico(self, provider: str, provedores_candidatos: list[str]) -> tuple[float, list[str]]:
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
        """Ordena candidatos por adequacao, capacidades, historico e qualidade observada."""
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
                adequado = False
                motivos.append("provider_sem_tool_calling")
            if exigir_streaming and not capacidades.streaming:
                adequado = False
                motivos.append("provider_sem_streaming")
            if contexto_necessario > capacidades.max_context_tokens > 0:
                adequado = False
                motivos.append("provider_contexto_insuficiente")
            if exigir_provider_saudavel and not self._manager.obter_healthcheck(provider)["saudavel"]:
                adequado = False
                motivos.append("provider_indisponivel")
            avaliacao = avaliar_modelo(modelo, perfil, hardware, tarefa=tarefa, contexto_necessario=contexto_necessario)
            if not avaliacao.adequado:
                adequado = False
            motivos.extend(avaliacao.motivos)
            score = avaliacao.score if adequado else -100.0
            if adequado and usar_historico:
                historico_modelo = self._manager.estatisticas_modelo(provider, modelo)
                if int(historico_modelo.get("chamadas", 0)) >= 3:
                    ajuste, motivos_historico = self._ajuste_historico_modelo(provider, modelo, pares)
                else:
                    ajuste, motivos_historico = self._ajuste_historico(provider)
                score += ajuste
                motivos.extend(motivos_historico)
                ajuste_qualidade, motivos_qualidade = self._ajuste_qualidade_tarefa(provider, modelo, tarefa, pares)
                score += ajuste_qualidade
                motivos.extend(motivos_qualidade)
                if considerar_custo:
                    ajuste_custo, motivos_custo = self._ajuste_custo_modelo(provider, modelo, pares)
                    score += ajuste_custo
                    motivos.extend(motivos_custo)
            avaliados.append(CandidatoRoteamento(provider, modelo, score, adequado, tuple(motivos)))
        return sorted(avaliados, key=lambda item: (-item.adequado, -item.score, item.provider, item.modelo))
